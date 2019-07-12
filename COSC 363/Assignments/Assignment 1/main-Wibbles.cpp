//
// Created by Zach Sanson on 6/03/2019.
//
//  ========================================================================
//  COSC363: Computer Graphics (2018);  University of Canterbury.
//
//  FILE NAME: main.cpp
//  ========================================================================

#include <iostream>
#include <fstream>
#include <climits>
#include <math.h>
#include <GL/freeglut.h>

using namespace std;

//--Globals ---------------------------------------------------------------
//float *x, *y, *z;  //vertex coordinate arrays
//int *t1, *t2, *t3; //triangles
//int nvrt, ntri;    //total number of vertices and triangles
float angle = - 10.0;  //Rotation angle for viewing
float cam_hgt = 100;


//----------draw a floor plane-------------------
void drawFloor()
{
    bool flag = false;
    glBegin(GL_QUADS);
    glNormal3f(0, 1, 0);
    for (int x = - 400; x <= 400; x += 20) {
        for (int z = - 400; z <= 400; z += 20) {
            if (flag) glColor3f(0.6, 1.0, 0.8);
            else glColor3f(0.8, 1.0, 0.6);
            glVertex3f(x, 0, z);
            glVertex3f(x, 0, z + 20);
            glVertex3f(x + 20, 0, z + 20);
            glVertex3f(x + 20, 0, z);
            flag = ! flag;
        }
    }
    glEnd();
}


//----------draw a floor plane-------------------
void create_wall(float wall_dimensions[3])
{
    // TODO: Does the shape generate from the middle coordinate?
    // Castle Walls
    float base_height = 5;
    float wall_length = wall_dimensions[0];
    float wall_height = wall_dimensions[1];
    float wall_width = wall_dimensions[2];
    // Wall Main
    glPushMatrix();
    glColor3f(0.5, 0.5, 0.5);
    glScalef(wall_dimensions[0], wall_dimensions[1], wall_dimensions[2]);
    glutSolidCube(1);
    glPopMatrix();

    // Wall Base
    glPushMatrix();
    glColor3f(0.4, 0, 0.2);
    glScalef(wall_dimensions[0] - 0.1, base_height, wall_dimensions[2] + 10);
    glutSolidCube(1);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.4, 0, 0.2);
    glScalef(wall_dimensions[0] - 0.1, base_height * 2, wall_dimensions[2] + 5);
    glutSolidCube(1);
    glPopMatrix();
}


//--Display: ----------------------------------------------------------------------
//--This is the main display module containing function calls for generating
//--the scene.
void display()
{
    float lpos[4] ={0., 100., 0., 1.0};  //Light's position
    float wall_dimensions[3] = {100, 50, 8}; // Length, height, width
    float gate_width = 15;

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);    //GL_LINE = Wireframe;   GL_FILL = Solid
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    gluLookAt(0, cam_hgt, 200, 0, 0, 0, 0, 1, 0);
    glLightfv(GL_LIGHT0, GL_POSITION, lpos);   //set light position
    glRotatef(angle, 0.0, 1.0, 0.0);        //rotate the whole scene

    drawFloor();

    glPushMatrix();
    glTranslatef(- gate_width - wall_dimensions[0]/2, 0, 0);
    create_wall(wall_dimensions);
    glPopMatrix();
    glPushMatrix();
    glTranslatef(gate_width + wall_dimensions[0]/2, 0, 0);
    create_wall(wall_dimensions);
    glPopMatrix();
    glPushMatrix();
    glRotatef(90, 0, 1, 0);
    glTranslatef((wall_dimensions[0] - gate_width)/2 + 5, 0, wall_dimensions[0] + gate_width);
    create_wall(wall_dimensions);
    glPopMatrix();
    glFlush();

}

//------- Initialize OpenGL parameters -----------------------------------
void initialize()
{
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);    //Background colour
    glEnable(GL_LIGHTING);                    //Enable OpenGL states
    glEnable(GL_LIGHT0);
    glEnable(GL_COLOR_MATERIAL);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_NORMALIZE);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60, 1, 50, 1000);  //The camera view volume
}

//------------ Special key event callback ---------------------------------
// To enable the use of left and right arrow keys to rotate the scene
void special(int key, int x, int y)
{
    if (key == GLUT_KEY_LEFT) angle ++;
    else if (key == GLUT_KEY_RIGHT) angle --;
    else if (key == GLUT_KEY_UP) cam_hgt ++;
    else if (key == GLUT_KEY_DOWN) cam_hgt --;
    if (cam_hgt > 200) cam_hgt = 200;
    else if (cam_hgt < 10) cam_hgt = 10;
    glutPostRedisplay();
}

//  ------- Main: Initialize glut window and register call backs -----------
int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_DEPTH);
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(10, 10);
    glutCreateWindow("Main");
    initialize();
    glutDisplayFunc(display);
    glutSpecialFunc(special);
    glutMainLoop();
    return 0;
}
