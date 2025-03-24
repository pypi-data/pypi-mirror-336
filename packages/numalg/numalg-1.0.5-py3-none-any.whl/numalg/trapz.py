#!/usr/bin/env python3

'''Composite Trapezoidal rule'''

import numpy as np

def trapz(x, y=[]) :
    '''
    trapz(y) computes an approximation of the integral of y using the Simson's method (with unit spacing).
    To compute the integral for spacing different from one, multiply simpson(y) by the spacing increment h.

    trapz(x,y) computes the integral of y with respect to x using the Simpson method. 
    x and y must be vectors of the same length.

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ].
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ].

    Return
    res (float): integral value
    '''
    if len(y) == 0 : # composite rule
      res = (x[0] + x[len(x)-1]) / 2.
      for i in range(1, len(x)-1) :
         res += x[i]
      return res
   # general rule: unequally spaced points 
    res = 0
    for i in range(len(x)-1) :
       res += (x[i+1]-x[i])*(y[i]+y[i+1])/2.
    return res

# Examples
def teste():
    '''x = [ 0., .25, .5, .75, 1. ], y = [ 1., 1.0645, 1.2840, 1.7551, 2.7183 ] with h = 0.25'''
    print ("trapz(y)=1.4906875")
    x = [ 0., .25, .5, .75, 1. ]
    y = [ 1., 1.0645, 1.2840, 1.7551, 2.7183 ]
    print(str(trapz(y)*.25))
    '''x = [ 0, .1, .25, .5, .8, 1. ], y = [ 1., 1.0101, 1.0645, 1.284, 1.8965, 2.7183 ]'''
    print ("trapz(x,y)=1.4882175")
    x = [ 0, .1, .25, .5, .8, 1. ]
    y = [ 1., 1.0101, 1.0645, 1.284, 1.8965, 2.7183 ]
    print(str(trapz(x, y)))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
