import numpy as np
import yaml

from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver import composition
from hydrosolver import optimization


with open('compositions.yaml') as db_file:
    db = composition.load_db(yaml.safe_load(db_file))


leafy_greens = Solution(
        10,
        db['Water (Berlin)'],
        [0.0053, 0.0053, 0.00265],
        [
            db['Masterblend 4-18-38 Tomato Formula'],
            db['CAN'],
            db['Magnesium sulfate heptahydrate (Epsom Salt)'],
        ]
        )

frut_bearing = Solution(
        10,
        db['Water (Berlin)'],
        [0.0063, 0.0063, 0.00315],
        [
            db['Masterblend 4-18-38 Tomato Formula'],
            db['CAN'],
            db['Magnesium sulfate heptahydrate (Epsom Salt)'],
        ]
        )

fertilizers = [
        db[name] for name in (
            'Hakaphos Green',
            'Hakaphos Blue',
            'Hakaphos Red',
            'Masterblend 4-18-38 Tomato Formula',
            'CAN',
            'Magnesium sulfate heptahydrate (Epsom Salt)',
            'Aquamarine (fruit and berry)'
            )
]

solution = Solution(
        10,
        db['Water (Berlin)'],
        np.zeros(len(fertilizers)),
        fertilizers,
        )

solution.composition_target = leafy_greens.composition

descent = optimization.gradient_descent(solution, iter_max=150)
