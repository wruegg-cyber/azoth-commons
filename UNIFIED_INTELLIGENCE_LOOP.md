# AZOTH Unified Intelligence Loop

Status: engineering brief for the Codex workflow
Last reviewed: 2026-09-16

Scope: Codex + Claude Code + GPT + Hive.

Integration points below were checked by the owner before this brief was written. Codex App Server can expose persistent Codex threads and tool/approval events. Claude Code can be driven non-interactively with structured JSON output and can consume MCP tools. OpenAI general GPT models are reachable through the Responses API, but API billing is separate from the ChatGPT subscription.

Implementation belongs in the relevant private project repository. This document is the shared contract, not the code.

## Mission

Build one unified intelligence system in which the Hive performs as much work as possible itself, while Codex and Claude Code primarily build, repair, extend, supervise, and teach the infrastructure that makes the Hive increasingly self-sufficient.

Codex and Claude Code must also be able to outsource small reasoning, research, criticism, planning, summarization, and diagnostic tasks to GPT or other models through Azoth rather than consuming their own expensive context unnecessarily.

The objective is not to make three AIs constantly talk to each other.

The objective is:

Hive first, then cheap/local help, then outside specialist help, then Codex/Claude only where their stronger agentic abilities are actually needed.

Every successful task should improve Azoth's permanent capabilities so that similar tasks require less external intelligence next time.

## 1. Core Architecture

Build this topology:

```
                         USER
                           |
                           v
                         AZOTH
                           |
                  TASK ORCHESTRATOR
                           |
                           v
                  CAPABILITY REGISTRY
                           |
             +-------------+-------------+
             |                           |
     CAPABILITY EXISTS             CAPABILITY GAP
             |                           |
             v                           v
          HIVE WORK             INTELLIGENCE GATEWAY
                                         |
                +------------------------+------------------------+
                |                        |                        |
                v                        v                        v
          LOCAL MODELS                  GPT                 FREE MODELS
          / OLLAMA                 OpenAI adapter         Gemini/Groq/etc.
                |                        |                        |
                +------------------------+------------------------+
                                         |
                           only escalate if necessary
                                         |
                          +--------------+--------------+
                          v                             v
                       CODEX                       CLAUDE CODE
                   App Server                    CLI / SDK
                          |                             |
                          +--------------+--------------+
                                         |
                                         v
                              EXISTING AZOTH MCP SERVER
                                         |
                     +-------------------+-------------------+
                     v                   v                   v
                   REPO               HIVE TOOLS          MEMORY
                                                             |
                                         +-------------------+
                                         v
                              EXECUTE / TEST / RENDER
                                         |
                                         v
                              VISUAL + FUNCTIONAL QA
                                         |
                                    FIX / VERIFY
                                         |
                                         v
                              CAPABILITY HARVEST
                                         |
                                         v
                              PERMANENT HIVE SKILL
```

## 2. Preserve the Existing Azoth MCP Server

Do not build another Azoth MCP server.

The current Azoth MCP server remains the universal doorway through which Codex, Claude Code, and other MCP-capable agents can access Hive memory, repo information, registered capabilities, execution tools, Godot tools, visual inspection, tests, research tools, asset tools, provenance, and future music/image/video systems.

The existing MCP server handles `OUTSIDE AGENT -> AZOTH`.

The new Intelligence Gateway handles `AZOTH -> OUTSIDE INTELLIGENCE`.

Together they provide two-way communication.

## 3. Wire Codex in Both Directions

Use Codex App Server as Azoth's primary programmatic Codex connection.

Azoth should be able to create a Codex thread, resume a Codex thread, send a task, receive streamed events, receive an answer, receive diffs, handle approvals, receive errors, cancel a task, and record usage.

Codex should simultaneously retain access to the existing Azoth MCP server:

```
Azoth -> Codex App Server -> Codex
Codex -> Azoth MCP Server -> Hive tools / memory / repo
```

This creates a closed loop. Codex should not have to stuff large amounts of Hive context into its prompt; it should query Azoth for the specific information it needs. That reduces token use.

## 4. Wire Claude Code in Both Directions

Claude Code must become an equal participant in the architecture.

Claude Code supports non-interactive invocation such as `claude -p "task"` and structured output via `claude -p "task" --output-format json`. It can also resume sessions and connect to MCP servers.

Create an Azoth Claude provider adapter around this interface:

```
Azoth -> ClaudeCodeAdapter -> Claude Code CLI / SDK
```

Track: session ID, task, response, tool calls, usage when available, errors, artifacts, files changed, verification status.

