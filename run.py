import numpy as np
import yaml

from hydrosolver.solution import Solution
from hydrosolver.composition import Composition
from hydrosolver import composition
from hydrosolver import optimization


with open('compositions.yaml') as db_file:
    db = composition.load_db(yaml.safe_load(db_file))

fertilizers = [
        db[name] for name in (
            'Hakaphos Green',
            'Hakaphos Blue',
            'Hakaphos Red',
            'CAN',
            'Magnesium sulfate heptahydrate (Epsom Salt)',
            'Aquamarine (fruit and berry)'
            )
]

solution = Solution(
        150,
        np.zeros(len(fertilizers)),
        db['Water (Berlin)'],
        *fertilizers,
        )

solution.composition_target = db['Howard Resh composition (peppers)']
