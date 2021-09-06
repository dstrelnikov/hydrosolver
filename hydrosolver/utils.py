import yaml
from .composition import Composition

def load_file(filename):
    with open(filename) as file:
        database_dict = yaml.safe_load(file)

    compositions = {
            name: Composition.from_dict({name: nutrients})
            for name, nutrients in database_dict.items()
            }

    return compositions
