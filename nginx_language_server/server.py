"""Nginx Language Server.

Creates the language server constant and wraps "features" with it.

Official language server spec:
    https://microsoft.github.io/language-server-protocol/specification
"""

import itertools
from typing import List, Optional, Union

from pygls.features import COMPLETION, HOVER
from pygls.protocol import LanguageServerProtocol
from pygls.server import LanguageServer
from pygls.types import (
    CodeAction,
    CodeActionKind,
    CodeActionParams,
    SymbolKind,
    CompletionItem,
    CompletionList,
    CompletionParams,
    DidChangeConfigurationParams,
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams,
    DidSaveTextDocumentParams,
    DocumentHighlight,
    DocumentSymbol,
    DocumentSymbolParams,
    Hover,
    InitializeParams,
    InitializeResult,
    InsertTextFormat,
    Location,
    MarkupContent,
    MarkupKind,
    RenameParams,
    SymbolInformation,
    TextDocumentPositionParams,
    WorkspaceEdit,
    WorkspaceSymbolParams,
)

from .parser import nginxconf
from .parser.directives import directives

# pylint: disable=line-too-long


SERVER = LanguageServer()


# Server capabilities


@SERVER.feature(COMPLETION, trigger_characters=[".", "'", '"'])
def completion(
    server: LanguageServer, params: CompletionParams
) -> Optional[CompletionList]:
    """Returns completion items."""
    document = server.workspace.get_document(params.textDocument.uri)
    parsed = nginxconf.convert(document.source)
    line = nginxconf.find(parsed, params.position.line)
    contexts = line["contexts"] if line["contexts"] else ["main"]
    possibilities = directives.get(contexts[-1], [])
    completion_items = [
        CompletionItem(
            label=directive["name"],
            filter_text=directive["name"],
            detail=directive["desc"],
            kind=SymbolKind.Property,
            insert_text=directive["name"],
            insert_text_format=InsertTextFormat.PlainText,
        )
        for directive in possibilities.values()
    ]
    return (
        CompletionList(is_incomplete=False, items=completion_items)
        if completion_items
        else None
    )

# @SERVER.feature(HOVER)
# def hover(
#     server: LanguageServer, params: TextDocumentPositionParams
# ) -> Optional[Hover]:
#     """Support Hover."""
#     document = server.workspace.get_document(params.textDocument.uri)
#     parsed = nginxconf.convert(document.source)
#     line = nginxconf.find(parsed, params.position.line)

#     jedi_script = jedi_utils.script(server.project, document)
#     jedi_lines = jedi_utils.line_column(jedi_script, params.position)
#     for name in jedi_script.help(**jedi_lines):
#         docstring = name.docstring()
#         if not docstring:
#             continue
#         markup_kind = _choose_markup(server)
#         docstring_clean = jedi_utils.convert_docstring(docstring, markup_kind)
#         contents = MarkupContent(kind=markup_kind, value=docstring_clean)
#         document = server.workspace.get_document(params.textDocument.uri)
#         _range = pygls_utils.current_word_range(document, params.position)
#         return Hover(contents=contents, range=_range)
#     return None
