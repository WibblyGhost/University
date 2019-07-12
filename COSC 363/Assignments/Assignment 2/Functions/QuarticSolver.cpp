/*
 * QuarticSolver.cpp
 * Created by Zachary Sanson on 25/05/2019.
 */


// ------------- Includes -------------
#include "QuarticSolver.h"


// ------------- Returns the roots of a complex square root -------------
static std::complex<double> complexSqrt(const std::complex<double> &z) {
    return pow(z, 1. / 2.);
}


// ------------- Returns the roots of a complex cube root -------------
static std::complex<double> complexCbrt(const std::complex<double> &z) {
    return pow(z, 1. / 3.);
}


// ------------- Returns the roots of a complex equation in the form ax^4 + bx^3 + cx^2 + dx + e -------------
void solveQuartic(std::complex<double> *coefficients, std::complex<double> *roots) {
    const std::complex<double> a = coefficients[4];
    const std::complex<double> b = coefficients[3] / a;
    const std::complex<double> c = coefficients[2] / a;
    const std::complex<double> d = coefficients[1] / a;
    const std::complex<double> e = coefficients[0] / a;
    const std::complex<double> Q1 = c * c - 3. * b * d + 12. * e;
    const std::complex<double> Q2 = 2. * c * c * c - 9. * b * c * d + 27. * d * d + 27. * b * b * e - 72. * c * e;
    const std::complex<double> Q3 = 8. * b * c - 16. * d - 2. * b * b * b;
    const std::complex<double> Q4 = 3. * b * b - 8. * c;
    const std::complex<double> Q5 = complexCbrt(Q2 / 2. + complexSqrt(Q2 * Q2 / 4. - Q1 * Q1 * Q1));
    const std::complex<double> Q6 = (Q1 / Q5 + Q5) / 3.;
    const std::complex<double> Q7 = 2. * complexSqrt(Q4 / 12. + Q6);
    roots[0] = (- b - Q7 - complexSqrt(4. * Q4 / 6. - 4. * Q6 - Q3 / Q7)) / 4.;
    roots[1] = (- b - Q7 + complexSqrt(4. * Q4 / 6. - 4. * Q6 - Q3 / Q7)) / 4.;
    roots[2] = (- b + Q7 - complexSqrt(4. * Q4 / 6. - 4. * Q6 + Q3 / Q7)) / 4.;
    roots[3] = (- b + Q7 + complexSqrt(4. * Q4 / 6. - 4. * Q6 + Q3 / Q7)) / 4.;
}
