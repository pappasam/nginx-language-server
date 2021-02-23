"""Parse JSON files from the data folder."""

import json
import pathlib
import textwrap
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from .utils import wrap_plain_text, wrap_rich_text

ListDicts = List[Dict[str, Any]]


class DirectiveDefinition(BaseModel):
    """Strongly typed directive, from directives.json."""

    name: str
    syntax: List[str]
    default: Optional[str] = Field(alias="def")
    contexts: List[str]
    desc: str
    notes: List[str]
    since: Optional[str]
    module: str
    information: str = ""

    # pylint: disable=no-self-argument
    # pylint: disable=no-self-use
    # pylint: disable=unused-argument

    @validator("information", always=True)
    def get_information(cls, v, values) -> str:
        """Obtain information immediately."""
        result = ""
        if values["default"]:
            result += (
                "```nginx\n"
                + wrap_plain_text(";\n".join(values["default"].split(";")))
                + "\n```\n\n"
            )
        else:
            result += (
                "```nginx\n" + wrap_plain_text(values["name"]) + "\n```\n\n"
            )

        result += wrap_rich_text(values["desc"].strip())
        if values["syntax"]:
            result += "\n\n"
            result += (
                "```nginx\n"
                + textwrap.indent(
                    wrap_plain_text(
                        "\n#--------------------\n".join(values["syntax"])
                    ),
                    "  ",
                )
                + "\n```"
            )
        if values["contexts"]:
            result += "\n"
            result += wrap_plain_text(
                "**Contexts:** `" + ", ".join(values["contexts"]) + "`"
            )
        if values["module"]:
            result += "\n"
            result += wrap_rich_text("**Module:** " + values["module"] + "")
        if values["since"]:
            result += "\n"
            result += wrap_rich_text("**Since:** " + values["since"])
        if values["notes"]:
            result += "\n**Notes:**"
            _notes_wrapped = [wrap_rich_text(note) for note in values["notes"]]
            if len(_notes_wrapped) == 1:
                result += _notes_wrapped[0]
            else:
                result += "\n- " + "\n- ".join(_notes_wrapped)
        return result.replace("“", '"').replace("”", '"').strip()


class VariableDefinition(BaseModel):
    """Strongly typed variable, from variables.json."""

    name: str
    desc: str
    module: str


# nested directive, with context and directive name as keys
DirectiveDefinitionLookup = Dict[str, Dict[str, DirectiveDefinition]]
VariableDefinitionLookup = Dict[str, VariableDefinition]


def load_raw_data(basename: str) -> ListDicts:
    """Pull in raw JSON data from directives file."""
    path_data = pathlib.Path(__file__).parent.parent.joinpath("data")
    with path_data.joinpath(basename).open() as outfile:
        data_raw = json.load(outfile)
    return data_raw


def get_directives(
    directives: ListDicts,
) -> DirectiveDefinitionLookup:
    """Translate raw JSON directives into cleaned output."""
    output = {}
    for directive in directives:
        for context in directive["contexts"]:
            new_context = {directive["name"]: DirectiveDefinition(**directive)}
            if context not in output:
                output[context] = new_context
            else:
                output[context].update(new_context)
    return output


def get_variables(variables: ListDicts) -> VariableDefinitionLookup:
    """Translate raw JSON data into cleaned output."""
    output = {}
    for variable_raw in variables:
        variable = VariableDefinition(**variable_raw)
        output[variable.name] = variable
    return output


DIRECTIVES = get_directives(load_raw_data("directives.json"))
VARIABLES = get_variables(load_raw_data("variables.json"))
