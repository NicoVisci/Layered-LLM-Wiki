---
kind: decision
status: draft
date: 2026-11-22
module: shared
---

# ADR-000: Documentation as a layered wiki of nodes and edges

## Context

Project documentation often has these problems:

- The same fact has copies in many documents. The copies become different.
- A link between two documents is in many locations. Each change must occur in each
  location.
- When the documentation becomes large, nobody can find the documents that a change
  affects.

The code is the source of truth for behavior. The documentation must record the
information that the code does not have: who needs the system, what must be true, and
why the system is built this way. An LLM agent can do the maintenance of many pages. A
script must be able to examine the result.

## Decision

Keep the documentation as a wiki of linked Markdown pages. Each page records one fact.
Other pages link to that page.

### Layers

Each node page is in one layer. The layer comes from the subject of the page. A lower
layer is more stable.

| Layer | Name | Node kinds |
| --- | --- | --- |
| 0 | Domain | `entity`, `concept`, `role`, `rule` |
| 1 | Actors | `persona` |
| 2 | Application | `use-case`, `port` |
| 3 | Adapters | `adapter`, `endpoint`, `command`, `ui`, `event`, `config` |
| 4 | Drivers | `driver` |

The `kind` sets the layer. A page has no `layer` field.

### Problem space and solution space

- Layers 0, 1 and 2 are the problem space: who needs what from the domain.
- Layers 2, 3 and 4 are the solution space: how the system gives it.
- Layer 2 is the hinge. A use case faces the problem space. A port faces the solution
  space. A link from a use case to a port joins the two spaces.

### Nodes and edges

A node page describes one thing. An edge page connects a group of nodes across layers.
Edge pages are first-class pages.

| Edge kind | Space | Meaning |
| --- | --- | --- |
| `requirement` | Problem | What must be true. |
| `scenario` | Problem | A measurable quality that must be true. |
| `decision` | Solution | Why the system is built this way. |

### Links

**Structural links** are in the body of node pages. They state facts, for example
"A payment belongs to an order". A structural link goes to the same layer or to a lower
layer.

A driver page links to its adapter, but in the code the adapter imports the driver. The
rule is about stability, not about imports. A third-party library changes most often,
so it is in the outer layer.

**Relational links** are in the front matter of edge pages:

| Edge | Can touch | Must touch | Can cite |
| --- | --- | --- | --- |
| `requirement` | Layers 0 and 1, use cases | One or more personas, one or more use cases | Requirements, scenarios |
| `scenario` | Layers 0 and 1, use cases | One or more use cases | Requirements, scenarios |
| `decision` | Use cases, ports, layers 3 and 4 | One or more layer 2 nodes | Requirements, scenarios, decisions |

- A decision can cite a requirement. A requirement never cites a decision. Thus the
  requirements stay independent of the design.
- A scenario does not name a driver. Write "when the payment provider is not
  available", not the name of a product.
- Only a decision links to a decision. A node page does not link to an edge page.
- A backlink is a query result. Do not write backlinks.

### Modules

Each page has a `module` field. Structural links obey the module dependencies of the
code. A page that all modules use has `module: shared`. An edge page can cross modules.

### Page format

- All links are relative Markdown links.
- The file name comes from the title, for example `place-an-order.md`. A decision also
  has an `ADR-nnn` prefix, as a short identifier.
- The status of each page is `draft`, `current` or `retired`.
- Edit each page in place, decisions also. The version control keeps the history.
- Write the statements of a requirement in EARS form: "When `<trigger>`, the `<system>`
  shall `<response>`".
- Write a scenario as a quality attribute scenario: source, stimulus, environment,
  response and response measure. Set its `quality` to an ISO/IEC 25010 characteristic.
- The front matter is the only store of the links of an edge page. The body can link
  to a page only if the front matter has the same page.

| Kind | Front matter fields |
| --- | --- |
| Node | `kind`, `module`, `status` |
| `requirement` | `kind`, `module`, `status`, `actors`, `domain`, `use_cases`, `cites` |
| `scenario` | `kind`, `module`, `status`, `quality`, `actors`, `domain`, `use_cases`, `cites` |
| `decision` | `kind`, `module`, `status`, `date`, `application`, `adapters`, `drivers`, `cites` |

### Directory layout

```
docs/wiki/
  index.md
  domain/        layer 0
  actors/        layer 1
  application/   layer 2
  adapters/      layer 3
  drivers/       layer 4
  requirements/  requirement and scenario edges
  decisions/     decision edges
```

### Maintenance

- Layers 0, 1 and 2 and all edge pages hold intent that the code does not have. The
  agent writes drafts. A person approves each change.
- Layers 3 and 4 repeat the code. The agent keeps them equal to the code.

### Checks

A script reads the links and the front matter of all pages and makes a graph. The
continuous integration runs it.

| Rule | Check |
| --- | --- |
| L1 | Each page has a known `kind` and a known `module`. |
| L2 | Each link goes to a page that exists. |
| L3 | Each structural link goes to the same layer or to a lower layer. |
| L4 | Each structural link obeys the module dependencies. |
| L5 | Each edge touches only the nodes and cites only the edges that its span permits. |
| L6 | Each edge touches the nodes that its span requires. |
| L7 | Only a decision links to a decision. |
| L8 | The body links of an edge page are also in its front matter. |
| L9 | Each use case has a requirement and links to a port. |
| L10 | Each persona has a requirement. |
| L11 | Each driver has a decision. |

An LLM pass also looks for contradictions and for terms that have no domain page. It
reports. It does not change pages.

## Consequences

Positive:

- One fact has one page.
- A script finds broken links, wrong directions, use cases without a requirement and
  drivers without a decision.
- A query on a use case shows what must be true and why the system is built this way.
- A query from a driver shows the personas that a change of the driver can affect.
- A decision is a usual page. It needs no special lifecycle.

Negative:

- Existing documentation must move to the new layout.
- The check script is code. It needs tests and maintenance.
- Front matter queries in an editor, for example Obsidian Dataview, cannot run in the
  continuous integration. They are only for exploration.

A planned change is not true yet, so it cannot be a wiki page.
[ADR-001](ADR-001-change-folders.md) gives the workflow for changes.

## Alternatives considered

- **The document type sets the layer.** Rejected: one requirement document can contain
  a domain rule, a use case and a command.
- **Personas in the domain layer.** Rejected: a persona is an actor, not an entity.
- **Links of edge pages in the body only.** Rejected: a script cannot get the type of a
  body link.
- **Links in the front matter and in the body.** Rejected: the two copies become
  different.
- **Requirements cite decisions.** Rejected: the requirements must stay independent of
  the design.
- **Append-only decisions that only a new decision can replace.** Rejected: this is a
  special lifecycle for one page kind. The version control keeps the history.
- **A typed-link toolchain, for example sphinx-needs.** Rejected for now: a small
  script is sufficient for the rules above.
