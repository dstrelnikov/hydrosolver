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


def load_db(database_dict):
    compositions = {
            name: load({name: nutrients})
            for name, nutrients in database_dict.items()
            }

    return compositions

def load(composition_dict):
    '''Load composition from a dict.'''

    composition = Composition()
    composition.name, nutrients_dict = composition_dict.popitem()
    composition.macronutrients = list(nutrients_dict['macronutrients'].values())
    composition.micronutrients = list(nutrients_dict['micronutrients'].values())

    return composition

class Composition:

    def __init__(
            self,
            macronutrients=np.zeros(len(macronutrients_desc)),
            micronutrients=np.zeros(len(micronutrients_desc)),
            name='',
            ):
        self.name = name
        self.macronutrients = np.array(macronutrients)
        self.micronutrients = np.array(micronutrients)

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

    @property
    def vector(self):
        '''All the nutrients as a vector (for optimization).'''
        return np.concatenate((self.macronutrients, self.micronutrients))

    def dump(self):
        '''Represent composition as a dict.'''

        macronutrients_dict = {
                nutrient: float(amount)
                for nutrient, amount
                in zip(macronutrients_desc, self.macronutrients)
                }
        micronutrients_dict = {
                nutrient: float(amount)
                for nutrient, amount
                in zip(micronutrients_desc, self.micronutrients)
                }
        composition_dict = {
                self.name: {
                    'macronutrients': macronutrients_dict,
                    'micronutrients': micronutrients_dict,
                    }
                }

        return composition_dict
