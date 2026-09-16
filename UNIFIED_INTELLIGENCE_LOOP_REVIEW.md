# Review Notes: Unified Intelligence Loop

Status: reviewer notes on [UNIFIED_INTELLIGENCE_LOOP.md](UNIFIED_INTELLIGENCE_LOOP.md)
Last reviewed: 2026-09-16

These are findings raised in review. They do not modify the brief. The owner decides which, if any, become part of the contract Codex builds against.

## 1. Re-entrancy: the gateway can call itself (blocking)

Sections 4, 5, and 9 combine into a cycle the brief does not close:

```
Claude Code -> Azoth MCP Server -> azoth.intelligence.ask
            -> Intelligence Gateway -> router -> ClaudeCodeAdapter
            -> claude -p ... -> Azoth MCP Server -> azoth.intelligence.ask -> ...
```

Section 9 STEP 8 explicitly permits the router to select Codex or Claude, and Section 19 lists `CLAUDE -> HIVE -> CODEX` and `CODEX -> HIVE -> CLAUDE` as supported patterns. So the router is allowed to route an agent's own delegation back to an agent. Section 20's per-request round and cost caps do not prevent this, because each nested call is a *new* request with a fresh budget.

Recommended contract addition, carried in the Section 12 task record and propagated across every provider call:

- `origin_agent` -- who started the outermost request
- `call_depth` -- incremented on every gateway hop, hard ceiling enforced by the gateway, not the caller
- `ancestry` -- the set of providers already on this call stack
- Router rule: a provider already in `ancestry` is ineligible. An agent may never be routed to itself at any depth.
- Budgets in Section 20 should be *inherited and decremented*, not reissued per call, so a nested chain cannot mint new allowance.

Without this, one delegated question can fan out into an unbounded tree of paid frontier-agent invocations. This is the finding most likely to cause real cost damage, and it should be built in step 3 of Section 26 (gateway contracts), not retrofitted.

## 2. Delegation has overhead; Section 7 needs a floor

Section 7's rule ("before consuming significant model context on a self-contained subproblem, consider delegating") is directionally right but has no threshold, and delegation is not free. Each round trip costs:

- tokens to *write* the context packet
- tokens to *read* the returned brief back into the agent's context
- the cheap model's own tokens
- latency, plus a verification step if the answer is load-bearing

Below roughly a few thousand tokens of expected internal reasoning, the round trip plausibly costs more than it saves and adds a correctness risk, because the delegate cannot see the surrounding code. Suggest the rule carry an explicit floor and an exemption:

- Delegate when the subproblem is self-contained **and** expected internal cost exceeds a configured token threshold.
- Do not delegate work that requires the agent's live cross-file context, which is exactly the capability Section 8 says to preserve.

The threshold should be configurable and, once Section 24 metrics exist, tuned from measured outcomes rather than guessed.

## 3. Build order gaps (Section 26)

Two items in the brief never appear in the build order:

- **Section 12 shared task representation.** Everything else writes into it. It should be step 2 or 3, before the gateway contracts, otherwise Codex and Claude adapters will each invent their own shape, which is the exact outcome Section 12 forbids.
- **Section 23 logging and provenance.** It appears only implicitly at step 19 (provider performance metrics), but Section 24's learned routing can only be computed from logs captured from the very first call. Logging should be step 4 at the latest. Metrics gathered later cannot reconstruct history that was never recorded.

Also worth moving earlier: the re-entrancy guard from finding 1, as part of step 3.

## 4. Section 29 states the Claude constraint asymmetrically

Section 28 correctly warns that OpenAI API billing is separate from the ChatGPT subscription. The symmetric fact for Claude is not stated: driving Claude Code non-interactively (`claude -p`) consumes the owner's Claude allowance and is subject to rate limits, whichever billing path is configured. An automated router that treats the ClaudeCodeAdapter as a cheap fallback can exhaust that allowance without an obvious signal.

Suggest Section 21's budget declaration treat Claude Code and Codex as *scarce metered* providers by default, with the router required to record remaining allowance in the Section 23 log and to degrade gracefully when a provider reports a rate limit rather than retrying blindly.

## 5. Some Section 15/16 machinery may already exist in the agents

Claude Code has native subagent delegation and native context compaction; Codex has its own session and thread management. Section 15 (critic) and Section 16 (compression) partly restate those. This is not an argument against building them -- the Hive versions are shared, cached, and logged across agents, which the native versions are not -- but the repository audit in Section 26 step 1 should explicitly record what is already native, so the Hive layer adds sharing and provenance rather than duplicating a mechanism the agent already applies to itself.

## 6. Section 27's success condition needs a measurable definition

"NO Claude / Codex / GPT required" is the right goal but is not yet a test. Suggest defining the pass condition against the Section 23 log:

- The second NPC task completes with **zero** provider calls logged to Codex, Claude Code, or any external API.
- Functional and visual QA pass at the same thresholds as the first run.
- The capability record, its tests, its example scene, and its known-failure notes all exist in the registry before the second task starts.

Stated that way, the experiment can actually fail, which is what makes it a proof.

## 7. Naming

`azoth.intelligence.ask` and similar dotted names are readable, but MCP tool names are conventionally flatter and namespaced by server. Worth confirming the exact naming the existing Azoth MCP server already uses during the Section 26 step 1 audit and matching it, rather than introducing a second convention.
