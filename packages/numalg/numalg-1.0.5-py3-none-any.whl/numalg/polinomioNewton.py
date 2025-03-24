#!/usr/bin/env python3

'''Given n+1 points (xi, yi) calculates  the divided differences y_0, y_{10}, y_{210}, ..., y_{n...210}
   of the Newton interpolator polynomial
   p_n(x) = y_0 + y_{10} * (x - x_0) + y_{210} * (x - x_0) * (x - x_1) + ... + y_{n...210} * (x - x_0) ... (x - x_{n-1})'''

def polinomioNewton(x, y) :
    '''
    polynewton calculates the divided differences y_0, y_{10}, y_{210}, ..., y_{n...210}
    of the Newton interpolator polynomial based on the points (x_0,y_0), ..., (x_n,y_n):
    p_n(x) = y_0 + y_{10} * (x - x_0) + y_{210} * (x - x_0) * (x - x_1) + ... + y_{n...210} * (x - x_0) ... (x - x_{n-1})

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ]
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ] 

    Return:
    d (list): vector with the divided differences [ y_0, y_{10}, y_{210}, ..., y_{n...210} ]
    
    Example:
    res = polinomioNewton.polinomioNewton([0.5, 2, 3.5], [3.82, 3.01, 2.14])
    print(res)
    returns
    [3.82, -0.54, -0.013333333333333234]  
    and the polynomial is given by 
    p(x) = 3.8200 - 0.54 (x - 0.5) - 0.013333 (x - 0.5) (x-2)
    '''
    d = [y[0]]
    for i in range(1, len(x)) :
       for j in range(len(x)-i) :
          y[j] = (y[j+1] - y[j]) / (x[j+i] - x[j])
       d += [y[0]]
    return d

def teste():
    '''x = [0.5, 2, 3.5], y = [3.82, 3.01, 2.14]'''
    print("polinomioNewton([0.5, 2, 3.5], [3.82, 3.01, 2.14])=[3.82, -0.54, -0.013333333333333234]") 
    print(polinomioNewton([0.5, 2, 3.5], [3.82, 3.01, 2.14]))
    print("polinomioNewton([1., 2., 3., 5., 6.], [4.75, 4., 5.25, 19.75, 36.])=[4.75, -0.75, 1.0, 0.25, 0.0]")
    print(polinomioNewton([1., 2., 3., 5., 6.], [4.75, 4., 5.25, 19.75, 36.]))

if __name__ == "__main__":
    teste()

# vim: set fileencoding=utf-8 :
