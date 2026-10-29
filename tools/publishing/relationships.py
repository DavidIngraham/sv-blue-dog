"""Retain native plain dependencies omitted by OpenSysML's requirement renderer.

Only project edges from the native document query onto already-rendered nodes.
No SysML parsing or authored engineering relationships live in this adapter.
"""
import re


def diagram_nodes(body):
    """Map native node IDs to model identities, including compact-label exports."""
    saved = dict(re.findall(r'^%% source-node (n\d+) ([\w:]+)$', body, re.M))
    packages = dict(re.findall(r'(n\d+)\["`\*«package»\*\s*\*\*([\w:]+)\*\*`"\]', body))
    native = dict(re.findall(r'(n\d+)\("`[^`]*?\*\*([\w:]+) :', body, re.S))
    return packages | native | saved


def basis_links(report):
    section = report.split('## Plain dependency', 1)[-1]
    return [(a.strip(), b.strip()) for a, b in
            re.findall(r'^\| ([\w:]+) \| ([\w:]+) \|', section, re.M)]


def include_basis(diagram, links, labels=None, identities=()):
    labels = (labels or {}) | dict((name, rid) for rid, name in
                  re.findall(r'^\*\*([A-Z]-\d+) (\w+)\*\*', diagram, re.M))
    # Native diagrams omit common namespaces. Resolve their displayed suffixes
    # only against authoritative native identities, including package nodes.
    known=set(identities) | {name for name in labels if '::' in name}
    def canonical(identity):
        if identity in known:
            return identity
        matches=[name for name in known if name.endswith('::'+identity)]
        if len(matches)>1:
            raise ValueError('Ambiguous native diagram identity: '+identity)
        return matches[0] if matches else identity
    def update(match):
        body = match[1]
        found = diagram_nodes(body).items()
        names = {}
        for node, qualified in found:
            qualified = canonical(qualified)
            if not qualified.startswith(('BlueDog::Requirements::', 'BlueDog::Goals::', 'GorgeChallenge::', 'BlueDog::Requirements::Structure::', 'BlueDog::DesignIntent')):
                continue
            name = qualified.rsplit('::', 1)[-1]
            if name in names:
                raise ValueError('Ambiguous requirement name: ' + name)
            names[name] = node
        edges = [f'  {names[a]} -.->|"dependency"| {names[b]}'
                 for a, b in links if a in names and b in names]
        identities = []
        def compact(node):
            node_id, qualified, definition = node[1], canonical(node[2]), node[3]
            requirement_id = labels.get(qualified, labels.get(definition))
            if requirement_id is None:
                return node[0]
            identities.append(f'%% source-node {node_id} {qualified}')
            title = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', definition)
            return f'{node_id}("`*«requirement»*\n**{requirement_id} {title}**`")'
        # Use native IDs/titles instead of repeating long qualified usage/type names.
        # Preserve the model identity for source navigation and graph checks.
        body = re.sub(r'(n\d+)\("`\*«requirement»\*\s*\*\*([\w:]+) : (\w+)\*\*`"\)', compact, body)
        body += '\n' + '\n'.join(identities)
        return '```mermaid\n' + body.rstrip() + '\n' + '\n'.join(edges) + '\n```'
    return re.sub(r'```mermaid\n(.*?)```', update, diagram, flags=re.S)
