# Card Breaker Prospector — Claude Code Project

A reusable research-and-export workflow for finding real card breakers, associating public selling and social profiles, researching business contacts and ranking opportunities for Community.

## Quick start
1. Unzip the project and open a terminal in its directory.
2. Start `claude` (Claude Code with web research/search capability enabled). Claude Code's availability of browsing/search/MCP depends on your setup; configure an authorized browser/search provider if necessary.
3. Prompt: `Run /prospect-breakers. Find 50 active US card breakers, prioritizing Whatnot and Fanatics Live. Research public business emails, cross-check socials, verify dated activity and export CSVs with evidence.`
4. Claude Code should read `CLAUDE.md` and the skill, research into `data/input/*.jsonl`, and run `python3 scripts/build_prospects.py --input data/input --output data/output`.
5. Review `data/output/prospects.csv`, `evidence.csv`, `review_queue.csv` and `run_summary.md`.

## Operational constraints
- This package is a **working research protocol and CSV data-processing tool**, not a magic source of buyer data. It ships with **zero fabricated leads**. Live results require Claude Code to have lawful web research tools configured.
- Emails must be publicly published for business use; `Published` does not prove an email inbox accepts mail.
- CSV files are not outbound campaigns. Review suppression, consent and applicable outreach rules before use.
- Repeat research by running the skill again. Data/input batches are preserved and identical prospects are deduplicated when cross-linked.

## Reusing
- Request `Find 100 new accounts not already in the CSV and review those with no business email`.
- Request `Refresh activity and SMS evidence for A-priority accounts`.
- Request `Audit 20% of all ready records and surface broken source links`.

## Contents
- `CLAUDE.md`: always-on project instructions
- `.claude/skills/prospect-breakers/SKILL.md`: reusable command
- `.claude/agents/`: discovery and QA specialists
- `docs/`: research methods, data dictionary, scoring, compliance, JSON example
- `scripts/build_prospects.py`: offline CSV compilation, validation, deduplication and scoring
- `tests/`: small automated tests
- `data/input/`: place live researched JSONL here
- `data/output/`: generated deliverables
