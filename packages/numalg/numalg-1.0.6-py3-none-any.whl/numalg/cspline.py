#!/usr/bin/env python3

'''cspline finds the cubic splines '''

import numpy as np

def cspline(x, y, xi, spl):
    '''
    cspline finds the cubic splines for the input data points (x,y)

    Parameters:
    x (list): vector with point abscissas [ x_0, x_1, ..., x_n ]
    y (list): vector with point ordinates [ y_0, y_1, ..., y_n ] 
    xi (np.ndarray): points where to predict the response using the spline
    spl (int): spline type
    
    spl = 0 for zero second derivatives at ends (Natural)
    yi, s, pp = cspline(x,y,xi,0)
    spl = 1 for first derivatives on boundary specified (complete)
    yi,s,pp = cspline(x,[dy0] + y + [dyN], xi, 1)
    spl = 2 for second derivatives on boundary specified
    yi,s,pp = cspline(x,[dy0] + y + [dyN], xi, 1)
    spl = 3 for second derivative on boundary extrapolated (not-a-knot)
    yi,s,pp=cspline(x,y,xi,3)
    dy0 = s'(x0) = s01: initial derivative,
    dyN = s'(xN) = sN1: final derivative
    d2y0 = s''(x0) = s02: initial second derivative,
    d2yN = s''(xN) = sN2: final second derivative

    Returns:
    yi (np.darray): predicted responses using the spline
    s (np.darray): spline coefficients in the form
    s_j(x)=s(j,1)*(x_{j+1}-x)^3+s(j,2)*(x-x_j)^3+s(j,3)*(x-x_j)+s(j,4)
    s(n,k); n=1:N, k=1,4  
    c (np.darray): spline coefficients in the pp-form
    s_j(x)=c(j,1)*(x-x_j)^3+c(j,2)*(x-x_j)^2+c(j,3)*(x-x_j)+c(j,4)
    c(n,k); n=1:N, k=1,4  

    Examples:
    natural spline
    x = [0, 1, 2, 3]; y = [exp(i) for i in x] ; xi = np.linspace(0, 3, 3001)
    yi, s, pp = cspline(x,y,xi,0)
    spline coefficients
    s = 0.2523         0    1.4660    1.0000
        1.6911    0.7569    2.2229    3.0929
       -1.9434    5.8301    8.8098  269.7421
    so, the spline function is
    s_1(x)=0.2523(1-x)^3+0(x-0)^3+1.4660(x-0)+1, x in [0,1]
    s_2(x)=1.6911(2-x)^3+0.7569(x-1)^3+2.2229(x-1)+3.0929, x in [1,2]
    s_3(x)=-1.9434(3-x)^3+5.8301(x-2)^3+8.8098(x-2)+269.7421, x in [2,3]
    complete spline
    dy0=-1; dyN=-1; # with specified first derivatives on boundary
    x=[-pi, 0, pi]; y = [sin(i) for i in x]; xi=np.linspace(-pi, pi, 6284)
    yi,s,pp = cspline(x,[dy0] + y + [dyN], xi, 1)
    spline coefficients
    s = 0.0507    0.0000    0.5000   -1.5708
        0.0000   -0.0507    0.5000   -0.0000
    second derivatives especified
    dy0=-2; dyN=-30; 
    x=[0, 1, 2, 5/2]; y=[0, 1, 8, 9]; xi=np.linspace(0, 2.5, 2501)
    yi,s,pp=cspline(x,[dy0]+ y +[dyN],xi,2)
    spline coefficients
    s = -0.3333    1.9545   -1.2879    0.3333
         1.9545   -1.4848   10.4394   -0.9545
        -2.9697  -10.0000    3.7576    8.3712
    second derivatives extrapolated
    x=[0, 1, 2, 3]; y=[0, 1, 4, 5];
    xi=np.linspace(0, 3, 3001);
    yi,s,pp=cspline(x,y,xi,3)
    spline coefficients
    s = 1.0000    0.3333    1.6667   -1.0000
        0.3333   -0.3333    3.6667    0.6667
       -0.3333   -1.0000    1.6667    4.3333
    '''
    N = len(x)
    if spl == 1 or spl == 2:
        dy0 = y[0]
        dyN = y[N+1]
        y = y[1:N+1]
    
    h = np.zeros(N-1)
    dy = np.zeros(N-1)
    
    for k in range(N-1):
        h[k] = x[k+1] - x[k]
        dy[k] = (y[k+1] - y[k]) / h[k]
    
    # Boundary condition
    if spl == 0:  # Natural spline
        if N > 3:
            A = np.zeros((N-2, N-2))
            b = np.zeros(N-2)
            A[0, 0:2] = [(h[0] + h[1]) / 3, h[1] / 6]
            b[0] = dy[1] - dy[0]
            A[N-3, N-4:N-2] = [h[N-3] / 6, (h[N-3] + h[N-2]) / 3]
            b[N-3] = dy[N-2] - dy[N-3]
            
            for m in range(1, N-3):
                A[m, m-1:m+2] = [h[m-1] / 6, (h[m-1] + h[m]) / 3, h[m] / 6]
                b[m] = dy[m] - dy[m-1]
        else:
            A = np.zeros((1, 1))
            b = np.zeros(1)
            A[0, 0] = (h[0] + h[1]) / 3
            b[0] = dy[1] - dy[0]
    elif spl == 1:  # First derivatives specified
        A = np.zeros((N, N))
        b = np.zeros(N)
        A[0, 0:2] = [h[0] / 3, h[0] / 6]
        b[0] = dy[0] - dy0
        A[N-1, N-2:N] = [h[N-2] / 6, h[N-2] / 3]
        b[N-1] = dyN - dy[N-2]
        
        for m in range(1, N-1):
            A[m, m-1:m+2] = [h[m-1] / 6, (h[m-1] + h[m]) / 3, h[m] / 6]
            b[m] = dy[m] - dy[m-1]
    elif spl == 2:  # Second derivatives specified
        A = np.zeros((N, N))
        b = np.zeros(N)
        A[0, 0] = 1
        b[0] = dy0
        A[N-1, N-1] = 1
        b[N-1] = dyN
        
        for m in range(1, N-1):
            A[m, m-1:m+2] = [h[m-1] / 6, (h[m-1] + h[m]) / 3, h[m] / 6]
            b[m] = dy[m] - dy[m-1]
    elif spl == 3:  # Second derivatives extrapolated
        if N < 4:
            print('The number of points must be at least 4')
            return None, None, None
        
        A = np.zeros((N, N))
        b = np.zeros(N)
        A[0, 0:3] = [h[1], -(h[0] + h[1]), h[0]]
        b[0] = 0
        A[N-1, N-3:N] = [h[N-2], -(h[N-2] + h[N-3]), h[N-3]]
        b[N-1] = 0
        
        for m in range(1, N-1):
            A[m, m-1:m+2] = [h[m-1] / 6, (h[m-1] + h[m]) / 3, h[m] / 6]
            b[m] = dy[m] - dy[m-1]
    
    # Solve system of equations
    M = np.linalg.solve(A, b)
    
    if spl == 0:
        M = np.concatenate(([0], M, [0]))
    
    Aj = np.zeros(N-1)
    Bj = np.zeros(N-1)
    s = np.zeros((N-1, 4))
    
    for j in range(N-1):
        Aj[j] = dy[j] - (M[j+1] - M[j]) * h[j] / 6
        Bj[j] = y[j] - M[j] * h[j]**2 / 6
    
    for j in range(N-1):
        s[j, 0] = M[j] / 6 / h[j]
        s[j, 1] = M[j+1] / 6 / h[j]
        s[j, 2] = Aj[j]
        s[j, 3] = Bj[j]
    
    # Evaluate spline at xi
    yi = np.zeros(len(xi))
    
    for i in range(len(xi)):
        for j in range(N-1):
            if xi[i] <= x[j+1] and xi[i] >= x[j]:
                yi[i] = s[j, 0] * (x[j+1] - xi[i])**3 + s[j, 1] * (xi[i] - x[j])**3 + s[j, 2] * (xi[i] - x[j]) + s[j, 3]
                break
    
    # Calculate coefficients for each segment
    c = np.zeros((N-1, 4))
    for j in range(N-1):
        c[j, 0] = (M[j+1] - M[j]) / 6 / h[j]
        c[j, 1] = 3 * x[j] * c[j, 0] + (M[j] * x[j+1] - M[j+1] * x[j]) / 2 / h[j]
        c[j, 2] = 2 * c[j, 1] * x[j] - 3 * c[j, 0] * x[j]**2 + Aj[j] + (x[j]**2 * M[j+1] - x[j+1]**2 * M[j]) / 2 / h[j]
        c[j, 3] = c[j, 2] * x[j] - c[j, 1] * x[j]**2 + c[j, 0] * x[j]**3 - Aj[j] * x[j] + Bj[j] + (x[j+1]**3 * M[j] - x[j]**3 * M[j+1]) / 6 / h[j]
    
    return yi, s, c

