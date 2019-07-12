/*
 * Cube.cpp
 * Created by Zachary Sanson on 21/05/2019.
 */


// ------------- Includes -------------
#include "Cube.h"
#include <math.h>


// ------------- Returns a colour value when the ray intercepts the object -------------
float Cube::intersect(glm::vec3 pos, glm::vec3 dir) {
    glm::vec3 min = glm::vec3(center.x - size / 2, center.y, center.z - size / 2);
    glm::vec3 max = glm::vec3(center.x + size / 2, center.y + size, center.z + size / 2);
    glm::vec3 axis[3] = {glm::vec3(1, 0, 0), glm::vec3(0, 1, 0), glm::vec3(0, 0, 1)};
    glm::vec3 maxNorm, minNorm;
    float tMin = -INFINITY;
    float tMax = INFINITY;
    float solutions[2];
    for (int k = 0; k < 3; k++) {
        if (dir[k] != 0) {
            solutions[0] = (min[k] - pos[k]) / dir[k];
            solutions[1] = (max[k] - pos[k]) / dir[k];
            tMin = fmax(tMin, fmin(solutions[0], solutions[1]));
            tMax = fmin(tMax, fmax(solutions[0], solutions[1]));
            if (solutions[0] > 0 && tMin == solutions[0]) minNorm = -axis[k];
            else if (solutions[1] > 0 && tMin == solutions[1]) minNorm = axis[k];
            else if (solutions[0] > 0 && tMax == solutions[0]) maxNorm = -axis[k];
            else if (solutions[1] > 0 && tMax == solutions[1]) maxNorm = axis[k];
        } else if ((pos[k] < min[k]) || (pos[k] > max[k])) return -1;
    }
    if (tMin >= tMax) return -1;
    else if (tMin > 0) return tMin;
    else if (tMax > 0) return tMax;
    return -1;
}


// ------------- Returns the unit normal vector at a given point -------------
glm::vec3 Cube::normal(glm::vec3 point) {
    glm::vec3 norm = glm::vec3(point.x - center.x, point.y - center.y - (size / 2), point.z - center.z);
    return glm::normalize(norm);
}
