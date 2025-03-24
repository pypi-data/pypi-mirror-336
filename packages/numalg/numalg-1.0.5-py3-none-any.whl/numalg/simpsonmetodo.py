#!/usr/bin/env python3

'''Composite Simpson's method using h such that | S_h-S_{h/2} | is sufficiently small (it begins with two sub-intervals).
   Can be used when it is possible to calculate the function at all points of the integration interval.'''


from numalg.simpson import simpson
import numpy as np

def simpsonmetodo(f, alpha, beta, epsilon=1e-3, iter_max=10) :
    '''
    simpsonmetodo finds the integral of the function f over the interval [alpha, beta] 
    using the Simpson rule.
    The function starts by calculating the integral with steps h0 = (beta - alpha) / 2 and h0 / 2,  and 
    then doubles the number of sub-intervals until the absolute difference between successive integrals 
    | S_h-S_{h/2} | is sufficiently small.

    Parameters:
    f (function): integrand function.
    alpha, beta (int or float): lower and upper bounda of the interval [alpha, beta].
    epsilon (float): maximum absolute difference between successive integrals: stopping criterion
                     | S_h - S_{h/2} | < epsilon.
    iter_max (int): maximum number of iterations.

    Returns:
    t[k] (float): integral value
    t (list): succession of integral values (iterations)
    potencia2 (int): power of 2 in 2^potencia2 sub-intervals
    h (list): succession of subinterval lengths (h0, h0/2, h0/2^2, ...)
    dif (list): absolute difference between successive iterations
    '''
    h, dif = [beta / 2 - alpha/ 2], []
    x = np.linspace(alpha, beta, 3) # k = 0, 2^1 + 1 pts
    y = np.array([f(i) for i in x])
    s = np.array([h[0] * simpson(y)])
    
    for k in range(1, iter_max):
        h.append(h[k - 1] / 2)
        x = np.linspace(alpha, beta, 2**(k+1)+1)
        y = np.array([f(i) for i in x])
        s = np.append(s, h[k] * simpson(y))
        
        dif.append(abs(s[k] - s[k - 1]))
        
        if dif[k - 1] < epsilon:
            break
        elif k == iter_max - 1:
            print('Maximum number of iterations has been exceeded)')
            break
    
    int_res = s[k]
    potencia2 = k + 1
    
    return int_res, s, potencia2, h, [x.tolist() for x in dif]

# Examples
from math import exp
def teste():
    '''Integral of the function f(x) = exp(x) over [0, 1], with | S_h-S_{h/2} | < 1e-8'''
    print("simpsonmetodo(y) = 1.71831678685")
    alpha, beta, epsilon = 0, 1, 1e-8
    res, s, potencia2, h, dif = simpsonmetodo(lambda x: exp(x), alpha, beta, epsilon)
    print(res, s, potencia2, h, dif)

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
