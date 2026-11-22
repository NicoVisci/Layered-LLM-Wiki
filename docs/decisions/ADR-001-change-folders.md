---
kind: decision
status: draft
date: 2026-11-22
module: shared
---

# ADR-001: Changes to the wiki through change folders

## Context

[ADR-000](ADR-000-documentation-model.md) makes the wiki a description of the current
system. Each page states what is true now.

A planned change is not true yet. Before the work starts, the change needs a location
for its reason, for the pages that it will change and for the work. If the agent writes
plans into the wiki, the wiki describes a system that does not exist. If the plans stay
in a chat or in an issue tracker, the agent cannot read them together with the code.

## Decision

A change that touches more than one wiki page uses a change folder. A smaller change
edits the wiki directly in its pull request.

```
docs/changes/<change-name>/
  proposal.md  Why. The personas that need the change. The scope.
  delta.md     The wiki pages to add, change or remove, with the new text.
  tasks.md     The work for each module.
```

Do these steps:

1. Make a branch. Open the change folder on the branch. Write a new decision in the
   wiki with the status `draft`, if the change needs one.
2. Do the work. Put the code and the wiki changes in the same pull request.
3. Before the merge, apply the delta to the wiki, set the new decisions to `current`
   and delete the change folder.

Rules:

- A change folder exists only on its branch. The main branch has no `docs/changes/`
  directory. Thus the wiki on the main branch always describes the merged system.
- A change is complete only when the wiki agrees with the code.
- The review of the pull request is the approval of the inner-layer pages that
  [ADR-000](ADR-000-documentation-model.md) requires.
- A change that touches more than one module has one folder, in the repository that
  contains all the affected modules.
- Write user stories in `proposal.md`. They describe a change, not the current system.

## Consequences

Positive:

- The wiki on the main branch stays true.
- The agent reads the plan together with the code.
- The reviewer sees the reason, the delta and the code in one pull request.
- No archive is necessary. The version control keeps each closed change.

Negative:

- The delta must stay current while the work continues.
- A long change can conflict with direct wiki edits on the main branch.

The check script gets one more rule: the main branch has no `docs/changes/` directory.

## Alternatives considered

- **Always edit the wiki directly.** Rejected for large changes: there is no location
  for the reason and the plan, and the reviewer cannot see the intent.
- **Plans in an issue tracker only.** Rejected: the agent cannot read them together
  with the code. An issue can link to the pull request.
- **Keep closed change folders in an archive directory.** Rejected: the version control
  keeps the history.
- **User stories as wiki pages.** Rejected: a user story describes a change, not the
  current system.
