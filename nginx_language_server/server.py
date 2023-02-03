"""Nginx Language Server.

Creates the language server constant and wraps "features" with it.

Official language server spec:
    https://microsoft.github.io/language-server-protocol/specification
"""

from typing import Optional

from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    CompletionItem,
    CompletionItemKind,
    CompletionList,
    CompletionOptions,
    CompletionParams,
    Hover,
    InsertTextFormat,
    MarkupContent,
    MarkupKind,
    TextDocumentPositionParams,
)
from pygls.server import LanguageServer

from nginx_language_server import __version__, pygls_utils
from nginx_language_server.parser import DIRECTIVES, VARIABLES, nginxconf

# pylint: disable=line-too-long


SERVER = LanguageServer(
    name="nginx-language-server",
    version=__version__,
)


# Server capabilities


@SERVER.feature(
    TEXT_DOCUMENT_COMPLETION,
    CompletionOptions(trigger_characters=["$"]),
)
def completion(
    server: LanguageServer, params: CompletionParams
) -> Optional[CompletionList]:
    """Returns completion items."""
    document = server.workspace.get_document(params.text_document.uri)
    parsed = nginxconf.convert(document.source)
    line = nginxconf.find(parsed, params.position.line)
    if not line:
        return None
    contexts = line.contexts if line.contexts else ["main"]
    last_context = contexts[-1]
    if last_context not in DIRECTIVES:
        return None
    directives = DIRECTIVES[last_context]
    completion_items = [
        CompletionItem(
            label=directive.name,
            filter_text=directive.name,
            detail=directive.ls_detail,
            documentation=MarkupContent(
                kind=MarkupKind.Markdown,
                value=directive.ls_documentation,
            ),
            kind=CompletionItemKind.Property,
            insert_text=directive.name,
            insert_text_format=InsertTextFormat.PlainText,
        )
        for directive in (
            *directives.values(),
            *DIRECTIVES["any"].values(),
            *VARIABLES.values(),
        )
    ]
    return (
        CompletionList(is_incomplete=False, items=completion_items)
        if completion_items
        else None
    )


@SERVER.feature(TEXT_DOCUMENT_HOVER)
def hover(
    server: LanguageServer, params: TextDocumentPositionParams
) -> Optional[Hover]:
    """Support Hover."""
    document = server.workspace.get_document(params.text_document.uri)
    parsed = nginxconf.convert(document.source)
    word = document.word_at_position(params.position)
    line = nginxconf.find(parsed, params.position.line)

    # append "_name" to beginning of word
    word_name = word.rsplit("_", maxsplit=1)[0] + "_name"

    if not line:
        return None
    contexts = line.contexts if line.contexts else ["main"]
    last_context = contexts[-1]
    possible_directives = (
        DIRECTIVES[last_context] if last_context in DIRECTIVES else {}
    )
    if (
        len(contexts) >= 2
        and contexts[-1] == "if"
        and contexts[-2] == "location"
    ):
        possible_directives = {
            **possible_directives,
            **DIRECTIVES["ifinlocation"],
        }
    possibilities = {**possible_directives, **DIRECTIVES["any"], **VARIABLES}
    if word not in possibilities:
        if line.line != params.position.line:
            return None
        if word_name not in possibilities:
            return None
        found = possibilities[word_name]
    else:
        found = possibilities[word]
    contents = MarkupContent(
        kind=MarkupKind.Markdown,
        value=found.ls_documentation,
    )
    _range = pygls_utils.current_word_range(document, params.position)
    return Hover(contents=contents, range=_range)
