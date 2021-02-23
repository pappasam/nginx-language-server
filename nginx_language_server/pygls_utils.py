"""Utilities to work with pygls.

Helper functions that simplify working with pygls
"""


import functools
import re
from typing import Optional

from pygls.types import Position, Range
from pygls.workspace import Document, position_from_utf16

_SENTINEL = object()

RE_END_WORD = re.compile(r'^[A-Za-z_0-9$\-]*')
RE_START_WORD = re.compile(r"[A-Za-z_0-9$\-]*$")


def rgetattr(obj: object, attr: str, default: object = None) -> object:
    """Get nested attributes, recursively.

    Usage:
        >> repr(my_object)
            Object(hello=Object(world=2))
        >> rgetattr(my_object, "hello.world")
            2
        >> rgetattr(my_object, "hello.world.space")
            None
        >> rgetattr(my_object, "hello.world.space", 20)
            20
    """
    result = _rgetattr(obj, attr)
    return default if result is _SENTINEL else result


def _rgetattr(obj: object, attr: str) -> object:
    """Get nested attributes, recursively."""

    def _getattr(obj, attr):
        return getattr(obj, attr, _SENTINEL)

    return functools.reduce(_getattr, [obj] + attr.split("."))  # type: ignore


def char_before_cursor(
    document: Document, position: Position, default=""
) -> str:
    """Get the character directly before the cursor."""
    try:
        return document.lines[position.line][position.character - 1]
    except IndexError:
        return default


def char_after_cursor(
    document: Document, position: Position, default=""
) -> str:
    """Get the character directly before the cursor."""
    try:
        return document.lines[position.line][position.character]
    except IndexError:
        return default


def word_at_position(document: Document, position: Position) -> str:
    """Get the word under the cursor returning the start and end positions."""
    lines = document.lines
    if position.line >= len(lines):
        return ""

    row, col = position_from_utf16(lines, position)
    line = lines[row]
    # Split word in two
    start = line[:col]
    end = line[col:]

    # Take end of start and start of end to find word
    # These are guaranteed to match, even if they match the empty string
    m_start = RE_START_WORD.findall(start)
    m_end = RE_END_WORD.findall(end)

    return m_start[0] + m_end[-1]


def current_word_range(
    document: Document, position: Position
) -> Optional[Range]:
    """Get the range of the word under the cursor."""
    word = word_at_position(document, position)
    word_len = len(word)
    line: str = document.lines[position.line]
    start = 0
    for _ in range(1000):  # prevent infinite hanging in case we hit edge case
        begin = line.find(word, start)
        if begin == -1:
            return None
        end = begin + word_len
        if begin <= position.character <= end:
            return Range(
                start=Position(line=position.line, character=begin),
                end=Position(line=position.line, character=end),
            )
        start = end
    return None
