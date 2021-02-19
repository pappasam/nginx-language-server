"""Parse directives data."""

import json
import pathlib

_path_data = pathlib.Path(__file__).parent.parent.joinpath("data")

with _path_data.joinpath("directives.json").open() as outfile:
    _directives = json.load(outfile)

directives = {}
for _directive in _directives:
    for context in _directive["contexts"]:
        if context not in directives:
            directives[context] = [_directive]
        else:
            directives[context].append(_directive)
