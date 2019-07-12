//
// Created by Zachary Sanson on 06/03/2019.
//
//  ========================================================================
//  COSC363: Computer Graphics (2019); Assignment 1
//
//  FILE NAME: main.cpp
//  ========================================================================

#include <iostream>
#include <fstream>
#include <climits>
#include <math.h>
#include "loadTGA.h"
//#include <cmath>
#include <GL/freeglut.h>

#define GL_CLAMP_TO_EDGE 0x812F


// IMPORTANT //
// COMPLETE: 2.1, 2.2, 2.3, 2.4, 2.5
// COMPLETE: 2.6 - Texture three objects - Wooden Crates (3 Types), Skybox, Walls (Textures < 10 MB)


// EXTRAS //
// COMPLETE: Create a shadow on a object - Spaceship, Robots (1 Mark)
// COMPLETE: Spotlight on a moving object - On the patrolling robots (2 Marks)
// TODO: Additional animated system inside castle (1 - 3 Marks)
// COMPLETE: Create two camera angles - One FP & one TP (2 Marks)
// COMPLETE: Physics models - Done on cannonball (1 - 2 Marks)
// TODO: Custom built sweep surface (1 - 2 Marks)
// COMPLETE: A surface generated from a mathematical equation - Archway (1 - 2 Marks)
// COMPLETE: Collision detection - Done on the edges of the skybox (1 - 2 Marks)
// TODO: Particle systems (2 - 4 Marks)


// ------------- Globals -------------
using namespace std;
struct player {
    float angle, lx, lz, x, z, height, movement_speed, turn_speed;
} Pl = {0, 0, - 1, 0, 150, 20, 5, 0.05};

struct objects {
    float ship_height, ship_angle, robot_pos, robot_angle, cannonball_y, cannonball_z;
} Ob = {0, 0, 0, 90, 42, 40};

GLuint object_textures[4];
GLuint skybox_texture[6];

bool is_flying = false;
float *x, *y, *z;
int *t1, *t2, *t3;
int n_vert, n_tri;
const float PI = 3.14159;
const int SKYBOX_SIZE = 400;
const char *CANNON = "../Assets/Cannon.off";
const char TEXTURE_LIST[5][30] = {"../Assets/wall.tga", "../Assets/crate0.tga", "../Assets/crate1.tga", "../Assets/crate2.tga"};
const char IMAGE_LIST[6][30] = {"../Assets/negx.tga", "../Assets/posz.tga", "../Assets/posx.tga", "../Assets/negz.tga", "../Assets/posy.tga", "../Assets/negy.tga"};


// ------------- Loads mesh file -------------
void load_mesh_file(const char *f_name)
{
    ifstream fp_in;
    int num, ne;
    fp_in.open(f_name, ios::in);
    if (! fp_in.is_open()) {
        cout << "Error opening mesh file" << endl;
        exit(1);
    }
    fp_in.ignore(INT_MAX, '\n');
    fp_in >> n_vert >> n_tri >> ne;
    x = new float[n_vert];
    y = new float[n_vert];
    z = new float[n_vert];
    t1 = new int[n_tri];
    t2 = new int[n_tri];
    t3 = new int[n_tri];
    for (int i = 0; i < n_vert; i ++) fp_in >> x[i] >> y[i] >> z[i];
    for (int i = 0; i < n_tri; i ++) {
        fp_in >> num >> t1[i] >> t2[i] >> t3[i];
        if (num != 3) {
            cout << "ERROR: Polygon with index " << i << " is not a triangle." << endl;
            exit(1);
        }
    }
    fp_in.close();
    cout << " File successfully read." << endl;
}


// ------------- Loads TGA texture file -------------
void load_TGA_textures(const char t_name[][30], GLuint *o_name, int n_textures)
{
    glGenTextures(n_textures, o_name);
    for (int i = 0; i < n_textures; i ++) {
        glBindTexture(GL_TEXTURE_2D, o_name[i]);
        loadTGA(t_name[i]);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
    }

}


// ------------- Computers normal vector  -------------
void normal(int t_index)
{
    float x1 = x[t1[t_index]], x2 = x[t2[t_index]], x3 = x[t3[t_index]];
    float y1 = y[t1[t_index]], y2 = y[t2[t_index]], y3 = y[t3[t_index]];
    float z1 = z[t1[t_index]], z2 = z[t2[t_index]], z3 = z[t3[t_index]];
    float nx, ny, nz;
    nx = y1 * (z2 - z3) + y2 * (z3 - z1) + y3 * (z1 - z2);
    ny = z1 * (x2 - x3) + z2 * (x3 - x1) + z3 * (x1 - x2);
    nz = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2);
    glNormal3f(nx, ny, nz);
}


