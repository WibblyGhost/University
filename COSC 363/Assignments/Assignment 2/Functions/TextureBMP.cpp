/*
 * TextureBMP.cpp
 * Created by Zachary Sanson on 22/05/2019.
 */


// ------------- Includes -------------
#include "TextureBMP.h"


// ------------- Defines an image loader for BMP files -------------
TextureBMP::TextureBMP(char *filename) {
    imageWidth = 0;
    imageHeight = 0;
    if (loadBMPImage(filename)) cout << "Image " << filename << "  loaded successfully.";
    else cerr << "Could not load image.";
}


glm::vec3 TextureBMP::getColorAt(float s, float t) {
    if (imageWidth == 0 || imageHeight == 0) return glm::vec3(0);
    int i = (int) (s * imageWidth);
    int j = (int) (t * imageHeight);
    if (i < 0 || i > imageWidth - 1 || j < 0 || j > imageHeight - 1) return glm::vec3(0);
    int index = ((j * imageWidth) + i) * imageChannels;
    int r = imageData[index];
    int g = imageData[index + 1];
    int b = imageData[index + 2];
    if (r < 0) r += 255;
    if (g < 0) g += 255;
    if (b < 0) b += 255;
    float rn = (float) r / 255.0;
    float gn = (float) g / 255.0;
    float bn = (float) b / 255.0;
    return glm::vec3(rn, gn, bn);
}


bool TextureBMP::loadBMPImage(char *filename) {
    char header1[18], header2[24];
    short int planes, bpp;
    int width, height;
    int nBytes, size, index, temp;
    ifstream file(filename, ios::in | ios::binary);
    if (! file) {
        cout << "*** Error opening image file: " << filename << endl;
        return false;
    }
    file.read(header1, 18);
    file.read((char *) &width, 4);
    file.read((char *) &height, 4);
    file.read((char *) &planes, 2);
    file.read((char *) &bpp, 2);
    file.read(header2, 24);
    nBytes = bpp / 8;
    size = width * height * nBytes;
    imageData = new char[size];
    file.read(imageData, size);
    if (nBytes > 2) {
        for (int i = 0; i < width * height; i ++) {
            index = i * nBytes;
            temp = imageData[index];
            imageData[index] = imageData[index + 2];
            imageData[index + 2] = temp;
        }
    }
    imageWidth = width;
    imageHeight = height;
    imageChannels = nBytes;
    return true;
}
