/*
 * Triangle.h
 * Created by Zachary Sanson on 23/05/2019.
 */


#ifndef H_TRIANGLE
#define H_TRIANGLE


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a triangle spanning across three vertices -------------
class Triangle : public SceneObject {
private:
    glm::vec3 a, b, c;
public:
    Triangle();

    bool isInside(glm::vec3 pos, glm::vec3 dir);

    Triangle(glm::vec3 pa, glm::vec3 pb, glm::vec3 pc, glm::vec3 col) : a(pa), b(pb), c(pc) {
        colour = col;
    };

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 pos);
};


#endif //H_TRIANGLE