// ------------- Draws a skybox from selected image files -------------
void skybox()
{
    glPushMatrix();
    glTranslatef(0, - 0.2, 0);
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE);
    glEnable(GL_TEXTURE_2D);
    // ------------- Left Wall -------------
    glBindTexture(GL_TEXTURE_2D, skybox_texture[0]);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 0);
    glVertex3f(- SKYBOX_SIZE, 0, SKYBOX_SIZE);
    glTexCoord2f(1, 0);
    glVertex3f(- SKYBOX_SIZE, 0, - SKYBOX_SIZE);
    glTexCoord2f(1, 1);
    glVertex3f(- SKYBOX_SIZE, SKYBOX_SIZE, - SKYBOX_SIZE);
    glTexCoord2f(0, 1);
    glVertex3f(- SKYBOX_SIZE, SKYBOX_SIZE, SKYBOX_SIZE);
    glEnd();
    // ------------- Front Wall -------------
    glBindTexture(GL_TEXTURE_2D, skybox_texture[1]);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 0);
    glVertex3f(- SKYBOX_SIZE, 0, - SKYBOX_SIZE);
    glTexCoord2f(1, 0);
    glVertex3f(SKYBOX_SIZE, 0, - SKYBOX_SIZE);
    glTexCoord2f(1, 1);
    glVertex3f(SKYBOX_SIZE, SKYBOX_SIZE, - SKYBOX_SIZE);
    glTexCoord2f(0, 1);
    glVertex3f(- SKYBOX_SIZE, SKYBOX_SIZE, - SKYBOX_SIZE);
    glEnd();
    // ------------- Right Wall -------------
    glBindTexture(GL_TEXTURE_2D, skybox_texture[2]);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 0);
    glVertex3f(SKYBOX_SIZE, 0, - SKYBOX_SIZE);
    glTexCoord2f(1, 0);
    glVertex3f(SKYBOX_SIZE, 0, SKYBOX_SIZE);
    glTexCoord2f(1, 1);
    glVertex3f(SKYBOX_SIZE, SKYBOX_SIZE, SKYBOX_SIZE);
    glTexCoord2f(0, 1);
    glVertex3f(SKYBOX_SIZE, SKYBOX_SIZE, - SKYBOX_SIZE);
    glEnd();
    // ------------- Rear Wall -------------
    glBindTexture(GL_TEXTURE_2D, skybox_texture[3]);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 0);
    glVertex3f(SKYBOX_SIZE, 0, SKYBOX_SIZE);
    glTexCoord2f(1, 0);
    glVertex3f(- SKYBOX_SIZE, 0, SKYBOX_SIZE);
    glTexCoord2f(1, 1);
    glVertex3f(- SKYBOX_SIZE, SKYBOX_SIZE, SKYBOX_SIZE);
    glTexCoord2f(0, 1);
    glVertex3f(SKYBOX_SIZE, SKYBOX_SIZE, SKYBOX_SIZE);
    glEnd();
    // ------------- Top -------------
    glBindTexture(GL_TEXTURE_2D, skybox_texture[4]);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 1);
    glVertex3f(- SKYBOX_SIZE, SKYBOX_SIZE, - SKYBOX_SIZE);
    glTexCoord2f(1, 1);
    glVertex3f(SKYBOX_SIZE, SKYBOX_SIZE, - SKYBOX_SIZE);
    glTexCoord2f(1, 0);
    glVertex3f(SKYBOX_SIZE, SKYBOX_SIZE, SKYBOX_SIZE);
    glTexCoord2f(0, 0);
    glVertex3f(- SKYBOX_SIZE, SKYBOX_SIZE, SKYBOX_SIZE);
    glEnd();
    // ------------- Floor -------------
    glBindTexture(GL_TEXTURE_2D, skybox_texture[5]);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 0);
    glVertex3f(- SKYBOX_SIZE, 0, SKYBOX_SIZE);
    glTexCoord2f(1, 0);
    glVertex3f(SKYBOX_SIZE, 0, SKYBOX_SIZE);
    glTexCoord2f(1, 1);
    glVertex3f(SKYBOX_SIZE, 0, - SKYBOX_SIZE);
    glTexCoord2f(0, 1);
    glVertex3f(- SKYBOX_SIZE, 0, - SKYBOX_SIZE);
    glEnd();
    glDisable(GL_TEXTURE_2D);
    glPopMatrix();
}


// ------------- Draws a floor plane -------------
void floor()
{
    float white[4] = {1, 1, 1, 1};
    float black[4] = {0};
    glColor4f(0.2, 0.5, 0.2, 1);
    glNormal3f(0, 1, 0);
    glMaterialfv(GL_FRONT, GL_SPECULAR, black);
    glBegin(GL_QUADS);
    for (int i = - SKYBOX_SIZE; i < SKYBOX_SIZE; i ++) {
        for (int j = - SKYBOX_SIZE; j < SKYBOX_SIZE; j ++) {
            glVertex3f(i, 0, j);
            glVertex3f(i, 0, j + 1);
            glVertex3f(i + 1, 0, j + 1);
            glVertex3f(i + 1, 0, j);
        }
    }
    glEnd();
    glClearColor(1, 1, 1, 1);
    glMaterialfv(GL_FRONT, GL_SPECULAR, white);
}


