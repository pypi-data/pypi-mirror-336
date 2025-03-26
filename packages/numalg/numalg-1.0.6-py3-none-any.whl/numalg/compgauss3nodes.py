#!/usr/bin/env python3
'''Composite Gauss-Legendre with 3 nodes'''

import numpy as np

def compgauss3nodes(f, alpha, beta, n) :
    '''
    compgauss3nodes finds the integral of the function f over the interval [a, b] 
    using the composite gauss-legendre rule with three nodes 

    Parameters:
    f (function): integrand function 
    a, b (int or float): lower and upper bounda of the interval [a, b]
    n (int): number of sub-intervals
    transformation used: to map the interval x in [x_i, x_{i+1}] to the standard interval t in [-1, 1]
    x_i + (x_{i+1} - x_i) / 2 * (t + 1) in [x_i, x_{i+1}]
    x_i + (x_{i+1} - x_i) / 2 * (1 - sqrt(3/5)) in [x_i, x_{i+1}]
    x_i + (x_{i+1} - x_i) / 2 * (1 + 0) in [x_i, x_{i+1}]
    x_i + (x_{i+1} - x_i) / 2 * (1 + sqrt(3/5)) in [x_i, x_{i+1}]

    Return:
    s (float): value of the integral
    '''
    h, dif = (beta - alpha) / n, []
    x = np.linspace(alpha, beta, n + 1)
    w = np.array([5/9, 8/9, 5/9])
    t = np.array([-np.sqrt(3/5), 0, np.sqrt(3/5)])

    s = 0
    for i in range(n):
        s += np.sum(w * np.vectorize(f)(x[i] + h * (t + 1) / 2))
    s *= h / 2
    
    return s

# Examples
def teste():
    '''Integral of the function f(x) = exp(sin(x)) over [2, 3]'''
    from math import exp, sin
    print(compgauss3nodes(lambda x: exp(sin(x)), 2, 3, 4))

if __name__ == "__main__":
  teste()

# vim: set fileencoding=utf-8 :

