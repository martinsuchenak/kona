"""Kona language server.

Completions and hovers are generated from kona.py's lexicon so the editor can
never advertise a word the compiler does not accept.
"""

from pygls.lsp.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_OPEN,
    CompletionItem,
    CompletionItemKind,
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
    DidOpenTextDocumentParams,
    PublishDiagnosticsParams,
)

try:
    from kona import (
        parse_kona, ACTIONS, TARGETS, MODIFIERS, FORMATS, PARTICLES,
        ASPECT_SUFFIXES, SHORTHAND_TARGET_MAP,
    )
    LEXICON_AVAILABLE = True
except ImportError:  # pragma: no cover - only when kona.py is not alongside
    ACTIONS = TARGETS = MODIFIERS = FORMATS = PARTICLES = {}
    ASPECT_SUFFIXES = SHORTHAND_TARGET_MAP = {}
    parse_kona = None
    LEXICON_AVAILABLE = False

server = LanguageServer("kona-server", "v0.3")

completion_items = []
hover_dict = {}


def add_completion(word, detail, documentation, kind):
    completion_items.append(
        CompletionItem(label=word, detail=detail,
                       documentation=documentation, kind=kind)
    )
    hover_dict.setdefault(word, f"**{detail}**\n\n{documentation}")


# Single-syllable modifiers are BOUND: they only ever occur affixed to a root.
# Offering them as standalone completions would teach a form the parser rejects.
BOUND_PREFIXES = [m for m in MODIFIERS if len(m) == 2]
FREE_MODIFIERS = [m for m in MODIFIERS if len(m) > 2]

for word, info in ACTIONS.items():
    add_completion(word, f"Action: {info['name']}", info["desc"],
                   CompletionItemKind.Function)
    add_completion(word + "na", f"Nominalized noun: {info['name']}",
                   f"The act of {info['name']}. {info['desc']}",
                   CompletionItemKind.Variable)

    # Aspect names come from kona.py, so the LSP cannot disagree with the
    # compiler about what '-sa' means (it is habitual, not prospective).
    for suffix, aspect in ASPECT_SUFFIXES.items():
        add_completion(word + suffix, f"Action [{aspect}]: {info['name']}",
                       info["desc"], CompletionItemKind.Function)

    for pref in BOUND_PREFIXES:
        add_completion(pref + word,
                       f"Action [{MODIFIERS[pref]}]: {info['name']}",
                       info["desc"], CompletionItemKind.Function)

for word, desc in TARGETS.items():
    add_completion(word, f"Target: {desc}", "", CompletionItemKind.Variable)
    # The parser accepts modifier-scoped targets (sunodata = [without-delay] data),
    # so these completions are genuinely parseable.
    for pref in BOUND_PREFIXES:
        add_completion(pref + word, f"Target [{MODIFIERS[pref]}]: {desc}", "",
                       CompletionItemKind.Variable)

for word in FREE_MODIFIERS:
    add_completion(word, f"Modifier: {MODIFIERS[word]}",
                   "Free modifier: may stand as its own word.",
                   CompletionItemKind.Keyword)

for word, desc in FORMATS.items():
    add_completion(word, f"Format: {desc}", "Output format specifier.",
                   CompletionItemKind.EnumMember)

for word, desc in PARTICLES.items():
    add_completion(word, f"Particle: {desc}", "Structural particle.",
                   CompletionItemKind.Keyword)

for alias, root in SHORTHAND_TARGET_MAP.items():
    add_completion("@" + alias, f"Shorthand target: {TARGETS.get(root, root)}",
                   f"Written shorthand for `{root}`.", CompletionItemKind.Variable)


@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams) -> CompletionList:
    """Return syntax completions."""
    return CompletionList(is_incomplete=False, items=completion_items)


@server.feature(TEXT_DOCUMENT_HOVER)
def hover(params: HoverParams):
    """Return documentation for the word under the cursor."""
    document = server.workspace.get_text_document(params.text_document.uri)
    word = document.word_at_position(params.position)
    if not word:
        return None

    if word in hover_dict:
        return Hover(contents=MarkupContent(kind=MarkupKind.Markdown,
                                            value=hover_dict[word]))

    # Decompose an affixed form, mirroring the parser: whole-word lookup first
    # (done above), then prefix stripping only if the remainder is a real root.
    for prefix in sorted(BOUND_PREFIXES, key=len, reverse=True):
        if word.startswith(prefix):
            base = word[len(prefix):]
            for suffix, aspect in list(ASPECT_SUFFIXES.items()) + [("", None)]:
                root = base[:-len(suffix)] if suffix and base.endswith(suffix) else base
                if root in hover_dict and (root in ACTIONS or root in TARGETS):
                    note = f"*modifier `{prefix}` = {MODIFIERS[prefix]}*"
                    if aspect and base.endswith(suffix):
                        note += f"\n\n*aspect `-{suffix}` = {aspect}*"
                    return Hover(contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"{note}\n\n{hover_dict[root]}"))
    return None


def validate_document(ls, uri):
    """Parse the document and publish diagnostics."""
    if parse_kona is None:
        return

    doc = ls.workspace.get_text_document(uri)
    diagnostics = []

    # Each non-empty line is its own utterance, so a syntax error is reported on
    # the line that actually contains it rather than always on line 0.
    for lineno, line in enumerate(doc.source.splitlines()):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            parse_kona(stripped)
        except SyntaxError as e:
            col = _error_column(e, line)
            diagnostics.append(Diagnostic(
                range=Range(start=Position(line=lineno, character=col),
                            end=Position(line=lineno, character=len(line))),
                message=str(e).replace("SyntaxError: ", ""),
                severity=DiagnosticSeverity.Error,
                source="kona",
            ))
        except Exception as e:
            # Never swallow silently: an internal error is a compiler bug and
            # must be visible rather than hidden behind `except Exception: pass`.
            diagnostics.append(Diagnostic(
                range=Range(start=Position(line=lineno, character=0),
                            end=Position(line=lineno, character=len(line))),
                message=f"internal compiler error: {type(e).__name__}: {e}",
                severity=DiagnosticSeverity.Warning,
                source="kona",
            ))

    ls.text_document_publish_diagnostics(
        PublishDiagnosticsParams(uri=uri, diagnostics=diagnostics))


def _error_column(exc, line):
    """Best-effort column from the parser's 'at position N' messages."""
    import re
    m = re.search(r"at position (\d+)", str(exc))
    if m:
        return min(int(m.group(1)), max(len(line) - 1, 0))
    m = re.search(r"unknown word '([^']+)'", str(exc))
    if m:
        idx = line.find(m.group(1))
        if idx >= 0:
            return idx
    return 0


@server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls, params: DidOpenTextDocumentParams):
    validate_document(ls, params.text_document.uri)


@server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    validate_document(ls, params.text_document.uri)


if __name__ == "__main__":
    server.start_io()