// Replacing glutSolidCube() to allow for textures
// ***** http://www.opengl.org/resources/libraries/glut/ *****//
static void drawBox(GLfloat size, GLuint texture)
{
    glPushMatrix();
    glRotatef(90, 1, 0, 0);
    GLenum type = GL_QUADS;
    static GLfloat n[6][3] =
            {
                    {- 1.0, 0.0,   0.0},
                    {0.0,   1.0,   0.0},
                    {1.0,   0.0,   0.0},
                    {0.0,   - 1.0, 0.0},
                    {0.0,   0.0,   1.0},
                    {0.0,   0.0,   - 1.0}
            };
    static GLint faces[6][4] =
            {
                    {0, 1, 2, 3},
                    {3, 2, 6, 7},
                    {7, 6, 5, 4},
                    {4, 5, 1, 0},
                    {5, 6, 2, 1},
                    {7, 4, 0, 3}
            };
    GLfloat v[8][3];
    GLint i;
    v[0][0] = v[1][0] = v[2][0] = v[3][0] = - size / 2;
    v[4][0] = v[5][0] = v[6][0] = v[7][0] = size / 2;
    v[0][1] = v[1][1] = v[4][1] = v[5][1] = - size / 2;
    v[2][1] = v[3][1] = v[6][1] = v[7][1] = size / 2;
    v[0][2] = v[3][2] = v[4][2] = v[7][2] = - size / 2;
    v[1][2] = v[2][2] = v[5][2] = v[6][2] = size / 2;
    // Textures
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, texture);
    for (i = 5; i >= 0; i --) {
        glBegin(type);
        glNormal3fv(&n[i][0]);
        glVertex3fv(&v[faces[i][0]][0]);
        glTexCoord2f(0, 0);
        glVertex3fv(&v[faces[i][1]][0]);
        glTexCoord2f(1, 0);
        glVertex3fv(&v[faces[i][2]][0]);
        glTexCoord2f(1, 1);
        glVertex3fv(&v[faces[i][3]][0]);
        glTexCoord2f(0, 1);
        glEnd();
    }
    glDisable(GL_TEXTURE_2D);
    glPopMatrix();
}
//
//void APIENTRY glutSolidCube(GLdouble size)
//{
//    drawBox(size, GL_QUADS);
//}
//// ***** http://www.opengl.org/resources/libraries/glut/ *****//


