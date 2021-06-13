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
    return np.linalg.lstsq(A, b)[0]

def norm(v):
    return np.linalg.norm(v)

def norm2(v):
    return np.dot(v, v)
