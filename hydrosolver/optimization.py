'''This module provides low-level optimization routines as well as high-level
enduser interfaces in order to mix and optimal solution.

Classes:
    ObjectiveFunctional
    WLSObjectiveFunctional
    OptimizationProblem
    OptimizationWaypoint

    One can see that the classes ObjectiveFunctional, OptimizationProblem, and
    OptimizationWaypoint make a sequence of the same functions which are getting
    partially-applied with one more arguments. The last level OptimizationWaypoint
    implements methods cost and grad which take no arguments.

Routines:
    project_simplex
    projected_gradient_descent

    These are low-level routines for performing optimization with full manual of
    every parameter.

End user interfaces:
    optimize

    Performs optimization based on weighted least square objective functional
    with default parameters.

Exceptions:
    DescendLoopException
    DescendToleranceException

'''

import argparse
from functools import cached_property
import logging

import numpy as np
from . import composition


parser = argparse.ArgumentParser()
parser.add_argument(
        '--log-level',
        default=40,
        type=lambda value: int(value),
    )
args = parser.parse_args()


logger = logging.getLogger(__name__)
logging.basicConfig(level=args.log_level, handlers=[logging.StreamHandler()])


class DescendLoopException(Exception):
    '''Raised when projected gradient descent routine has looped.'''
    pass

class DescendToleranceException(Exception):
    '''Raised when the predefined tolerance was reached.'''
    pass


class ObjectiveFunctional:
    def cost(self, A, b, x):
        pass

    def grad(self, A, b, x):
        pass

    def test(self, A, b, x, direction=None):
        raise NotImplementedError


class WLSObjectiveFunctional(ObjectiveFunctional):
    '''Provides the weighted least squares objective functional.'''

    def __init__(self, weights=None):
        if weights is None:
            weights = np.ones(len(composition.nutrients_stencil))
        self.weights = weights

    def cost(self, A, b, x):
        return np.inner(self.weights, (A @ x - b)**2)

    def grad(self, A, b, x):
        return 2 * self.weights * (A @ x - b).transpose() @ A


class OptimizationProblem:
    '''Defines a complete optimization problem formulation.'''
    def __init__(
            self,
            solution_init,
            composition_target,
            objective_functional,
            ):

        self.A = solution_init.A.copy()
        self.b = solution_init.mass * composition_target.vector
        self.x_init = solution_init.formulation
        self.objective_functional = objective_functional

    def cost(self, x):
        return self.objective_functional.cost(self.A, self.b, x)

    def grad(self, x):
        return self.objective_functional.grad(self.A, self.b, x)


class OptimizationWaypoint:
    '''Provides a point (an iteration) of iterative optimization process with
    convenient interfaces and caching.'''

    def __init__(self, optimization_problem, x=None):
        self.optimization_problem = optimization_problem
        if x is None:
            self.x = optimization_problem.x_init
        else:
            self.x = x

    @cached_property
    def cost(self):
        return self.optimization_problem.cost(self.x)

    @cached_property
    def grad(self):
        return self.optimization_problem.grad(self.x)

    @cached_property
    def grad_norm2(self):
        return np.dot(self.grad, self.grad)

    @cached_property
    def grad_norm(self):
        return np.sqrt(self.grad_norm2)

    def spawn(self, x):
        return OptimizationWaypoint(self.optimization_problem, x)


def project_simplex(v, m):
    '''Projects vector v in R(n+1) to the simplex m * delta(n).'''
    # see Algorithm 2
    # https://mblondel.org/publications/mblondel-icpr2014.pdf

    v_sorted = np.flip(np.sort(v))
    pi = (np.cumsum(v_sorted) - m) / (np.arange(len(v)) + 1)
    theta = pi[v_sorted - pi > 0][-1]
    projection = np.maximum(v - theta, 0)

    return projection


def projected_gradient_descent(
        optimization_problem,
        iter_max=100,
        step_init=10**-1,
        tolerance=10**-10,
        sigma=10**-2,
        beta=.5,
        step_prediction=False,
        ):
    '''Implements projected gradient descent routine.

    Parameters:
        optimization_problem (OptimizationProblem):
            Optimization problem to solve.
        iter_max (int):
            Maximal number of descent iterations (breaking condition).
        step_init (float):
            Initial gradient descent step size.
        tolerance (float):
            Desired tolarance (breaking condition).
        sigma (float):
            Adjustable coefficient in Armijo condition.
        beta (float):
            Adjustable coefficient for вуысуте acceleration and deceleration.
        step_prediction (bool):
            Whether the prediction formula will be used to adjust the next step
            size.


    At each iteration the projection is made on the simplex m * delta(n).

    '''

    logger.info('Starting the gradient descent procedure...')

    point = OptimizationWaypoint(optimization_problem)
    mass = point.x.sum()
    step = step_init

    descent = [point]

    logger.info(f"{'i':>3}.{'j':<2}{'step':>15}{'cost':>15}{'norm(grad)':>15}")
    logger.info(f"{point.cost:36.7e}{point.grad_norm:15.7e}")

    try:
        for i in range(1, iter_max + 1):
            if point.grad_norm < tolerance:
                raise DescendToleranceException

            j = 0
            while True:
                # make a step in the negative gradient direction
                # project the trial extended formulation on the simplex
                x_trial = project_simplex(point.x - step * point.grad, mass)
                
                if np.allclose(x_trial, point.x):
                    raise DescendLoopException

                point_trial = point.spawn(x_trial)

                # check if Armijo condition is satisfied, reduce the step otherwise
                if point_trial.cost < point.cost - sigma * step * point.grad_norm2:
                    break
                
                logger.info(f"{i:3}.{j:<2}{step:15.7e}{point_trial.cost:15.7e}{13*'-':>15}")
                j += 1
                step *= beta

            # after a successful iteration adjust the step size for the next iteration
            if step_prediction:
                step *= point.grad_norm2 / point_trial.grad_norm2
            if j==0:
                step /= beta

            point = point_trial
            descent.append(point)
            logger.info(f"{i:3}.{j:<2}{step:15.7e}{point.cost:15.7e}{point.grad_norm:15.7e}")
        else:
            logger.info('Maximal number of iterations was reached.')

    except KeyboardInterrupt:
        logger.info('Interrupted by user...')
    except DescendLoopException:
        logger.info('Loop breaking condition was triggered.')
    except DescendToleranceException:
        logger.info('Tolerance breaking condition was triggered.')

    logger.info('Terminating gradient descent.')

    return descent


def optimize(solution_init, composition_target, weights=None):
    '''Provides a high-level end user interface for projected gradient descent
    optimization.

    Parameters:
        solution_init (Solution):
            A solution which formulation msut be optimized towards composition_targer.
        composition_target (Composition):
            The desired composition.
        weights (np.array(float)):
            Weights to pass to the WLSObjectiveFunctional.

    Returns:
        solution_optimized (Solution)
            Optimized solution which resulting composition is as close as possible
            to composition_target in the WLS metric. The total mass and the list
            of compositions coincide with those in solution_init.

    '''

    optimization_problem = OptimizationProblem(
            solution_init,
            composition_target,
            WLSObjectiveFunctional(weights)
        )
    descent = projected_gradient_descent(optimization_problem)

    return solution_init.spawn(descent[-1].x) 
