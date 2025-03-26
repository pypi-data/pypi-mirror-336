#!/usr/bin/env python3

'''Least squares method with a generic approximating function g(x) = c_0 * phys_0(x) + ... + c_m * phys_m(x)'''

import numpy as np

def mmq(x, y, phys):
    '''
    mmq(x,y,phys) calculates the unknown coefficients of the
    approximating function g(x) = c_0 * phys_0(x) + ... + c_m * phys_m(x)
    obtained by the least squares method with the points (Xi,Yi)
 
    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ]
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ] 
    phys (list): vector of basis functions
 
    Return:
    coef (np.ndarray): coefficients of the basis functions
    '''
    x = np.array(x).reshape(-1, 1)  
    y = np.array(y).reshape(-1, 1) 
    A = np.zeros((len(x), len(phys)))
    
    for i in range(len(phys)):
        A[:, i] = phys[i](x).flatten() 
    
    AtA = A.T @ A  
    Aty = A.T @ y 
    coef = np.linalg.inv(AtA) @ Aty
    
    return coef

# Example
def teste():
    '''x = [-1.0, 0.5, 2.0, 3.5, 5.0], y = [6.34, 3.82, 3.01, 2.14, 2.10], phys_0(x) = 1/(4+x) and phys_1(x) = x/(1+x^2)
       g(x) = 18.3 / (4 + x) - 0.447 * x /  (1 + x^2)'''
    x = [-1.0, 0.5, 2.0, 3.5, 5.0]
    y = [6.34, 3.82, 3.01, 2.14, 2.10]
    def f1(x):
       return 1 / (4 + x)
    def f2(x):
       return x / (1 + x**2)
    phys = [f1, f2]
    coef = mmq(x, y, phys)
    print("Coefficients:", coef)

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
