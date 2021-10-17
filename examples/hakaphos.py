from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver.database import pure, compo, chelates
from hydrosolver import utils


solution_basis_2 = Solution.dissolve(
        150,
        Composition(name='RO water'),
        [
            compo['Hakaphos Basis 2'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
            chelates['Fe-EDTA 13.3%'],
            chelates['Zn-EDTA 15%'],
            pure['Boric acid'],
        ],
        [0.154, 0.145, 0.040, 0.004, 0.00017,  0.0002],
    )

solution_basis_3 = Solution.dissolve(
        150,
        Composition(name='RO water'),
        [
            compo['Hakaphos Basis 3'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
            chelates['Fe-EDTA 13.3%'],
            chelates['Zn-EDTA 15%'],
            pure['Boric acid'],
        ],
        [0.154, 0.145, 0.040, 0.004, 0.00017,  0.0002],
    )
