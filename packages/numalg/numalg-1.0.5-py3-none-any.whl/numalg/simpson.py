#!/usr/bin/env python3

'''Composite Simpson's Rule.'''

def simpson(x, y=[]) :
    '''
    simpson(y) computes an approximation of the integral of y using the Simson's method (with unit spacing).
    To compute the integral for spacing different from one, multiply simpson(y) by the spacing increment h.

    simpson(x,y) computes the integral of y with respect to x using the Simpson method. 
    x and y must be vectors of the same length.

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ].
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ].

    Return
    res (float): integral value
    '''
    xlen = len(x) - 1
    if xlen > 0 and xlen % 2 == 1 :
       print ("O número de pontos deve ser ímpar")
       return -1
    if len(y) == 0 : # composite rule
       res = x[0] + x[xlen]
       for i in range(1, xlen, 2) :
          res += 4 * x[i]
       for i in range(2, xlen, 2) :
          res += 2 * x[i]
       return res / 3.
   # general rule: equally spaced points three to three
    res = 0
    for i in range(0, xlen, 2) :
       res += (x[i+2]-x[i])*(y[i]+y[i+1]*4+y[i+2])/6.
    return res

# Examples
def teste():
    '''y = [ 1., 1.0645, 1.2840, 1.7551, 2.7183 ] with h = 0.25'''
    print ("simpson(y)=1.463725")
    h = .25
    y = [ 1., 1.0645, 1.2840, 1.7551, 2.7183 ]
    print(str(simpson(y) * h))
    '''y = [ 1., 1.0645, 1.2840, 1.7551, 2.7183, 4.7707, 9.4877, 21.381, 54.598 ] with h = 0.25'''
    print ("simpson(y)=16.5386")
    y = [ 1., 1.0645, 1.2840, 1.7551, 2.7183, 4.7707, 9.4877, 21.381, 54.598 ]
    print(str(simpson(y) * h))
    '''x = [ 0, .1, .2, .4, .6 ], y = [ 1., 1.0101, 1.0408, 1.1735, 1.4333 ]'''
    print ("simpson(x,y)=0.68058")
    x = [ 0, .1, .2, .4, .6 ]
    y = [ 1., 1.0101, 1.0408, 1.1735, 1.4333 ]
    print(str(simpson(x, y)))
    print ("simpson(x,y)=5.31113")
    x = [ 0, .1, .2, .4, .6, 1.1, 1.6 ]
    y = [ 1., 1.0101, 1.0408, 1.1735, 1.4333, 3.3535, 12.936 ]
    print(str(simpson(x, y)))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
