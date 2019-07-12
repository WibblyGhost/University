/*
 * main.cpp
 * COSC 363: Computer Graphics - Assignment 2
 * Created by Zachary Sanson on 06/05/2019.
 */


// ------------- TODOS -------------
/* Main */
// Complete: Lighting
// Complete: Shadows
// Complete: Reflections
// Complete: Parallelepiped -> Cube
// Complete: Textured surface -> Plane
/* Extras */
// TODO: *Cones, *cylinders, tetrahedrons, *torus
// TODO: Spotlight
// COMPLETE: Transparent object -> Sphere on the top
// COMPLETE: Refraction of light
// COMPLETE: Anti-aliasing
// COMPLETE: Object transformation (rotation/shear transformation -> Torus
// COMPLETE: Non-planar object textured with an image -> Sphere / Cube
// COMPLETE: Non-planar object textured with a procedural pattern -> Cube / Cylinder
// COMPLETE: Fog


// ------------- Includes -------------
#include <iostream>
#include <cmath>
#include <vector>
#include <GL/glut.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "Models/Torus.h"
#include "Models/Plane.h"
#include "Models/Sphere.h"
#include "Models/Cylinder.h"
#include "Models/Cone.h"
#include "Models/Cube.h"
#include "Models/Triangle.h"
#include "Models/Tetrahedron.h"
#include "Functions/TextureBMP.h"
#include "Functions/SceneObject.h"
#include "Functions/Ray.h"


// ------------- Globals -------------
using namespace std;

struct scene_size {
    float width = 20;
    float height = 20;
    float eDist = 40;
    float xMin = -width * 0.5;
    float xMax = width * 0.5;
    float yMin = -height * 0.5;
    float yMax = height * 0.5;
    float zMin = eDist * -1;
    float zMax = (eDist + 10) * -4;
};

vector<SceneObject *> sceneObjects;
const struct scene_size FLOOR = {100, 20, 40};
const struct scene_size EYE;
const float PI = float(M_PI);
const float PHONG = 10;
const int ANTI_ALIASING_DEPTH = 2;
const int MAX_STEPS = 30;
const int NUMDIV = 600;

char FILENAME_1[] = "../Images/crate0.bmp";
char FILENAME_2[] = "../Images/fire_coral_block.bmp";
char FILENAME_3[] = "../Images/grass_block_side.bmp";
bool ANTI_ALIASING = false;


