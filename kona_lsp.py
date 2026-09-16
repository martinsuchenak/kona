import re
from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    CompletionItem,
    CompletionList,
    CompletionParams,
    Hover,
    HoverParams,
    MarkupContent,
    MarkupKind,
    Diagnostic,
    DiagnosticSeverity,
    Position,
    Range,
    DidChangeTextDocumentParams,
    DidOpenTextDocumentParams
)

try:
    from kona import parse_kona, ACTIONS, TARGETS, MODIFIERS
except ImportError:
    # If the extension launches this without PYTHONPATH, provide fallbacks
    ACTIONS = {}
    TARGETS = {}
    MODIFIERS = {}
    parse_kona = None

server = LanguageServer("kona-server", "v0.1")

# Build dictionaries for completions and hovers
completion_items = []
hover_dict = {}

def add_completion(word, detail, documentation, kind):
    completion_items.append(
        CompletionItem(
            label=word,
            detail=detail,
            documentation=documentation,
            # 3 = Function (Action), 6 = Variable (Target), 14 = Keyword (Modifier)
            kind=kind
        )
    )
    hover_dict[word] = f"**{detail}**\n\n{documentation}"

for word, info in ACTIONS.items():
    if isinstance(info, dict):
        add_completion(word, f"Action: {info['name']}", info['desc'], 3)

for word, desc in TARGETS.items():
    add_completion(word, f"Target: {desc}", "", 6)

for word, desc in MODIFIERS.items():
    add_completion(word, f"Modifier: {desc}", "", 14)


@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams) -> CompletionList:
    """Returns syntax completions."""
    return CompletionList(
        is_incomplete=False,
        items=completion_items
    )


@server.feature(TEXT_DOCUMENT_HOVER)
def hover(params: HoverParams):
    """Returns documentation for the word under the cursor."""
    document = server.workspace.get_text_document(params.text_document.uri)
    word = document.word_at_position(params.position)
    
    # Check if we have a definition for this word
    if word in hover_dict:
        return Hover(
            contents=MarkupContent(
                kind=MarkupKind.Markdown,
                value=hover_dict[word]
            )
        )
    
    # Strip modifiers for lookup (e.g., suyuki -> yuki)
    if word and len(word) > 2:
        for prefix in ["de", "su", "ve", "re", "no", "ni"]:
            if word.startswith(prefix):
                base = word[len(prefix):]
                if base in hover_dict:
                    return Hover(
                        contents=MarkupContent(
                            kind=MarkupKind.Markdown,
                            value=f"*(Modified with '{prefix}')*\n\n" + hover_dict[base]
                        )
                    )

    return None

def validate_document(ls, uri):
    """Parses the document and sends diagnostics (squiggles)."""
    if parse_kona is None:
        return
        
    doc = ls.workspace.get_text_document(uri)
    text = doc.source
    diagnostics = []

    try:
        parse_kona(text)
    except SyntaxError as e:
        # Simple error extraction, normally we'd parse line numbers from exceptions
        # but for Kona it's a single line script mostly.
        diagnostics.append(
            Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=10)
                ),
                message=str(e),
                severity=DiagnosticSeverity.Error
            )
        )
    except Exception:
        pass

    ls.publish_diagnostics(uri, diagnostics)

@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params: DidOpenTextDocumentParams):
    validate_document(ls, params.text_document.uri)

@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    validate_document(ls, params.text_document.uri)

if __name__ == "__main__":
    # Start the server on stdio
    server.start_io()
