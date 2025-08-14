import re

from typing import Dict


def clean_str(s: str, replacers: Dict[str, str] | None = None) -> str:
    if not replacers:
        replacers = {"(list)": "", " ": ""}

    for k, v in replacers.items():
        s = s.replace(k, v)

    s = re.sub(r'[\\/:"*?<>|]+', "_", s)
    return s



