from pathlib import Path
import yaml
from .composition import Composition


def load_file(file_path):
    if isinstance(file_path, Path):
        with file_path.open() as file:
            database_dict = yaml.safe_load(file)

    elif isinstance(file_path, str): 
        with open(file_path) as file:
            database_dict = yaml.safe_load(file)

    compositions = {
            name: Composition.from_dict({name: nutrients})
            for name, nutrients in database_dict.items()
            }

    return compositions
