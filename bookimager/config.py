import yaml
from functools import lru_cache


@lru_cache
def read_config(path: str = 'config.yaml'):
    """
    Parses config file to get
    the contents
    """
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)


CONFIG = read_config()
