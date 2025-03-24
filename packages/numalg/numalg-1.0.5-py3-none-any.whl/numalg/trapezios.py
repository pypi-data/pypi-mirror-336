#!/usr/bin/env python3

'''Composite Trapezoidal rule using h such that | T_h-T_{h/2} | is sufficiently small (it begins with two sub-intervals).
   Can be used when it is possible to calculate the function at all points of the integration interval.'''



from numalg.trapz import trapz
import numpy as np

def trapezios(f, alpha, beta, epsilon=1e-3, iter_max=10) :
    '''
    trapezios finds the integral of the function f over the interval [alpha, beta] 
    using the Trapeziodal rule.
    The function starts by calculating the integral with steps h0 = (beta - alpha) / 2 and h0 / 2,  and 
    then doubles the number of sub-intervals until the absolute difference between successive integrals 
    | T_h - T_{h/2} | is sufficiently small.

    Parameters:
    f (function): integrand function.
    alpha, beta (int or float): lower and upper bounda of the interval [alpha, beta].
    epsilon (float): maximum absolute difference between successive integrals: stopping criterion
                     | T_h - T_{h/2} | < epsilon.
    iter_max (int): maximum number of iterations.

    Returns:
    int_res (float): integral value
    t (list): succession of integral values (iterations)
    potencia2 (int): power of 2 in 2^potencia2 sub-intervals
    h (list): succession of subinterval lengths (h0, h0/2, h0/2^2, ...)
    dif (list): absolute difference between successive iterations
    '''
    h, dif = [beta - alpha], []
    x = np.linspace(alpha, beta, 2) # k = 0, 2^0 + 1 pts
    y = np.array([f(i) for i in x])
    t = np.array([h[0] * trapz(y)])
    
    for k in range(1, iter_max):
        h.append(h[k - 1] / 2)
        x = np.linspace(alpha, beta, 2**k+1)
        y = np.array([f(i) for i in x])
        t = np.append(t, h[k] * trapz(y))
        
        dif.append(abs(t[k] - t[k - 1]))
        
        if dif[k - 1] < epsilon:
            break
        elif k == iter_max - 1:
            print('Maximum number of iterations has been exceeded)')
            break
    
    int_res = t[k]
    potencia2 = k
    
    return int_res, t, potencia2, h, [x.tolist() for x in dif]

# Examples
def teste():
    '''Integral of the function f(x) = exp(x) over [0, 1], with | S_h-S_{h/2} | < 1e-3'''
    from math import exp
    print('int_0^1 exp(d) dx')
    int_res, t, potencia2, h, dif = trapezios(lambda x: exp(x), 0, 1)
    print(int_res, t, potencia2, h, dif)

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
