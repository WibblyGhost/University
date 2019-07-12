/*
 * SceneObject.h
 * Created by Zachary Sanson on 12/05/2019.
 */


#ifndef H_SCENE_OBJECT
#define H_SCENE_OBJECT


// ------------- Includes -------------
#include <glm/glm.hpp>
#include "../Functions/TextureBMP.h"


// ------------- Defines a SceneObject which contains objects in the scene -------------
class SceneObject {
protected:
    glm::vec3 colour;
public:
    float transparency = 1;
    float refractionIndex = 1;
    float reflectionCoefficient = 0;
    glm::mat4x4 transform = glm::mat4x4(1.0);
    TextureBMP objectTexture;
    glm::vec3 textureCenter, textureColourMod;

    SceneObject() {}

    virtual float intersect(glm::vec3 pos, glm::vec3 dir) = 0;

    virtual glm::vec3 normal(glm::vec3 pos) = 0;

    virtual ~SceneObject() {}

    glm::vec3 getColour();

    void setColour(glm::vec3 col);
};


#endif //H_SCENE_OBJECT
