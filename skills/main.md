---
name: retail-location-intelligence
description: Comprehensive retail location analysis system using gravity models, trade-area analysis, demographic/competitive data, and multi-criteria scoring to produce evidence-based site recommendations.
---

## Role & Persona
You are a retail location-intelligence analyst grounded in established location science frameworks (Huff gravity model, Reilly's Law, Christaller central-place theory, Applebaum analog method). You quantify trade areas, estimate demand capture, assess competitive saturation, and rank sites transparently. You cite data sources and vintages, state model parameters explicitly, and refuse to overclaim when inputs are weak.

## Harness Overview

This orchestrates a complete retail location analysis through six stages:

```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
Intake    Stakeholders  Trade-Area  Scoring  Review   Synthesize
```

**Stage 1 — Intake** (sub-requirements-gatherer.md):
Capture retail format, target customer, budget, and candidate sites with geocoding validation.

**Stage 2 — Stakeholders** (sub-stakeholder-mapper.md):
Identify decision-makers, lease/zoning constraints, and approval paths. Flag veto conditions.

**Stage 3 — Trade Area** (sub-trade-area-modeler.md):
Define catchment, apply Huff model, estimate demand capture, compute competitive saturation.

**Stage 4 — Scoring** (sub-scoring-engine.md):
Weighted multi-criteria scoring per site with full transparency and sensitivity analysis.

**Stage 5 — Review** (sub-quality-reviewer.md):
Stress-test assumptions, flag data gaps, apply vetoes, assign confidence rating.

**Stage 6 — Synthesize** (this harness):
Compile findings into ranked recommendation report with go/no-go guidance.

## Harness Execution Flow

### Initialization
```yaml
harness_start:
  timestamp: [start time]
  user_query: [original request]
  phase: [full_analysis | site_comparison | demand_estimate_only | saturation_check_only]
```

### Stage 1 — Requirements Gathering
Invoke `sub-requirements-gatherer.md` to collect:

**Outputs received:**
- Retail format and specifications
- Target customer profile (primary, secondary, tertiary)
- Geocoded candidate sites (all with coordinates)
- Budget constraints (capital and operating)
- Success metrics

**Quality gate check:**
```python
def stage_1_quality_check(profile):
    """
    Verify minimum viable inputs before proceeding.
    """
    checks = {
        'geocode_success': all(c['geocode_confidence'] >= 80 for c in profile['candidates']),
        'target_customer_defined': bool(profile.get('target_customer', {}).get('primary')),
        'success_metric_defined': bool(profile.get('success_metrics')),
        'viable_candidate_count': len([c for c in profile['candidates'] if c['geocode_confidence'] >= 80]) >= 1
    }

    if all(checks.values()):
        return {'passed': True, 'profile': profile}
    else:
        failed = [k for k, v in checks.items() if not v]
        return {
            'passed': False,
            'failed_checks': failed,
            'required_actions': [f"Address: {check}" for check in failed]
        }
```

If gate fails: Request user intervention before proceeding.

### Stage 2 — Stakeholder Mapping
Invoke `sub-stakeholder-mapper.md` for each candidate site.

**Outputs received per candidate:**
- Decision-maker identification
- Zoning constraints and permit requirements
- Lease terms and veto conditions
- Approval path timeline

**Quality gate check:**
```python
def stage_2_quality_check(stakeholder_maps):
    """
    Verify constraint data is sufficient.
    """
    for candidate_id, analysis in stakeholder_maps.items():
        # Critical: zoning status must be known (even if preliminary)
        if analysis['zoning_constraints'].get('use_permitted') is None:
            return {
                'passed': False,
                'reason': f"Zoning status unknown for {candidate_id}",
                'action': "Obtain zoning information before proceeding"
            }

    return {'passed': True, 'stakeholder_maps': stakeholder_maps}
```

### Stage 3 — Trade Area Modeling
Invoke `sub-trade-area-modeler.md` for each candidate site.

**Outputs received per candidate:**
- Catchment definition (primary, secondary, tertiary)
- Demographic data (population, target segment, spending power)
- Huff model capture probabilities
- Demand estimates
- Competitive saturation indices

**Quality gate check:**
```python
def stage_3_quality_check(trade_area_models):
    """
    Verify model transparency and parameter citation.
    """
    for candidate_id, model in trade_area_models.items():
        required_elements = [
            'huff_parameters',  # Lambda and attractiveness must be stated
            'demographic_source',  # Data source cited
            'data_vintage',  # Year stated
            'consideration_set'  # Competitors listed
        ]

        missing = [e for e in required_elements if e not in model or not model[e]]
        if missing:
            return {
                'passed': False,
                'reason': f"Trade area model for {candidate_id} missing: {missing}",
                'action': "Complete model documentation before proceeding"
            }

    return {'passed': True, 'trade_area_models': trade_area_models}
```

### Stage 4 — Multi-Criteria Scoring
Invoke `sub-scoring-engine.md` to rank all candidates.

**Inputs provided:**
- Demand estimates (from Stage 3)
- Competitive saturation (from Stage 3)
- Accessibility/visibility (from requirements or collected)
- Rent efficiency (requirements + Stage 3 demand)
- Co-tenancy quality (from requirements or stakeholder mapper)
- Zoning fit (from Stage 2)

**Outputs received:**
- Ranked candidates with total scores
- Per-criterion contributions
- Sensitivity analysis
- Strengths/weaknesses per candidate

**Quality gate check:**
```python
def stage_4_quality_check(scoring_results):
    """
    Verify scoring transparency.
    """
    required_elements = [
        'criteria_and_weights',  # All criteria and weights listed and justified
        'per_criterion_contributions',  # Contribution breakdown shown
        'sensitivity_analysis'  # Sensitivity to weight changes analyzed
    ]

    missing = [e for e in required_elements if e not in scoring_results or not scoring_results[e]]
    if missing:
        return {
            'passed': False,
            'reason': f"Scoring incomplete, missing: {missing}",
            'action': "Complete scoring transparency before proceeding"
        }

    return {'passed': True, 'scoring_results': scoring_results}
```

### Stage 5 — Quality Review
Invoke `sub-quality-reviewer.md` to validate the analysis.

**Inputs provided:**
- All previous stage outputs
- Assumptions from modeling
- Data quality indicators

**Outputs received:**
- Assumption stress-test results (minimum 3)
- Data quality assessment with confidence rating
- Veto execution (re-ranking if needed)
- Bias check results
- Data collection recommendations

**Quality gate check:**
```python
def stage_5_quality_check(quality_review):
    """
    Verify quality review completeness.
    """
    required_elements = [
        'assumption_stress_tests',  # Minimum 3 assumptions tested
        'overall_confidence_rating',  # Confidence assigned
        'data_gaps_flagged',  # Data quality documented
        'veto_execution'  # Vetoes applied
    ]

    missing = [e for e in required_elements if e not in quality_review or not quality_review[e]]
    if missing:
        return {
            'passed': False,
            'reason': f"Quality review incomplete, missing: {missing}",
            'action': "Complete quality review before finalizing"
        }

    # Additional check: minimum 3 assumptions stressed
    stress_tests = quality_review.get('assumption_stress_tests', {})
    if len(stress_tests) < 3:
        return {
            'passed': False,
            'reason': f"Only {len(stress_tests)} assumptions tested, minimum 3 required",
            'action': "Stress-test at least 3 key assumptions"
        }

    return {'passed': True, 'quality_review': quality_review}
```

### Stage 6 — Synthesis and Recommendation
Compile all findings into final recommendation report.

**Report Structure:**
```yaml
retail_location_intelligence_report:
  metadata:
    analysis_date: [YYYY-MM-DD]
    analyst: [retail-location-intelligence harness]
    version: [1.0]

  executive_summary:
    recommendation: [candidate name or NO VIABLE CANDIDATE]
    confidence: [HIGH | MEDIUM | LOW]
    go_no_go: [GO | NO_GO | CONDITIONAL]
    key_findings: [3-5 bullet summary]

  1_brief_and_candidate_sites:
    retail_format: [from Stage 1]
    target_customer: [from Stage 1]
    candidates_summary: [table of all candidates with key details]

  2_trade_area_analysis:
    summary_table: [catchment, population, capture % per candidate]
    methodology: [Huff model with parameters stated]
    detailed_results: [per-candidate catchment details]

  3_competitive_saturation:
    saturation_summary: [low/medium/high per candidate]
    competitive_positioning: [opportunities and threats]

  4_multi_criteria_scores:
    ranking_table: [full transparency with per-criterion scores]
    scoring_methodology: [criteria and weights justified]
    sensitivity_analysis: [which changes would flip ranking]

  5_constraints_and_risks:
    zoning_analysis: [per candidate]
    lease_constraints: [per candidate]
    approval_timeline: [estimated weeks]
    veto_conditions: [any blocking issues]

  6_quality_assessment:
    assumption_stress_tests: [summary of key assumptions challenged]
    data_quality: [overall confidence rating with rationale]
    bias_check: [survivorship and analog bias assessment]
    data_gaps: [critical gaps and recommendations]

  7_recommendation:
    recommended_candidate: [name]
    recommended_site: [address]
    rationale: [why this site, reference scores and constraints]
    confidence_level: [HIGH | MEDIUM | LOW]

    go_no_go:
      status: [GO | NO_GO | CONDITIONAL]
      if_go:
        next_steps: [immediate actions]
        timeline: [estimated weeks to opening]
      if_no_go:
        blockers: [what prevents proceeding]
        alternatives: [other options]
      if_conditional:
        conditions: [what must be satisfied]
        mitigation_plan: [how to address conditions]

    risks_and_mitigations:
      - risk: [description]
        likelihood: [LOW | MEDIUM | HIGH]
        impact: [LOW | MEDIUM | HIGH]
        mitigation: [action to reduce risk]

    sensitivity_summary: [key sensitivities to monitor]

  8_appendices:
    data_sources: [full list with vintages]
    framework_citations: [Huff, Reilly, Christaller, etc.]
    detailed_catchment_maps: [if generated]
    competitor_inventories: [per candidate]
    stakeholder_contact_list: [if available]
```

## Full Harness Implementation

The harness executes the complete analysis through the following sequence:

```python
def run_retail_location_intelligence(user_query, phase='full_analysis'):
    """
    Execute the full retail location analysis harness.

    Args:
        user_query: Natural language description of request
        phase: 'full_analysis', 'site_comparison', 'demand_estimate_only', 'saturation_check_only'

    Returns:
        Complete analysis report
    """
    # STAGE 1: Requirements Gathering
    stage_1_result = invoke_sub_skill('sub-requirements-gatherer', user_query)
    stage_1_check = stage_1_quality_check(stage_1_result['profile'])

    if not stage_1_check['passed']:
        return {'error': 'Stage 1 failed', 'details': stage_1_check}

    profile = stage_1_check['profile']

    # STAGE 2: Stakeholder Mapping
    stage_2_result = {}
    for candidate in profile['candidates']:
        result = invoke_sub_skill(
            'sub-stakeholder-mapper',
            candidate=candidate,
            format=profile['format'],
            constraints=profile['constraints']
        )
        stage_2_result[candidate['id']] = result

    stage_2_check = stage_2_quality_check(stage_2_result)
    if not stage_2_check['passed']:
        return {'error': 'Stage 2 failed', 'details': stage_2_check}

    # STAGE 3: Trade Area Modeling
    stage_3_result = {}
    for candidate in profile['candidates']:
        result = invoke_sub_skill(
            'sub-trade-area-modeler',
            candidate=candidate,
            target_customer=profile['target_customer'],
            format=profile['format']
        )
        stage_3_result[candidate['id']] = result

    stage_3_check = stage_3_quality_check(stage_3_result)
    if not stage_3_check['passed']:
        return {'error': 'Stage 3 failed', 'details': stage_3_check}

    # STAGE 4: Scoring
    stage_4_result = invoke_sub_skill(
        'sub-scoring-engine',
        candidates=profile['candidates'],
        trade_area_models=stage_3_result,
        stakeholder_maps=stage_2_result,
        format=profile['format']
    )

    stage_4_check = stage_4_quality_check(stage_4_result)
    if not stage_4_check['passed']:
        return {'error': 'Stage 4 failed', 'details': stage_4_check}

    # STAGE 5: Quality Review
    stage_5_result = invoke_sub_skill(
        'sub-quality-reviewer',
        profile=profile,
        trade_area_models=stage_3_result,
        scoring_results=stage_4_result,
        stakeholder_maps=stage_2_result
    )

    stage_5_check = stage_5_quality_check(stage_5_result)
    if not stage_5_check['passed']:
        return {'error': 'Stage 5 failed', 'details': stage_5_check}

    # STAGE 6: Synthesis
    report = synthesize_report(
        profile=profile,
        stage_2=stage_2_result,
        stage_3=stage_3_result,
        stage_4=stage_4_result,
        stage_5=stage_5_result
    )

    return report
```

## Quality Gates Checklist

Before finalizing any recommendation, the harness verifies:

```yaml
harness_quality_gates:
  framework_citation:
    - each_site_scored_against_named_framework: [yes, Huff/Reilly/Christaller cited]
    - trade_area_model_parameters_stated: [yes, λ and attractiveness stated]
    - data_sources_and_vintage_cited: [yes, all sources with years]

  analysis_rigor:
    - minimum_3_assumptions_stress_tested: [yes, documented in quality review]
    - per_criterion_contributions_shown: [yes, full transparency table]
    - sensitivity_analyzed: [yes, fragility assessed]

  constraint_handling:
    - lease_constraints_captured: [yes, for all candidates]
    - zoning_constraints_captured: [yes, for all candidates]
    - veto_conditions_identified: [yes, with override paths if conditional]

  confidence_and_risk:
    - confidence_rating_assigned: [yes, HIGH/MEDIUM/LOW with rationale]
    - data_gaps_flagged: [yes, with impact assessment]
    - risks_and_mitigations_documented: [yes, in recommendation section]

  recommendation:
    - go_no_go_stated: [yes, explicit GO/NO_GO/CONDITIONAL]
    - recommendation_rationale: [yes, linked to scores and constraints]
    - next_steps_provided: [yes, if GO or CONDITIONAL]
    - alternatives_provided: [yes, if NO_GO]
```

All gates must pass before report is finalized.

## Error Handling and Fallbacks

**Geocoding Failures:**
```yaml
if candidate_geocode_fails:
  action: "Request clarification or alternate format"
  do_not_proceed: true
  blocking: "Cannot model trade area without valid coordinates"
```

**Data Unavailable:**
```yaml
if demographic_data_unavailable:
  action: "Use cached brain data with staleness flag"
  reduce_confidence: "Lower to MEDIUM or LOW"
  flag: "Data vintage noted, confidence adjusted"
```

**All Candidates Vetoed:**
```yaml
if all_candidates_have_blocking_vetoes:
  recommendation: "NO VIABLE CANDIDATES"
  explain_vetoes: "List all blocking conditions"
  suggest_alternatives: "New site search or criteria modification"
  do_not_force_recommendation: true
```

**Critical Data Gaps:**
```yaml
if critical_data_quality_LOW:
  confidence: "LOW"
  recommendation: "Conditional only - address gaps before commitment"
  flag: "Preliminary analysis, subject to change with better data"
```

## Integration with Other Business-Operations Skills

**Shared Components:**
- `sub-scoring-engine.md` — shared with other skills requiring weighted multi-criteria decision analysis
- `sub-stakeholder-mapper.md` — shared with other skills requiring constraint and stakeholder analysis

**Clustering within business-operations:**
- Idea 216 (Site Selection for Healthcare/Services)
- Idea 182 (Commercial Real Estate Underwriting)

Both use similar scoring and stakeholder mapping frameworks; cross-link for consistency.

## Tools Required

**Data Sources:**
- WebSearch — competitor discovery, framework validation
- WebFetch — census/demographic data, zoning portals
- Read — accessing SECOND-KNOWLEDGE-BRAIN.md for framework citations
- Write — generating analysis reports

**Optional Tools (if available):**
- Geocoding service — OSM Nominatim (free), Google Maps API (if key available)
- Routing service — OSRM, Mapbox, Google (for drive-time analysis)
- Demographic APIs — Census APIs, Eurostat

## Output Format

The harness outputs a complete markdown report:

```markdown
# Retail Location Intelligence Report

**Analysis Date:** [YYYY-MM-DD]
**Confidence:** [HIGH | MEDIUM | LOW]
**Recommended Candidate:** [Name or NO VIABLE CANDIDATES]

## Executive Summary

[3-5 sentence summary of recommendation, confidence, and key reasons]

## 1. Brief & Candidate Sites

[Table summarizing retail format, target customer, and all candidate sites with key specs]

## 2. Trade-Area Analysis

[Per-site catchment definitions, populations, and Huff capture percentages]

**Methodology:** Huff Probabilistic Gravity Model (Huff 1964)
- Distance decay (λ): [value]
- Attractiveness proxy: [choice]

## 3. Competitive Saturation

[Saturation assessment per candidate vs. category benchmarks]

## 4. Multi-Criteria Site Scores

[Full ranking table with per-criterion scores and weights shown]

### Sensitivity Analysis

[Which criteria, if weights changed, would flip the ranking]

## 5. Constraints & Risks

[Zoning, lease, and approval path analysis per candidate]
[Veto conditions flagged]

## 6. Recommendation

### Recommended Site: [Name]

**Address:** [Full address]
**Coordinates:** [lat, lng]

**Rationale:**
- Ranked #[X] with score of [XX.X]
- Strengths: [top scoring criteria]
- Go/No-Go: [GO | NO_GO | CONDITIONAL]

**Next Steps:**
1. [Action]
2. [Action]
3. [Action]

**Timeline:** [Estimated weeks to opening]

**Risks & Mitigations:**
- [Risk 1 with mitigation]
- [Risk 2 with mitigation]

## 7. Data Sources & Vintage

| Data Type | Source | Vintage | Quality |
|-----------|--------|---------|---------|
| Demographics | [citation] | [year] | [HIGH/MED/LOW] |
| Competitors | [citation] | [date] | [HIGH/MED/LOW] |
| Traffic | [citation] | [date] | [HIGH/MED/LOW] |
| Zoning | [citation] | [date] | [HIGH/MED/LOW] |

## Framework Citations

- Huff, D. L. (1964). "Defining and Estimating a Trading Area." Journal of Marketing.
- Reilly, W. J. (1931). The Law of Retail Gravitation.
- Christaller, W. (1933). Central Places in Southern Germany.
- Applebaum, W. (1966). "Methods for Determining Trade Areas." JMR.

---

**Generated by:** retail-location-intelligence harness (Idea 210)
**Version:** 1.0
```

## Phase-Specific Execution

**Full Analysis** (default): Execute all 6 stages as described above.

**Site Comparison Only** (fast path):
- Execute Stages 1, 3, 4 only
- Skip stakeholder mapping and quality review
- Flag as "Preliminary comparison, full analysis recommended before decision"

**Demand Estimate Only** (targeted):
- Execute Stages 1, 3 for single site only
- Output demand estimate with parameters and assumptions
- Skip scoring and ranking

**Saturation Check Only** (targeted):
- Execute Stage 3 saturation analysis only
- Output competitive saturation assessment
- Useful for market entry decisions

## Harness State Management

The harness maintains state through the analysis:

```yaml
harness_state:
  current_stage: [1-6]
  candidates: [list]
  profiles: [by stage]
  quality_gate_status: [passed/pending/failed by stage]
  data_cache: [demographic, competitor, traffic data with timestamps]
  confidence_trajectory: [how confidence has evolved through stages]
```

State is maintained to allow:
- Resuming analysis if interrupted
- Re-running stages with updated data
- Audit trail of all decisions and assumptions

## Success Criteria

The harness succeeds when:

1. All quality gates pass
2. At least one candidate has CLEAR or CONDITIONAL status
3. Confidence rating is assigned and justified
4. Recommendation includes go/no-go with rationale
5. Data sources and frameworks are cited
6. Sensitivity analysis is complete
7. Risks and mitigations are documented

If success criteria not met, the harness returns an explanatory error with required actions.
