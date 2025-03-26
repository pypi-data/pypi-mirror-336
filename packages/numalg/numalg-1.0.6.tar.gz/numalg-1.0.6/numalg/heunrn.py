#!/usr/bin/env python3

'''Heun method for solving a system of ordinary differential equations (ODEs) with a given vector of initial conditions.'''

def heunrn(f, y0, t0, tn, n = 10):
    '''
    heunrn finds solutions of initial value problems
    y '= F(t, y), y(t0) = y0
    where y belongs to R^k and the function f : R x R^k -> R^k  
    using Euler method
    
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
    y0 = np.array(y0).flatten() # Ensure y0 is a row vector
    y = np.zeros((n + 1, len(y0)))  
    y[0, :] = y0 
    t = np.linspace(t0, tn, n + 1) 
    h = (tn - t0) / n 
    
    for i in range(n):
        k1 = f(t[i], y[i, :]) 
        k2 = f(t[i] + h, y[i, :] + h * k1)  
        y[i+1, :] = y[i, :] + (k1 + k2) * h / 2 
    yn = y[-1, :]  
    return yn, y, t, h

# Example
def teste():
    '''[y0'; y1'] = [y1; exp(t) - 2y1 - y0] with [y0(0); y1(0)] = [1; -1]'''
    import numpy as np
    print('teste')
    f = lambda t, y: np.array([y[1], np.exp(t) - 2 * y[1] - y[0]])
    y0 = [1, -1]; t0 = 0; tn = 0.2; n = 2;
    yn, t, y, h = heunrn(f, y0, t0, tn, n)
    print(yn, t, y, h)

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
