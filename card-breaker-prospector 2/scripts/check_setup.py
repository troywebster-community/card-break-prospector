#!/usr/bin/env python3
"""Check repository completeness before a Claude Code research run."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
NEEDED = [
    'CLAUDE.md', 'PROSPECTING_PROMPT.md', 'README.md',
    '.claude/skills/prospect-breakers/SKILL.md',
    '.claude/agents/discovery-researcher.md',
    '.claude/agents/evidence-auditor.md',
    'docs/research-playbook.md', 'docs/data-dictionary.md',
    'docs/scoring.md', 'docs/record-schema-example.json',
    'scripts/build_prospects.py', 'tests/test_pipeline.py',
]
missing = [name for name in NEEDED if not (ROOT / name).is_file()]
for name in NEEDED:
    print(f'{"MISSING" if name in missing else "OK     "}  {name}')
if missing:
    print('\nUpload fix: use git push instead of browser drag-and-drop. See README.md.')
    print('Fallback: paste PROSPECTING_PROMPT.md into Claude Code.')
    sys.exit(1)
print('\nProject files complete. Separately check that Claude Code has web/search access.')
