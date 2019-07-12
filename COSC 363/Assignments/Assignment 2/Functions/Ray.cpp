/*
 * Ray.cpp
 * Created by Zachary Sanson on 12/05/2019.
 */


// ------------- Includes -------------
#include "Ray.h"


// ------------- Normalizes the direction vector to a unit vector -------------
void Ray::normalize() {
    dir = glm::normalize(dir);
}


// ------------- Finds the closest point of intersection with the object -------------
void Ray::closestPt(std::vector<SceneObject *> &sceneObjects) {
    glm::vec3 point(0, 0, 0);
    float min = 1.e+6;
    for (unsigned int i = 0; i < sceneObjects.size(); i ++) {
        float t = sceneObjects[i]->intersect(pt, dir);
        if (t > 0) {
            point = pt + dir * t;
            if (t < min) {
                oPoint = point;
                xIndex = i;
                xDist = t;
                min = t;
            }
        }
    }
}
