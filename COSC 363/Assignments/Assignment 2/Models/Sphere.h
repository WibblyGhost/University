/*
 * Sphere.h
 * Created by Zachary Sanson on 12/05/2019.
 */


#ifndef H_SPHERE
#define H_SPHERE


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a sphere located at the center with given radius -------------
class Sphere : public SceneObject {
private:
    glm::vec3 center;
    float radius;
public:
    bool half = false;

    Sphere() : center(glm::vec3(0)), radius(1) {
        colour = glm::vec3(1);
    };

    Sphere(glm::vec3 c, float r, glm::vec3 col) : center(c), radius(r) {
        colour = col;
    };

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 point);
};


#endif //H_SPHERE