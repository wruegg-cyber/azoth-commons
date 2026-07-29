# Repository and Worktree Recovery Status

Snapshot: 2026-07-29

This is a preservation checkpoint, not a claim that every private workshop file
is publication-ready.

## Confirmed on GitHub

- `will-codeing`: the active `prism-sensorium-build` commits are pushed.
- `azoth-prism`: deterministic band rows are pushed on a draft pull request.
- `azoth-voice`: the standalone private repository is created and its clean
  `main` branch is pushed.
- `east-texas-historical-os`: Hallsville, architecture, and historical intake
  work are pushed as a three-pull-request stack.
- `azoth-commons`: repository standards are on `main`; the portfolio ledger is
  proposed on a review branch.

The configured GitHub connector can currently enumerate all five repositories.
This proves reachability only; least-privilege write/read roles still need to be
checked against the intended human or service identity.

## Clean local worktrees

- PRISM band-row branch
- Voice `main`
- all three Historical OS worktrees

## Unresolved private workshop state

At this snapshot, `will-codeing` still has **88 uncommitted entries**: **11
tracked modifications** and **77 untracked paths**. They remain on disk and were
not cleaned or bulk-staged. Some are meaningful source/evidence; others are
virtual environments, caches, generated output, machine-local state, or large
capture material.

Therefore the honest verdict is: the known repositories and committed project
records are backed up, but the private workshop recovery is **not complete**.
Each remaining entry must be classified before it can be committed, extracted,
ignored, archived, or deliberately discarded.

## Cross-chat recovery ledger

### PRISM / Sensorium build chat — covered

Audit source task: `019f9f02-7c0f-75c0-80a5-ce7d9aabc21b`  
Disposition: covered by pushed workshop history and standalone extraction.

- `0fe263f5`: Vision Physics research, GPT brief, Sensorium, and direction
  records.
- `9f0b5e7e`: PRISM-R2/R3 packets.
- `a227fcd8`: owner PRISM lens specification plus PRISM-02/03 and ORP-E4
  packets.
- `16b1e5ea`: 13 PRISM-R2 tests.
- `6f685920`: tracked `SESSION_HANDOFF_PRISM_SENSORIUM.md`, which supersedes
  the original 93-line attached handoff with corrections and expansion rather
  than deleting its substance.

All five commits are ancestors of the pushed `origin/prism-sensorium-build`
branch. The only workshop files from that chat still untracked are:

- `src/v8/prism/bands.py` — SHA-256
  `799290ef5e0c9cdd08dff915b8b986dcb4a3d3cbaa9e5e0c3f5316b281f41300`
- `tests/test_prism_bands.py` — SHA-256
  `18299cea09256fe613a2aa96e71538064b3ea75b35575f7bfd66db58f344d963`

Both are preserved on the pushed `azoth-prism` branch
`codex/prism-band-rows` at `1c34704`. Its changes are limited to standalone
package/import paths, direct-script documentation, and repository integration.
Keep the two original workshop copies until the PRISM pull request is reviewed
and consolidation is explicitly closed.

### Repository, History, Hallsville, and Voice chat — covered

The documents and implementation discussed in the organizing/History chat have
stable Git destinations:

- Historical vision and Genesis: `000_Vision_and_Constitution.md` and
  `001_Project_Genesis.md` in `east-texas-historical-os`.
- Complete GPT handoff:
  `docs/handoffs/East_Texas_Historical_OS_Complete_Handoff_v1.md`.
- The later architecture packet, including the History Engine, canonical
  status, facade, Observer Beta, and Hive specification sources: the preserved
  `docs/handoffs/2026-07-28-architecture-stabilization/source/` manifest at
  pushed commit `9fe4d5a`.
- Hallsville public-data compiler, map viewer, Godot walking client, collision,
  topography, minimap, street-scale tuning, and validation records: pushed
  commit `9b2bf2d` and draft PR 3.
- Stabilized Historical OS contracts and architecture: pushed commit `9fe4d5a`
  and draft PR 4.
- Bounded Hallsville historical intake lab: pushed commit `26e7b5e` and draft
  PR 5.
- Voice reader and Phase 1 synth in the private workshop: pushed commits
  `9cc521ac`, `0198f7ec`, and `0148dd90`.
- Standalone Voice repository: pushed `azoth-voice` commit `27709ee`, with
  provenance, clean-install dependencies, and deterministic tests.
- Portfolio decomposition and dependency queue: this `azoth-commons` review
  branch.

The Historical RPG remains intentionally inside the History repository as a
prototype. The ledger requires a separate distributable repository only after
the compiled-world and runtime/save contracts stabilize.

## Recovery rule

Never use a blanket add or cleanup command in the private workshop. For each
group:

1. identify the owning project lane;
2. separate source from generated or machine-local data;
3. scan source and history for secrets and rights problems;
4. commit to the private workshop or copy through a reviewed extraction
   allowlist;
5. prove the destination from a clean clone;
6. update `PROJECT_PORTFOLIO.json` and this checkpoint.
