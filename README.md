# AI Content Agent

Autonomous Arabic faceless short-form content engine for **Behind The Number | خلف الرقم**.

## Goal
Research high-potential topics, verify claims, score ideas, generate Arabic short-video content packages, and learn from performance while keeping human approval available before publishing.

## MVP pipeline
1. Topic discovery
2. Viral scoring
3. Research + evidence collection
4. Fact checking
5. Arabic hook + script
6. Voice/visual production hooks
7. Captions + platform metadata
8. Quality gate
9. Telegram approval
10. Publishing adapters
11. Analytics + learning loop

## Safety and quality principles
- No fabricated facts or sources.
- No mass-produced duplicate content.
- Claims require evidence before production.
- AI/synthetic-content disclosure metadata is supported.
- Publishing is disabled by default until platform credentials and approval rules are configured.

## Quick start
```bash
pip install -r requirements.txt
python run.py --demo
```

The demo runs without paid APIs and writes a content package to `data/output/`.
