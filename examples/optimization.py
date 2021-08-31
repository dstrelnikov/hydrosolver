import numpy as np

from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver import composition
from hydrosolver import optimization
from hydrosolver import utils


pure = utils.load_file('compositions/pure.yaml')
compo = utils.load_file('compositions/compo.yaml')
chelates = utils.load_file('compositions/chelates.yaml')
resh = utils.load_file('compositions/howard-resh.yaml')


composition_target = resh['Resh composition for peppers']

compositions = [
        compo['Hakaphos Basis 2'],
        pure['Calcium-ammonium nitrate decahydrate'],
        pure['Magnesium sulfate heptahydrate'],
        chelates['Fe-EDTA 13.3%'],
        chelates['Zn-EDTA 15%'],
        pure['Boric acid'],
    ]

solution_init = Solution.dissolve(
        150,
        Composition(name='RO water'),
        compositions,
        np.zeros(len(compositions)),
    )

solution_optimal, _ = optimization.gradient_descent(
        solution_init,
        composition_target,
    )
