'''Basic routines for the linear system A x = b.'''

import numpy as np


def residual(A, b, x):
    return A @ x - b

def gradient(A, b, x):
    '''Computes the gradient of the least square objective functional.
        A x -> b

    '''
    return 2 * (A @ x - b).transpose() @ A

def solve_lstsq(A, b):
    return np.linalg.lstsq(A, b, rcond=None)[0]

def norm(v):
    return np.linalg.norm(v)

def norm2(v):
    return np.dot(v, v)

def project_simplex(v, m):
    '''Projects vector v∈R(n+1) to the simplex m*Δn.'''
    # see Algorithm 2
    # https://mblondel.org/publications/mblondel-icpr2014.pdf

    v_sorted = np.flip(np.sort(v))
    pi = (np.cumsum(v_sorted) - m) / (np.arange(len(v)) + 1)
    theta = pi[v_sorted - pi > 0][-1]
    projection = np.maximum(v - theta, 0)

    return projection
