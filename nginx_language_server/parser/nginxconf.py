"""The main module."""

import os
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List, NamedTuple, Optional

import crossplane


class ParsedSymbol(NamedTuple):
    """Expected dictionary."""

    args: List[str]
    directive: str
    line: int
    contexts: List[str]


ParsedSymbols = Dict[int, ParsedSymbol]


def _convert(
    parsed_symbols: ParsedSymbols,
    list_dicts: List[Dict[str, Any]],
    contexts: List[str],
) -> None:
    """Load the first arg using data from the second and third args."""
    for my_dict in list_dicts:
        line_number = my_dict["line"] - 1
        parsed_symbols[line_number] = ParsedSymbol(
            args=my_dict["args"],
            directive=my_dict["directive"],
            line=line_number,
            contexts=contexts,
        )
        if "block" in my_dict:
            new_contexts = contexts + [my_dict["directive"]]
            _convert(parsed_symbols, my_dict["block"], new_contexts)


def convert(code: str) -> ParsedSymbols:
    """Load and parse symbols into a container for future processing."""
    try:
        with NamedTemporaryFile(mode="w", delete=False) as nginx:
            nginx.write(code)
        parsed = crossplane.parse(nginx.name)["config"][0]["parsed"]
        result: ParsedSymbols = {}
        _convert(result, parsed, [])
        return result
    finally:
        os.remove(nginx.name)


def find(parsed_symbols: ParsedSymbols, start: int) -> Optional[ParsedSymbol]:
    """Find a symbol starting at a line number and searching backwards."""
    for i in range(50):
        if start - i in parsed_symbols:
            return parsed_symbols[start - i]
    return None