// ------------- Draws a cannon from mesh file -------------
void create_cannon()
{
    // Cannon
    glPushMatrix();
    glRotatef(- 90, 0, 1, 0);
    glRotatef(15, 0, 0, 1);
    glColor3f(0.4, 0.5, 0.4);
    glBegin(GL_TRIANGLES);
    for (int tIndex = 0; tIndex < n_tri; tIndex ++) {
        normal(tIndex);
        glVertex3d(x[t1[tIndex]], y[t1[tIndex]], z[t1[tIndex]]);
        glVertex3d(x[t2[tIndex]], y[t2[tIndex]], z[t2[tIndex]]);
        glVertex3d(x[t3[tIndex]], y[t3[tIndex]], z[t3[tIndex]]);
    }
    // Stand
    glEnd();
    glPopMatrix();
    glPushMatrix();
    glScalef(1, 4, 1);
    glutSolidCube(12);
    glPopMatrix();
    // Cannon Ball
    glPushMatrix();
    glColor3f(0.2, 0.2, 0.2);
    glTranslatef(0, Ob.cannonball_y, Ob.cannonball_z);
    glutSolidSphere(6, 15, 15);
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a pile of crates -------------
void create_crate(float crate_size)
{
    drawBox(crate_size, object_textures[1]);
    glPushMatrix();
    glScalef(0.6, 0.6, 0.6);
    glTranslatef(crate_size / 3, crate_size * 1.32, 0);
    glRotatef(25, 0, 1, 0);
    drawBox(crate_size, object_textures[2]);
    glPopMatrix();
    glPushMatrix();
    glScalef(0.7, 0.7, 0.7);
    glTranslatef(0, - (crate_size * 0.2), crate_size * 1.2);
    drawBox(crate_size, object_textures[1]);
    glPopMatrix();
    glPushMatrix();
    glScalef(0.4, 0.4, 0.4);
    glTranslatef(crate_size * 1.8, - crate_size * 0.7, 0);
    drawBox(crate_size, object_textures[3]);
    glPopMatrix();
}


// ------------- Draws a pile of crates -------------
void create_crate_shadow(float crate_size)
{
    glColor3f(0.1, 0.1, 0.1);
    glutSolidCube(crate_size);
    glPushMatrix();
    glScalef(0.6, 0.6, 0.6);
    glTranslatef(crate_size / 3, crate_size * 1.32, 0);
    glRotatef(25, 0, 1, 0);
    glutSolidCube(crate_size);
    glPopMatrix();
    glPushMatrix();
    glScalef(0.7, 0.7, 0.7);
    glTranslatef(0, - (crate_size * 0.2), crate_size * 1.2);
    glutSolidCube(crate_size);
    glPopMatrix();
    glPushMatrix();
    glScalef(0.4, 0.4, 0.4);
    glTranslatef(crate_size * 1.8, - crate_size * 0.7, 0);
    glutSolidCube(crate_size);
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a castle pillar -------------
void create_pillar(float pillar_dimensions[2])
{
    float base_height = 2.5;
    int circle_divisions = 15;
    // Pillar base
    glPushMatrix();
    glColor3f(0.4, 0, 0.2);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCylinder(pillar_dimensions[0] + 5, base_height, circle_divisions, circle_divisions);
    glutSolidCylinder(pillar_dimensions[0] + 2.5, base_height * 3, circle_divisions, circle_divisions);
    glPopMatrix();
    // Pillar Main
    glPushMatrix();
    glColor3f(0.2, 0.2, 0.2);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCylinder(pillar_dimensions[0], pillar_dimensions[1], circle_divisions, circle_divisions);
    glPopMatrix();
    glClearColor(1, 1, 1, 1);

}


// ------------- Draws a castle wall -------------
void create_wall(float wall_dimensions[3])
{
    // Castle Walls
    float base_height = 2.5;
    // Wall Base
    glPushMatrix();
    glColor3f(0.4, 0, 0.2);
    glTranslatef(0, base_height / 2, 0);
    glScalef(wall_dimensions[0] - 0.1, base_height, wall_dimensions[2] + 10);
    glutSolidCube(1);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.4, 0, 0.2);
    glTranslatef(0, (base_height / 2) * 3, 0);
    glScalef(wall_dimensions[0] - 0.1, base_height * 3, wall_dimensions[2] + 5);
    glutSolidCube(1);
    glPopMatrix();
    // Wall Main
    glPushMatrix();
    glColor3f(0.2, 0.2, 0.2);
    glTranslatef(0, wall_dimensions[1] / 2, 0);
    glScalef(wall_dimensions[0], wall_dimensions[1], wall_dimensions[2]);
    // FIXME: Texture is stretched
    drawBox(1, object_textures[0]);
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a castle wall -------------
void create_wall_shadow(float wall_dimensions[3])
{
    // Castle Walls
    float base_height = 2.5;
    glPushMatrix();
    glScalef(1, 0.7, 1);
    // Wall Base
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, base_height / 2, 0);
    glScalef(wall_dimensions[0] - 0.1, base_height, wall_dimensions[2] + 10);
    glutSolidCube(1);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, (base_height / 2) * 3, 0);
    glScalef(wall_dimensions[0] - 0.1, base_height * 3, wall_dimensions[2] + 5);
    glutSolidCube(1);
    glPopMatrix();
    // Wall Main
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, wall_dimensions[1] / 2, 0);
    glScalef(wall_dimensions[0], wall_dimensions[1], wall_dimensions[2]);
    glutSolidCube(1);
    glPopMatrix();
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws an archway -------------
void create_archway(float width, float depth, float height, float offset, float slices)
{
    glPushMatrix();
    glColor3f(0.2, 0.2, 0.2);
    glTranslatef(0, 0, - depth / 2);
    glScalef(width / 2, height / offset, 1);
    // Archway Walls
    glBegin(GL_QUADS);
    for (float i = 0; i < slices; i ++) {
        for (float j : {0.f, depth}) {
            float curve_angle = (i * PI) / slices;
            float next_angle = ((i + 1) * PI) / slices;
            glVertex3f(cos(curve_angle), sin(curve_angle), j);
            glVertex3f(cos(curve_angle), offset, j);
            glVertex3f(cos(next_angle), offset, j);
            glVertex3f(cos(next_angle), sin(next_angle), j);
        }
    }
    glEnd();
    // Archway Inner
    glBegin(GL_QUAD_STRIP);
    for (float i = 0; i < slices; i ++) {
        float curve_angle = (i * PI) / slices;
        float next_angle = ((i + 1) * PI) / slices;
        glVertex3f(cos(curve_angle), sin(curve_angle), depth);
        glVertex3f(cos(next_angle), sin(next_angle), depth);
        glVertex3f(cos(curve_angle), sin(curve_angle), 0);
        glVertex3f(cos(next_angle), sin(next_angle), 0);
    }
    glEnd();
    // Archway Top
    glBegin(GL_QUADS);
    glVertex3f(1, offset, 0);
    glVertex3f(1, offset, depth);
    glVertex3f(- 1, offset, depth);
    glVertex3f(- 1, offset, 0);
    glEnd();
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws an archway -------------
void create_archway_shadow(float width, float depth, float height, float offset, float slices)
{
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, 0, - depth / 2);
    glScalef(width / 2, (height / offset) * 0.7, 1);
    // Archway Walls
    glBegin(GL_QUADS);
    for (float i = 0; i < slices; i ++) {
        for (float j : {0.f, depth}) {
            float curve_angle = (i * PI) / slices;
            float next_angle = ((i + 1) * PI) / slices;
            glVertex3f(cos(curve_angle), sin(curve_angle), j);
            glVertex3f(cos(curve_angle), offset, j);
            glVertex3f(cos(next_angle), offset, j);
            glVertex3f(cos(next_angle), sin(next_angle), j);
        }
    }
    glEnd();
    // Archway Inner
    glBegin(GL_QUAD_STRIP);
    for (float i = 0; i < slices; i ++) {
        float curve_angle = (i * PI) / slices;
        float next_angle = ((i + 1) * PI) / slices;
        glVertex3f(cos(curve_angle), sin(curve_angle), depth);
        glVertex3f(cos(next_angle), sin(next_angle), depth);
        glVertex3f(cos(curve_angle), sin(curve_angle), 0);
        glVertex3f(cos(next_angle), sin(next_angle), 0);
    }
    glEnd();
    // Archway Top
    glBegin(GL_QUADS);
    glVertex3f(1, offset, 0);
    glVertex3f(1, offset, depth);
    glVertex3f(- 1, offset, depth);
    glVertex3f(- 1, offset, 0);
    glEnd();
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a spaceship -------------
void create_spaceship()
{
    float top_height = 35;
    float body_height = 35;
    float body_radius = 15;
    float thruster_height = 15;
    float fin_height = 30;
    int no_legs = 4;
    float model_height = top_height + body_height - (fin_height / 3);
    // Cone
    glPushMatrix();
    glColor3f(0.6, 0.6, 0);
    glTranslatef(0, model_height, 0);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCone(15, top_height, 10, 10);
    glPopMatrix();
    model_height -= top_height;
    // Body
    glPushMatrix();
    glColor3f(0.3, 0.2, 0);
    glTranslatef(0, model_height, 0);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCylinder(15, body_height, 10, 10);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.3, 0.2, 0);
    glTranslatef(0, model_height, 0);
    glutSolidSphere(body_radius - 0.2, 10, 10);
    glPopMatrix();
    // Fins
    for (int i = 0; i < no_legs; i ++) {
        int seperation_angle = (360 * i) / no_legs;
        glPushMatrix();
        glColor3f(0.6, 0.6, 0);
        glTranslatef(0, model_height + 10, 0);
        glRotatef(seperation_angle, 0, 1, 0);
        glRotatef(55, 1, 0, 0);
        glTranslatef(0, 0, 15);
        glutSolidCone(8, fin_height, 4, 10);
        glPopMatrix();
    }
    model_height -= body_height / 2;
    // Thruster
    glPushMatrix();
    glColor3f(0.6, 0.6, 0);
    glTranslatef(0, model_height, 0);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCone(10, thruster_height, 10, 10);
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a spaceship shadow -------------
void create_spaceship_shadow()
{
    float top_height = 35;
    float body_height = 35;
    float body_radius = 15;
    float thruster_height = 15;
    float fin_height = 30;
    int no_legs = 4;
    float model_height = top_height + body_height - (fin_height / 3);
    // Cone
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height, 0);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCone(15, top_height, 10, 10);
    glPopMatrix();
    model_height -= top_height;
    // Body
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height, 0);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCylinder(15, body_height, 10, 10);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height, 0);
    glutSolidSphere(body_radius - 0.2, 10, 10);
    glPopMatrix();
    // Fins
    for (int i = 0; i < no_legs; i ++) {
        int seperation_angle = (360 * i) / no_legs;
        glPushMatrix();
        glColor3f(0.1, 0.1, 0.1);
        glTranslatef(0, model_height + 10, - 1);
        glRotatef(seperation_angle, 0, 1, 0);
        glRotatef(55, 1, 0, 0);
        glTranslatef(0, 0, 15);
        glutSolidCone(8, fin_height, 4, 10);
        glPopMatrix();
    }
    model_height -= body_height / 2;
    // Thruster
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height, 0);
    glRotatef(- 90, 1, 0, 0);
    glutSolidCone(10, thruster_height, 10, 10);
    glPopMatrix();
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a robot -------------
void create_robot()
{
    float slices = 20;
    float stacks = 10;
    float torch_length = 20;
    float torch_width = 4;
    float torch_cone = 6;
    // Body Dimensions
    float radius = 10;
    float neck_height = 4;
    float body_height = 30;
    float leg_height = body_height;
    float foot_height = neck_height;
    float foot_length = leg_height / 2;
    float model_height = radius + neck_height + body_height + leg_height + foot_height;
    // Robot head
    glPushMatrix();
    glColor3f(0.6, 0, 0.4);
    glTranslatef(0, model_height, 0);
    glutSolidSphere(radius, slices, stacks);
    glPopMatrix();
    model_height -= radius;
    // Robot Neck
    glPushMatrix();
    glColor3f(0.6, 0, 0.3);
    glTranslatef(0, model_height + 2, 0);
    glRotatef(90, 1, 0, 0);
    glutSolidCylinder(radius / 3, neck_height + 2, slices, stacks);
    glPopMatrix();
    model_height -= neck_height;
    // Robot Body
    glPushMatrix();
    glColor3f(0.2, 0, 0.09);
    glTranslatef(0, model_height, 0);
    glRotatef(90, 1, 0, 0);
    glutSolidCylinder(radius, body_height, slices, stacks);
    glPopMatrix();
    // Robot Shoulder
    glPushMatrix();
    glColor3f(0.2, 0, 0.09);
    glTranslatef(0, model_height - 2, 0);
    glScalef(radius * 3.5, 4, radius);
    glutSolidCube(1);
    glPopMatrix();
    // Robot Arms
    for (int flag = - 1; flag <= 1; flag += 2) {
        glPushMatrix();
        glColor3f(0.6, 0, 0.3);
        glTranslatef(flag * radius * 1.5, model_height - 2, 0);
        glRotatef(90, 1, 0, 0);
        glutSolidCylinder(radius / 3, body_height, 6, 6);
        glPopMatrix();
    }
    model_height -= body_height;
    // Torch
    glPushMatrix();
    glColor3f(0, 0, 0);
    glTranslatef(radius * 1.5, model_height - torch_width, torch_length / 2 - 2);
    glScalef(torch_width, torch_width, torch_length);
    glutSolidCube(1);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.8, 0.8, 0.8);
    glTranslatef(radius * 1.5, model_height - torch_width, torch_length);
    glRotatef(180, 1, 0.4, 0);
    glutSolidCone(torch_cone, torch_cone, 4, 4);
    glPopMatrix();
    // Robot Legs
    for (int flag = - 1; flag <= 1; flag += 2) {
        glPushMatrix();
        glColor3f(0.6, 0, 0.2);
        glTranslatef(flag * radius / 2, model_height, 0);
        glRotatef(90, 1, 0, 0);
        glutSolidCylinder(radius / 3, body_height, 6, 6);
        glPopMatrix();
    }
    model_height -= leg_height;
    // Robot Feet
    for (int flag = - 1; flag <= 1; flag += 2) {
        glPushMatrix();
        glColor3f(0.6, 0, 0.3);
        glTranslatef(flag * radius / 2, model_height / 2, foot_length / 2.5);
        glScalef(radius / 2, foot_height, foot_length);
        glutSolidCube(1);
        glPopMatrix();
    }
    glClearColor(1, 1, 1, 1);
}


