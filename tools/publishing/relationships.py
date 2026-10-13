"""Retain native plain dependencies omitted by OpenSysML's requirement renderer.

Only project edges from the native document query onto already-rendered nodes.
No SysML parsing or authored engineering relationships live in this adapter.
"""
import re


def diagram_nodes(body):
    """Map native node IDs to model identities, including compact-label exports."""
    saved = dict(re.findall(r'^%% source-node (n\d+) ([\w:]+)$', body, re.M))
    packages = dict(re.findall(r'(n\d+)\["`\*«package»\*\s*\*\*([\w:]+)\*\*`"\]', body))
    return packages | (saved or dict(re.findall(r'(n\d+)\("`.*?\*\*([\w:]+) :', body, re.S)))


def basis_links(report):
    section = report.split('## Plain dependency', 1)[-1]
    return [(a.strip(), b.strip()) for a, b in
            re.findall(r'^\| ([\w:]+) \| ([\w:]+) \|', section, re.M)]


def include_basis(diagram, links):
    labels = dict((name, rid) for rid, name in
                  re.findall(r'^\*\*([A-Z]-\d+) (\w+)\*\*', diagram, re.M))
    def update(match):
        body = match[1]
        found = diagram_nodes(body).items()
        names = {}
        for node, qualified in found:
            if not qualified.startswith(('BlueDogRequirements::', 'BlueDog::Goals::', 'GorgeChallenge::', 'BlueDogStructure::', 'BlueDog::DesignIntent')):
                continue
            name = qualified.rsplit('::', 1)[-1]
            if name in names:
                raise ValueError('Ambiguous requirement name: ' + name)
            names[name] = node
        edges = [f'  {names[a]} -.->|"dependency"| {names[b]}'
                 for a, b in links if a in names and b in names]
        identities = []
        def compact(node):
            node_id, qualified, definition = node[1], node[2], node[3]
            if definition not in labels:
                return node[0]
            identities.append(f'%% source-node {node_id} {qualified}')
            title = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', definition)
            return f'{node_id}("`*«requirement»*\n**{labels[definition]} {title}**`")'
        # Use native IDs/titles instead of repeating long qualified usage/type names.
        # Preserve the model identity for source navigation and graph checks.
        body = re.sub(r'(n\d+)\("`\*«requirement»\*\s*\*\*([\w:]+) : (\w+)\*\*`"\)', compact, body)
        body += '\n' + '\n'.join(identities)
        return '```mermaid\n' + body.rstrip() + '\n' + '\n'.join(edges) + '\n```'
    return re.sub(r'```mermaid\n(.*?)```', update, diagram, flags=re.S)