// ------------- Ray Tracer -------------
glm::vec3 trace(Ray ray, int step, bool refraction = false) {
    /* ------ Declarations ------ */
    enum objectIndex {  // Index of objects inside the scene
        coneLime,
        cubeTexture,
        cylinderCyan,
        cylinderMaroon,
        sphereBlue,
        sphereRefracted,
        sphereTexture,
        sphereTransparentHalf,
        planeTexture,
        torusMagenta
    };
    // Changeable variables
    float shadowBrightness[2] = {1.0f, 2.3f};
    glm::vec3 lights[2] = {glm::vec3(10, 15, -3), glm::vec3(-16, -10, 0)};
    // Colour storage
    glm::vec3 colourSum(0);
    glm::vec3 ambientColour(0.2);
    glm::vec3 backgroundColour(0);
    glm::vec3 checkerColour(0);
    glm::vec3 specularColour(0);
    glm::vec3 reflectionColour(0);
    glm::vec3 fogColour(0);

    /* ------ Object Ray Calculations ------ */
    ray.closestPt(sceneObjects);
    if (ray.xIndex == -1) return backgroundColour;
    SceneObject *selectedObject = sceneObjects[ray.xIndex];
    glm::vec3 viewVector = -ray.dir;
    glm::vec3 materialColour = selectedObject->getColour();
    glm::vec3 normalVector = selectedObject->normal(ray.oPoint);
    glm::vec3 lightVector[2] = {glm::normalize(lights[0] - ray.oPoint), glm::normalize(lights[1] - ray.oPoint)};
    glm::vec3 reflectionVector[2] = {glm::reflect(-lightVector[0], normalVector),
                                     glm::reflect(-lightVector[1], normalVector)};
    Ray shadows[2] = {Ray(ray.oPoint, lightVector[0]), Ray(ray.oPoint, lightVector[1])};
    float transparency = selectedObject->transparency;
    float refractionIndex = selectedObject->refractionIndex;
    float reflectionCoefficient = selectedObject->reflectionCoefficient;
    float lDotN[2] = {glm::dot(normalVector, lightVector[0]), glm::dot(normalVector, lightVector[1])};
    float rDotV[2] = {glm::dot(reflectionVector[0], viewVector), glm::dot(reflectionVector[1], viewVector)};

    /* ------ Images ------ */
    bool noSpec = false;
    glm::vec3 dir;
    float s, t;
    switch (ray.xIndex) {
        default:
            break;
        case cubeTexture:
            // Cube with a checkered pattern & a texture
            noSpec = true;
            dir = glm::normalize(ray.oPoint - selectedObject->textureCenter);
            s = (0.5 - atan2(dir.z, dir.x) + PI) / (2 * PI);
            t = 0.5 + asin(dir.y) / PI;
            materialColour = selectedObject->objectTexture.getColorAt(s, t) /** selectedObject->textureColourMod*/;
            // ((int(ray.oPoint.x) - int(ray.oPoint.z)) % 2) ? checkerColour = glm::vec3(0) : checkerColour = glm::vec3(1); // Checkered colour
            break;
        case planeTexture:
            s = (ray.oPoint.x - FLOOR.xMin) / (FLOOR.xMax - FLOOR.xMin);
            t = (ray.oPoint.z - FLOOR.zMin) / (FLOOR.zMax - FLOOR.zMin);
            materialColour = selectedObject->objectTexture.getColorAt(s, t) * selectedObject->textureColourMod;
            break;
        case cylinderCyan:
            // Cylinder with orange stripes
            if (int(ray.oPoint.x + ray.oPoint.y) % 2 == 0) materialColour = selectedObject->textureColourMod;
            break;
        case coneLime:
            // Cone with black stripes (in opposite direction)
            if (int(ray.oPoint.x - ray.oPoint.y) % 2 == 0) materialColour = selectedObject->textureColourMod;
            break;
        case sphereTexture:
            // Textured sphere with crate image
            dir = glm::normalize(ray.oPoint - selectedObject->textureCenter);
            s = (0.5 - atan2(dir.z, dir.x) + PI) / (2 * PI);
            t = 0.5 + asin(dir.y) / PI;
            materialColour = selectedObject->objectTexture.getColorAt(s, t);
            break;
    }

    /* ------ Refraction & Transparency ------ */
    if ((transparency != 1 || refractionIndex != 1) && step < MAX_STEPS) {
        float eta = 1 / refractionIndex;
        if (refraction) {
            eta = refractionIndex / 1;
            normalVector *= -1.0f;
        }
        glm::vec3 refractionColour = trace(Ray(ray.oPoint, glm::refract(ray.dir, normalVector, eta)), step + 1, true);
        return colourSum * transparency + refractionColour * (1 - transparency);
    }

    /* ------ Reflection ------ */
    if (reflectionCoefficient > 0 && step < MAX_STEPS) {
        glm::vec3 reflectedDir = glm::reflect(ray.dir, normalVector);
        glm::vec3 reflectedColour = trace(Ray(ray.oPoint, reflectedDir), step + 1);
        reflectionColour += (0.8f * reflectedColour) * reflectionCoefficient;
    }

    /* ------ Fog ------ */
    fogColour = glm::vec3(-0.001f * ray.xDist);

    /* ------ Shadows ------ */
    // FIXME: Shadows not appearing through transparent objects
    for (int count = 0; count < 2; count++) {
        shadows[count].closestPt(sceneObjects);
        // Check if object is transparent -> Don't render shadow (Fix/To-do change shadow colour)
        // if (shadows[count].xIndex > -1 && sceneObjects[shadows[count].xIndex]->transparency != 1) {
        if ((lDotN[count] <= 0 || (shadows[count].xIndex > -1 && shadows[count].xDist < ray.xDist)) &&
            (!refraction))
            return materialColour * ambientColour * (shadowBrightness[count] + fogColour * 15.0f);
        // Apart of reflection
        if (!noSpec && rDotV[count] >= 0)
            specularColour = glm::vec3(pow(rDotV[count], PHONG));  // Phong's light equation
    }

    return materialColour * (ambientColour + lDotN[0])
           + checkerColour * materialColour
           + specularColour
           + reflectionColour
           + fogColour;
}


