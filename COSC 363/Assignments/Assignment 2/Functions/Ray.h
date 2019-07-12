/*
 * Ray.h
 * Created by Zachary Sanson on 12/05/2019.
 */


#ifndef H_RAY
#define H_RAY


// ------------- Includes -------------
#include <glm/glm.hpp>
#include <vector>
#include "SceneObject.h"


// ------------- Defines a ray at given point facing a given direction -------------
class Ray {
public:
    glm::vec3 pt, dir, oPoint;
    int xIndex;
    float xDist;

    Ray() {
        pt = glm::vec3(0, 0, 0);
        dir = glm::vec3(0, 0, - 1);
        oPoint = glm::vec3(0, 0, 0);
        xIndex = - 1;
        xDist = 0;
    };

    Ray(glm::vec3 point, glm::vec3 direction) : pt(point), dir(direction) {
        oPoint = glm::vec3(0, 0, 0);
        xIndex = - 1;
        xDist = 0;
    };

    void normalize();

    void closestPt(std::vector<SceneObject *> &sceneObjects);
};


#endif //H_RAY