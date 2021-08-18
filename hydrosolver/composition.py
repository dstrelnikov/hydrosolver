import numpy as np
from tabulate import tabulate


macronutrients_desc = [
    'N (NO3-)',
    'N (NH4+)',
    'P',
    'K',
    'Mg',
    'Ca',
    'S',
]

micronutrients_desc = [
    'Fe',
    'Zn',
    'B',
    'Mn',
    'Cu',
    'Mo',
]

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


def load_db(database_dict):
    compositions = {
            name: load({name: nutrients})
            for name, nutrients in database_dict.items()
            }

    return compositions

def load( composition_dict):
    '''Load composition from a dict.'''

    name, nutrients_dict = tuple(composition_dict.items())[0]
    vector = np.zeros(len(nutrients_stencil))

    for i, nutrient in enumerate(nutrients_stencil):
        if nutrient in nutrients_dict:
            vector[i] = nutrients_dict[nutrient]

    return Composition(name, vector)


class Composition:

    def __init__(self, name='', vector=np.zeros(len(nutrients_stencil))):
        self.name = name
        self.vector = vector


    def __repr__(self):

        description = f'Composition: {self.name}'

        table = tabulate(
                [
                    (nutrient, value, value * 10**6)
                    for (nutrient, value)
                    in zip(nutrients_stencil, self.vector)
                    if value != 0
                ],
                headers=['Nutrient', 'Ratio', 'Amount mg/kg'],
                tablefmt='simple',
                )

        return '\n\n'.join((description, table))

    def __str__(self):
        nutrients_list = (
                f'{desc}: {value}'
                for (desc, value) in zip(nutrients_stencil, self.vector)
                if value != 0
                )

        return ' :: '.join((self.name, ', '.join(nutrients_list)))

    def __add__(self, composition):
        name = f'{self.name} + {composition.name}'
        vector = self.vector + composition.vector

        return Composition(name, vector)

    def __rmul__(self, number):
        name = f'{number} * ({self.name})'
        vector = self.vector * number

        return Composition(name, vector)

    def dump(self):
        '''Represent a composition as a dict.'''

        nutrients_dict = {
                nutrient: value
                for nutrient, value in zip(nutrients_stencil, self.vector)
                if value != 0
                }

        return {self.name: nutrients_dict}
