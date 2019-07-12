/*
 * Plane.cpp
 * Created by Zachary Sanson on 12/05/2019.
 */


// ------------- Includes -------------
#include "Plane.h"
#include <math.h>


// ------------- Returns true if given point is inside object -------------
bool Plane::isInside(glm::vec3 point) {
    glm::vec3 norm = normal(point);
    float A = glm::dot(glm::cross((b - a), (point - a)), norm);
    float B = glm::dot(glm::cross((c - b), (point - b)), norm);
    float C = glm::dot(glm::cross((d - c), (point - c)), norm);
    float D = glm::dot(glm::cross((a - d), (point - d)), norm);
    return A >= 0 && B >= 0 && C >= 0 && D >= 0;
}


// ------------- Returns a colour value when the ray intercepts the object -------------
float Plane::intersect(glm::vec3 pos, glm::vec3 dir) {
    glm::vec3 norm = normal(pos);
    glm::vec3 vDiff = a - pos;
    float vDotN = glm::dot(dir, norm);
    if (fabs(vDotN) < 1.e-4) return -1;
    float solution = glm::dot(vDiff, norm) / vDotN;
    if (fabs(solution) < 0.0001) return -1;
    glm::vec3 q = pos + dir * solution;
    if (isInside(q)) return solution;
    else return -1;
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Plane::normal(glm::vec3 point) {
    return glm::normalize(glm::cross((b - a), (d - a)));
}
