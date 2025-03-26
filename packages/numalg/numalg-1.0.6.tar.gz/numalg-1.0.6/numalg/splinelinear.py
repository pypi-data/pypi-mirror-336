#!/usr/bin/env python3

''' 1D linear spline function based on points (xi, yi)'''

def splinelinear(x, y, z = None):
    '''
    splinelinear(x,y,xi) returns a vector with the interpolated values of a 1D linear spline function 
    at the points of the vector xi, using linear interpolation, and the coefficients of the spline function. 
   
    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ]
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ] 
    z (list): vector with points at which you want to calculate the value of the polynomial.

    Returns:
    s (list): polynomial values at z.
    coefs (list): coefficients of the spline function.

    Example:
    s, coefs = splinelinear([0, 1, 2, 4], [1, 3, 4, 2])
    returns the coefficients of the linear spline written with the Newton basis polynomials
    [[1, 2.0], [3, 1.0], [4, -1.0]]
    which means,
    s0(x) = 1 + 2(x - 0), x in [0 1]
    s1(x) = 3 + 1(x - 1), x in [1 2]
    s2(x) = 4 - 1(x - 2), x in [2 4]
    '''
    s = []
    if z:
       for i in range(len(z)):
          for j in range(len(x) - 1):
             if z[i] <= x[j+1] and z[i] >= x[j]:
                s += [ y[j] + (y[j+1] - y[j]) / (x[j+1] - x[j]) * (z[i] - x[j]) ]
                break
    coefs = []
    for j in range(len(x) - 1):
       coefs += [[y[j], (y[j+1] - y[j]) / (x[j+1] - x[j])]]
    return s, coefs

# Example
def teste():
    '''x = 0, pi/4, pi/2, ..., 2pi, f(x) = sin(x)'''
    from math import pi, sin
    x = [i*pi/4 for i in range(9)]
    y = [sin(i) for i in x]
    s, coefs = splinelinear(x, y, [1.2, 2.5])
    print(s)
    s, coefs = splinelinear([0, 1, 2, 4], [1, 3, 4, 2])
    print(coefs)

if __name__ == "__main__":
    teste()    

# vim: set fileencoding=utf-8 :
