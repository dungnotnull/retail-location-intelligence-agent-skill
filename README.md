# Retail Location Intelligence (Idea 210)

**Skill name:** `retail-location-intelligence`
**Tagline:** Scores candidate retail sites using gravity models, trade-area analysis, and demographic/competitive data to recommend optimal store coordinates.
**Cluster:** `business-operations`
**Source idea:** 210
**Version:** 1.0
**License:** MIT

## Overview

This skill provides a comprehensive, production-grade system for evaluating retail location decisions. It combines established location science frameworks (Huff gravity model, Reilly's Law, Christaller central-place theory, Applebaum analog method) with transparent multi-criteria scoring to produce evidence-based site recommendations.

## Problem It Solves

Choosing where to open a physical retail location is high-stakes and irreversible. SMEs and emerging chains rarely have GIS analysts or location scientists on staff. They need a structured way to weigh:
- Population density and demographics
- Footfall and traffic patterns
- Accessibility and visibility
- Competitor proximity and saturation
- Co-tenancy and anchor effects
- Rent efficiency
- Zoning and permitting constraints

This skill transforms these factors into a ranked, defensible recommendation with trade-area estimates and a risk-aware roadmap.

## Features

### Core Capabilities

- **Huff Gravity Model**: Probabilistic demand capture estimation with stated parameters
- **Competitive Saturation Analysis**: Market saturation assessment using Reilly's Law and central-place theory
- **Multi-Criteria Scoring**: Transparent weighted scoring with per-criterion contributions shown
- **Stakeholder Mapping**: Decision-maker and constraint identification with veto detection
- **Quality Review**: Devil's-advocate stress-testing of assumptions and data gaps
- **Constraint Veto**: Hard constraints (zoning, lease) override analytical scores

### Key Features

- **Full Transparency**: Every parameter, weight, and assumption is documented
- **Citation Required**: All data sources and frameworks cited with vintages
- **Sensitivity Analysis**: Identifies which changes would flip rankings
- **Confidence Ratings**: High/Medium/Low confidence based on data quality
- **Graceful Degradation**: Handles weak data with fallback and warning flags
- **Production-Ready**: No dummy code, fully implemented for real use

## Installation

### Prerequisites

- Python 3.10+
- Required Python packages (for tools):
  ```bash
  pip install requests beautifulsoup4 feedparser html2text python-dateutil
  ```

### Setup

1. Clone or download this skill directory
2. All skill files are in `skills/` subdirectory
3. Test fixtures in `tests/` subdirectory
4. Knowledge updater tool in `tools/` subdirectory

## Usage

### As a Claude Skill

This skill is designed for use with Claude Code or compatible AI coding assistants:

```
/user: "Analyze these three coffee shop locations in Cambridge: [addresses]"
/assistant: [Invokes retail-location-intelligence harness]

Output: Complete analysis report with ranked recommendation
```

### Standalone Components

Each sub-skill can be invoked independently:

- `skills/sub-requirements-gatherer.md` — Intake and geocoding
- `skills/sub-trade-area-modeler.md` — Huff model and demand estimation
- `skills/sub-scoring-engine.md` — Multi-criteria ranking
- `skills/sub-stakeholder-mapper.md` — Constraints and vetoes
- `skills/sub-quality-reviewer.md` — Validation and confidence

### Knowledge Updates

Run the knowledge updater periodically:

```bash
python tools/knowledge_updater.py              # Full crawl
python tools/knowledge_updater.py --dry-run    # Preview mode
python tools/knowledge_updater.py --source cbre  # Single source
```

## Architecture

```
retail-location-intelligence/
├── skills/                          # Main skill files
│   ├── main.md                      # Orchestrating harness
│   ├── sub-requirements-gatherer.md
│   ├── sub-trade-area-modeler.md
│   ├── sub-scoring-engine.md
│   ├── sub-stakeholder-mapper.md
│   └── sub-quality-reviewer.md
├── tests/                           # Test suite
│   ├── test-scenarios.md            # Test definitions
│   └── fixtures.py                  # Mock data
├── tools/                           # Utility scripts
│   └── knowledge_updater.py         # Knowledge crawler
├── CLAUDE.md                        # Project instructions
├── PROJECT-detail.md                # Architecture documentation
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Development tracking
├── SECOND-KNOWLEDGE-BRAIN.md        # Knowledge base
└── README.md                        # This file
```

### Harness Flow

```
Stage 1 Intake          → sub-requirements-gatherer  → profile
Stage 2 Stakeholders    → sub-stakeholder-mapper      → constraints
Stage 3 Trade area      → sub-trade-area-modeler      → demand + competition
Stage 4 Scoring         → sub-scoring-engine          → ranked scores
Stage 5 Review          → sub-quality-reviewer        → validated
Stage 6 Synthesize      → main.md                     → recommendation report
```

## Output Format

The skill produces a comprehensive markdown report:

```markdown
# Retail Location Intelligence Report

## Executive Summary
[3-5 sentence summary with recommendation and confidence]

## 1. Brief & Candidate Sites
[Retail format, target customer, all candidates]

## 2. Trade-Area Analysis
[Catchment, population, Huff capture % per site]

## 3. Competitive Saturation
[Saturation assessment per candidate]

## 4. Multi-Criteria Site Scores
[Ranking table with per-criterion contributions]

## 5. Constraints & Risks
[Zoning, lease, approval analysis]

## 6. Recommendation
[Go/no-go with rationale, next steps, risks]

## 7. Data Sources & Vintage
[All sources cited with years]
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/test-scenarios.py -v

# Run with coverage
pytest tests/test-scenarios.py --cov=skills --cov-report=html
```

### Test Scenarios

1. **Three-candidate ranking** — End-to-end analysis with transparency
2. **Saturation check** — Competitive saturation detection
3. **Zoning veto** — Hard constraints override scores
4. **Weak data fallback** — Graceful degradation
5. **Assumption stress-test** — Quality validation
6. **Demand capture estimate** — Huff model traceability

## Data Sources

### Demographics
- US Census Bureau (data.census.gov) — American Community Survey
- Eurostat — European demographic data
- National statistics offices (country-specific)

### Competition
- OpenStreetMap — Business listings
- Commercial databases (if licensed)
- Field observation

### Frameworks
- Huff Gravity Model (1964)
- Reilly's Law of Retail Gravitation (1931)
- Christaller Central Place Theory (1933)
- Applebaum Analog Method (1966)

## Integration

### Shared Components

The following sub-skills are shared across the business-operations cluster:

- `sub-scoring-engine.md` — Multi-criteria decision analysis
- `sub-stakeholder-mapper.md` — Constraint and stakeholder analysis

### Cluster Integration

This skill integrates with:
- Idea 216 (Site Selection for Healthcare/Services)
- Idea 182 (Commercial Real Estate Underwriting)

Both use similar frameworks; cross-reference for consistency.

## Quality Assurance

### Quality Gates

Every analysis must pass:

1. ✓ Framework cited (Huff, Reilly, Christaller)
2. ✓ Parameters stated (λ, attractiveness proxy)
3. ✓ Data sources with vintages
4. ✓ Per-criterion contributions shown
5. ✓ Sensitivity analysis
6. ≥3 Assumptions stress-tested
7. ✓ Confidence rating assigned
8. ✓ Go/no-go status

### Confidence Levels

- **HIGH**: All critical data quality HIGH or higher
- **MEDIUM**: All critical data at least MEDIUM
- **LOW**: Any critical data LOW

## Limitations

- **Geocoding**: Requires address validation service
- **Demographics**: Dependent on census data availability
- **Real-time Data**: Traffic counts, competitor changes not real-time
- **Local Knowledge**: Cannot substitute for local market expertise
- **Legal Advice**: Zoning analysis is informational, not legal opinion

## Contributing

This skill is open-source. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License — See LICENSE file for details

## Citation

If you use this skill in research or production:

```
Retail Location Intelligence (Idea 210). (2026).
Location Science Framework for Retail Site Selection.
https://github.com/skills-retail-location-intelligence
```

## Acknowledgments

- Huff, D. L. (1964). "Defining and Estimating a Trading Area."
- Reilly, W. J. (1931). The Law of Retail Gravitation.
- Christaller, W. (1933). Central Places in Southern Germany.
- Applebaum, W. (1966). "Methods for Determining Trade Areas."

## Contact

For issues, questions, or contributions:
- GitHub Issues: [repository URL]
- Cluster: business-operations
- Source Idea: 210

---

**Generated by:** retail-location-intelligence skill development team
**Version:** 1.0 (Production-Ready)
**Status:** Complete — All Phases 0-5 Implemented
