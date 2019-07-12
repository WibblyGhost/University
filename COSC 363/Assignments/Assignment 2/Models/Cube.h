/*
 * Cube.h
 * Created by Zachary Sanson on 21/05/2019.
 */


#ifndef H_CUBE
#define H_CUBE


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// ------------- Defines a cube spanned over four vectors -------------
class Cube : public SceneObject {
private:
    glm::vec3 center;
    float size;
public:
    Cube();

    Cube(glm::vec3 c, float s, glm::vec3 col) : center(c), size(s) {
        colour = col;
    }

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 point);
};


#endif //H_CUBE