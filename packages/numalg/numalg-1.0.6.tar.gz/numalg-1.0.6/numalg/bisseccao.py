#!/usr/bin/env python3

'''bissection method root-finding method'''

import math

def bisseccao(f, a, b, eps_abs=1e-6, eps_step=1e-6, iter_max=1e3) :
    '''
    bisseccao search for roots of single-variable equations f(x) = 0 
    using Bisection method.

    Parameters:
    f (function): function such that f(z) = 0 with z in the interval [a, b]
    eps_abs (float): maximum allowed value for |f(z)|, |f(z)| < eps_abs
    eps_step (float): maximum error allowed.
    iter_max (int): maximum number of iterations.

    Returns:
    raiz (float): root
    fc (float): f value at the root
    k (int): number of iterations to achieve root
    c (list): vector with all iterations
    e (list): vector with de sucessive errors
    '''
    k, c, e = 0, [], []
    fc = fa = f(a)
    fb = f(b)
    if fa * fb < 0. :
       while abs(b - a) >= eps_step :
          k = k + 1
          if k > iter_max :
             print('Maximum number of iterations exceeded: '+str(iter_max))
             break
          c += [(a + b)/2.]
          e += [(b - a)/2.]
          fc = f(c[k-1])
          if abs(fc) < eps_abs :
             break
          elif fa * fc < 0. :
             b = c[k-1]
             fb = fc
          else :
             a = c[k-1]
             fa = fc
    else :
       print('The function must have opposite signs at the extreme points')
       return ()
    raiz = c[len(c)-1]
    return (raiz, fc, k, c, e) 

# testing examples
def teste():
    '''cos(x) = 0 in [1, 3]'''
    print("bisseccao(lambda x: math.cos(x), 1, 3)")
    x = bisseccao(lambda x: math.cos(x), 1, 3)
    print("raiz="+str(x[0]) +" f(raiz)="+str(x[1]) +" iter="+str(x[2]))
    print
    '''2 - x - exp(-x) = 0 in [0, 2]'''
    print("bisseccao(lambda x: 2-x-math.exp(-x),0,2,1e-2,1e-2,100)")
    print(bisseccao(lambda x: 2-x-math.exp(-x),0,2,1e-2,1e-2,100))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
