#!/usr/bin/env python3

'''Euler method for solving ordinary differential equations (ODEs) with a given initial value.'''

def euler(f, y0, t0, tn, n = 10) :
    '''
    eulerrn finds solutions of initial value problems
    y '= f(t, y), y(t0) = y0
    where y belongs to R and the function f : R x R -> R  
    using Euler method
    
    Parameters:
    f (function): function representing the ODE, and can be specified using a lambda function.
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
       print('t0 must be less than tn')
    h, y, t = (tn - t0) / (1. * n), [y0], [t0]
    for i in range(n) :
        fty = f(t[i],y[i])
        y += [y[i] + h * fty]
        t += [t[i] + h]
    return (y[n], h, t, y)

# Example
def teste():
    ''' y' = 2 * exp(-y), y(0) = 2'''
    from math import exp
    print("euler(lambda t, y: 2*exp(-y), 2, 0, 1, 5)")
    fun = lambda t, y: 2*exp(-y)
    print(euler(fun, 2, 0, 1, 5))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
