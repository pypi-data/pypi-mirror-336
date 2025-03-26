#!/usr/bin/env python3

'''Given n+1 points (xi, yi) calculates the coefficients of the interpolating polynomial in the usual base 
and the Lagrange basis for interpolating polynomial written with the usual basis'''

import numpy as np

def lagrangepol(x, y):
    '''
    lagrangepol calculates usual basis polynomial coefficients, and
    Lagrange basis polynomials coefficients (written in the usual basis).

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ]
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ] 

    Returns:
    pol (numpy.poly1d): usual basis polynomial coefficients of degree leq n
    l (list): Lagrange basis polynomials of degree n (written in the usual basis).

    Example:
    x = [-0.8, 0, 1.5]; y = [-1.02, 0, 14.10];
    pol, l = lagrangepol(x, y)
    returns
    pol = [3.5326087, 4.10108696, 0.]
    l1 = [0.54347826, -0.81521739, -0.]
    l2 = [-0.83333333, 0.58333333, 1.]
    l3 = [0.28985507, 0.23188406, 0.]
    consequently
    p(x) = 3.5326 x^2 + 4.1011 x
    l_0(x) =  0.5435 x^2 - 0.8152 x
    l_1(x) = -0.8333 x^2 + 0.5833 x + 1
    l_2(x) =  0.2899 x^2 + 0.2319 x
    '''
    n = len(x) - 1 
    pol = 0
    l = []
    for m in range(n + 1): 
       p = np.poly1d([1]) 
       for k in range(n + 1):
          if k != m:
              p = np.poly1d(p) * np.poly1d([1, -x[k]]) / (x[m] - x[k])
       l.append(p)
       pol += y[m] * p
    l = np.array([x.coeffs for x in l])
    return pol.coeffs, [l[x].tolist() for x in range(len(l))]

# Example
def teste():
    '''x = [-0.8, 0, 1.5]; y = [-1.02, 0, 14.10]'''
    x = [-0.8, 0, 1.5]; y = [-1.02, 0, 14.10];
    pol, l = lagrangepol(x, y)
    print("lagrangepol([-0.8, 0, 1.5], [-1.02, 0, 14.10])") 
    print('p(x) = ', pol) 
    print('l0(x), ..., ln(x)=', l) 

if __name__ == "__main__":
    teste()   

# vim: set fileencoding=utf-8 :
