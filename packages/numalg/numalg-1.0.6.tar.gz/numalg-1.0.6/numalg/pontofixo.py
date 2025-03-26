#!/usr/bin/env python3

'''fixed-point method of computing fixed points of a function g(x) = x'''

def pontofixo(g, x0, eps=1e-6, iter_max=100) :
    '''
    pontofixo finds fixed points of nonlinear x = g(x).
    It finds zeros of nonlinear equations f(x) = 0 if f(x) = 0 <=> x = g(x)

    Parameters:
    G (function): iterative function.
    x0 (float): initial guess.
    eps (flaot): maximum value allowed for distance between successive iterations | x_{k+1} - x_k |.
    iter_max - maximum number of iterations.
 
    Returns:
    z[i+1] (float): root
    i+1 (int): number of iterations to achieve root z.
    z (list); vector with all iterations.
    dif (list): all absolute differences between successive iterations.
    '''
    gz, z, dif = g(x0), [x0], []
    i = 0
    while i < iter_max :
       z += [g(x0)]
       dif += [abs(z[i+1] - x0)]
       if dif[i] < eps :
          break
       x0 = z[i+1]
       i += 1
    if i == iter_max :
       print('Maximum number of iterations exceeded (iter_max)')
       return (z[i], i, z, dif)
    return (z[i+1], i+1, z, dif)

# Example
from math import sin
def teste():
    '''x + 0.5 + sin(x) = x with x0 = 4'''
    print(pontofixo(lambda x: x + 0.5 + sin(x), 4, 1e-3, 100))

if __name__ == "__main__":
    teste()
# vim: set fileencoding=utf-8 :
