import os
import re
import yaml

from typing import Dict


def clean_str(s: str, replacers: Dict[str, str] | None = None) -> str:
    """
    util function to clean string
    :param s: the string to clean
    :param replacers: a dict of replacement substrings
    :return: cleaned string
    """
    if not replacers:
        replacers = {"(list)": "", " ": ""}

    for k, v in replacers.items():
        s = s.replace(k, v)

    s = re.sub(r'[\\/:"*?<>|]+', "_", s)
    return s

def load_yaml(path: str) -> dict:
    """
    util function to load yaml file
    :param path: yaml path
    :return: dictionary loaded from yaml file
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def abs_path(file_path: str):
    """
    util function to get absolute path of a file
    :param file_path: path to file
    :return: absolute path of file
    """
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    return os.path.abspath(file_path)