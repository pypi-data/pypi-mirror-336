#!/usr/bin/env python3

'''Composite Midpoint method'''

import numpy as np

def midpoint(f, a, b, n):
    '''
    midpoint finds the integral of the function f over the interval [a, b] 
    using the composite mid point method.
    
    Parameters:
    f (function): integrand function. 
    a, b (int or float): lower and upper bounda of the interval [a, b].
    n (int): number of sub-intervals.
    Transformation used: x_i + (x_{i+1} - x_i) / 2 mid point of the interval [x_i, x_{i+1}].
    
    Return:
    s (float): value of the integral
    '''
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    s = 0
    for i in range(n):
        s += f((x[i] + x[i+1]) / 2)
    s *= h
    return s

# Examples
def exerc1():
    '''integrate f(x) = 4/(1+x^2) over the range [0, 1] with 10 intervals'''
    print('integrate f(x) = 4/(1+x^2) over the range [0, 1] with 10 intervals')
    f = lambda x: 4 / (1 + x**2) 
    s = midpoint(f, 0, 1, 10)
    print(s)

def exerc2():
    '''integrate f(x) = exp(sin(x)) over the range [2, 3] with 4 intervals'''
    print('integrate f(x) = exp(sin(x)) over the range [2, 3] with 4 intervals')
    f = lambda x: np.exp(np.sin(x)) 
    s = midpoint(f, 2., 3., 4)
    print(s)

def teste():
    ''' All examples '''
    exerc1()
    exerc2()

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
