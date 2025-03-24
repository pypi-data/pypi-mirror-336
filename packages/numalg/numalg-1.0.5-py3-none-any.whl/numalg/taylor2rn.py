#!/usr/bin/env python3

'''Taylor of order two method for solving a system of ordinary differential equations (ODEs) with a given vector of initial conditions.'''


def taylor2rn(f, dft, dfy, y0, t0, tn, n = 10):
    '''
    eulerrn finds solutions of initial value problems
    y '= F(t, y), y(t0) = y0
    where y belongs to R^k and the function f : R x R^k -> R^k  
    using Taylor of order two method
    
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
        fti = np.array(f(t[i], y[i, :]))
        dt = np.array(dft(t[i], y[i, :]))
        dy = np.array(dfy(t[i], y[i, :]))
        y[i+1, :] = y[i, :] + (h * fti + h**2 / 2 * (dt + dy @ fti)).T
    yn = y[-1, :] # Approximated solution at tn 
    
    return yn, y, t, h

# Examples
def teste():
    '''[y0'; y1'] = [1+y0^2*y1-2*y0; y0-y0^2*y1], with [y0(0); y1(0)] = [1; 2], t in [0, 1]'''
    print("[y0'; y1'] = [1+y0**2*y1-2*y0; y0-y0**2*y1], with [y0(0); y1(0)] = [1; 2], t in [0, 1]")
    f = lambda t, y: [[1+y[0]**2*y[1]-2*y[0]], [y[0]-y[0]**2*y[1]]]
    dft = lambda t, y: [[0], [0]]
    dfy = lambda t, y: [[2*y[0]*y[1]-2, y[0]**2], [1-2*y[0]*y[1], -y[0]**2]]
    y0 = [1, 2]; t0 = 0; tn = 1; n = 5;
    yn, y, t, h = taylor2rn(f, dft, dfy, y0, t0, tn, n)
    print(yn, y, t, h)

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
