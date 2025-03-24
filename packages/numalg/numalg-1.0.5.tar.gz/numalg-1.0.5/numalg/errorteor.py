#!/usr/bin/env python3

'''Calculation of mean and variance with different algorithms, adding numbers and Calculation of terms of a sequence.'''

def suc(x0, k):
    '''
    suc allows to calculate the first k terms of the sequence
    x_{i+1} = 1 - (i + 1) x_i, i = 0, 1, 2, ... 

    Parameters:
    x0 (float): initial value.
    k (int): number of terms.
    
    Return:
    x (list): first n terms of the sequence
    
    Observation: Calculate the first 50 terms of the sequence using the suc function 
    and the following initial values x0 = 0.2, x0 = 1 and x0 = (e − 1)/e.
    Knowing that, for x0 = (e − 1)/e, the sequence tends to zero, explain the result obtained.
    '''
    x = [0] * k  # Initialize a list of size k
    x[0] = x0  # Set the first element to x0
    for i in range(1, k):
        x[i] = 1 - i * x[i-1]  # Apply the recurrence relation
    return x

import math

def round_significant(x, k):
    '''Rounds a number x to k significant digits.'''
    if x == 0:
        return 0
    else:
        magnitude = math.floor(math.log10(abs(x)))
        factor = 10 ** (k - magnitude - 1)
        return round(x * factor) / factor

def mvamostral(x, k):
    '''
    Compute the mean and variance of a list x with rounding to k significant digits.

    Parameters:
    x (list): set of numbers
    k (int): number of significant digits in the Floating Point system

    Returns:
    m (float): mean of the set of numbers
    v (float): variance of the set of numbers
    
    Observation: run the program to calculate the mean and variance considering 
    k = 6, 7, 8, 9, 10 digits of precision and the vector 
    x = [1002, 1000, 1003, 1001, 1002, 1002, 1001, 1004, 1002, 1001]
    Calculate the mean and variance of the elements of this vector using the 
    np.mean and np.var commands of python and to obtain the relative errors of 
    the values you obtained using the mvamostral function. Are any of the results wrong?
    If so, please explain the reason.
    '''
    n = len(x)
    sum1 = 0
    sum2 = 0

    for i in range(n):
        sum1 = round_significant(sum1 + round_significant(x[i] ** 2, k), k)
        sum2 = round_significant(sum2 + x[i], k)

    m = round_significant(sum2 / n, k)
    v = round_significant((sum1 - round_significant(sum2 ** 2, k) / n) / (n - 1), k)
    
    return m, v

def meanvar(x, k):
    '''
    Compute the mean and variance of a list x with rounding to k significant digits.

    Parameters:
    x (list): set of numbers
    k (int): number of significant digits in the Floating Point system

    Returns:
    m (float): mean of the set of numbers
    v (float): variance of the set of numbers

    Observation: function meanvar allows to calculate the sample variance more accurately 
    than the mvamostral, without increasing the number of digits in the mantissa.
    '''
    n = len(x)
    sum2 = 0

    # Calculate the sum of the values and round each step to k significant digits
    for i in range(n):
        sum2 = round_significant(sum2 + x[i], k)

    # Calculate mean
    m = round_significant(sum2 / n, k)

    sum1 = 0
    # Calculate the sum of squared deviations from the mean, rounded to k significant digits
    for i in range(n):
        sum1 = round_significant(sum1 + round_significant((x[i] - m), k) ** 2, k)

    # Calculate variance
    v = round_significant(sum1 / (n - 1), k)
    
    return m, v

def soma(n):
    '''
    soma calculates the sum of the first n terms starting from the first to the last, 
    that is, from k = 1 to k = n.
    sum_{k = 1}^infty 1/k^2 = pi^2/6

    Parameter:
    n (int): number of term uin the sumation.

    Return:
    sum (float): value of the sumation.

    Observation: Use this code to calculate the value of this sum. 
    What is the relative error of the value obtained?
    Write the code to calculate the sum of the first 3000 terms but now in reverse order, 
    that is, from the last to the first, from k = 3000 to k = 1, also using a system with 
    four digits in the mantissa. Obtain the value of the sum using your code and calculate 
    the relative error of the result. Explain the difference between the results obtained 
    using your code and the statement. It should be noted that the calculations do not 
    involve any subtraction.
    '''
    sum = 0
    for i in range(1, n + 1):
        sum = round_significant(sum + round_significant(1 / i**2, 4), 4)
    return sum


# Examples
def teste_suc():
    '''First 10 terms of a sequence: x0 = 0.5, x_{i+1} = 1 - (i + 1) x_i, i = 0, 1, 2, ... 10'''
    print('x0 = 0.5, x_{i+1} = 1 - (i + 1) x_i, i = 0, 1, 2, ... 10') 
    x0 = 0.5; k = 10 
    result = suc(x0, k)
    print(result)

def teste_mvamostral():
    '''Mean and variance with floating point with 3 mantisse digits for 'x = [2.5, 3.5, 4.5, 5.5] using mvamostral''' 
    print('x = [2.5, 3.5, 4.5, 5.5]; k = 3 using mvamostral')
    x = [2.5, 3.5, 4.5, 5.5]; k = 3
    m, v = mvamostral(x, k)
    print("Mean:", m)
    print("Variance:", v)

def teste_meanvar():
    '''Mean and variance with floating point with 3 mantisse digits for 'x = [2.5, 3.5, 4.5, 5.5] using meanvar''' 
    print('x = [2.5, 3.5, 4.5, 5.5]; k = 3 using meanvar')
    x = [2.5, 3.5, 4.5, 5.5]; k = 3
    m, v = meanvar(x, k)
    print("Mean:", m)
    print("Variance:", v)

def teste_soma():
    '''sum_{k = 1}^{3000} 1/k^2'''
    print('sum_{k = 1}^{infty} 1/k^2 = pi^2/6')
    print('sum_{k = 1}^{3000} 1/k^2')
    n = 3000
    s = soma(n)
    print(s)

def teste():
    '''All examples'''
    teste_suc()
    teste_mvamostral()
    teste_meanvar()

if __name__ == "__main__":
    teste()
    
# vim: set fileencoding=utf-8 :
