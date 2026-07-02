# CLAUDE.md — Retail Location Intelligence (Idea 210)

**Skill name:** `retail-location-intelligence`
**Tagline:** Scores candidate retail sites using gravity models, trade-area analysis, and demographic/competitive data to recommend optimal store coordinates.
**Cluster:** `business-operations`
**Source idea:** 210
**Current phase:** Full deliverable set scaffolded

## Problem This Skill Solves
Choosing where to open a physical retail point is high-stakes and irreversible. This skill ingests candidate locations plus population density, traffic flow, competitor positions, and urban-planning data, then scores each site against world-renowned location-science frameworks (Huff gravity model, Reilly's Law, Christaller central-place theory, analog method) and outputs a ranked recommendation with trade-area estimates and a risk-aware roadmap.

## Harness Flow Summary
1. **Intake** → `sub-requirements-gatherer` — retail format, target customer, budget, candidate coordinates.
2. **Stakeholder map** → `sub-stakeholder-mapper` — who decides, constraints (lease, zoning).
3. **Trade-area model** → `sub-trade-area-modeler` — catchment, gravity model, demand estimate.
4. **Scoring** → `sub-scoring-engine` — multi-criteria site score vs. frameworks.
5. **Quality review** → `sub-quality-reviewer` — challenge assumptions, data gaps.
6. **Synthesize** → ranked recommendation + roadmap.

## Sub-skills
- `sub-requirements-gatherer.md` — retail/site intake.
- `sub-trade-area-modeler.md` — Huff/Reilly catchment & demand modeling.
- `sub-scoring-engine.md` — multi-criteria weighted site scoring.
- `sub-stakeholder-mapper.md` — decision-makers & constraints.
- `sub-quality-reviewer.md` — devil's-advocate validation.

## Tools Required
WebSearch, WebFetch (census/planning portals), Read, Write, Bash.

## Knowledge Sources
US Census/Eurostat demographics; OpenStreetMap/GIS; CBRE/JLL retail reports; ICSC; academic geomarketing (Huff, Reilly, Christaller, Applebaum analog method); municipal zoning/urban-plan portals.

## Supporting Tools
- `tools/knowledge_updater.py` — crawls geomarketing literature + retail-real-estate reports.

## Active Development Tasks
- [x] Scaffold deliverables
- [ ] Add per-region demographic source table
- [ ] Calibrate Huff distance-decay defaults

## Reference Docs
`PROJECT-detail.md`, `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`, `SECOND-KNOWLEDGE-BRAIN.md`.
