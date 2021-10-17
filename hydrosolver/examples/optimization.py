import numpy as np

from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver.optimization import optimize
from hydrosolver.database import pure, compo, chelates, howard_resh
from hydrosolver import utils


composition_target = howard_resh['Resh composition for peppers']

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
    )

solution_optimal = optimize(solution_init, composition_target)
