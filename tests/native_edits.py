"""Isolated native model edits and explicit single-site source mutations for tests."""
from tools.boat_analysis.model.runtime import connection


def edit_sources(sources, configure):
    """Return edited source snapshots; never write the checked-out model."""
    sources = tuple(sources)
    model = connection().parse_sources(sources, strict=True)
    editor = model.edit()
    configure(editor)
    result = editor.apply()
    rewritten = {document.name: document.content for document in result.documents}
    if not rewritten:
        if len(sources) != 1:
            raise AssertionError("Native edit returned no document identities")
        rewritten = {sources[0][0]: result.content}
    assert set(rewritten) <= {path for path, _ in sources}
    changed = tuple((path, rewritten.get(path, text)) for path, text in sources)
    assert changed != sources, "Negative control must alter its intended model"
    return changed


def set_values(sources, bindings):
    def configure(editor):
        for target, expression in bindings.items():
            editor.set_value(target, expression)
    return edit_sources(sources, configure)


def delete_symbols(sources, *identities):
    def configure(editor):
        for identity in identities:
            editor.delete(identity)
    return edit_sources(sources, configure)


def replace_unique(sources, old, new):
    """Retain narrow expression controls that have exactly one authored site."""
    sources = tuple(sources)
    assert old != new
    assert sum(text.count(old) for _, text in sources) == 1
    return tuple((path, text.replace(old, new)) for path, text in sources)
