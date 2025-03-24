#!/usr/bin/env python3

''' Gauss–Seidel method for solving a system of linear equations '''

import numpy as np

def gaussSeidel(a, b, norma, x = [], eps = 1e-6, itermax = 1000) :
    '''
    gaussSeidel solves a system a * x = b of linear equations using the SOR iterative method

    Parameters:
    a (list): coefficient matrix
    b (list): vector of constants
    x (list): initial aproximation for the vector of unknowns
    norma (float): norm used for the stopping criterion ||x^(k+1) - x^(k)|| < eps
    eps (float): maximum value allowed for distance between successive iterations (tolerance)
    itermax (int): maximum number of iterations 

    Returns:
    x (numpy.ndarray): solution for the vector of unknowns
    r (numpy.ndarray): matrix with all iterations
    dif (list): all norm of the difference between successive iterations
    rho (float): spectral radiusof the iteration matrix c = - inv(m) * n where
                 m = L + D
                 n = U
    '''
    if len(x) == 0 :
        x = [0] * len(b)
    dim, dif, r = len(b), [], x
    m = np.tril(a)
    n = np.triu(a, 1)
    minv = np.linalg.inv(m)
    c = -np.matmul(minv, n)
    m1b = minv.dot(b)
    for k in range(itermax):
        x = c.dot(x) + m1b
        r = np.vstack([r, x])
        dif += [ np.linalg.norm( r[k+1] - r[k], norma ) ]
        if dif[k] < eps:
            return x, r, dif
    print('Maximum number of iterations exceeded (itermax)') 
    return x, r, dif

# Example
def teste():
    '''a * x = b with a = [[10, 2, 6], [1, 10, 8], [2, -7, -10]] and b = [34, 28, -23]^T'''
    a = [[10, 2, 6], [1, 10, 8], [2, -7, -10]]
    b = [34, 28, -23]
    x0 = [1] * len(b)
    x, r, dif = gaussSeidel(a, b, np.inf, x0)
    print(x, r, dif)

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
