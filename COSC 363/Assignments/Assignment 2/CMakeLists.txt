cmake_minimum_required(VERSION 2.8)

project(ass2)

add_executable(main.out main.cpp Functions/Ray.cpp Functions/SceneObject.cpp Models/Sphere.cpp Models/Plane.cpp Models/Cylinder.cpp Models/Cone.cpp Models/Cone.h Models/Cube.cpp Models/Cube.h Functions/TextureBMP.cpp Functions/TextureBMP.h Models/Triangle.cpp Models/Triangle.h Models/Torus.cpp Models/Torus.h Functions/QuarticSolver.cpp Functions/QuarticSolver.h Models/Tetrahedron.cpp Models/Tetrahedron.h)

find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)
include_directories(${OPENGL_INCLUDE_DIRS} ${GLUT_INCLUDE_DIRS})

target_link_libraries(main.out ${OPENGL_LIBRARIES} ${GLUT_LIBRARY})

