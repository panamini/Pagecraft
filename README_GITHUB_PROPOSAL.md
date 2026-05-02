# Pagecraft

Pagecraft turns a local Markdown vault into active memory for LLM agents.

It gives Codex, Claude Code, and other agents a small, repeatable way to find project context, keep durable knowledge organized, and avoid duplicating pages.

## Why Pagecraft Exists

LLM agents are most useful when they can read the right project facts quickly. Most Markdown vaults are too expensive to scan blindly.

Pagecraft adds a small operating contract:

- `wiki/hot.md` is the short active-memory cache agents read first in an initialized vault.
- `wiki/index.md` is the canonical retrieval map.
- `wiki/log.md` records persistent mutations.
- `rawinput/` is staging for new notes and sources.
- `raw/` is immutable after ingest.
- `CLAUDE.md` remains the canonical write-time contract.

The goal is simple: make the wiki cheap enough that agents use it by default.

## 60-Second Start

```bash
git clone https://github.com/panamini/Pagecraft.git
cd Pagecraft
python3 scripts/init_vault.py /path/to/my-vault
```

Then ask your agent:

```text
Use this vault as memory. Start from llms.txt, then read wiki/hot.md before opening broader wiki pages.
```

## What Agents Should Read

| Agent | First file | Why |
| --- | --- | --- |
| Generic LLM agent | `llms.txt` | Compact discovery map. |
| Codex or AGENTS-aware tool | `AGENTS.md` | Compatibility shim. |
| Claude Code | `CLAUDE.md` | Canonical write-time rules. |

For project context in an initialized vault, the retrieval order is:

`wiki/hot.md` -> `wiki/index.md` -> relevant canonical pages

Agents should not scan the whole vault unless the task needs a deep audit.

## Core Workflows

### Use the wiki as memory

```text
Use this vault as memory. Start from llms.txt and answer using the smallest relevant read set.
```

### Ingest a note

Drop a file into `rawinput/`, then ask:

```text
Use the ingest-wiki skill. Ingest the files in rawinput.
```

The agent should create or reuse source pages, update durable pages, move the raw file into `raw/`, and update `wiki/index.md`, `wiki/log.md`, and `wiki/hot.md`.

## Status

Pagecraft is intentionally small. It is not an Obsidian plugin, vector database, MCP server, or auto-commit system.

It is a portable contract for agent-readable Markdown memory.
