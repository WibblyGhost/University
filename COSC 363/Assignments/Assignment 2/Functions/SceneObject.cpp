/*
 * SceneObject.cpp
 * Created by Zachary Sanson on 12/05/2019.
 */


// ------------- Includes -------------
#include "SceneObject.h"


// ------------- Returns the colour of object within the scene -------------
glm::vec3 SceneObject::getColour() {
    return colour;
}


// ------------- Sets the colour of an object in the scene -------------
void SceneObject::setColour(glm::vec3 col) {
    colour = col;
}
