"""General utility functions."""

import textwrap


def wrap_rich_text(instr: str) -> str:
    """Wrap a string by intended to be normal text."""
    return "\n".join(
        textwrap.wrap(
            instr,
            width=72,
            replace_whitespace=True,
            fix_sentence_endings=True,
            break_long_words=False,
            tabsize=2,
        )
    ).replace("_", r"\_")


def wrap_plain_text(instr: str) -> str:
    """Wrap a string intended to be plain text and displayed as such."""
    return "\n".join(
        textwrap.wrap(
            instr,
            width=72,
            replace_whitespace=False,
            break_long_words=False,
            tabsize=2,
        )
    )
