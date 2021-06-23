import numpy as np
from .core import project_simplex as project
from . import core


class DescendLoopException(Exception):
    pass

class DescendToleranceException(Exception):
    pass


def gradient_descent(
        solution,
        iter_max=100,
        step_init=10**-1,
        tolerance=10**-10,
        sigma=10**-2,
        beta=.5,
        step_prediction=False
        ):
    try:
        print('Starting the gradient descent procedure...')
        descent = [solution]
        step = step_init
        mass = solution.mass_total

        print(f"{'i':>3}.{'j':<2}{'step':>15}{'R':>15}{'norm(grad)':>15}{'norm(Pgrad)':>15}")
        print(f"{solution.R:36.7e}{solution.grad_norm:15.7e}{solution.Pgrad_norm:15.7e}")

        for i in range(1, iter_max + 1):
            if solution.Pgrad_norm < tolerance:
                raise DescendToleranceException
            j = 0
            while True:
                print(f"{i:3}.{j:<2}{step:15.7e}", end='', flush=True)

                # make a step in the negative gradient direction
                # project the trial extended formulation on the simples
                # cut the last element off (alignment due to float arithmetics)
                formulation_trial = project(
                        solution.x - step * solution.grad, mass)[:-1]

                if np.allclose(formulation_trial, solution.formulation):
                    raise DescendLoopException

                solution_trial = solution.spawn(formulation_trial)

                # check if Armijo condition is satisfied, reduce the step otherwise
                if solution_trial.R < solution.R - sigma * step * solution.grad_norm2:
                    break

                print(f"{solution_trial.R:15.7e}{13*'-':>15}{13*'-':>15}")
                j += 1
                step *= beta

            # after a successful iteration adjust the step size for the next iteration
            if step_prediction:
                step *= solution.Pgrad_norm2 / solution_trial.Pgrad_norm2
            if j==0:
                step /= beta

            solution = solution_trial
            descent.append(solution)
            print(f"{solution.R:15.7e}{solution.grad_norm:15.7e}{solution.Pgrad_norm:15.7e}")

        else:
            print('Maximal number of iterations was reached.')

    except KeyboardInterrupt:
        print('\nInterrupted by user...')
    except DescendLoopException:
        print('\nThe descend procedure has looped:\n'
              'project(formulation_next) == formulation.')
    except DescendToleranceException:
        print('\nThe descend procedure was interrupted since\n'
              'solution.Pgrad_norm < tolerance.')

    print('Terminating.')

    return descent


def solve_lstsq(solution):
    return solution.spawn(core.solve_lstsq(solution.A, solution.b)[:-1])
