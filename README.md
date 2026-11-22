# Layered-LLM-Wiki

A documentation method for software projects. The documentation is a wiki of linked
Markdown pages. An LLM agent does the maintenance. A script examines the links.

- Each node page is in one layer, from the domain (layer 0) to the drivers (layer 4).
- Requirements, scenarios and decisions (ADRs) are edge pages. Each edge page connects
  nodes across layers.
- Requirements stay in the problem space (layers 0 to 2). Decisions stay in the solution
  space (layers 2 to 4). Use cases and ports in layer 2 join the two spaces.

## Contents

| Path | Content |
| --- | --- |
| [docs/decisions/ADR-000-documentation-model.md](docs/decisions/ADR-000-documentation-model.md) | The structure of the wiki: layers, nodes, edges, links and checks. |
| [docs/decisions/ADR-001-change-folders.md](docs/decisions/ADR-001-change-folders.md) | The workflow for changes to the wiki. |
| [examples/sale-service/docs/wiki/](examples/sale-service/docs/wiki/) | An example wiki for a sale service. |
| [tools/wiki_graph.py](tools/wiki_graph.py) | Reads a wiki and writes a view of its graph as one HTML file. |
| [tools/graph_template.html](tools/graph_template.html) | The template of the view. |

## View a wiki

```bash
python3 tools/wiki_graph.py examples/sale-service/docs/wiki build/wiki-graph.html
```

Open `build/wiki-graph.html` in a browser. The script needs Python 3 only. The page
needs no network.

- Each layer is a horizontal lane. The domain is at the bottom.
- Each edge is a vertical lane across the layers of its pages.
- The left panel shows or hides layers and kinds of link.
- The right panel shows or hides the vertical lanes. A click on a title selects the
  edge and shows its pages and links.
