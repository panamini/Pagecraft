#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

WIKI_DIRS = [
    "archive",
    "concepts",
    "design",
    "entities",
    "howto",
    "meta",
    "outputs",
    "product",
    "sources",
    "strategy",
    "tasks",
    "tech",
]


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    shutil.copy2(src, dst)


def system_page(title: str, category: str, body: str) -> str:
    today = date.today().isoformat()
    return f"""---
title: "{title}"
category: {category}
status: current
created: {today}
updated: {today}
---

{body}
"""


def init_vault(target: Path, with_sample: bool) -> None:
    target.mkdir(parents=True, exist_ok=True)

    copy_file(ROOT / "WIKI_SCHEMA.md", target / "WIKI_SCHEMA.md")
    copy_file(ROOT / "llms.txt", target / "llms.txt")
    copy_file(ROOT / "CLAUDE.md", target / "CLAUDE.md")
    copy_file(ROOT / "AGENTS.md", target / "AGENTS.md")
    copy_file(
        ROOT / "skills" / "ingest-wiki" / "SKILL.md",
        target / "skills" / "ingest-wiki" / "SKILL.md",
    )

    (target / "rawinput").mkdir(exist_ok=True)
    (target / "raw" / "assets").mkdir(parents=True, exist_ok=True)
    (target / ".claude-plugin").mkdir(exist_ok=True)

    for name in WIKI_DIRS:
        (target / "wiki" / name).mkdir(parents=True, exist_ok=True)

    write_if_missing(
        target / "wiki" / "hot.md",
        system_page(
            "Hot Cache",
            "overview",
            """# Hot Cache

Active memory cache for agents. Keep this page under 500 words.

## Current Focus
- This vault uses Pagecraft: read `wiki/index.md`, then only the relevant canonical pages.

## Retrieval Map
- Project overview: `wiki/overview.md`
- Canonical page catalog: `wiki/index.md`
- Mutation history: `wiki/log.md`

## Guardrails
- This page is a cache, not canonical truth.
- Update durable pages first; update this page only to keep near-term retrieval cheap.
""",
        ),
    )

    write_if_missing(
        target / "wiki" / "overview.md",
        system_page(
            "Overview",
            "overview",
            """# Overview

This vault was initialized with Pagecraft.

## Current State
Add the durable project summary here after the first ingest or direct update.
""",
        ),
    )

    write_if_missing(
        target / "wiki" / "index.md",
        system_page(
            "Index",
            "overview",
            """# Index

## Retrieval Map
- Active cache: `wiki/hot.md`
- Overview: `wiki/overview.md`
- Log: `wiki/log.md`

## Durable Pages
No durable pages yet.

## Sources
No sources yet.

## Outputs
No outputs yet.
""",
        ),
    )

    write_if_missing(
        target / "wiki" / "log.md",
        system_page(
            "Log",
            "overview",
            f"""# Log

## {date.today().isoformat()}
- Initialized Pagecraft vault structure.
""",
        ),
    )

    write_if_missing(
        target / "rawinput" / "README.md",
        """# rawinput

Drop new source files here, then ask an agent to run the `ingest-wiki` ingest workflow.
""",
    )

    if with_sample:
        write_if_missing(
            target / "rawinput" / "pagecraft-sample.md",
            """# Pagecraft Sample Source

Pagecraft should make wiki retrieval cheap enough that agents check the vault before asking broad context questions.

Key points:
- `wiki/hot.md` is the first active-memory read.
- `wiki/index.md` remains the canonical retrieval map.
- `raw/` is immutable after ingest.
- Durable pages should be updated instead of duplicated.
""",
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize a Pagecraft-compatible wiki vault."
    )
    parser.add_argument("target", help="Target vault directory to create or update.")
    parser.add_argument(
        "--with-sample",
        action="store_true",
        help="Add a small markdown source to rawinput/ for smoke testing.",
    )
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    init_vault(target, args.with_sample)
    print(f"Initialized Pagecraft vault at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
