/*
 * Tetrahedron.h
 * Created by Zachary Sanson on 30/05/2019.
 */


#ifndef H_TETRAHEDRON
#define H_TETRAHEDRON


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/SceneObject.h"


// TODO: Finish tetrahedron class
// ------------- Defines a tetrahedron located at the center with given radius -------------
class Tetrahedron : public SceneObject {
private:
    glm::vec3 a, b, c, d;
public:
    Tetrahedron();

    bool isInside(glm::vec3 pos, glm::vec3 dir);

    Tetrahedron(glm::vec3 pa, glm::vec3 pb, glm::vec3 pc, glm::vec3 pd, glm::vec3 col) : a(pa), b(pb), c(pc), d(pd) {
        colour = col;
    };

    float intersect(glm::vec3 pos, glm::vec3 dir);

    glm::vec3 normal(glm::vec3 pos);
};


#endif //H_TETRAHEDRON
