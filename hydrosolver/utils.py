import yaml
from .composition import load_compositions

def load_file(filename):
    with open(filename) as file:
        compositions_list = load_compositions(yaml.safe_load(file))

    return compositions_list