// ------------- Anti-Aliasing -------------
glm::vec3 antiAliasing(glm::vec3 eye, float pixelSize, float xPoint, float yPoint) {
    float quarter = pixelSize * 0.25;
    float threeQuarters = pixelSize * 0.75;
    glm::vec3 colourSum(0);
    glm::vec3 average(0.25);
    // List of actions to apply to the ray equations below
    float signs[4][2] = {
            {quarter,       quarter},
            {quarter,       threeQuarters},
            {threeQuarters, quarter},
            {threeQuarters, threeQuarters}
    };
    for (float *sign : signs) {
        Ray ray = Ray(eye, glm::vec3(xPoint + sign[0], yPoint + sign[1], -EYE.eDist));
        ray.normalize();
        colourSum += trace(ray, 1);
    }
    return colourSum *= average;
}


// ------------- Display -------------
void display() {
    /* ------ Scene Rendering ------ */
    float xPoint, yPoint;
    float cellX = (EYE.xMax - EYE.xMin) / NUMDIV;
    float cellY = (EYE.yMax - EYE.yMin) / NUMDIV;
    glm::vec3 eye(0, 0, 0);
    glm::vec3 colour;
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glBegin(GL_QUADS);
    for (int i = 0; i < NUMDIV; i++) {
        xPoint = EYE.xMin + i * cellX;
        for (int j = 0; j < NUMDIV; j++) {
            yPoint = EYE.yMin + j * cellY;
            glm::vec3 dir(xPoint + 0.5 * cellX, yPoint + 0.5 * cellY, -EYE.eDist);
            Ray ray = Ray(eye, dir);
            ray.normalize();
            if (ANTI_ALIASING) colour = antiAliasing(eye, cellX / ANTI_ALIASING_DEPTH, xPoint, yPoint); // Anti-aliasing
            else colour = trace(ray, 1);
            glColor3f(colour.r, colour.g, colour.b);
            glVertex2f(xPoint, yPoint);
            glVertex2f(xPoint + cellX, yPoint);
            glVertex2f(xPoint + cellX, yPoint + cellY);
            glVertex2f(xPoint, yPoint + cellY);
        }
    }
    glEnd();
    glutSwapBuffers();
}


