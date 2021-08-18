from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver import composition
from hydrosolver import utils


pure = utils.load_file('compositions/pure.yaml')
compo = utils.load_file('compositions/compo.yaml')
chelates = utils.load_file('compositions/chelates.yaml')

basis_2 = Solution(
        150,
        Composition(name='RO water'),
        [0.154, 0.145, 0.040, 0.004, 0.00017,  0.0002],
        [
            compo['Hakaphos Basis 2'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
            chelates['Fe-EDTA 13.3%'],
            chelates['Zn-EDTA 15%'],
            pure['Boric acid'],
        ]
    )

basis_3 = Solution(
        150,
        Composition(name='RO water'),
        [0.154, 0.145, 0.040, 0.004, 0.00017,  0.0002],
        [
            compo['Hakaphos Basis 3'],
            pure['Calcium nitrate tetrahydrate'],
            pure['Magnesium sulfate heptahydrate'],
            chelates['Fe-EDTA 13.3%'],
            chelates['Zn-EDTA 15%'],
            pure['Boric acid'],
        ]
    )
