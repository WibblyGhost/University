/*
 * Sphere.cpp
 * Created by Zachary Sanson on 12/05/2019.
 */


// ------------- Includes -------------
#include "Sphere.h"
#include <math.h>
#include "../Functions/Ray.h"


// ------------- Returns a colour value when the ray intercepts the object -------------
float Sphere::intersect(glm::vec3 pos, glm::vec3 dir) {
    glm::vec3 vDiff = pos - center;
    float len = glm::length(vDiff);
    float b = glm::dot(dir, vDiff);
    float c = pow(len, 2) - pow(radius, 2);
    // Determinant: b^2 - 4ac
    float determinant = pow(b, 2) - c;
    if (fabs(determinant) < 0.001) return -1;
    if (determinant < 0.0) return -1;
    // t-Values: -b +- sqrt(b^2 - 4ac) / 2a
    float solutions[2];
    solutions[0] = -b - sqrt(determinant);
    solutions[1] = -b + sqrt(determinant);
    if (fabs(solutions[0]) < 0.001) {
        if (solutions[1] > 0) return solutions[1];
        else solutions[0] = -1.0;
    }
    if (fabs(solutions[1]) < 0.001) solutions[1] = -1;
    if (half) {
        float y1 = pos.y + dir.y * solutions[0];
        if (y1 < center.y) return -1;
        // TODO: Generate base of semi-sphere
    }
    return (solutions[0] < solutions[1]) ? solutions[0] : solutions[1];
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Sphere::normal(glm::vec3 point) {
    return glm::normalize(point - center);
}
