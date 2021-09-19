import numpy as np
from tabulate import tabulate


nutrients_stencil = [
    'N (NO3-)',
    'N (NH4+)',
    'P',
    'K',
    'Mg',
    'Ca',
    'S',
    'Fe',
    'Zn',
    'B',
    'Mn',
    'Cu',
    'Mo',
]


class Composition:

    def __init__(self, name='', vector=np.zeros(len(nutrients_stencil))):
        '''Creates a new composition.

        Parameters:
            name: string, default=''
                A human-readable name for the composition.
            vector: [float]
                A list or a numpy array containing relative amounts of each
                nunitrient in the composition. The length of this vector must
                coincide with the length of composition.nutrients_stencil.

        '''
        self.name = name
        self.vector = np.array(vector)

    @classmethod
    def from_dict(cls, composition_dict):
        '''Creates a new Composition from a dict.'''

        name, nutrients_dict = tuple(composition_dict.items())[0]
        vector = np.zeros(len(nutrients_stencil))

        for i, nutrient in enumerate(nutrients_stencil):
            if nutrient in nutrients_dict:
                vector[i] = nutrients_dict[nutrient]

        return cls(name, vector)

    def __add__(self, composition):
        name = f'{self.name} + {composition.name}'
        vector = self.vector + composition.vector

        return Composition(name, vector)

    def __neg__(self):
        return Composition(f'- ({self.name})', - self.vector)

    def __sub__(self, composition):
        name = f'{self.name} - {composition.name}'
        vector = self.vector - composition.vector

        return Composition(name, vector)

    def __eq__(self, other):
        return np.all(self.vector == other.vector)

    def __repr__(self):
        return self.table()

    def __str__(self):
        return f'{self.name} :: ' + ', '.join(
                    f'{nutrient}: {amount_ppm:.2f}'
                    for nutrient, amount_ppm
                    in zip(nutrients_stencil, 10**6 * self.vector)
                    )

    def __rmul__(self, number):
        name = f'{number} * ({self.name})'
        vector = self.vector * number

        return Composition(name, vector)

    def __len__(self):
        return len(self.vector)

    def as_dict(self):
        '''Returns a dict representation for the given composition.'''

        nutrients_dict = {
                nutrient: float(value)
                for nutrient, value in zip(nutrients_stencil, self.vector)
                if value != 0
                }

        return {self.name: nutrients_dict}

    def table(self, sparse=True, ref=None, tablefmt='simple'):
        description = f'Composition: {self.name}'

        nutrients = np.array(nutrients_stencil)
        vector = self.vector

        if ref is not None:
            vector_ref = ref.vector
        else:
            vector_ref = np.zeros(len(nutrients_stencil))

        if sparse:
            mask_nonzero = (vector != 0) | (vector_ref != 0)
            nutrients = nutrients[mask_nonzero]
            vector = vector[mask_nonzero]
            vector_ref = vector_ref[mask_nonzero]

        table_dict = {
                'Nutrient': nutrients,
                'Ratio': vector,
                'Amount mg/kg': 10**6 * vector,
                }

        if ref is not None:
            description += f'\nReference: {ref.name}'
            table_dict['Diff mg/kg'] = 10**6 * (vector - vector_ref)

        table = tabulate(table_dict, headers='keys', tablefmt=tablefmt)

        return '\n\n'.join((description, table))
