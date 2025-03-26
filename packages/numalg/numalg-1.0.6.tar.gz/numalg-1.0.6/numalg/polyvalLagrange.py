#!/usr/bin/env python3

'''Given n+1 points (xi, yi), evaluates the interpolator polynomial, at a single point or at a set of points.'''

import numpy as np

def polyvalLagrange(x, y, u) :
    '''
    polyvalLagrange evaluates the interpolator polynomial, 
    based on the points (x_i, y_i), at each point in u. 

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ].
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ]. 
    u (list): vector with points at which you want to calculate the value of the polynomial.

    Returns:
    v (np.ndarray): polynomial values at u.
    '''
    n = len(x)
    m = len(u)
    x = np.array(x)
    y = np.array(y)
    v = [0] * m
    for k in range(n) :
       w = np.array([1]*m)
       for j in range(n) :
          if x[k] != x[j]:
             w = (u-x[j])/(x[k]-x[j])*w
       v += w*y[k]
    return v

# Example
def teste():
    '''x = [0.8, 1.0, 1.6], y = [1.8900, 2.000, 3.185], evaluaed in [1.3, 1.5]'''
    print("polyvalLagrange([0.8, 1.0, 1.6],[1.8900, 2.000, 3.185],[1.3, 1.5])")
    print(polyvalLagrange([0.8, 1.0, 1.6],[1.8900, 2.000, 3.185],[1.3, 1.5]))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
