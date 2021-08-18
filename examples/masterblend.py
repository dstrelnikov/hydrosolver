from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver import composition
from hydrosolver import utils


pure = utils.load_file('compositions/pure.yaml')
masterblend = utils.load_file('compositions/masterblend.yaml')


leafy_greens = Solution(
        10,
        Composition(name='RO water'),
        [0.0053, 0.0053, 0.00265],
        [
            masterblend['Masterblend 4-18-38 Tomato Formula'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
        ]
    )

frut_bearing = Solution(
        10,
        Composition(name='RO water'),
        [0.0063, 0.0063, 0.00315],
        [
            masterblend['Masterblend 4-18-38 Tomato Formula'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
        ]
    )
