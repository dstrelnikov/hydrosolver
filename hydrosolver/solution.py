import numpy as np
from tabulate import tabulate

from .composition import Composition


class Solution:
    def __init__(self, compositions, formulation):
        '''Creates a solution.

        Parameters:
            compositions ([Composition]):
                The compositions to use.
            formulation (array_like(float)):
                Masses of the compositions (including the water) in kg.

        Raises:
            ValueError:
                If the lengths of compositions and formulation do not match.

        '''

        if not len(compositions) == len(formulation):
            raise ValueError(
                'The compositions length does not match the formulation length.')

        self.compositions = compositions
        self.formulation = np.array(formulation)

    @classmethod
    def dissolve(cls, mass, water, compositions_, formulation_=None):
        '''Creates a new Solution by dissolving the given compositions in water.

        Parameters:
            mass (float):
                The total mass of the solution in kg.
            water (Composition):
                The composition of the water used for dissolving.
            compositions_ [Composition]:
                Truncated list of compositions, i.e. the compositions to
                dissolve in the water.
            formulation_ (array_like(float)):
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

    def __iadd__(self, other):
        if self.compositions == other.compositions:
            self.formulation += other.formulation
            return self
        else:
            raise ArithmeticError(
                'Only solutions of the same compositions can be added or subtracted.')

    def __neg__(self):
        return self.spawn(-self.formulation)

    def __sub__(self, other):
        return self + (- other)

    def __mul__(self, number):
        return number * self

    def __rmul__(self, number):
        return self.spawn(number * self.formulation)

    def __imul__(self, number):
        self.formulation *= number
        return self

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
            return Composition(name='Resulting composition')
        else:
            return Composition(
                name='Resulting composition',
                vector=(self.A @ self.formulation / self.mass),
                )

    def spawn(self, formulation_new):
        '''Spawns a new Solution with the same list of compositions.

        Parameters:
            formulation_new (np.array(float)):
                Masses of the compositions (including the water) in kg.

        '''
        return Solution(self.compositions.copy(), formulation_new)

    def copy(self):
        return self.spawn(self.formulation.copy())

    def add(self, composition, amount, index=-1, align=True):
        '''Adds the given composition in the given amount to the solution.

        If the given composition already exist in the solution then its amount
        will be increased by the given amount.
        Otherwise the composition will be inserted.

        Parameters:
            composition (Composition):
                The composition to add to the solution.
            amount (float):
                The amount in which the given composition will be added.
            index (int):
                Position to insert the composition.
            align (bool):
                Whether the total mass of the solution will be compensated by
                the last composition (typically water).

        '''

        if composition in self.compositions:
            self.formulation[self.compositions.index(composition)] += amount
        else:
            self.compositions.insert(index, composition)
            self.formulation = np.concatenate(
                (self.formulation[:index], [amount], self.formulation[index:])
            )

        if align:
            self.align(self.mass - amount)

    def align(self, mass, index=-1):
        '''Aligns the total mass of the solution by the amount of composition
        at the given index.

        Parameters:
            mass (float):
                Desired total mass of the solution after alignment.
            index (int):
                The index of the composition which will be used for alignment.

        '''
        self.formulation[index] += mass - self.mass

    def merge(self, other):
        '''Creates a new solution by merging another solution into the current
        solution.

        '''

        if self.compositions == other.compositions:
            return self + other

        solution = self.copy()
        for composition, amount in zip(other.compositions, other.formulation):
            solution.add(composition, amount, align=False)

        return solution
