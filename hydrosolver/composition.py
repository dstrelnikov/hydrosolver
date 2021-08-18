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


class Composition:

    def __init__(self, composition_dict):
        '''Load composition from a dict.'''

        self.name, nutrients_dict = tuple(composition_dict.items())[0]
        self.vector = np.zeros(len(nutrients_stencil))

        for i, nutrient in enumerate(nutrients_stencil):
            if nutrient in nutrients_dict:
                self.vector[i] = nutrients_dict[nutrient]

    def __repr__(self):
        description = f'Composition: {self.name}'

        table_macro = tabulate(
                [[desc, amount, amount * 10**6] for (desc, amount) in
                            zip(macronutrients_desc, self.macronutrients)],
                headers=['Macronutrient', 'Ratio', 'Amount mg/kg'],
                tablefmt='simple',
                )

        table_micro = tabulate(
                [[desc, amount, amount * 10**6] for (desc, amount) in
                            zip(micronutrients_desc, self.micronutrients)],
                headers=['Micronutrient', 'Ratio', 'Amount mg/kg'],
                tablefmt='simple',
                )

        return '\n\n'.join([description, table_macro, table_micro])

    def __str__(self):
        list_macro = (f'{desc}: {amount}' for (desc, amount) in
                            zip(macronutrients_desc, self.macronutrients))
        list_micro = (f'{desc}: {amount}' for (desc, amount) in
                            zip(micronutrients_desc, self.micronutrients))

        return '\n'.join(
                (
                    self.name,
                    ', '.join(list_macro),
                    ', '.join(list_micro)
                ))

    def __add__(self, composition):
        name = f'{self.name} + {composition.name}'
        macronutrients = .5 * (self.macronutrients + composition.macronutrients)
        micronutrients = .5 * (self.micronutrients + composition.micronutrients)

        return Composition(macronutrients, micronutrients, name)

    def __rmul__(self, number):
        name = f'{number} * ({self.name})'
        macronutrients = self.macronutrients * number
        micronutrients = self.micronutrients * number

        return Composition(macronutrients, micronutrients, name)

    def dump(self):
        '''Represent a composition as a dict.'''

        nutrients_dict = {
                nutrient: value
                for nutrient, value in zip(nutrients_stencil, self.vector)
                if value != 0
                }

        return {self.name: nutrients_dict}
