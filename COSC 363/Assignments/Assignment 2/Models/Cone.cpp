/*
 * Cone.cpp
 * Created by Zachary Sanson on 20/05/2019.
 */


// ------------- Includes -------------
#include "Cone.h"
#include <math.h>


// ------------- Returns a colour value when the ray intercepts the object -------------
float Cone::intersect(glm::vec3 pos, glm::vec3 dir) {
    float solutions[2], y1, y2;
    // Line Equation: ax^2 + bx + c
    float tan = radius / height;
    float a = pow(dir.x, 2) + pow(dir.z, 2) - pow(tan, 2) * pow(dir.y, 2);
    float b = 2 * ((pos.x - center.x) * dir.x + (pos.z - center.z) * dir.z
                   + pow(tan, 2) * (height - pos.y + center.y) * dir.y);
    float c = pow((pos.x - center.x), 2) + pow((pos.z - center.z), 2) -
              pow(tan, 2) * pow((height - pos.y + center.y), 2);
    // Determinant: b^2 - 4ac
    float determinant = pow(b, 2) - 4 * a * c;
    if (determinant < 0 || fabs(determinant) < 0.001) return -1;
    // t-Values: -b +- sqrt(b^2 - 4ac) / 2a
    solutions[0] = (-b - sqrt(determinant)) / (2 * a);
    solutions[1] = (-b + sqrt(determinant)) / (2 * a);
    if (solutions[0] < 0.01) solutions[0] = -1;
    if (solutions[1] < 0.01) solutions[1] = -1;
    y1 = pos.y + dir.y * solutions[0];
    y2 = pos.y + dir.y * solutions[1];
    // Boundaries of the cone
    if ((y1 > center.y) && (y1 < center.y + height)) return solutions[0];
    else if ((y2 > center.y) && (y2 < center.y + height)) return solutions[1];
    return -1;
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Cone::normal(glm::vec3 point) {
    // n = (sin(a)cos(theta), sin(theta), cos(a)cos(theta);
    // a = tan^-1 ((x - center)/ (z - center))
    float theta = atan(radius / height);
    float a = atan((point.x - center.x) / (point.z - center.z));
    glm::vec3 norm = glm::vec3(glm::vec3(sin(a) * cos(theta), sin(theta), cos(a) * cos(theta)));
    return glm::normalize(norm);
}