#!/usr/bin/env python3
"""Read a layered wiki (ADR-000) and write a 2D swimlane view of its graph as one HTML file.

Usage: python3 tools/wiki_graph.py <wiki-dir> [<out.html>]
"""

import json
import re
import sys
from pathlib import Path

# The kind of a node page sets its layer (ADR-000, Layers).
LAYERS = {
    "entity": 0, "concept": 0, "role": 0, "rule": 0,
    "persona": 1,
    "use-case": 2, "port": 2,
    "adapter": 3, "endpoint": 3, "command": 3, "ui": 3, "event": 3, "config": 3,
    "driver": 4,
}

# The front matter fields that hold the members of each edge kind.
EDGE_FIELDS = {
    "requirement": ("actors", "domain", "use_cases"),
    "scenario": ("actors", "domain", "use_cases"),
    "decision": ("application", "adapters", "drivers"),
}

LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")
TEMPLATE = Path(__file__).with_name("graph_template.html")


def parse_front_matter(text):
    """Return (fields, body). Supports scalars, [a, b] lists and '- item' lists."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fields, key = {}, None
    for line in text[4:end].splitlines():
        if line.lstrip().startswith("- ") and key:
            fields[key].append(line.lstrip()[2:].strip().strip("\"'"))
            continue
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        if value.startswith("[") and value.endswith("]"):
            fields[key] = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        elif value == "":
            fields[key] = []
        else:
            fields[key] = value.strip("\"'")
    return fields, text[end + 4:]


def page_id(path, root):
    return path.relative_to(root).with_suffix("").as_posix()


def resolve(source, target, root):
    """Return the page id of a relative link, or None if it leaves the wiki."""
    path = (source.parent / target).resolve()
    try:
        return page_id(path, root)
    except ValueError:
        return None


def build_graph(root):
    root = root.resolve()
    pages, problems = {}, []
    for path in sorted(root.rglob("*.md")):
        fields, body = parse_front_matter(path.read_text(encoding="utf-8"))
        kind = fields.get("kind")
        if kind not in LAYERS and kind not in EDGE_FIELDS:
            if path.name != "index.md":
                problems.append(f"{page_id(path, root)}: unknown kind {kind!r}")
            continue
        title = next((l[2:].strip() for l in body.splitlines() if l.startswith("# ")), path.stem)
        pages[page_id(path, root)] = (path, fields, body, title)

    # Nodes go into the horizontal lanes of their layers, with their structural links.
    # Edges become vertical lanes across the layers of their members.
    nodes, edges, links = [], [], []
    for pid, (path, fields, body, title) in pages.items():
        kind = fields["kind"]
        page = {"id": pid, "title": title, "kind": kind,
                "module": fields.get("module", ""), "status": fields.get("status", "")}
        if kind in EDGE_FIELDS:
            members = [resolve(path, t, root) for f in EDGE_FIELDS[kind] for t in fields.get(f, [])]
            problems += [f"{pid}: member page {m} is missing" for m in members if m not in pages]
            page["memberIds"] = [m for m in members if m in pages and pages[m][1]["kind"] in LAYERS]
            edges.append(page)
            continue
        page["layer"] = LAYERS[kind]
        for t in dict.fromkeys(LINK.findall(body)):
            target = resolve(path, t, root)
            if target not in pages:
                problems.append(f"{pid}: link {t} is missing")
                continue
            target_kind = pages[target][1]["kind"]
            # A node never links to an edge (ADR-000, Links).
            if target_kind in EDGE_FIELDS:
                problems.append(f"{pid}: link to the edge {target} is not permitted")
                continue
            # A node links only to its layer or to a lower layer (L3).
            violation = LAYERS[target_kind] > LAYERS[kind]
            if violation:
                problems.append(f"{pid}: link to {target} breaks the layer rule")
            links.append({"source": pid, "target": target, "violation": violation})
        nodes.append(page)
    return {"nodes": nodes, "edges": edges, "links": links, "problems": problems}


def main(argv):
    if len(argv) not in (2, 3):
        sys.exit(__doc__)
    graph = build_graph(Path(argv[1]))
    out = Path(argv[2] if len(argv) == 3 else "build/wiki-graph.html")
    data = json.dumps(graph, ensure_ascii=False).replace("</", "<\\/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(TEMPLATE.read_text(encoding="utf-8").replace("__GRAPH_DATA__", data), encoding="utf-8")
    print(f"{len(graph['nodes'])} nodes, {len(graph['edges'])} edges, {len(graph['links'])} links -> {out}")
    for problem in graph["problems"]:
        print(f"  problem: {problem}")


if __name__ == "__main__":
    main(sys.argv)
