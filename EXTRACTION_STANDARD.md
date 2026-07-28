# Extraction Standard

A project earns its own repository only when:

1. Its purpose makes sense without the Hive desktop or private monorepo.
2. Source, tests, fixtures, and documentation fit an explicit allowlist.
3. It has no undeclared monorepo imports or machine-specific absolute paths.
4. A fresh clone can install and pass focused tests.
5. Assets and dependencies have recorded, compatible rights.
6. The README states what works, what is experimental, and what is excluded.
7. The repository contains a license decision, security policy, contribution guide, dependency manifest, CI, and provenance records.

Extraction copies reviewed files into clean history. It does not publish the private archive's history or bulk-copy an output directory.

Never publish credentials, tokens, local configuration, personal indexes, embeddings, ROMs, BIOS files, commercial game dumps, private media, uncertain-rights samples, logs, caches, model weights, or internal handoffs.
