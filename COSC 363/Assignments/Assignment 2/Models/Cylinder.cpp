/*
 * Cylinder.cpp
 * Created by Zachary Sanson on 20/05/2019.
 */


// ------------- Includes -------------
#include "Cylinder.h"
#include <math.h>


// ------------- Returns a colour value when the ray intercepts the object -------------
float Cylinder::intersect(glm::vec3 pos, glm::vec3 dir) {
    float solutions[2];
    float L = sqrt(pow(dir.x, 2) + pow(dir.z, 2));
    // Line Equation: ax^2 + bx + c
    float a = pow(dir.x, 2)
              + pow(dir.z, 2);
    float b = 2 * (dir.x * (pos.x - center.x)
                   + dir.z * (pos.z - center.z));
    float c = pow(pos.x - center.x, 2)
              + pow(pos.z - center.z, 2)
              - pow(radius, 2);
    // Determinant: b^2 - 4ac
    float determinant = pow(b, 2) - 4 * a * c;
    if (determinant < 0 || fabs(determinant) < 0.001) return -1;
    // t-Values: -b +- sqrt(b^2 - 4ac) / 2a
    solutions[0] = (-b + sqrt(determinant)) / (2 * a);
    solutions[1] = (-b - sqrt(determinant)) / (2 * a);
    float y1 = pos.y + dir.y * solutions[0];
    float y2 = pos.y + dir.y * solutions[1];
    float top = center.y + height;
    // If one point is above the cylinder and one point intercepts the cylinder
    if ((y1 > top && y2 < top) || (y2 > top && y1 < top)) return L * (top - pos.y) / dir.y;
    // If the point lies within the cylinder
    if (y2 < top && y2 > center.y) return L * solutions[1];
    if (y1 < top && y1 > center.y) return L * solutions[0];
    // If both points lie outside the cylinder
    return -1;
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Cylinder::normal(glm::vec3 point) {
    glm::vec3 norm = glm::vec3((point.x - center.x) / radius, 0, (point.z - center.z) / radius);
    return glm::normalize(norm);
}
