/*
 * Cone.h
 * Created by Zachary Sanson on 20/05/2019.
 */


#ifndef H_CONE
#define H_CONE


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a cone located at the center with given radius & height-------------
class Cone : public SceneObject {
private:
    glm::vec3 center;
    float radius;
    float height;
public:
    Cone() : center(glm::vec3()), radius(1), height(1) {
        colour = glm::vec3(1);
    };

    Cone(glm::vec3 c, float r, float h, glm::vec3 col) : center(c), radius(r), height(h) {
        colour = col;
    };

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 point);
};


#endif //H_CONE