"""The main module."""

import os
from tempfile import NamedTemporaryFile
from typing import Dict, List, Optional, Tuple, TypedDict

import crossplane


class Parsed(TypedDict):
    """Expected dictionary."""

    args: List[str]
    directive: str
    line: int
    contexts: List[str]


def _convert(
    loaded: Dict[int, Parsed],
    list_dicts: List[dict],
    contexts: List[str],
) -> None:
    for my_dict in list_dicts:
        my_dict["line"] -= 1
        loaded[my_dict["line"]] = my_dict
        my_dict["contexts"] = contexts
        if "block" in my_dict:
            new_contexts = contexts + [my_dict["directive"]]
            _convert(loaded, my_dict["block"], new_contexts)


def convert(code: str) -> Dict[int, Parsed]:
    try:
        with NamedTemporaryFile(mode="w", delete=False) as nginx:
            nginx.write(code)
        parsed = crossplane.parse(nginx.name)["config"][0]["parsed"]
        result: Dict[int, Parsed] = {}
        _convert(result, parsed, [])
        return result
    finally:
        os.remove(nginx.name)


def find(d: Dict[int, Parsed], start: int) -> Optional[Parsed]:
    for i in range(50):
        if (start - i) in d:
            return d[start - i]
    return None
