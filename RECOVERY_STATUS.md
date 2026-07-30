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

The ChatGPT Codex Connector is intentionally installed with **All repositories**
access. The owner confirmed that it is the shared collaboration and handoff path
for GPT, Codex, and the project family, so cross-project read/write access is an
accepted operational tradeoff rather than an unresolved least-privilege defect.
Repository visibility, rights, secret hygiene, scoped branches, pull-request
review, and non-destructive worktree rules remain unchanged.

## Clean local worktrees

- PRISM band-row branch
- Voice `main`
- all three Historical OS worktrees

## Private workshop preservation complete; consolidation remains

The live `will-codeing` worktree still has **88 intentionally uncommitted
entries**: **11 tracked modifications** and **77 untracked paths**. They remain
on disk and were not cleaned or bulk-staged. Preservation is now complete even
though consolidation is not:

- **63 source/design/operational entries** were copied into canonical paths on
  the private recovery branch, verified file-for-file, tested, committed, and
  pushed;
- **18 private evidence/capture/sample/test-result entries** were copied to the
  local AZOTH evidence store and verified against a per-file SHA-256 manifest;
- **7 generated/cache/machine-local entries** were copied to a separate local
  forensic snapshot, with full hashes for unique records and structural parity
  plus environment receipts for the reproducible cache/environment trees.

These remain preservation buckets, not publication allowlists. Logs, samples,
device inventories, handoffs, captures, and machine state remain private until
their owner, rights, and repository boundaries are reviewed.

The exact private manifest, source receipt, archive counts, validation results,
and limitations are preserved on `codex/workshop-recovery-ledger` at
`bb8a8c84` (draft PR 3). The source snapshot commit is `5c684b0c`. The manifest
mechanically matches the live status set 88-for-88; the live files themselves
were not moved or staged.

Therefore the honest verdict is: **workshop preservation is complete**. Project
assignment, standalone extraction, rights review, PR review, and eventual
cleanup remain separate work. Keep the live originals until those consolidation
decisions are reviewed; preservation alone does not authorize deletion.

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
  `9cc521ac`, `0198f7ec`, `0148dd90`, `5a637c59`, and `3d86821a`.
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
