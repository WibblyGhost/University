/*
 * Torus.cpp
 * Created by Zachary Sanson on 25/05/2019.
 */


// ------------- Includes -------------
#include "Torus.h"
#include "../Functions/QuarticSolver.h"
#include <glm/gtx/string_cast.hpp>
#include <algorithm>
#include <iostream>
#include <complex>
#include <vector>
#include <cmath>

using namespace std;


// ------------- Returns a colour value when the ray intercepts the object -------------
float Torus::intersect(glm::vec3 pos, glm::vec3 dir) {
    // Transformed torus vectors
    glm::vec3 tPos = glm::vec3(transform * glm::vec4(pos.x, pos.y, pos.z, 1));
    glm::vec3 tDir = glm::vec3(transform * glm::vec4(dir.x, dir.y, dir.z, 0));
    // Quartic equation in the form of ax^4 + bx^3 + cx^2 + dx + e
    double a = tDir.x * tDir.x * tDir.x * tDir.x +
               tDir.y * tDir.y * tDir.y * tDir.y +
               tDir.z * tDir.z * tDir.z * tDir.z;
    a += 2 * (tDir.x * tDir.x * tDir.y * tDir.y +
              tDir.x * tDir.x * tDir.z * tDir.z +
              tDir.y * tDir.y * tDir.z * tDir.z);
    double b = 4 * (tDir.x * tDir.x * tDir.x * tPos.x +
                    tDir.x * tDir.x * tDir.y * tPos.y +
                    tDir.x * tDir.x * tDir.z * tPos.z +
                    tDir.x * tDir.y * tDir.y * tPos.x +
                    tDir.x * tDir.z * tDir.z * tPos.x);
    b += 4 * (tDir.y * tDir.y * tDir.y * tPos.y +
              tDir.y * tDir.y * tDir.z * tPos.z +
              tDir.y * tDir.z * tDir.z * tPos.y +
              tDir.z * tDir.z * tDir.z * tPos.z);
    double c = 2 * (tDir.x * tDir.x * tPos.y * tPos.y +
                    tDir.x * tDir.x * tPos.z * tPos.z) +
               6 * tDir.x * tDir.x * tPos.x * tPos.x -
               20 * tDir.x * tDir.x * radius * radius;
    c += 2 * tDir.y * tDir.y * tPos.x * tPos.x +
         6 * tDir.y * tDir.y * tPos.y * tPos.y +
         8 * (tDir.x * tDir.y * tPos.x * tPos.y +
              tDir.x * tDir.z * tPos.x * tPos.z) -
         20 * tDir.y * tDir.y * radius * radius;
    c += 2 * (tDir.y * tDir.y * tPos.z * tPos.z +
              tDir.z * tDir.z * tPos.x * tPos.x) +
         8 * tDir.y * tDir.z * tPos.y * tPos.z +
         16 * tDir.z * tDir.z * radius * radius;
    c += 2 * tDir.z * tDir.z * tPos.y * tPos.y +
         6 * tDir.z * tDir.z * tPos.z * tPos.z;
    double d = 4 * (tDir.x * tPos.x * tPos.x * tPos.x +
                    tDir.x * tPos.x * tPos.y * tPos.y +
                    tDir.x * tPos.x * tPos.z * tPos.z) -
               40 * tDir.x * radius * radius * tPos.x;
    d += 4 * (tDir.y * tPos.x * tPos.x * tPos.y +
              tDir.y * tPos.y * tPos.z * tPos.z) +
         32 * tDir.z * radius * radius * tPos.z -
         40 * tDir.y * radius * radius * tPos.y;
    d += 4 * (tDir.z * tPos.x * tPos.x * tPos.z +
              tDir.z * tPos.y * tPos.y * tPos.z +
              tDir.z * tPos.z * tPos.z * tPos.z);
    double e = 16 * radius * radius * tPos.z * tPos.z -
               20 * (radius * radius * tPos.x * tPos.x -
                     radius * radius * tPos.y * tPos.y) +
               64 * radius * radius * radius * radius;
    e += tPos.x * tPos.x * tPos.x * tPos.x +
         tPos.y * tPos.y * tPos.y * tPos.y +
         tPos.z * tPos.z * tPos.z * tPos.z +
         2 * (tPos.x * tPos.x * tPos.y * tPos.y +
              tPos.x * tPos.x * tPos.z * tPos.z +
              tPos.y * tPos.y * tPos.z * tPos.z);
    // Solve the quartic for real roots
    std::complex<double> coefficients[5] = {e + 0i, d + 0i, c + 0i, b + 0i, a + 0i};
    std::complex<double> solutions[4];
    std::vector<double> roots;
    solveQuartic(coefficients, solutions);
    for (complex<double> solution : solutions) {
        if (abs(solution.imag()) < 0.001 && solution.real() > 0.001) roots.push_back(solution.real());
    }
    // If no real positive roots are present
    if (roots.empty()) return -1.0;
    // A real positive root is present, find & return
    std::sort(roots.begin(), roots.end());
    return roots[0];
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Torus::normal(glm::vec3 point) {
    glm::vec3 tPoint = glm::vec3(transform * glm::vec4(point.x, point.y, point.z, 1));
    glm::vec3 norm = glm::normalize(glm::vec3(tPoint.x, tPoint.y, 0)) * radius * 3.0f;
    glm::vec3 diff = glm::normalize(tPoint - norm);
    // Apply a reverse transformation
    return glm::vec3(glm::inverse(transform) * glm::vec4(diff.x, diff.y, diff.z, 0));
}
