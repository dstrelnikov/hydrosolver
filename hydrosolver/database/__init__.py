from importlib.resources import contents, is_resource, path
from ..utils import load_file

for item in contents(__name__):
    if is_resource(__name__, item) and item.endswith('.yaml'):
        with path(__name__, item) as file_path:
            locals()[item[:-5]] = load_file(file_path)
