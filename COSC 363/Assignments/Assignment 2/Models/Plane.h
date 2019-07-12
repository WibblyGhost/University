/*
 * Plane.h
 * Created by Zachary Sanson on 12/05/2019.
 */


#ifndef H_PLANE
#define H_PLANE


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a plane spanned over four vectors -------------
class Plane : public SceneObject {
private:
    glm::vec3 a, b, c, d;
public:
    Plane();

    Plane(glm::vec3 pointA, glm::vec3 pointB, glm::vec3 pointC, glm::vec3 pointD, glm::vec3 col)
            : a(pointA), b(pointB), c(pointC), d(pointD) {
        colour = col;
    };

    bool isInside(glm::vec3 point);

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 point);
};


#endif //H_PLANE