Claude Code should also connect to the existing Azoth MCP server, giving `Azoth -> Claude Code` and `Claude Code -> Azoth MCP Server`. Claude should query Hive memory and tools rather than carrying giant duplicated context inside its conversation.

Claude Code supports MCP integration and programmatic print/JSON modes, so this structure should use those supported interfaces rather than UI automation. (Source: Claude Platform Docs.)

## 5. Give Both Codex and Claude Access to Hive Intelligence

Expose the Intelligence Gateway itself through the Azoth MCP server. Create tools conceptually similar to:

```
azoth.intelligence.ask
azoth.intelligence.research
azoth.intelligence.critic
azoth.intelligence.compare
azoth.intelligence.verify
azoth.intelligence.summarize
```

Then, instead of spending another large internal reasoning turn, Claude or Codex calls `azoth.intelligence.ask(...)` and the Hive decides who should answer.

Codex and Claude must not directly own GPT credentials. They ask Azoth. Azoth controls the provider.

## 6. GPT as an Outsourced Intelligence Tool

Implement a GPT provider inside the Intelligence Gateway. Use an OpenAI API adapter for general GPT model calls where API access and budget are configured.

The OpenAI API and the ChatGPT subscription are billed separately, so do not assume ordinary ChatGPT chat allowance can be consumed as a general programmatic GPT backend. (Source: OpenAI Help Center.)

Codex can separately use the owner's ChatGPT-backed Codex access through its supported authentication and session mechanisms. (Source: OpenAI.)

GPT should be used for tasks such as: summarize these logs; compare these two approaches; research this narrow question; criticize this architecture; extract these requirements; write candidate tests; explain this unfamiliar library; inspect an image; identify likely bugs; turn these notes into structured data; propose several alternatives.

Do not automatically send an entire repository to GPT. Send the smallest useful context.

## 7. Claude and Codex Should Outsource Before Burning Context

Give Codex and Claude a permanent working rule:

> Before consuming significant model context on a self-contained subproblem, consider delegating the subproblem through `azoth.intelligence.*`.

Example: Claude is building a Godot world generator and encounters an unfamiliar spherical-navigation problem.

Bad: Claude spends 20,000 tokens researching and reasoning internally.

Better:

```
Claude: "Azoth, research practical Godot spherical navigation options.
         Return concise findings with tradeoffs."

Azoth Gateway:
    local knowledge search
       -> local model
       -> free external model if needed
       -> GPT if justified

Azoth returns: 1,500-token verified technical brief

Claude continues implementation.
```

The same rule applies to Codex.

## 8. Do Not Outsource Everything

Codex and Claude remain valuable specifically because they can maintain agentic continuity across the repo.

They stay responsible for architecture, integration, large refactors, difficult debugging, cross-file reasoning, framework construction, test architecture, capability design, repairing Hive infrastructure, and reviewing dangerous changes.

They delegate bounded subproblems. Do not turn them into message routers that accomplish nothing themselves.

## 9. Hive-First Work Policy

Before asking any external model:

```
STEP 1  Search Hive knowledge.
STEP 2  Search capability registry.
STEP 3  Search failure memory.
STEP 4  Try deterministic tool.
STEP 5  Try local model.
STEP 6  Try free outside intelligence.
STEP 7  Try GPT/API if configured.
STEP 8  Use Codex or Claude for hard unresolved work.
```

This hierarchy should be configurable rather than hardcoded.

## 10. Codex and Claude Are Framework Builders

The long-term job of Codex and Claude is not to personally perform every Hive task forever. Their priority is to build infrastructure so that Azoth can increasingly perform those tasks itself.

For every substantial assignment they should ask:

- Can this become a Hive capability?
- Can this become a deterministic tool?
- Can this become a reusable playbook?
- Can this become a local-model task?
- Can this knowledge be stored?
- Can we add a test so another model never has to rediscover this?
- Can we add an evaluator so Azoth can tell whether this worked?
- Can the Hive perform this next time without Claude or Codex?

## 11. Example Transformation

First request: **Build NPC wandering.**

Initial execution may require Claude or Codex. They research, write code, run Godot, inspect video, repair, and test.

Once working, do not stop. Harvest:

```
capability:     npc.random_wander
tool:           configure_random_wander()
tests:          navigation containment
                destination validity
                idle/walk switching
visual QA:      feet on ground
                facing direction
                reasonable movement
example:        random_wander_demo.tscn
known failures: missing navmesh
                disconnected nav islands
                missing animation state
```

Next request: **Give these 40 villagers wandering behavior.**

The Hive should call the capability itself. Claude and Codex should not be required.

## 12. Shared Task Board

