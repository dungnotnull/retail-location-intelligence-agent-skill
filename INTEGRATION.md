# Integration Guide — Retail Location Intelligence (Idea 210)

## Cluster Integration

This skill is part of the `business-operations` cluster and shares components with related skills.

### Shared Components

#### Sub-Scoring Engine

**Shared With:**
- Idea 216: Site Selection for Healthcare/Services
- Idea 182: Commercial Real Estate Underwriting

**Integration Points:**
```yaml
shared_component: sub-scoring-engine.md
interface:
  input:
    candidates: [list of candidate sites]
    criteria: [evaluation dimensions]
    data_by_criteria: [values for each candidate]
  output:
    ranked_candidates: [sorted by score]
    per_criterion_contributions: [transparency table]
    sensitivity_analysis: [fragility assessment]

customization_by_idea:
  idea_210_retail:
    criteria_weights:
      demand_capture: 0.30
      competitive_position: 0.20
      accessibility_visibility: 0.15

  idea_216_healthcare:
    criteria_weights:
      patient_access: 0.35
      provider_network: 0.25
      regulatory_compliance: 0.20

  idea_182_cre:
    criteria_weights:
      rent_roll_quality: 0.30
      tenant_credit: 0.25
      market_rent_growth: 0.20
```

#### Sub-Stakeholder Mapper

**Shared With:**
- Idea 216: Site Selection for Healthcare/Services
- Idea 182: Commercial Real Estate Underwriting

**Integration Points:**
```yaml
shared_component: sub-stakeholder-mapper.md
interface:
  input:
    site_details: [candidate information]
    organizational_context: [decision structure]
  output:
    stakeholder_map: [decision-makers and priorities]
    constraint_register: [hard constraints with veto flags]
    approval_path: [timeline and steps]

customization_by_idea:
  idea_210_retail:
    focus_constraints: [zoning, lease, franchisor]
    veto_conditions: [use_not_permitted, rent_over_budget]

  idea_216_healthcare:
    focus_constraints: [certificate_of_need, staffing, licensing]
    veto_conditions: [CON_not_approved, staffing_insufficient]

  idea_182_cre:
    focus_constraints: [environmental, title, financing_contingencies]
    veto_conditions: [environmental_issue, title_defect]
```

### Cross-Link Documentation

Each shared component documents its cluster relationships:

```markdown
## Integration Points

- **Calls**: [tools or sub-skills invoked]
- **Called By**: [which harnesses use this component]
- **Inputs From**: [data sources]
- **Outputs To**: [consumers of this data]
- **Cluster Relationships**: [related skills in business-operations]
```

## API Integration

### External Data Sources

The skill integrates with external APIs and data sources:

```yaml
demographic_apis:
  us_census:
    endpoint: "https://api.census.gov/data"
    authentication: "none (public)"
    rate_limits: "1000 requests/day"
    fallback: "SECOND-KNOWLEDGE-BRAIN cached data"

  eurostat:
    endpoint: "https://ec.europa.eu/eurostat/api"
    authentication: "none (public)"
    rate_limits: "unspecified"
    fallback: "national statistics offices"

geocoding_services:
  osm_nominatim:
    endpoint: "https://nominatim.openstreetmap.org/search"
    authentication: "none (public, email required)"
    rate_limits: "1 request/second"
    fallback: "Google Maps API (if key available)"

  google_maps:
    endpoint: "https://maps.googleapis.com/maps/api/geocode/json"
    authentication: "API key required"
    rate_limits: "Quota-based"
    cost: "$2000 free/month, then $0.005 per request"

routing_services:
  osrm:
    endpoint: "http://router.project-osrm.org/route/v1/driving"
    authentication: "none (public)"
    rate_limits: "unspecified, be respectful"
    fallback: "Euclidean distance approximation"

  mapbox:
    endpoint: "https://api.mapbox.com/directions/v5/mapbox/driving"
    authentication: "Access token required"
    rate_limits: "100,000 free requests/month"
    cost: "Free tier available"
```

### Error Handling

