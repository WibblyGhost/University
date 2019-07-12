/*
 * Cylinder.h
 * Created by Zachary Sanson on 20/05/2019.
 */


#ifndef H_CYLINDER
#define H_CYLINDER


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a cylinder located at the center with given radius & height-------------
class Cylinder : public SceneObject {
private:
    glm::vec3 center;
    float radius;
    float height;
public:
    Cylinder() : center(glm::vec3(0)), radius(1), height(1) {
        colour = glm::vec3(1);
    };

    Cylinder(glm::vec3 c, float r, float h, glm::vec3 col) : center(c), radius(r), height(h) {
        colour = col;
    };

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 point);
};


#endif //H_CYLINDER