import matplotlib.pyplot as plt

def exerc1():
    ''' natural spline with f(x) = exp(x), x = 0, 1, 2, 3 '''
    from math import exp
    x = [0, 1, 2, 3]; y = [exp(i) for i in x] ; xi = np.linspace(0, 3, 3001)
    yi, s, pp = cspline(x,y,xi,0)
    print('s =', s, '\npp =', pp)
    plt.plot(x,y,'ko', xi,yi,'r-',xi,[ exp(i) for i in xi],'-')
    plt.show()

def exerc2():
    ''' complete spline with f(x) = sin(x), x = -pi, 0, pi, first derivatives on boundary equal to -1  '''
    from math import pi, sin
    dy0 = -1; dyN = -1; # with specified first derivatives on boundary
    x = [-pi, 0, pi]; y = [sin(i) for i in x]; xi = np.linspace(-pi, pi, 6284)
    yi, s, pp = cspline(x,[dy0] + y + [dyN], xi, 1)
    print('s =', s, '\npp =', pp)
    plt.plot(x,y,'ko', xi,yi,'r-',xi,[ sin(i) for i in xi],'-')
    plt.show()

def exerc3():
    ''' second derivatives especified, x = [0, 1, 2, 5/2]; y = [0, 1, 8, 9], second derivatives on boundary equal to -2 and -30 '''
    dy0 = -2; dyN = -30; 
    x = [0, 1, 2, 5/2]; y = [0, 1, 8, 9]; xi = np.linspace(0, 2.5, 2501)
    yi, s, pp = cspline(x,[dy0]+ y +[dyN],xi,2)
    print('s =', s, '\npp =', pp)
    plt.plot(x,y,'ko', xi,yi,'r-')
    plt.show()

def exerc4():
    ''' second derivatives extrapolated, x = [0, 1, 2, 5/2]; y = [0, 1, 8, 9] '''
    x = [0, 1, 2, 3]; y = [0, 1, 4, 5];
    xi = np.linspace(0, 3, 3001);
    yi, s, pp = cspline(x,y,xi,3)
    print('s =', s, '\npp =', pp)
    plt.plot(x,y,'ko', xi,yi,'r-')
    plt.show()

def teste():
    ''' All Examples'''
    exerc1()
    exerc2()
    exerc3()
    exerc4()

if __name__ == '__main__':
    teste()

# vim: set fileencoding=utf-8 :
