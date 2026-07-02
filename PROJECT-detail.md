# PROJECT-detail.md — Retail Location Intelligence

## Executive Summary
A harness that evaluates candidate retail locations using established location-science methods and emits a ranked, evidence-based site recommendation with trade-area (catchment) estimates, competitive saturation analysis, and a go/no-go roadmap. Scoring is grounded in named frameworks (Huff probabilistic gravity model, Reilly's Law of Retail Gravitation, Christaller central-place theory, Applebaum analog method) — never ad hoc.

## Problem Statement
Site-selection mistakes are expensive and slow to reverse. SMEs and emerging chains rarely have GIS analysts. They need a structured way to weigh population density, footfall/traffic, accessibility, competitor proximity, co-tenancy, rent, and zoning into a defensible ranking.

## Target Users & Use Cases
- **F&B / retail founder** — "Which of these 3 storefronts should I lease?" → ranked score + trade-area.
- **Franchise development** — "Is this town saturated for our category?" → competitive saturation index.
- **Expansion manager** — "Estimate demand for a 5km catchment here." → Huff-based capture estimate.
- **Investor** — "Stress-test this site's assumptions." → quality-reviewer challenge.
- **Pop-up planner** — "Best high-footfall coordinate for a weekend?" → traffic-weighted score.

## Harness Architecture
```
/retail-location-intelligence
  Stage 1 Intake          → sub-requirements-gatherer  → retail+site profile
  Stage 2 Stakeholders    → sub-stakeholder-mapper      → decision/constraint map
  Stage 3 Trade area      → sub-trade-area-modeler      → catchment + demand
  Stage 4 Scoring         → sub-scoring-engine          → ranked site scores
  Stage 5 Review          → sub-quality-reviewer        → validated findings
  Stage 6 Synthesize      → main.md                     → recommendation report
```

## Full Sub-Skill Catalog
| Sub-skill | Purpose | Inputs | Outputs | Tools | Quality gate |
|-----------|---------|--------|---------|-------|--------------|
| requirements-gatherer | Capture format/target/candidates | user | profile | Read | All candidates geocoded |
| trade-area-modeler | Catchment + demand | profile, demo data | catchment + capture % | WebFetch | Model named + parameters stated |
| scoring-engine | Weighted multi-criteria score | all data | ranked scores | — | Weights justified; framework cited |
| stakeholder-mapper | Decision/constraints | profile | stakeholder+constraint map | — | Lease/zoning constraints captured |
| quality-reviewer | Challenge assumptions | draft | issues list | — | ≥3 assumptions stress-tested |

## Skill File Format Specification
Frontmatter `name`/`description`; sections per Claude skill standard. See `skills/main.md`.

## E2E Execution Flow
Intake → stakeholders → for each candidate run trade-area model → score → review → rank. Fallback to cached demographics if portals unavailable (signal staleness). Error handling: ungeocodable address → request clarification.

## SECOND-KNOWLEDGE-BRAIN Integration
`knowledge_updater.py` crawls geomarketing papers + CBRE/JLL/ICSC reports; appends dated method/benchmark entries.

## Quality Gates
- Each candidate scored against a named framework.
- Trade-area model parameters (distance decay, attractiveness) stated.
- Data sources + vintage cited.
- ≥3 assumptions stress-tested by quality reviewer.
- Recommendation includes go/no-go + sensitivity note.

## Test Scenarios
See `tests/test-scenarios.md` (6 scenarios).

## Key Design Decisions
1. Huff model as primary demand estimator (probabilistic, well-cited).
2. Multi-criteria weighting transparent and user-adjustable.
3. Competitive saturation always computed (Reilly/central-place).
4. Recommends data collection when inputs are weak rather than overclaiming.
5. Zoning/lease constraints can veto a high-scoring site.
