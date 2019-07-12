/*
 * Triangle.cpp
 * Created by Zachary Sanson on 23/05/2019.
 */


// ------------- Includes -------------
#include "Triangle.h"
#include <math.h>


// ------------- Returns true if given point is inside object -------------
bool Triangle::isInside(glm::vec3 pos, glm::vec3 dir) {
    glm::vec3 norm = glm::cross(b - a, c - a);
    float nDotD = glm::dot(norm, dir);
    if (fabs(nDotD) < 0.0001) return false;
    float t = (glm::dot(norm, pos) + glm::dot(norm, a)) / nDotD;
    if (t < 0) return false;
    glm::vec3 point = pos + t * dir;
    glm::vec3 edges[3] = {b - a, c - b, a - c};
    glm::vec3 points[3] = {point - a, point - b, point - c};
    for (int count = 0; count < 3; count++) {
        glm::vec3 eCrossV = glm::cross(edges[count], points[count]);
        if (glm::dot(norm, eCrossV) < 0) return false;
    }
    return true;
}


// ------------- Returns a colour value when the ray intercepts the object -------------
float Triangle::intersect(glm::vec3 pos, glm::vec3 dir) {
    return isInside(pos, dir);
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Triangle::normal(glm::vec3 pos) {
    return glm::normalize(glm::cross((c - a), (b - a)));
}