// ------------- Draws a robot shadow -------------
void create_robot_shadow()
{
    float slices = 20;
    float stacks = 10;
    float torch_length = 20;
    float torch_width = 4;
    float torch_cone = 6;
    // Body Dimensions
    float radius = 10;
    float neck_height = 4;
    float body_height = 30;
    float leg_height = body_height;
    float foot_height = neck_height;
    float foot_length = leg_height / 2;
    float model_height = radius + neck_height + body_height + leg_height + foot_height;
    // Robot head
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height, 0);
    glutSolidSphere(radius, slices, stacks);
    glPopMatrix();
    model_height -= radius;
    // Robot Neck
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height + 2, 0);
    glRotatef(90, 1, 0, 0);
    glutSolidCylinder(radius / 3, neck_height + 2, slices, stacks);
    glPopMatrix();
    model_height -= neck_height;
    // Robot Body
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height, 0);
    glRotatef(90, 1, 0, 0);
    glutSolidCylinder(radius, body_height, slices, stacks);
    glPopMatrix();
    // Robot Shoulder
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(0, model_height - 2, 0);
    glScalef(radius * 3.5, 4, radius);
    glutSolidCube(1);
    glPopMatrix();
    // Robot Arms
    for (int flag = - 1; flag <= 1; flag += 2) {
        glPushMatrix();
        glColor3f(0.1, 0.1, 0.1);
        glTranslatef(flag * radius * 1.5, model_height - 2, 0);
        glRotatef(90, 1, 0, 0);
        glutSolidCylinder(radius / 3, body_height, 6, 6);
        glPopMatrix();
    }
    model_height -= body_height;
    // Torch
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(radius * 1.5, model_height - torch_width, torch_length / 2 - 2);
    glScalef(torch_width, torch_width, torch_length);
    glutSolidCube(1);
    glPopMatrix();
    glPushMatrix();
    glColor3f(0.1, 0.1, 0.1);
    glTranslatef(radius * 1.5, model_height - torch_width, torch_length);
    glRotatef(180, 1, 0.4, 0);
    glutSolidCone(torch_cone, torch_cone, 4, 4);
    glPopMatrix();
    // Robot Legs
    for (int flag = - 1; flag <= 1; flag += 2) {
        glPushMatrix();
        glColor3f(0.1, 0.1, 0.1);
        glTranslatef(flag * radius / 2, model_height, 0);
        glRotatef(90, 1, 0, 0);
        glutSolidCylinder(radius / 3, body_height, 6, 6);
        glPopMatrix();
    }
    model_height -= leg_height;
    // Robot Feet
    for (int flag = - 1; flag <= 1; flag += 2) {
        glPushMatrix();
        glColor3f(0.1, 0.1, 0.1);
        glTranslatef(flag * radius / 2, model_height / 2, foot_length / 2.5);
        glScalef(radius / 2, foot_height, foot_length);
        glutSolidCube(1);
        glPopMatrix();
    }
    glClearColor(1, 1, 1, 1);
}


