"""Parse directives data."""

import json
import pathlib
from typing import Any, Dict, List, NamedTuple, Optional

RawDirectiveDefinition = List[Dict[str, Any]]


class DirectiveDefinition(NamedTuple):
    """Strongly typed directive, from directives.json."""

    name: str
    syntax: List[str]
    default: Optional[str]
    contexts: List[str]
    desc: str
    notes: List[str]
    since: Optional[str]
    module: str

    @classmethod
    def from_dict(cls, invalue: Dict[str, Any]) -> "DirectiveDefinition":
        """Construct a directive definition from a dictionary."""
        return cls(
            name=invalue["name"],
            syntax=invalue["syntax"],
            default=invalue["def"],
            contexts=invalue["contexts"],
            desc=invalue["desc"],
            notes=invalue["notes"],
            since=invalue["since"],
            module=invalue["module"],
        )


# nested directive, with context and directive name as keys
DirectiveDefinitionLookup = Dict[str, Dict[str, DirectiveDefinition]]


def load_raw_directives() -> RawDirectiveDefinition:
    """Pull in raw JSON data from directives file."""
    path_data = pathlib.Path(__file__).parent.parent.joinpath("data")
    with path_data.joinpath("directives.json").open() as outfile:
        directives = json.load(outfile)
    return directives


def get_directives(
    directives: RawDirectiveDefinition,
) -> DirectiveDefinitionLookup:
    """Translate raw JSON directives into cleaned output."""
    output = {}
    for directive in directives:
        for context in directive["contexts"]:
            new_context = {
                directive["name"]: DirectiveDefinition.from_dict(directive)
            }
            if context not in output:
                output[context] = new_context
            else:
                output[context].update(new_context)
    return output


DIRECTIVES = get_directives(load_raw_directives())
