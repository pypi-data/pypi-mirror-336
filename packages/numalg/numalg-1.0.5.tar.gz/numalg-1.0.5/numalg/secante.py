#!/usr/bin/env python3

'''secant method root-finding algorithm.'''

def secante(f, x0, x1, eps_abs=1e-6, eps_step =1e-6, iter_max=100) :
    '''
    secante finds zeros of nonlinear equations f(z) = 0 using Secant method
 
    Parameters:
    f (function): function such that f(z) = 0 with z in the interval [a, b]
    x0, x1 (float); initial guesses.
    eps_abs (float): maximum allowed value for |f(z)|, |f(z)| < eps_abs
    eps_step (float): maximum allowed value for distance between successive iterations | x_{k+1} - x_k |
    iter_max (int): maximum number of iterations.

    Returns:
    z[i+1] (float): root
    i+1 (int): number of iterations to achieve root z.
    z (list); vector with all iterations.
    dif (list): all absolute differences between successive iterations.
    fvalue (float): function f evaluated at all iterations.
    '''
    z, iterdif, dif, fvalue = [x0, x1], [x1 - x0], [abs(x1 - x0)], [f(x0), f(x1)]
    fxdif = [ fvalue[1] - fvalue[0] ]
    i = 0
    while i < iter_max :
       if abs(fxdif[i]) < 1e-15 : # denominator zero 
          print('f(Xi+1) - f(Xi) can not be zero (denominator)')
          return (z[i], i, z, dif, fvalue)
       iterdif += [ - iterdif[i] * fvalue[i+1] / fxdif[i] ]
       z += [ z[i+1] + iterdif[i+1] ]
       fvalue += [ f(z[i+2]) ]
       fxdif += [ fvalue[i+2] - fvalue[i+1] ]
       dif += [ abs(iterdif[i+1]) ]
       if dif[i+1] < eps_step and abs(fvalue[i+2]) < eps_abs :
          break
       i += 1
    if i == iter_max :
       print('Foi excedido o número máximo de iterações (iter_max)') 
    return (z[i+1], i+1, z, dif, fvalue)

# Example
def teste():
    '''- 3t + 2t^3 + 1 = 0 with initial values t0 = 0 and t1 = 0.5'''
    from math import exp
    print( secante(lambda t: - 3 * t + 2 * t ** 3 + 1, 0, 0.5, 1e-2, 1e-2, 100) )

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
