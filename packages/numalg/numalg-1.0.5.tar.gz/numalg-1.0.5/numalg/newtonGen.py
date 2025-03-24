#!/usr/bin/env python3

'''Newton method for solving nonlinear systems of equations.''' 

import numpy
from math import pow

def newtonGen(f, jac, norma, x0=[], eps_abs=1e-6, eps_passo=1e-6, iter_max=1e3) :
    '''
    newtongen solves systems of nonlinear equations using iterative n-dimensioanl Newton method.
    It finds the roots of a system of equations where each equation is a function of multiple variables. 

    Parameters:
    f (function): function such that f(X) = 0.
    jac (function): Jacobian matrix of f.
    norma (float): norm used for the stopping criterion ||x^(k+1) - x^(k)|| < EPS_PASSO and  ||f(x^(k+1))|| < eps_abs.
    x0 (float): initial guess for the solution vector. 
    eps_abs (float): maximum value allowed for ||f(x^(k+1))||.
    eps_passo (float): maximum value allowed for distance between successive iterations ||x^(k+1) - x^(k)||.
    iter_max (int): maximum number of iterations.
   
    Returns
    z (np.ndarrys): solution vector.
    normafz (np.float): ||f(z)||, z = x^(i).
    normadelta (np.float): ||x^(i) - x^(i-1)||.
    i (int): number of iterations.
    '''
    dim = len(x0)
    fz = f(x0)
    fdet = numpy.linalg.det(jac(x0))
    for i in range(1, iter_max+1) :
       if abs(fdet) < 1e-12 : # f'(x0) near zero
          print('The value of det(Jac) in xi can not be zero')
          print('the method does not converge')
          return ()
       delta = numpy.linalg.solve(jac(x0), -f(x0))
       z = x0 + delta
       fz = f(z)
       fdet = numpy.linalg.det(jac(z))
       normadelta = numpy.linalg.norm(delta, norma)
       normafz = numpy.linalg.norm(fz, norma)
       if normadelta < eps_passo and normafz < eps_abs :
          break
       elif i == iter_max :
          print('Maximum number of iterations exceeded (iter_max)')
          return (z, normafz, normadelta, i)
    return (z, normafz, normadelta, i)

# Example
def teste():
    '''System of two equations: x0^2 - 2 + (x1 - 1)^2 - 4 = 0 and (x0 - 3)^2 + (x1 - 2)^2 - 1 = 0'''
    from math import inf
    f = lambda x: numpy.array( [ pow(x[0]-2, 2) + pow(x[1]-1, 2) - 4 , pow(x[0]-3, 2) + pow(x[1]-2, 2) - 1 ] )
    jac = lambda x: numpy.array( [ [ 2 * x[0] - 4 , 2 * x[1] - 2 ] , [ 2 * x[0] - 6 , 2 * x[1] - 4 ] ] )
    print( newtonGen(f, jac, inf, [2, 3], 1e-3, 1e-3, 100) )

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