Create one Hive task/job representation that Codex, Claude, and Azoth all understand. A task contains:

```
task_id, goal, requirements, constraints, owner, subtasks,
capabilities required, provider calls, artifacts, tests,
QA status, failures, token/cost budget, provenance, status
```

Do not have separate incompatible task representations for Codex and Claude.

## 13. Context Packets Instead of Giant Prompts

Create a ContextBuilder. Before sending work to Claude, Codex, GPT, or another model, build the minimum context packet, which may contain: goal, relevant files, relevant code excerpts, relevant capability records, known failures, current tests, recent changes, acceptance criteria.

Do not dump the entire Hive memory into every task. This is one of the primary mechanisms for reducing token usage.

## 14. Shared Research Service

Neither Codex nor Claude should repeatedly perform identical research. Create `azoth.research.query()`.

Cache research output with: question, date, sources, claims, confidence, provider, verification, expiration/freshness.

If Claude researches something and verifies it, Codex should later retrieve the Hive research record instead of researching it again.

## 15. Shared Critic Service

Create `azoth.intelligence.critic()`.

```
Codex creates architecture
   -> cheap/local critic
   -> GPT critic if needed
   -> Claude sees only concise criticism
   -> Claude improves architecture
```

Claude and Codex roles may be reversed. This avoids spending two frontier-agent contexts on completely independent full solutions.

## 16. Shared Summarization / Compression

Long logs, discussions, and tool results should be compressed by the Hive before going back into Claude/Codex context. Create `azoth.context.compress()`, but retain the original artifact in storage.

```
10 MB logs
   -> Hive stores original
   -> cheap model extracts relevant failures
   -> Claude receives 2 KB diagnosis packet
```

Never destroy the raw evidence.

## 17. Visual Inspection Loop

Because the Hive, Claude, and Codex can visually inspect outputs, graphical tasks must use a closed loop:

```
BUILD -> RUN -> CAPTURE SCREENSHOT / VIDEO -> HIVE VISUAL QA
   PASS? yes -> continue
         no  -> defect report
                 -> Hive attempts repair
                 -> Claude/Codex only if necessary
```

Codex and Claude should not manually stare at every iteration if the Hive's evaluator can reject obvious failures first.

## 18. Functional QA

```
RUN TESTS -> HIVE DIAGNOSIS
   simple repair? yes -> Hive repairs
                  no  -> escalate
```

Only difficult failures should consume Claude/Codex context.

## 19. Model Collaboration Patterns

Support these patterns:

```
HIVE -> GPT -> HIVE
HIVE -> CLAUDE -> HIVE
HIVE -> CODEX -> HIVE
CODEX -> HIVE -> GPT -> HIVE -> CODEX
CLAUDE -> HIVE -> GPT -> HIVE -> CLAUDE
CODEX -> HIVE -> CLAUDE
CLAUDE -> HIVE -> CODEX
CODEX -> HIVE -> cheap critic -> CODEX
CLAUDE -> HIVE -> local researcher -> CLAUDE
```

Do not build direct uncontrolled `Codex <-> Claude <-> GPT <-> Codex <-> GPT...` chatter.

All delegation goes through Azoth. This preserves budgets, permissions, logging, provenance, context filtering, provider replacement, and privacy policy.

## 20. Prevent Infinite AI Conversations

Every delegated request requires: goal, maximum rounds, maximum context, maximum cost, required output schema, verification requirement, stop condition.

Example:

```
Goal:                  Find likely cause of this shader artifact.
Maximum external calls: 2
Output:                top 3 hypotheses
Stop:                  when one hypothesis is verified by render test
```

Do not permit models to endlessly debate.

## 21. Provider Independence

Core Hive code must never assume that GPT, Claude, Codex, or Gemini always exists. Instead request capabilities:

```
needs:
    reasoning = high
    code = true
    vision = true
budget:
    low
```

The router chooses the currently available provider.

## 22. Credentials

All credentials remain behind provider adapters. Agents receive no API keys, passwords, session cookies, or OAuth secrets.

Claude and Codex invoke Hive tools. The Hive invokes providers.

## 23. Logging and Provenance

For every delegated subtask record: requesting agent, reason for delegation, provider selected, model, context supplied, response, cost/usage, whether the result was used, whether it was verified, artifacts affected, capability learned.

This will eventually allow Azoth to determine which providers are actually worth using.

## 24. Provider Performance Learning

Track results per provider. Illustrative examples only:

```
GPT:          excellent at research synthesis; average at Godot patching
Claude:       excellent at architecture; expensive for repetitive searching
Codex:        excellent at repo modification; scarce allowance
Local model:  excellent cheap summarizer; weak difficult debugging
```

