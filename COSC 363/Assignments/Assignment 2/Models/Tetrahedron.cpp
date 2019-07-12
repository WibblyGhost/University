/*
 * Tetrahedron.cpp
 * Created by Zachary Sanson on 30/05/2019.
 */


// ------------- Includes -------------
#include "Tetrahedron.h"
#include "Triangle.h"
#include <math.h>


// Try implement baycenter coordinates instead?
// Pluecker coordinates method?

// FIXME: Code is not correctly implemented yet!
// ------------- Returns true if given point is inside object -------------
bool Tetrahedron::isInside(glm::vec3 pos, glm::vec3 dir) {
    Triangle t1 = Triangle(a, b, c, glm::vec3(0, 0, 0));
    Triangle t2 = Triangle(a, c, d, glm::vec3(1, 0, 0));
    Triangle t3 = Triangle(a, d, b, glm::vec3(0, 1, 0));
    Triangle t4 = Triangle(d, c, b, glm::vec3(0, 0, 1));
    bool tt1 = t1.isInside(pos, dir);
    bool tt2 = t2.isInside(pos, dir);
    bool tt3 = t3.isInside(pos, dir);
    bool tt4 = t4.isInside(pos, dir);
    return (tt1 && tt2) || (tt1 && tt3) || (tt1 && tt4) || (tt2 && tt3) || (tt2 && tt4) || (tt3 && tt4);
}


// ------------- Returns a colour value when the ray intercepts the object -------------
float Tetrahedron::intersect(glm::vec3 pos, glm::vec3 dir) {
    return isInside(pos, dir);
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Tetrahedron::normal(glm::vec3 pos) {
    Triangle t1 = Triangle(a, b, c, glm::vec3(0, 0, 0));
    Triangle t2 = Triangle(a, c, d, glm::vec3(1, 0, 0));
    Triangle t3 = Triangle(a, d, b, glm::vec3(0, 1, 0));
    Triangle t4 = Triangle(d, c, b, glm::vec3(0, 0, 1));


    return glm::normalize(glm::cross((b - a), (c - a)));
}
