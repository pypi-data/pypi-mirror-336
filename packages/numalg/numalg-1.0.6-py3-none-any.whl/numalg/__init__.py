# @(c) Isabel Reis dos Santos, IST Ulisboa, 2024
"""
Numerical analysis algorithms

For each module in the package contents use help for explanation and import,
for instance:
>>> help("numalg.bisseccao")
>>> import numalg.bisseccao as bis
>>> root, f_root, niter, iters, errors = bis.bisseccao(lambda x: math.cos(x),1,35)
"""

__author__ = 'Isabel Reis dos Santos <isabel.santos@tecnico.ulisboa.pt>'
__web__ = 'https://github.com/isabel-mc/pip.git'
__version__ = '1.0.5'
# visible modules within the package
__all__ = [ 'bisseccao', 'bvphold', 'bvp', 'compgauss2nodes',
    'compgauss3nodes', 'cspline', 'errorteor', 'euler', 'eulerrn',
    'gaussSeidel', 'heun', 'heunrn', 'jacobi', 'lagrangepol', 'midpointedo',
    'midpointedorn', 'midpoint', 'mmq', 'newtonGen', 'newton_raphson',
    'polinomioNewton', 'polynewton', 'polyvalLagrange', 'pontofixo',
    'rungekutta4', 'rungekutta4rn', 'secante', 'simpsonmetodo', 'simpson',
    'sorgs', 'splinelinear', 'taylor2', 'taylor2rn', 'trapezios', 'trapz' ]
