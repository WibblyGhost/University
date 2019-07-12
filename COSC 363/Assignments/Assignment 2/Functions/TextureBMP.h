/*
 * TextureBMP.h
 * Created by Zachary Sanson on 22/05/2019.
 */


#ifndef H_TEXTURE_BMP
#define H_TEXTURE_BMP


// ------------- Includes -------------
#include <iostream>
#include <fstream>
#include <glm/glm.hpp>

using namespace std;


// ------------- Defines an image loader for BMP files -------------
class TextureBMP {
private:
    int imageWidth, imageHeight, imageChannels;
    char *imageData;

    bool loadBMPImage(char *string);

public:
    TextureBMP() : imageWidth(0), imageHeight(0), imageChannels(0) {}

    TextureBMP(char *string);

    glm::vec3 getColorAt(float s, float t);
};


#endif //H_TEXTURE_BMP
