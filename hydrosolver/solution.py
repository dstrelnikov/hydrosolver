from functools import cached_property

import numpy as np
from tabulate import tabulate

from . import composition
from . import core


class Solution:
    def __init__(self, mass_total, water, formulation, fertilizers):
        '''Create a solution.

        Parameters:
            mass_total: float
                The total mass of the solutions.
            water: Composition
                The composition of the water used.
            formulation: np.array(float), (n,)
                Masses of the compositions (excluding water) in kg.
            fertilizers: [Composition], (n,)
                The fertilizers (compositions) to use.

    '''
        formulation = np.array(formulation)

        if not len(fertilizers) == len(formulation):
            raise ValueError(
                'The formulation does not match the number of fertilizers.')

        self.mass_total = mass_total
        self.water = water
        self.formulation = formulation
        self.fertilizers = fertilizers

    def __repr__(self):
        return self.as_table_plain()

    def as_table_plain(self):
        lines = [[fertilizer.name, amount, amount * 10**3]
                 for (fertilizer, amount)
                 in zip(self.fertilizers, self.formulation)]
        lines.append([self.water.name, self.mass_water, self.mass_water * 10**3])
        lines.append(['Total:', self.mass_total, self.mass_total * 10**3])

        table_solution = tabulate(
                lines,
                headers=['Composition', 'Amount in kg', 'Amount in g'],
                tablefmt='simple',
                )

        return '\n\n'.join((table_solution, self.composition.as_table_plain()))

    @cached_property
    def mass_water(self):
        return self.mass_total - sum(self.formulation)

    @cached_property
    def x(self):
        return np.concatenate((self.formulation, [self.mass_water]))

    @cached_property
    def A(self):
        '''The LHS matrix of the linear system.'''
        return np.stack(
                [f.vector for f in self.fertilizers] + [self.water.vector]
                ).transpose()

    @cached_property
    def b(self):
        '''The RHS vector of the linear system.'''
        return self.mass_total * self.composition_target.vector

    @cached_property
    def vector(self):
        '''Gives the resulting composition vector.'''
        return self.A @ self.x / self.mass_total

    @cached_property
    def composition(self):
        '''Gives the resulting Composition object.'''
        return composition.Composition(
            name='Resulting composition',
            vector=self.vector,
            )

    @cached_property
    def residual(self):
        return core.residual(self.A, self.b, self.x)

    @cached_property
    def R(self):
        return core.norm2(self.residual)

    @cached_property
    def grad(self):
        return core.gradient(self.A, self.b, self.x)

    @cached_property
    def grad_norm(self):
        return core.norm(self.grad)

    @cached_property
    def grad_norm2(self):
        return core.norm2(self.grad)

    # dummy projected gradient
    @cached_property
    def Pgrad(self):
        return self.grad

    @cached_property
    def Pgrad_norm(self):
        return core.norm(self.Pgrad)

    @cached_property
    def Pgrad_norm2(self):
        return core.norm2(self.Pgrad)

    def spawn(self, formulation_new):
        solution = Solution(
                self.mass_total,
                self.water,
                formulation_new,
                self.fertilizers
                )

        solution.composition_target = self.composition_target

        return solution