// ------------- Initialize -------------
void initialize() {
    glMatrixMode(GL_PROJECTION);
    gluOrtho2D(EYE.xMin, EYE.xMax, EYE.yMin, EYE.yMax);
    glClearColor(0, 0, 0, 1);

    /* ------ Object Declarations ------ */
    Cone *coneLime = new Cone(glm::vec3(-5, -20, -85), 2, 10, glm::vec3(0.6, 0.8, 0));
    Cube *cubeTexture = new Cube(glm::vec3(8, -20, -90), 4, glm::vec3(0));
    Cylinder *cylinderCyan = new Cylinder(glm::vec3(-15, -20, -90), 2.5, 3.5, glm::vec3(0, 0.8, 1));
    Cylinder *cylinderMaroon = new Cylinder(glm::vec3(-15, -17, -90), 5, 1, glm::vec3(0.5, 0, 0));
    Sphere *sphereBlue = new Sphere(glm::vec3(-5, -5, -110), 15, glm::vec3(0, 0, 1));
    Sphere *sphereRefracted = new Sphere(glm::vec3(5, -15, -100), 2, glm::vec3(1));
    Sphere *sphereTexture = new Sphere(glm::vec3(-15.0, -5.0, -70.0), 3.0, glm::vec3(0));
    Sphere *sphereTransparentHalf = new Sphere(glm::vec3(-15, -16, -90), 3, glm::vec3(1));
    Plane *planeTexture = new Plane(glm::vec3(FLOOR.xMin, -FLOOR.height, FLOOR.zMin),
                                    glm::vec3(FLOOR.xMax, -FLOOR.height, FLOOR.zMin),
                                    glm::vec3(FLOOR.xMax, -FLOOR.height, FLOOR.zMax),
                                    glm::vec3(FLOOR.xMin, -FLOOR.height, FLOOR.zMax),
                                    glm::vec3(0.5, 0.5, 0));
    Torus *torusMagenta = new Torus(glm::vec3(0.0, 0.0, 0.0), 1.0, glm::vec3(1, 0, 1));

    // Temporary fix until I can get Tetrahedrons rendering without triangles.
    glm::vec3 ptA = glm::vec3(15, -20, -85);
    glm::vec3 ptB = glm::vec3(12, -20, -90);
    glm::vec3 ptC = glm::vec3(18, -20, -90);
    glm::vec3 top = glm::vec3(15, -15, -92);
    Triangle *fLTriangle = new Triangle(ptA, top, ptC, glm::vec3(1));
    Triangle *fRTriangle = new Triangle(ptA, ptB, top, glm::vec3(0.8));
    Triangle *rearTriangle = new Triangle(ptC, ptB, top, glm::vec3(0.2, 0.2, 0.2));
    Triangle *bottomTriangle = new Triangle(ptA, ptB, ptC, glm::vec3(0.2, 0.8, 0.2));
//    Tetrahedron *tetra = new Tetrahedron(ptA, ptB, ptC, top, glm::vec3(1));

    /* ------ Object Properties ------ */
    coneLime->textureColourMod = glm::vec3(0.7, 0.4, 0); // Orange

    cubeTexture->objectTexture = TextureBMP(FILENAME_3);
    cubeTexture->textureCenter = glm::vec3(10, -20, -90);
    cubeTexture->textureColourMod = glm::vec3(0.5, 0.36, 0.23); // Brown

    cylinderCyan->textureColourMod = glm::vec3(0); // Black

    sphereBlue->reflectionCoefficient = 1;
    sphereRefracted->transparency = 0.2;
    sphereRefracted->refractionIndex = 1.05;
    sphereTexture->objectTexture = TextureBMP(FILENAME_2);
    sphereTexture->textureCenter = glm::vec3(-15.0, -5.0, -70.0);
    sphereTransparentHalf->transparency = 0.3;
    sphereTransparentHalf->half = true;

    planeTexture->objectTexture = TextureBMP(FILENAME_1);
    planeTexture->textureColourMod = glm::vec3(0.7);
    planeTexture->reflectionCoefficient = 0.1;

    torusMagenta->transform = glm::translate(torusMagenta->transform, glm::vec3(15, 0, -80.0));
    torusMagenta->transform = glm::rotate(torusMagenta->transform, -PI / 3, glm::vec3(0, 1, 0));

    /* ------ Object Applications ------ */
    // Pushing objects to the stack
    sceneObjects.push_back(coneLime);
    sceneObjects.push_back(cubeTexture);
    sceneObjects.push_back(cylinderCyan);
    sceneObjects.push_back(cylinderMaroon);
    sceneObjects.push_back(sphereBlue);
    sceneObjects.push_back(sphereRefracted);
    sceneObjects.push_back(sphereTexture);
    sceneObjects.push_back(sphereTransparentHalf);
    sceneObjects.push_back(planeTexture);
    sceneObjects.push_back(torusMagenta);
    // Creation of the tetrahedron
    sceneObjects.push_back(fLTriangle);
    sceneObjects.push_back(fRTriangle);
    sceneObjects.push_back(rearTriangle);
    sceneObjects.push_back(bottomTriangle);
//    sceneObjects.push_back(tetra);

    // Apply an inverse transformation on the transformed objects
    for (SceneObject *object : sceneObjects) object->transform = glm::inverse(object->transform);
}


// ------------- Main -------------
int main(int argc, char *argv[]) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(800, 800);
    glutInitWindowPosition(20, 20);
    glutCreateWindow("Main");
    glutDisplayFunc(display);
    initialize();
    glutMainLoop();
    return 0;
}


// Disclaimer
/*
 * Images provided by following links on an open source license:
 * https://opengameart.org/content/3-crate-textures-w-bump-normal
 * https://bdcraft.net/downloads/purebdcraft-minecraft/ - Allowed usage of their work
 *
 */