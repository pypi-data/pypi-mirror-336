#!/usr/bin/env python3

'''Euler method for solving ordinary differential equations (ODEs) with a given initial value.'''

from math import exp
import numpy as np

def midpointedo(f, y0, t0, tn, n=10) :
    '''
    midpointedo finds solutions of initial value problems
    y '= f(t, y), y(t0) = y0
    where y belongs to R and the function f : R x R -> R  
    using Euler method
    
    Parameters:
    f (function): The function representing the ODE, and can be specified using a lambda function.
    y0 (float): Initial condition for y.
    t0 (float): Initial time.
    tn (float): Final time.
    n (int, optional): Number of time steps (default is 10).
    
    Returns:
    y[n] (ndarray): The last value of the solution.
    y (ndarray): The array of values of the solution at each time step.
    t (ndarray): The time vector.
    h (float): The time step size.
    '''
    if t0 > tn :
       print('t0 must be less than tn')
       return()
    h, y = (tn - t0) / (1. * n), [y0]
    t = np.linspace(t0, tn, n+1)
    for i in range(n) :
       k0 = f(t[i], y[i])
       y += [y[i] + h * f(t[i] + h/2, y[i] + h * k0/2)]
    return (y[n], y, t, h)

# Example
def teste():
    ''' y' = 2 * exp(-y), y(0) = 2'''
    print("midpointedo(lambda t, y: 2*exp(-y), 2, 0, 1, 5)")
    fun = lambda t, y: 2*exp(-y)
    print(midpointedo(fun, 2, 0, 1, 5))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
