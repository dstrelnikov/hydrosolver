from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver import utils


pure = utils.load_file('compositions/pure.yaml')
masterblend = utils.load_file('compositions/masterblend.yaml')

# https://hydroponicseuro.com/mixing-instructions/

leafy_greens = Solution.dissolve(
        10,
        Composition(name='RO water'),
        [
            masterblend['Masterblend 4-18-38 Tomato Formula'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
        ],
        [0.0053, 0.0053, 0.00265],
    )

frut_bearing = Solution.dissolve(
        10,
        Composition(name='RO water'),
        [
            masterblend['Masterblend 4-18-38 Tomato Formula'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
        ],
        [0.0063, 0.0063, 0.00315],
    )