// ------------- Timer for spaceship take off -------------
void timer_ship(int value)
{
    static float increment = 0;
    Ob.ship_height += (increment += 0.2);
    Ob.ship_angle += 2;
    if (increment >= 10) increment = 10;
    if (Ob.ship_height >= SKYBOX_SIZE) return;
    glutPostRedisplay();
    glutTimerFunc(35, timer_ship, 0);
}


// ------------- Timer for patrolling robots -------------
void timer_robot(int value)
{
    static float increment = 1;
    static int flag = 1;
    if (Ob.robot_pos > 50) {
        flag = - 1;
        Ob.robot_angle -= 18;
    } else if (Ob.robot_pos < 0) {
        flag = 1;
        Ob.robot_angle += 18;
    }
    if (increment >= 1) increment = 1;
    else if (increment <= - 1) increment = - 1;
    Ob.robot_pos += (increment += 0.2 * flag);
    glutPostRedisplay();
    glutTimerFunc(35, timer_robot, 0);
}


// ------------- Timer for cannonball -------------
void timer_cannonball(int value)
{
    static float increment = 8;
    static float increment_1 = 30;
    Ob.cannonball_y += -- increment;
    Ob.cannonball_z += -- increment_1;
    if (Ob.cannonball_y < - 100) return;
    glutPostRedisplay();
    glutTimerFunc(35, timer_cannonball, 0);
}


// ------------- Special key event callback -------------
/*
 * Left Arrow: Rotate Left
 * Right Arrow: Rotate Right
 * Up Arrow: Move Forward
 * Down Arrow: Move Backward
 * Shift + Up Arrow: Increase Height
 * Shift + Down Arrow: Decrease Height
 */
