#!/usr/bin/env python3

'''Newton–Raphson method  root-finding algorithm.'''

def newton_raphson(f, flinha, x0, eps=1e-6, iter_max=100) :
    '''
    newton_raphson finds zeros of nonlinear equations f(z) = z using Newton-Raphson method.

    Parameters:
    f (function): function such that f(z) = 0 with z in the interval [a, b]
    flinha (function): derivative of f
    x0 (float); initial guess.
    eps (float): maximum allowed value for distance between successive iterations | x_{k+1} - x_k |
    iter_max (int): maximum number of iterations.

    Returns:
    z[i+1] (float): root
    fz (float): function f evaluated at the root.
    i+1 (int): number of iterations to achieve root z.
    z (list); vector with all iterations.
    dif (list): all absolute differences between successive iterations.
    '''
    dif, z, fz, fzlinha = [], [x0], f(x0), flinha(x0)
    i = 0
    while i < iter_max :
       if abs(fzlinha) < 1e-15 : # f'(x0) equal zero 
          print('Derivative value in Xi can not be zero')
          return (z[i], fz, i, z, dif)
       d = fz / fzlinha	 
       z += [z[i] - d]
       dif += [abs(d)]
       if dif[i] < eps :
          break
       fz = f(z[i+1])
       fzlinha = flinha(z[i+1])
       i += 1
    if i == iter_max :
       print('Maximum number of iterations exceeded (iter_max)') 
       return (z[i], fz, i, z, dif)
    return (z[i+1], fz, i+1, z, dif)

# Example
def teste():
    '''2 - x - exp(-x) = 0 with x0 = 2'''
    from math import exp
    print( newton_raphson(lambda x: 2-x-exp(-x), lambda x:  -1 + exp(-x), 2, 1e-8, 100) )

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
