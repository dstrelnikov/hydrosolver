import argparse
from functools import cache
import logging

import numpy as np
from .core import project_simplex as project
from . import core


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
    pass

class DescendToleranceException(Exception):
    pass

class OptimizationProblem:
    def __init__(
            self,
            solution_init,
            composition_target,
            weights,
            ):

        self.A = solution_init.A.copy()
        self.b = solution_init.mass * composition_target.vector
        self.weights = weights

    def r(self, x):
        return core.residual(self.A, self.b, x)

    def r_norm2(self, x):
        return core.norm2(self.r(x))

    def grad(self, x):
        return core.gradient(self.A, self.b, x, self.weights)

    def grad_norm(self, x):
        return core.norm(self.grad(x))

    def grad_norm2(self, x):
        return core.norm2(self.grad(x))

    def Pgrad_norm(self, x):
        return self.grad_norm(x)

    def Pgrad_norm2(self, x):
        return self.grad_norm2(x)


def gradient_descent(
        solution_init,
        composition_target,
        weights=None,
        iter_max=100,
        step_init=10**-1,
        tolerance=10**-10,
        sigma=10**-2,
        beta=.5,
        step_prediction=False,
        ):
    try:
        if weights is None:
            weights = np.ones(len(composition_target))

        logger.info('Starting the gradient descent procedure...')
        step = step_init
        mass = solution_init.mass
        x = solution_init.formulation

        c = OptimizationProblem(solution_init, composition_target, weights)
        c.descent = [x]

        logger.info(f"{'i':>3}.{'j':<2}{'step':>15}{'R':>15}{'norm(grad)':>15}{'norm(Pgrad)':>15}")
        logger.info(f"{c.r_norm2(x):36.7e}{c.grad_norm(x):15.7e}{c.Pgrad_norm(x):15.7e}")

        for i in range(1, iter_max + 1):
            if c.Pgrad_norm(x) < tolerance:
                raise DescendToleranceException
            j = 0
            while True:
                # logger.info(f'{i:3}.{j:<2}{step:15.7e}')

                # make a step in the negative gradient direction
                # project the trial extended formulation on the simplex
                x_trial = project(x - step * c.grad(x), mass)

                if np.allclose(x_trial, x):
                    raise DescendLoopException

                # check if Armijo condition is satisfied, reduce the step otherwise
                if c.r_norm2(x_trial) < c.r_norm2(x) - sigma * step * c.grad_norm2(x):
                    break

                logger.info(f"{i:3}.{j:<2}{step:15.7e}{c.r_norm2(x_trial):15.7e}{13*'-':>15}{13*'-':>15}")
                j += 1
                step *= beta

            # after a successful iteration adjust the step size for the next iteration
            if step_prediction:
                step *= c.Pgrad_norm2(x) / c.Pgrad_norm2(x_trial)
            if j==0:
                step /= beta

            x = x_trial
            c.descent.append(x)
            logger.info(f"{i:3}.{j:<2}{step:15.7e}{c.r_norm2(x):15.7e}{c.grad_norm(x):15.7e}{c.Pgrad_norm(x):15.7e}")

        else:
            logger.info('Maximal number of iterations was reached.')

    except KeyboardInterrupt:
        logger.info('\nInterrupted by user...')
    except DescendLoopException:
        logger.info('\nThe descend procedure has looped:\n'
              'project(formulation_next) == formulation.')
    except DescendToleranceException:
        logger.info('\nThe descend procedure was interrupted since\n'
              'solution.Pgrad_norm < tolerance.')

    logger.info('Terminating.')

    return solution_init.spawn(c.descent[-1]), c


def solve_lstsq(solution):
    return solution.spawn(core.solve_lstsq(solution.A, solution.b))
