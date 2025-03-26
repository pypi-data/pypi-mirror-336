#!/usr/bin/env python3
'''Solves Boundary Value Problems (BVP) using finite difference method
   y" - w * y' - v * y = u, y(t0) = y0, y(tf) = yf, uniform mesh with (n+1) points.'''

import numpy as np

def bvp(w, v, u, t0, tf, y0, yf, n):
    '''
    Solves Boundary Value Problems (BVP).
    bvp(w,v,u,t0,tf,y0,yf,n) integrates a differential equation of the form 
    y" - w * y' - v * y = u
    subject to the boundary conditions 
    y(t0) = y0, y(tf) = yf
    with a uniform mesh with (n+1) points.

    Parameters:
    w, v, u (function): are functions of t or constant functions.
    t0, tf (float): the start and end points of the interval.
    y0, yf (float): the boundary conditions at the start and end points.
    n (int): number of sub-intervals.
    
    Returns:
    t (list): mesh points.
    y (list): approximated solution values at mesh points.
    '''
    h = (tf - t0) / n  
    h2 = 2 * h * h  
    t = (np.linspace(t0, tf, n+1)).reshape(-1, 1)

    w = np.array([w(i) for i in t[1:n]]).reshape(-1,1)
    v = np.array([v(i) for i in t[1:n]]).reshape(-1,1)
    u = np.array([u(i) for i in t[1:n]]).reshape(-1,1)

    A = np.zeros((n - 1, n - 1))
    b = -h2 * u
    hw = h * w[0]
    A[0, 0] = 4 + h2 * v[0]
    A[0, 1] = hw - 2
    b[0] += (2 + hw) * y0

    for m in range(1, n - 2):
        hw = h * w[m]
        A[m, m-1]  = -2 - hw
        A[m, m] = 4 + h2 * v[m]
        A[m, m+1] = hw - 2

    hw = h * w[n - 2]
    A[n-2, n-3] = -2 - hw
    A[n - 2, n-2] = 4 + h2 * v[n - 2]
    b[n - 2] -= (hw - 2) * yf
    y = [y0] + [r[0] for r in np.linalg.solve(A, b).tolist()] + [yf]

    return [r[0] for r in t.tolist()], y

def exerc1():
    '''Example: y'' + 2y' - 2y = 0, y(0) = 1 y(1) = 2'''
    print('exerc1')
    t0 = 0; y0 = 1; tf = 1; yf = 2; n = 3;
    w = lambda x: -2; v = lambda x: 2; u = lambda x: 0; 
    t,y = bvp(w,v,u,t0,tf,y0,yf,n)
    print(t, y)

def exerc2():
    '''Example: y'' + y = t, y(0) = 0  y(pi) = 0'''
    print('exerc2')
    t0 = 0; y0 = 0; tf = np.pi; yf = 0; n = 3;
    w = lambda x: 0; v = lambda x: -1; u = lambda t: t; 
    t, y = bvp(w, v, u, t0, tf, y0, yf, n)
    print(t, y)

def exerc3():
    '''Example: y'' - y' - 2y = cos(t), y(0) = -0.3  y(0.5pi) = -0.1'''
    print('exerc3')
    t0 = 0; y0 = -0.3; tf = 0.5*np.pi; yf = -0.1; n = 5;
    w = lambda x: 1; v = lambda x: 2; u = lambda t: np.cos(t); 
    t, y = bvp(w, v, u, t0, tf, y0, yf, n)
    print(t, y)

def exerc4():
    '''Example: y'' + 2y' = -10t, y(0) = 1 y(1) = 1'''
    print('exerc4')
    t0 = 0; y0 = 1; tf = 1; yf = 1; n = 3;
    w = lambda x: -2; v = lambda x: 0; u = lambda t: -10*t; 
    t, y = bvp(w, v, u, t0, tf, y0, yf, n)
    print(t, y)

def exerc5():
    '''Example: y'' + 2y' + y = -10t, y(0) = 1 y(1) = 2'''
    print('exerc5')
    t0 = 0; y0 = 1; tf = 1; yf = 2; n = 4;
    w = lambda x: -2; v = lambda x: -1; u = lambda t: -10*t; 
    t, y = bvp(w, v, u, t0, tf, y0, yf, n)
    print(t, y)

def exerc6():
    '''Example: y'' - sin(t) y' - cos(t) y = -10t, y(0) = 2 y(1) = 3'''
    print('exerc6')
    t0, y0, tf, yf, n, w, v, u = 0, 2, 1, 3, 4, lambda t: np.sin(t), lambda t: np.cos(t), lambda t: -10*t
    t, y = bvp(w, v, u, t0, tf, y0, yf, n)
    print(t, y)

def teste():
    ''' All examples'''
    exerc1()
    exerc2()
    exerc3()
    exerc4()
    exerc5()
    exerc6()

if __name__ == "__main__":
   teste()

# vim: set fileencoding=utf-8 :
