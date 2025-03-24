#!/usr/bin/env python3

''' Fourth Order Runge-Kutta for solving ordinary differential equations (ODEs) with a given initial value.'''

def rungekutta4(f, y0, t0, tn, n = 10) :
    '''
    rungrkutta4 finds solutions of initial value problems
    y '= f(t, y), y(t0) = y0
    where y belongs to R and the function f : R x R -> R  

    Parameters:
    f (function): The function representing the ODE, and can be specified using a lambda function.
    y0 (float): Initial condition for y.
    t0 (float): Initial time.
    tn (float): Final time.
    n (int, optional): Number of time steps (default is 10).
    
    Returns:
    yn (ndarray): The last value of the solution.
    y (ndarray): The array of values of the solution at each time step.
    t (ndarray): The time vector.
    h (float): The time step size.
    '''
    import numpy as np
    h = (tn - t0) / n  
    y = np.zeros(n+1)  
    t = np.linspace(t0, tn, n+1)  
    y[0] = y0  
    
    for i in range(len(t)-1):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + 0.5 * h, y[i] + 0.5 * h * k1)
        k3 = f(t[i] + 0.5 * h, y[i] + 0.5 * h * k2)
        k4 = f(t[i] + h, y[i] + k3 * h)
        y[i+1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) * h / 6
    yn = y[-1]  
    return yn, y, t, h

# Example
def teste():
   ''' y' = 2 * exp(-y), y(0) = 2'''
   from math import exp
   print("rungekutta4(lambda t, y: 2*exp(-y), 2, 0, 1, 5)")
   fun = lambda t, y: 2 * exp(-y)
   print(rungekutta4(fun, 2, 0, 1, 5))

if __name__ == "__main__":
   teste()

# vim: set fileencoding=utf-8 :
