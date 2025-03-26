#!/usr/bin/env python3
'''Given n+1 points (xi, yi) calculates  the divided differences y_0, y_{10}, y_{210}, ..., y_{n...210}
   of the Newton interpolator polynomial
   p_n(x) = y_0 + y_{10} * (x - x_0) + y_{210} * (x - x_0) * (x - x_1) + ... + y_{n...210} * (x - x_0) ... (x - x_{n-1})
    Also calculates the polynomial in the usual base.
'''

import numpy as np

def polynewton(x, y):
    '''
    polynewton calculates the divided differences y_0, y_{10}, y_{210}, ..., y_{n...210}
    of the Newton interpolator polynomial based on the points (x_0,y_0), ..., (x_n,y_n):
    p_n(x) = y_0 + y_{10} * (x - x_0) + y_{210} * (x - x_0) * (x - x_1) + ... + y_{n...210} * (x - x_0) ... (x - x_{n-1})
    Also calculates the polynomial in the usual base.

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ]
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ] 

    Returns:
    d (list): vector with the divided differences [ y_0, y_{10}, y_{210}, ..., y_{n...210} ]
    p (list): vector with the coefficients of the polynomial in the usual base

    Example:
    x = [0.5, 2, 3.5]; y = [3.82, 3.01, 2.14]; 
    d, p = polinomioNewton(x, y)
    print(d, p)
    returns
    [3.8200, -0.5400, -0.0133]
    [-0.0133, -0.5067, 4.0767]
    and the polynomial is given by
    p(x) = 3.8200 - 0.54 (x - 0.5) - 0.0133 (x - 0.5) (x-2)
    p(x) = -0.0133 x^2 - 0.5067 x + 4.0767
    '''
    y = y.copy()
    d = [y[0]]
    for i in range(1, len(x)) :
       for j in range(len(x)-i) :
          y[j] = (y[j+1] - y[j]) / (x[j+i] - x[j])
       d += [y[0]]
   
    n = len(x) - 1  # polynomial degree
    p = [d[n]]  # start with the last value of d
    for k in range(n-1, -1, -1):  # iterate backwards from n to 1
        # Construct the polynomial: p(x) * (x - x(k-1)) + d(k-1)
        q = (1, -x[k])
        p = np.polynomial.polynomial.polymul(p, q) + np.array([0]*len(p)+[d[k]])
    return d, p.tolist()

def teste():
    '''x = [0.5, 2, 3.5]; y = [3.82, 3.01, 2.14]'''
    x = [0.5, 2, 3.5]; y = [3.82, 3.01, 2.14]
    print(polynewton(x, y))

if __name__ == "__main__":
   teste()

# vim: set fileencoding=utf-8 :
