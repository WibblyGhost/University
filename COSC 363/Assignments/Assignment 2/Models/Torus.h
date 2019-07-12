/*
 * Torus.h
 * Created by Zachary Sanson on 25/05/2019.
 */


#ifndef H_TORUS
#define H_TORUS


// ------------- Includes -------------
#define GLM_ENABLE_EXPERIMENTAL

#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a torus located at the center with given radius -------------
class Torus : public SceneObject {
protected:
    glm::vec3 center;
    float radius;
public:
    Torus() : center(glm::vec3(0)), radius(1) {
        colour = glm::vec3(1);
    };

    Torus(glm::vec3 c, float r, glm::vec3 col) : center(c), radius(r) {
        colour = col;
    };

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 point);
};


#endif //H_TORUS