void special(int key, int x, int y)
{
    int skybox_limit = SKYBOX_SIZE - 5;
    if (key == GLUT_KEY_CTRL_L) is_flying = ! is_flying;
    if (! is_flying) {
        switch (key) {
            case GLUT_KEY_LEFT:
                Pl.angle -= Pl.turn_speed;
                Pl.lx = sin(Pl.angle);
                Pl.lz = - cos(Pl.angle);
                break;
            case GLUT_KEY_RIGHT:
                Pl.angle += Pl.turn_speed;
                Pl.lx = sin(Pl.angle);
                Pl.lz = - cos(Pl.angle);
                break;
            case GLUT_KEY_UP:
                if (glutGetModifiers() == GLUT_ACTIVE_SHIFT) Pl.height ++;
                else {
                    Pl.x += Pl.lx * Pl.movement_speed;
                    Pl.z += Pl.lz * Pl.movement_speed;
                }
                break;
            case GLUT_KEY_DOWN:
                if (glutGetModifiers() == GLUT_ACTIVE_SHIFT) Pl.height --;
                else {
                    Pl.x -= Pl.lx * Pl.movement_speed;
                    Pl.z -= Pl.lz * Pl.movement_speed;
                }
                break;
        }
    }
    if (Pl.height < 10) Pl.height = 10;
    else if (Pl.height > 100) Pl.height = 100;
    if (Pl.x > skybox_limit) Pl.x = skybox_limit;
    else if (Pl.x < - skybox_limit) Pl.x = - skybox_limit;
    if (Pl.z > skybox_limit) Pl.z = skybox_limit;
    else if (Pl.z < - skybox_limit) Pl.z = - skybox_limit;
    glutPostRedisplay();
}


// ------------- Keyboard key event callback -------------
/*
 * X: Launch Ship
 * Z: Launch Cannonballs
 */
void keyboard(unsigned char key, int x, int y)
{
    switch (key) {
        case 'x':
            glutTimerFunc(35, timer_ship, 0);
            break;
        case 'z':
            glutTimerFunc(35, timer_cannonball, 0);
            break;
    }
    glutPostRedisplay();
}


