#!/usr/bin/env python3

'''Taylor of order two method for solving ordinary differential equations (ODEs) with a given initial value.'''

import math
def taylor2(f, dft, dfy, y0, t0, tn, n) :
    '''
    taylo2 finds solutions of initial value problems
    y '= f(t, y), y(t0) = y0
    where y belongs to R and the function f : R x R -> R  
    using Taylor method of order two
    
    Parameters:
    f (function): function representing the ODE, and can be specified using a lambda function.
    dft (function): partial derivative in order to t.
    dfy (function): partial derivative in order to y.
    y0 (float): Initial condition for y.
    t0 (float): Initial time.
    tn (float): Final time.
    n (int, optional): Number of time steps (default is 10).
    
    Returns:
    y[n] (ndarray): The last value of the solution.
    h (float): The time step size.
    t (ndarray): The time vector, successive points in the independent variable or grid points.
    y (ndarray): The array of values of the solution at each time step.
    '''
    if t0 > tn :
       print('t0 tem de ser menor que tn');
    h, y, t = (tn - t0) / (1. * n), [y0], [t0]
    for i in range(n) :
       funcao = f(t[i], y[i])
       dt = dft(t[i], y[i])
       dy = dfy(t[i], y[i])
       y += [y[i] + h * funcao + math.pow(h, 2.)/2. * (dt + funcao * dy)]
       t += [t[i] + h]
    return (y[n], h, t, y)

# Examples
def teste():
    '''y'(t) = t^2 cos(y(t)/t^2), y(2) = 1'''
    f = lambda t,y: math.pow(t,2)*math.cos(y/math.pow(t,2))
    dft = lambda t,y: 2*t*math.cos(y/math.pow(t,2)) + 2*y*math.sin(y/math.pow(t,2))/t
    dfy = lambda t,y: - math.sin(y/math.pow(t,2))
    print(taylor2(f, dft, dfy, 1, 2, 3, 4))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
