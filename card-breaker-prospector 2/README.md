# Card Breaker Prospector (Claude Code)

Research and export sourced card-breaker prospects for Community. Designed to work with limited access to Whatnot, Fanatics Live and Instagram without fabricating evidence. **No live leads ship in this package.**

## Easiest reliable GitHub upload (Mac terminal)

1. Unzip this archive locally. Open Terminal in the unzipped `card-breaker-prospector` folder (the folder that contains `CLAUDE.md`).
2. Create an **empty private** repository called `card-breaker-prospector` on GitHub; do not initialize it with a README.
3. Run these commands, substituting your GitHub account:

```bash
python3 scripts/check_setup.py
git init
git add -A
git commit -m "Initial card breaker prospecting project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/card-breaker-prospector.git
git push -u origin main
```

Authenticate with GitHub as prompted, or use GitHub Desktop to publish the **local folder** as a private repository. `git add -A` includes `.claude/` and `.gitignore`, whereas GitHub drag-and-drop uploads may omit hidden directories. If you already created a repository with a README or other commits, clone it and copy this project's files into the clone, then commit/push; don't force push blindly.

**Verification in GitHub:** confirm `.claude/skills/prospect-breakers/SKILL.md` and `.claude/agents/` are visible, and `PROSPECTING_PROMPT.md` exists. Run `python3 scripts/check_setup.py` in Claude Code too.

## Start Claude Code

Open your repo in Claude Code and enter:

```text
Read CLAUDE.md. Run python3 scripts/check_setup.py. Then run /prospect-breakers to find 50 active US card breakers, prioritizing Whatnot and Fanatics Live. Use compliant publicly indexed sources when direct platforms are unavailable. Find public business emails with exact URLs, capture promotion/activity evidence, identify SMS signup signals, score and export CSVs. No invented claims; report coverage and limitations.
```

If `/prospect-breakers` does not appear, paste the **entire `PROSPECTING_PROMPT.md`** into Claude Code. The prospecting instructions and scripts still work without a registered slash command. Restart Claude Code from the repository root after updating hidden files.

## Project files

- `CLAUDE.md`: always-on instructions
- `PROSPECTING_PROMPT.md`: fallback that works even when slash commands aren't registered
- `.claude/skills/prospect-breakers/SKILL.md`: `/prospect-breakers` skill
- `.claude/agents/`: discovery researcher and evidence auditor
- `docs/access-and-coverage.md`: fallback research channels and evidence tiers
- `docs/`: data dictionary, scoring, research playbook and compliance
- `scripts/check_setup.py`: detect missing upload files
- `scripts/build_prospects.py`: compile JSONL to validated CSV
- `tests/`: automated tests
- `data/input/`: real researched JSONL records (gitignored)
- `data/output/`: prospects.csv, evidence.csv, review_queue.csv, run_summary.md (gitignored)

## Export and validation

```bash
python3 scripts/build_prospects.py --input data/input --output data/output
python3 -m unittest discover -s tests -v
```

Scoring is a documented **evidence-and-fit score**, not a revenue forecast. Missing audience counts remain unknown. Published business email is not proof of deliverability. Never transmit prospect data to public repositories.