Azoth should calculate its own profiles from actual results. The router should eventually choose models based on empirical success and cost.

## 25. Self-Teaching Loop

```
UNKNOWN TASK
  -> SEARCH SELF
  -> ASK OUTSIDE INTELLIGENCE
  -> IMPLEMENT
  -> TEST
  -> VISUALLY INSPECT
  -> REPAIR
  -> VERIFY
  -> DISTILL WHAT WORKED
  -> CREATE CAPABILITY
  -> ADD TESTS / EXAMPLES / FAILURE NOTES
  -> REGISTER
  -> NEXT TIME: HIVE DOES IT ITSELF
```

This is the central purpose of the system.

## 26. Build Order

1. Audit existing Azoth repo and MCP server.
2. Implement/extend Capability Registry.
3. Implement normalized Intelligence Gateway request/response contracts.
4. Implement provider registry.
5. Implement local-model adapter.
6. Implement Codex App Server adapter.
7. Implement Claude Code adapter using programmatic CLI/SDK behavior.
8. Connect both Codex and Claude to existing Azoth MCP server.
9. Expose Intelligence Gateway operations as Azoth MCP tools.
10. Implement GPT provider adapter.
11. Add free-provider adapters.
12. Implement ContextBuilder.
13. Implement shared research cache.
14. Implement compression/summarization.
15. Implement visual and functional QA.
16. Implement bounded repair loop.
17. Implement Capability Harvest.
18. Implement Failure Memory.
19. Implement provider performance metrics.
20. Implement automatic low-cost routing.

Do not skip the repository audit.

## 27. First Proof of Architecture

Run one controlled experiment. User request: **Create a reusable Godot wandering-NPC system.**

Expected behavior:

```
Azoth searches itself
  -> finds no complete capability
  -> local model makes first plan
  -> Claude Code or Codex takes framework task
  -> agent calls GPT through Azoth for a narrow subproblem if useful
  -> implementation created
  -> Hive launches Godot
  -> Hive captures result
  -> Hive visually inspects
  -> Hive runs functional tests
  -> repair loop
  -> PASS
  -> capability harvested
  -> second NPC task uses capability directly
  -> NO Claude / Codex / GPT required
```

If that works, the core architecture is successful.

## 28. Important OpenAI Constraint

Do not attempt to turn ordinary ChatGPT consumer chat usage into a homemade GPT API.

For programmatic general GPT calls, use the supported OpenAI API provider when configured. ChatGPT and the OpenAI API are billed separately. (Source: OpenAI Help Center.)

For subscription-backed Codex work, use Codex through its supported ChatGPT-authenticated tooling and App Server rather than trying to automate ChatGPT UI conversations. (Source: OpenAI.)

## 29. Important Claude Constraint

Do not attempt to replace Claude Code's underlying model with GPT merely to "outsource." Instead let Claude Code invoke `azoth.intelligence.ask` through the existing Azoth MCP server.

Claude Code officially supports MCP connections and programmatic non-interactive invocation with structured output, which is sufficient for the two-way architecture described here. (Source: Claude Platform Docs.)

## 30. Final Role Assignment

**The Hive** should progressively own: routine research, memory, capability discovery, task decomposition, asset retrieval, test execution, visual inspection, simple repairs, local-model work, provider routing, context compression, knowledge storage, failure memory, capability execution.

**Codex** primarily: repo-wide engineering, framework construction, difficult code repair, integration, refactors, tests, architecture implementation, Hive capability creation.

**Claude Code** primarily: architecture reasoning, independent code review, framework building, difficult implementation, large-context project reasoning, second engineering perspective, Hive capability creation.

**GPT and other models** primarily outsourced: bounded research, criticism, alternative solutions, summarization, analysis, visual interpretation, test ideas, documentation, specialized questions.

The exact roles can change based on empirical performance.

## 31. North-Star Rule

Codex and Claude should spend their limited intelligence building Azoth's machinery, not repeatedly doing work that the machinery should eventually perform itself.

Every major development session should leave behind one or more of: a new capability, a better tool, a better evaluator, a new test, a new playbook, a new failure lesson, better provider routing, better local knowledge.

The long-term success condition is that Codex and Claude become teachers, mechanics, architects, and escalation specialists for the Hive, while the Hive increasingly performs the actual recurring work itself.

The most important addition compared with the earlier plan is the shared MCP intelligence tool: Codex and Claude both get to outsource bounded subproblems through Azoth, while Azoth controls whether that request goes to GPT, a free model, a local model, or somewhere else. That conserves both of their scarce contexts while simultaneously building the Hive's own competence.