```python
def fetch_with_fallback(primary_source, fallback_source, data_type):
    """
    Fetch data with fallback chain.

    Args:
        primary_source: First source to try
        fallback_source: Backup source
        data_type: Type of data for logging

    Returns:
        Data or None with appropriate flags
    """
    try:
        data = primary_source.fetch()
        if validate_data(data):
            return {
                'data': data,
                'source': primary_source.name,
                'quality': 'HIGH',
                'vintage': primary_source.vintage
            }
        else:
            logger.warning(f"Primary source validation failed for {data_type}")
    except Exception as e:
        logger.warning(f"Primary source failed for {data_type}: {e}")

    # Fallback
    try:
        data = fallback_source.fetch()
        return {
            'data': data,
            'source': fallback_source.name,
            'quality': 'MEDIUM',  # Downgrade confidence
            'vintage': fallback_source.vintage,
            'fallback_used': True
        }
    except Exception as e:
        logger.error(f"Fallback source failed for {data_type}: {e}")
        return {
            'data': None,
            'source': None,
            'quality': 'LOW',
            'error': str(e)
        }
```

## Environment Configuration

### Required Environment Variables

```bash
# Optional: Google Maps API (if not using OSM)
export GOOGLE_MAPS_API_KEY="your_key_here"

# Optional: Mapbox Token (if not using OSRM)
export MAPBOX_ACCESS_TOKEN="your_token_here"

# Optional: Census API Key (for higher rate limits)
export CENSUS_API_KEY="your_key_here"

# Logging
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
export LOG_FILE="logs/retail_location_intelligence.log"
```

### Configuration File

`config.yaml`:

```yaml
api:
  geocoding:
    primary: "osm_nominatim"
    fallback: "google_maps"
    timeout_seconds: 10

  routing:
    primary: "osrm"
    fallback: "mapbox"
    timeout_seconds: 30

  demographics:
    primary: "us_census"
    fallback: "cached_brain_data"
    timeout_seconds: 20

analysis:
  huff:
    default_lambda: 2.0
    default_alpha: 1.0
    default_attractiveness_proxy: "floor_area"

  catchment:
    default_drive_time_minutes: 5
    default_distance_miles: 1.5

quality:
  minimum_confidence_for_recommendation: "MEDIUM"
  stale_data_threshold_years: 2

output:
  format: "markdown"
  include_charts: false
  verbosity: "standard"  # minimal, standard, detailed
```

## Deployment Options

### Option 1: Claude Skill

Deploy as a Claude Code or compatible AI skill:

1. Place skill files in appropriate directory
2. Configure in `CLAUDE.md` or skill registry
3. Invoke through natural language

### Option 2: Standalone Python Package

Package as Python module:

```bash
# Setup structure
retail_location_intelligence/
├── retail_location_intelligence/
│   ├── __init__.py
│   ├── harness.py
│   ├── sub_skills/
│   └── tools/
├── setup.py
└── requirements.txt

# Install
pip install -e .

# Use
from retail_location_intelligence import analyze_location

result = analyze_location(
    candidates=[...],
    retail_format={...},
    target_customer={...}
)
```

### Option 3: REST API

Deploy as microservice:

```python
# api.py
from fastapi import FastAPI
from retail_location_intelligence import analyze_location

app = FastAPI(title="Retail Location Intelligence API")

@app.post("/analyze")
def analyze(request: AnalysisRequest):
    """Run location analysis."""
    result = analyze_location(
        candidates=request.candidates,
        retail_format=request.retail_format,
        target_customer=request.target_customer
    )
    return result

# Run with uvicorn
# uvicorn api:app --reload
```

### Option 4: CLI Tool

Command-line interface:

```bash
# cli.py
import argparse
from retail_location_intelligence import analyze_location

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidates', required=True)
    parser.add_argument('--format', required=True)
    parser.add_argument('--output', default='report.md')
    args = parser.parse_args()

    # Run analysis
    result = analyze_location(...)

    # Write report
    with open(args.output, 'w') as f:
        f.write(result['report'])

if __name__ == '__main__':
    main()
```

## Monitoring and Logging

### Logging Strategy

```python
import logging
from pathlib import Path

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/retail_location_intelligence.log'),
        logging.StreamHandler()
    ]
)

# Key events to log
logger.info("Analysis started", extra={
    'candidate_count': len(candidates),
    'retail_format': format['category']
})

logger.warning("Data quality issue", extra={
    'data_type': 'demographics',
    'quality': 'LOW',
    'vintage': 2020
})

logger.error("Analysis failed", extra={
    'stage': 'trade_area_modeling',
    'error': str(e)
})
```

### Metrics to Track

