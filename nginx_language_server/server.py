"""Nginx Language Server.

Creates the language server constant and wraps "features" with it.

Official language server spec:
    https://microsoft.github.io/language-server-protocol/specification
"""

import itertools
from typing import List, Optional, Union

from pygls.features import COMPLETION
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
        for directive in possibilities
    ]
    return (
        CompletionList(is_incomplete=False, items=completion_items)
        if completion_items
        else None
    )
