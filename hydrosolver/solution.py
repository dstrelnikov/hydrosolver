from functools import cached_property

import numpy as np
from tabulate import tabulate

from . import composition
from . import core


class Solution:
    def __init__(self, compositions, formulation):
        '''Create a solution.

        Parameters:
            compositions: [Composition], (n,)
                The compositions to use.
            formulation: np.array(float), (n,)
                Masses of the compositions (including the water) in kg.

        '''

        if not len(compositions) == len(formulation):
            raise ValueError(
                'The formulation is inconsistent with the number of compositions.')

        self.compositions = compositions
        self.formulation = np.array(formulation)

    @classmethod
    def dissolve(cls, mass, water, compositions_, formulation_=None):
        '''Creates a new Solution by dissolving the given compositions in water.

        Parameters:
            mass: float, >= 0
                The total mass of the solution in kg.
            water: Composition
                The composition of the water used.
            compositions_: [Composition], (n-1,)
                Truncated list of compositions, i.e. the compositions to
                dissolve in the water.
            formulation_: np.array(float), (n-1,)
                Truncated array of amounts, i.e. the masses of the compositions
                (excluding the water) in kg.

        '''

        compositions = compositions_ + [water]
        if formulation_ is None:
            formulation_ = np.zeros(len(compositions_))
        formulation = np.concatenate((formulation_, [mass - sum(formulation_)]))
        return cls(compositions, formulation)

    def __add__(self, other):
        if self.compositions == other.compositions:
            return self.spawn(self.formulation + other.formulation)
        else:
            raise ArithmeticError(
                'Only solutions of the same compositions can be added or subtracted.')

    def __neg__(self):
        return self.spawn(-self.formulation)

    def __sub__(self, other):
        return self + (- other)

    def __rmul__(self, number):
        return self.spawn(number * self.formulation)

    def __repr__(self):
        return self.as_table_plain()

    def as_table_plain(self):
        lines = [
                    [composition.name, amount, amount * 10**3]
                    for (composition, amount)
                    in zip(self.compositions, self.formulation)
                ]
        lines.append(['Total:', self.mass, self.mass * 10**3])

        table_solution = tabulate(
                lines,
                headers=['Composition', 'Amount in kg', 'Amount in g'],
                tablefmt='simple',
                )

        return '\n\n'.join((table_solution, self.composition.table()))

    @property
    def mass(self):
        return self.formulation.sum()

    @property
    def A(self):
        '''Computes the LHS matrix of the linear system.'''
        return np.stack([c.vector for c in self.compositions], axis=-1)

    @property
    def composition(self):
        '''Gives the resulting Composition object.'''
        if self.mass == 0:
            return composition.Composition(name='Resulting composition')
        else:
            return composition.Composition(
                name='Resulting composition',
                vector=(self.A @ self.formulation / self.mass),
                )

    def spawn(self, formulation_new):
        '''Spawns a new Solution with the same list of compositions.

        Parameters:
            formulation_new: np.array(float), (n,)
                Masses of the compositions (including the water) in kg.

        '''
        return Solution(self.compositions, formulation_new)