// ------------- Display -------------
void display()
{
    float l_pos[4] = {0, 120, 300, 1};
    float l_dir[3] = {0, -6, -10};

    float lgt_pos1[4] = {7, 15, 5, 1};
    float lgt_dir1[3] = {- 0.2, - 1, 1};
    float wall_dimensions_f[3] = {150, 25, 8}; // Wall Length, Height, Wall Width
    float wall_dimensions_s[3] = {400, 25, 8}; // Wall Length, Height, Wall Width
    float pillar_dimensions[2] = {wall_dimensions_f[2] + 5,
                                  wall_dimensions_f[1] + 10}; // Pillar Radius, Pillar Height
    float gate_width = 15;
    float archway[5] = {gate_width * 2, wall_dimensions_f[2], wall_dimensions_f[1], 1.1,
                        15}; // Archway Width, Archway Depth, Archway Height, Archway Offset, Archway Slices
    float crate_dimensions[3] = {20, 80, 70}; // Crate Size, Crate X-Pos, Crate Y-Pos
    float shadowMat[16] = {l_pos[1], 0, 0, 0, - l_pos[0], 0, - l_pos[2], - 1, 0, 0, l_pos[1], 0, 0, 0, 0, l_pos[1]};
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    // Change view from FP to TP (TP of spaceship)
    if (is_flying) {
        gluLookAt(0, 130 + Ob.ship_height, - 130,
                  0, - 200 + Ob.ship_height, 0,
                  0, 1, 0);
    } else {
        gluLookAt(Pl.x, Pl.height, Pl.z,
                  Pl.x + Pl.lx, Pl.height, Pl.z + Pl.lz,
                  0, 1, 0);
    }
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, l_dir);
    glLightfv(GL_LIGHT0, GL_POSITION, l_pos);
    // Creating objects
    skybox();
    glPushMatrix();
    glTranslatef(0, - 0.1, 0);
    floor();
    glPopMatrix();
    create_archway(archway[0], archway[1], archway[2], archway[3], archway[4]);
    // Symmetrical Function
    for (int flag = - 1; flag <= 1; flag += 2) {
        // Front Walls
        glPushMatrix();
        glTranslatef(flag * (gate_width + (wall_dimensions_f[0] / 2)), 0, 0);
        create_wall(wall_dimensions_f);
        glPopMatrix();
        // Side Walls
        glPushMatrix();
        glRotatef(90, 0, 1, 0);
        glTranslatef(wall_dimensions_s[0] / 2, 0,
                     flag * (wall_dimensions_f[0] + (gate_width * 0.75) + (wall_dimensions_f[2] / 2)));
        create_wall(wall_dimensions_s);
        glPopMatrix();
        // Front Pillars
        glPushMatrix();
        glTranslatef(flag * (gate_width + wall_dimensions_f[0]), 0, 0);
        create_pillar(pillar_dimensions);
        glPopMatrix();
        // Robots
        glPushMatrix();
        glTranslatef(flag * ((gate_width + 10) + Ob.robot_pos), 0, 60);
        glRotatef(flag * Ob.robot_angle, 0, 1, 0);
        if (flag == - 1) {
            glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, lgt_dir1);
            glLightfv(GL_LIGHT1, GL_POSITION, lgt_pos1);
        } else {
            glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, lgt_dir1);
            glLightfv(GL_LIGHT2, GL_POSITION, lgt_pos1);
        }
        glScalef(0.25, 0.25, 0.25);
        create_robot();
        glPopMatrix();
        // Cannons
        glPushMatrix();
        glTranslatef(flag * (gate_width + 10), wall_dimensions_f[1], 0);
        glScalef(0.3, 0.3, 0.3);
        create_cannon();
        glPopMatrix();
        glPushMatrix();
        glTranslatef(flag * (wall_dimensions_f[0] - gate_width + 10), wall_dimensions_f[1], 0);
        glScalef(0.3, 0.3, 0.3);
        create_cannon();
        glPopMatrix();
        // Crate Stacks
        glPushMatrix();
        glTranslatef(flag * crate_dimensions[1], crate_dimensions[0] / 2, - crate_dimensions[2]);
        if (flag == 1) glRotatef(270, 0, 1, 0);
        create_crate(crate_dimensions[0]);
        glPopMatrix();
        // ** Shadows ** //
        glDisable(GL_LIGHTING);
        // Front Walls
        glPushMatrix();
        glMultMatrixf(shadowMat);
        glTranslatef(flag * (gate_width + (wall_dimensions_f[0] / 2)), 0, 0);
        create_wall_shadow(wall_dimensions_f);
        glPopMatrix();
        // Side Walls
        glPushMatrix();
        glMultMatrixf(shadowMat);
        glRotatef(90, 0, 1, 0);
        glTranslatef(wall_dimensions_s[0] / 2, 0,
                     flag * (wall_dimensions_f[0] + (gate_width * 0.75) + (wall_dimensions_f[2] / 2)));
        create_wall_shadow(wall_dimensions_s);
        glPopMatrix();
        // Robots
        glPushMatrix();
        glMultMatrixf(shadowMat);
        glTranslatef(flag * ((gate_width + 10) + Ob.robot_pos), 0, 60);
        glRotatef(flag * Ob.robot_angle, 0, 1, 0);
        glScalef(0.25, 0.25, 0.25);
        create_robot_shadow();
        glPopMatrix();
        // Crate Stacks
        glPushMatrix();
        glMultMatrixf(shadowMat);
        glTranslatef(flag * crate_dimensions[1], crate_dimensions[0] / 2, - crate_dimensions[2]);
        if (flag == 1) glRotatef(270, 0, 1, 0);
        create_crate_shadow(crate_dimensions[0]);
        glPopMatrix();
        glEnable(GL_LIGHTING);
    }
    // Spaceship
    glPushMatrix();
    glTranslatef(0, Ob.ship_height, - 100);
    glRotatef(Ob.ship_angle, 0, 1, 0);
    create_spaceship();
    glPopMatrix();
    // ** Shadows **//
    // Spaceship
    glDisable(GL_LIGHTING);
    glPushMatrix();
    glMultMatrixf(shadowMat);
    glTranslatef(0, Ob.ship_height, - 100);
    glRotatef(Ob.ship_angle, 0, 1, 0);
    create_spaceship_shadow();
    glPopMatrix();
    glPushMatrix();
    glMultMatrixf(shadowMat);
    create_archway_shadow(archway[0], archway[1], archway[2], archway[3], archway[4]);
    glPopMatrix();
    glEnable(GL_LIGHTING);
    glutSwapBuffers();
}


// ------------- Initialization -------------
void initialize()
{
    float grey[4] = {0.2, 0.2, 0.2, 1};
    float white[4] = {1, 1, 1, 1};
    load_mesh_file(CANNON);
    load_TGA_textures(IMAGE_LIST, skybox_texture, 6);
    load_TGA_textures(TEXTURE_LIST, object_textures, 4);
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
    glEnable(GL_COLOR_MATERIAL);
    glMaterialfv(GL_FRONT, GL_SPECULAR, white);
    glMaterialf(GL_FRONT, GL_SHININESS, 20);
    glEnable(GL_LIGHTING);
    // Lights
    for (int light : {GL_LIGHT0, GL_LIGHT1, GL_LIGHT2}) {
        glLightfv(light, GL_AMBIENT, grey);
        glLightfv(light, GL_DIFFUSE, white);
        glLightfv(light, GL_SPECULAR, white);
        if (light == GL_LIGHT0) {
            glLightf(light, GL_SPOT_CUTOFF, 50);
            glLightf(light, GL_SPOT_EXPONENT, 20);

        }
        else {
            glLightf(light, GL_SPOT_CUTOFF, 50);
            glLightf(light, GL_SPOT_EXPONENT, 30);

        }
        glEnable(light);
    }
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_NORMALIZE);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(70, 1, 1, 2000);
    glutTimerFunc(35, timer_robot, 0);
}


// ------------- Main -------------
int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH); // Double buffering
    glutInitWindowSize(800, 800);
    glutInitWindowPosition(10, 10);
    glutCreateWindow("Main");
    initialize();
    glutDisplayFunc(display);
    glutSpecialFunc(special);
    glutKeyboardFunc(keyboard);
    glutMainLoop();
    return 0;
}


// Disclaimer
/*
 * Textures provided by following links on an open source license:
 * http://www.humus.name/index.php?page=Textures
 * http://www.humus.name/Textures/Yokohama3.zip
 * https://opengameart.org/content/3-crate-textures-w-bump-normal
 *
 */