```yaml
operational_metrics:
  analysis_duration: [time from start to report]
  stage_durations: [time per stage]
  data_fetch_time: [time spent on external APIs]
  error_rate: [analyses that fail / total]

data_quality_metrics:
  stale_data_rate: [analyses using data > 2 years old / total]
  fallback_rate: [analyses using cached data / total]
  low_confidence_rate: [analyses with LOW confidence / total]

outcome_metrics:
  go_recommendations: [count of GO recommendations]
  no_go_recommendations: [count of NO_GO recommendations]
  conditional_recommendations: [count of CONDITIONAL recommendations]
  veto_conditions: [count of analyses with veto conditions]
```

## Security Considerations

### API Key Management

```python
# Never hardcode API keys
import os
from dotenv import load_dotenv

load_dotenv()

google_key = os.getenv('GOOGLE_MAPS_API_KEY')
if not google_key:
    logger.warning("Google Maps API key not found, using OSM")
```

### Data Privacy

```yaml
privacy_considerations:
  user_data:
    - Candidate addresses may be proprietary
    - Financial terms may be confidential
    - Strategic plans should be protected

  handling:
    - No persistent storage of user queries (unless requested)
    - Reports may contain sensitive information
    - Logs should not include sensitive user data

  recommendations:
    - Encrypt reports if storing
    - Sanitize logs before sharing
    - Use secure channels for transmission
```

## Compliance

### Geographic Considerations

```yaml
regional_compliance:
  gdpr_europe:
    - Census data handling requirements
    - User data retention limits
    - Right to deletion

  ccpa_california:
    - Privacy policy requirements
    - Data disclosure transparency

  data_residency:
    - Some countries require data storage within borders
    - Check local requirements for demographic data
```

## Troubleshooting

### Common Issues

```yaml
issue_geocoding_fails:
  symptoms: "All candidates fail geocoding"
  causes:
    - Address format incorrect
    - Geocoding service down
    - Rate limit exceeded
  solutions:
    - Verify address format
    - Try alternate geocoding service
    - Use coordinates directly

issue_no_demographic_data:
  symptoms: "Demographic queries return no data"
  causes:
    - Census API down
    - Invalid geography code
    - Network connectivity
  solutions:
    - Check API status
    - Verify geography codes
    - Use cached brain data as fallback

issue_low_confidence:
  symptoms: "All analyses return LOW confidence"
  causes:
    - Stale demographic data
    - Partial competitor data
    - Missing critical information
  solutions:
    - Update knowledge base
    - Conduct competitive audit
    - Collect missing data

issue_all_candidates_vetoed:
  symptoms: "No viable candidates in recommendation"
  causes:
    - All sites have zoning issues
    - All over budget
    - All have structural blockers
  solutions:
    - Verify zoning analysis
    - Adjust budget if flexible
    - Search for new candidates
```

## Version Compatibility

### Skill Version Matrix

```yaml
version_1.0:
  skills:
    main: "1.0"
    requirements_gatherer: "1.0"
    trade_area_modeler: "1.0"
    scoring_engine: "1.0"
    stakeholder_mapper: "1.0"
    quality_reviewer: "1.0"

  tools:
    knowledge_updater: "1.0"

  dependencies:
    python: ">=3.10"
    requests: ">=2.28"
    beautifulsoup4: ">=4.11"
    feedparser: ">=6.0"

  compatible_with:
    claude_code: ">=2024.01"
    claude_models: "opus, sonnet, haiku"
```

## Upgrade Path

### From 0.x to 1.0

```yaml
breaking_changes:
  - sub_scoring_engine: Now requires weights justification
  - sub_trade_area_modeler: Requires lambda citation
  - main: Quality gates are now mandatory

migration_steps:
  1. Review existing custom weights
  2. Add justifications for all weights
  3. Update lambda citations in trade area model
  4. Verify quality gates pass
  5. Test with sample data

rollback:
  - Previous versions archived in tags
  - Can downgrade by checking out previous tag
```

## Support

### Documentation

- `README.md` — Overview and quick start
- `PROJECT-detail.md` — Architecture documentation
- `CLAUDE.md` — Development guidelines
- `INTEGRATION.md` — This file

### Issue Tracking

Report issues via:
- GitHub Issues (if open-source)
- Internal issue tracker (if proprietary)

Include:
- Skill version
- Error messages
- Input data (sanitized)
- Expected vs. actual behavior

### Community

- Cluster: business-operations
- Related: Idea 216, Idea 182
- Discussion: [forum or channel]

---

**Document Version:** 1.0
**Last Updated:** 2026-07-02
**Maintainer:** Retail Location Intelligence Development Team
