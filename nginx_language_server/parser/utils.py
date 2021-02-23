"""General utility functions."""

import textwrap

from .parser import DirectiveDefinition


def _wrap(instr: str) -> str:
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


def _wrap_plain_text(instr: str) -> str:
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


def full_information(
    directive: DirectiveDefinition, include_name: bool = True
) -> str:
    """Get complete information from a directive's docs."""
    result = directive.desc.strip()
    if include_name:
        result = _wrap(
            "**" + directive.name + "** " + result[0].lower() + result[1:]
        )
    if directive.default:
        result += "\n\n"
        result += (
            "**Default:**\n```nginx\n"
            + textwrap.indent(
                _wrap_plain_text(";\n".join(directive.default.split(";"))),
                "  ",
            )
            + "\n```"
        )
    if directive.syntax:
        result += "\n\n"
        result += (
            "**Syntax:**\n```text\n"
            + textwrap.indent(
                _wrap_plain_text("\n=-=-=-=-=-=\n".join(directive.syntax)),
                "  ",
            )
            + "\n```"
        )
    if directive.contexts:
        result += "\n"
        result += _wrap_plain_text(
            "**Contexts:** `" + ", ".join(directive.contexts) + "`"
        )
    if directive.module:
        result += "\n"
        result += _wrap("**Module:** " + directive.module + "")
    if directive.since:
        result += "\n"
        result += _wrap("**Since:** " + directive.since)
    if directive.notes:
        result += "\n**Notes:**"
        _notes_wrapped = [_wrap(note) for note in directive.notes]
        if len(_notes_wrapped) == 1:
            result += _notes_wrapped[0]
        else:
            result += "\n- " + "\n- ".join(_notes_wrapped)
    return result.replace("“", '"').replace("”", '"').strip()
