---
name: sub-quality-reviewer
description: Devil's-advocate review of the location analysis — stress-tests assumptions, flags data gaps, applies vetoes, and assesses confidence before recommendation. Shared across business-operations cluster.
---

## Purpose
Prevent overconfident recommendations built on weak data, unchallenged assumptions, or ignored constraints. The quality reviewer plays devil's advocate, challenging the analysis from multiple angles before a recommendation is finalized.

## Inputs
- Draft trade-area model (from sub-trade-area-modeler)
- Draft scoring results (from sub-scoring-engine)
- Stakeholder constraints (from sub-stakeholder-mapper)
- Requirements profile (from sub-requirements-gatherer)

## Procedure

### 1. Stress-Test Key Assumptions
Challenge the foundational assumptions that drive the analysis.

**Assumption 1: Distance Decay Parameter (λ)**
```
Challenge questions:
  - What if consumers are less sensitive to distance than assumed?
  - What if λ should be 1.5 instead of 2.0? How do rankings change?
  - Is the chosen λ supported by local market research or just industry defaults?
  - For destination formats, is λ too high (over-penalizing distance)?

Sensitivity test:
  - Recalculate Huff capture with λ ± 0.5
  - Note if ranking changes
  - If ranking fragile to λ, flag as "high sensitivity to distance decay assumption"

Resolution:
  - If ranking robust (no change with ±0.5): assumption acceptable
  - If ranking fragile: flag for additional calibration research or present multiple scenarios
```

**Assumption 2: Attractiveness Proxy**
```
Challenge questions:
  - Is floor area truly correlated with attractiveness for this format?
  - Should brand equity be included in attractiveness (if data available)?
  - Are we over- or under-estimating competitor attractiveness?
  - For new concepts, how do we know our attractiveness assumption is valid?

Sensitivity test:
  - Vary candidate attractiveness by ±20%
  - Note impact on capture probability
  - If high sensitivity, flag as "attractiveness assumption critical"

Resolution:
  - If robust to ±20%: assumption acceptable
  - If fragile: recommend market research to validate attractiveness or use conservative estimate
```

**Assumption 3: Spend Per Capita**
```
Challenge questions:
  - Is national/category spend appropriate for this specific trade area?
  - Should spend be adjusted for local income, demographics, or culture?
  - Are we assuming full capture of addressable spend (optimistic)?
  - What if recession or economic downturn reduces spend?

Sensitivity test:
  - Reduce spend per capita by 20%
  - Note impact on demand estimates
  - Check if sites still meet viability thresholds

Resolution:
  - If robust to -20%: assumption acceptable
  - If fragile: flag as "high sensitivity to economic conditions" and recommend contingency planning
```

**Assumption 4: Trade Area Boundaries**
```
Challenge questions:
  - What if actual catchment is smaller/larger than modeled?
  - Are natural barriers (rivers, highways, railways) properly accounted for?
  - What if competitor locations draw customers from outside our modeled area?
  - Is drive-time data accurate for this specific geography?

Sensitivity test:
  - Reduce primary catchment radius by 25%
  - Note impact on population and demand
  - If significant impact, flag as "catchment boundary assumption critical"

Resolution:
  - If robust to ±25%: assumption acceptable
  - If fragile: recommend field observation or traffic study to validate catchment
```

**Assumption 5: Competitive Set Completeness**
```
Challenge questions:
  - Are we missing competitors? (newly opened, under construction, planned)
  - Are online competitors relevant? (Amazon, delivery services)
  - Are indirect competitors understated? (substitute formats)
  - What if a major competitor enters the market after we open?

Sensitivity test:
  - Add 20-30% more competitor floorspace (simulate missing competitors)
  - Recalculate saturation and capture
  - Note impact on ranking and viability

Resolution:
  - If robust to +30% competitor space: assumption acceptable
  - If fragile: flag as "competitive uncertainty high" and recommend competitive audit
```

### 2. Flag Data Gaps and Impact
Identify missing or low-quality data and assess their impact on confidence.

**Data Quality Assessment:**
```yaml
data_quality_matrix:
  demographic_data:
    source: [from trade-area modeler]
    vintage: [year]
    completeness: [high | medium | low]
    spatial_resolution: [census_block | tract | county | national]
    gap_impact:
      if_high_quality: "Confidence in demand estimates: High"
      if_medium_quality: "Confidence in demand estimates: Medium; vintage or resolution limitations"
      if_low_quality: "Confidence in demand estimates: Low; treat as order-of-magnitude only"
    recommended_actions:
      if_high_quality: "Proceed with current estimates"
      if_medium_quality: "Consider updating demographic estimates with local data if available"
      if_low_quality: "Strongly recommend commissioning local demographic study before final decision"

  competitor_data:
    source: [from trade-area modeler]
    completeness: [percentage of real competitors captured]
    verification_status: [verified | estimated | partial]
    gap_impact:
      if_complete: "Confidence in saturation analysis: High"
      if_partial: "Confidence in saturation analysis: Medium; may be missing competitors"
      if_unknown: "Confidence in saturation analysis: Low; saturation estimate unreliable"
    recommended_actions:
      if_complete: "Proceed with current analysis"
      if_partial: "Conduct field survey to validate competitor list"
      if_unknown: "Commission competitive audit; treat saturation analysis as preliminary"

  traffic_footfall_data:
    source: [from requirements or external]
    collection_method: [traffic_count | estimate | assumption | none]
    vintage: [if applicable]
    gap_impact:
      if_measured: "Confidence in accessibility score: High"
      if_estimated: "Confidence in accessibility score: Medium"
      if_assumed: "Confidence in accessibility score: Low; score based on general location characteristics"
    recommended_actions:
      if_measured: "Use actual counts in analysis"
      if_estimated: "Document estimation method; consider spot validation"
      if_assumed: "Recommend traffic count before final commitment; use conservative estimate"

  rent_lease_terms:
    source: [from requirements or stakeholder mapper]
    completeness: [complete | partial | asking_rate_only]
    verification_status: [confirmed_negotiated | asking_rate | unknown]
    gap_impact:
      if_complete: "Confidence in rent efficiency score: High"
      if_partial: "Confidence in rent efficiency score: Medium; asking rate may not reflect final deal"
      if_unknown: "Confidence in rent efficiency score: Low; rent assumptions may be inaccurate"
    recommended_actions:
      if_complete: "Use confirmed terms in analysis"
      if_partial: "Document asking rate caveat; note that final rent may differ"
      if_unknown: "Obtain rent quote before relying on scoring results"

  zoning_constraints:
    source: [from stakeholder mapper]
    verification_status: [confirmed | preliminary | unverified]
    gap_impact:
      if_confirmed: "Confidence in zoning fit: High"
      if_preliminary: "Confidence in zoning fit: Medium; preliminary review, may miss restrictions"
      if_unverified: "Confidence in zoning fit: Low; zoning status unknown, veto risk unassessed"
    recommended_actions:
      if_confirmed: "Proceed with confirmed analysis"
      if_preliminary: "Recommend zoning verification before lease commitment"
      if_unverified: "Critical gap: obtain zoning confirmation immediately; high veto risk"
```

**Overall Confidence Rating:**
```
Calculate confidence as the lowest critical data quality:

If any critical data quality is LOW:
  Overall confidence = LOW
  Implication: Do NOT recommend proceeding without addressing gap
  Required action: Address critical gap before decision

If all critical data quality at least MEDIUM:
  Overall confidence = MEDIUM
  Implication: Proceed with caution; note uncertainties
  Required action: Note uncertainties; consider additional data collection

If all critical data quality HIGH:
  Overall confidence = HIGH
  Implication: Proceed with confidence
  Required action: Continue monitoring for changes

Critical data = demographics, competitor_data, zoning_constraints
```

### 3. Apply Zoning/Lease Vetoes
Execute hard constraints identified by stakeholder mapper.

**Veto Execution Logic:**
```python
def apply_vetoes(candidate_scores, stakeholder_analysis):
    """
    Apply veto conditions from stakeholder analysis to candidate ranking.

    Args:
        candidate_scores: list of candidates with scores from scoring engine
        stakeholder_analysis: dict of veto conditions per candidate

    Returns:
        Modified list with vetoed candidates demoted or removed
    """
    vetoed_candidates = []

    for candidate in candidate_scores:
        candidate_id = candidate['candidate_id']
        veto_status = stakeholder_analysis[candidate_id]['veto_assessment']['overall_status']

        if veto_status == 'BLOCKED':
            # Absolute veto: demote to bottom or remove
            candidate['veto_status'] = 'BLOCKED'
            candidate['veto_reasons'] = stakeholder_analysis[candidate_id]['veto_assessment']['veto_conditions']
            candidate['original_score'] = candidate['total_score']
            candidate['total_score'] = -1  # Demote to bottom
            vetoed_candidates.append(candidate_id)

        elif veto_status == 'CONDITIONAL':
            # Conditional veto: flag but keep in ranking with warning
            candidate['veto_status'] = 'CONDITIONAL'
            candidate['conditional_vetoes'] = stakeholder_analysis[candidate_id]['veto_assessment']['conditional_vetoes']
            # Keep original score; flag for review

        else:  # CLEAR
            candidate['veto_status'] = 'CLEAR'

    # Re-rank after veto adjustments
    non_vetoed = [c for c in candidate_scores if c['veto_status'] != 'BLOCKED']
    vetoed = [c for c in candidate_scores if c['veto_status'] == 'BLOCKED']

    # Sort non-vetoed by score (descending)
    non_vetoed_sorted = sorted(non_vetoed, key=lambda x: x['total_score'], reverse=True)
    vetoed_sorted = sorted(vetoed, key=lambda x: x['original_score'], reverse=True)

    # Re-assign ranks
    ranked_candidates = []
    for rank, candidate in enumerate(non_vetoed_sorted, start=1):
        candidate['rank'] = rank
        ranked_candidates.append(candidate)

    # Append vetoed candidates at bottom with no rank or "VETOED" rank
    for candidate in vetoed_sorted:
        candidate['rank'] = 'VETOED'
        ranked_candidates.append(candidate)

    return ranked_candidates
```

**Veto Output:**
```yaml
veto_analysis:
  vetoed_candidates: [list of candidates with BLOCKED status]
  veto_reasons:
    - candidate_id: [A]
      veto_status: [BLOCKED]
      veto_conditions: [list]
      cannot_proceed_reason: [explanation]
      if_override_possible: [path and probability]

  conditional_candidates: [list of candidates with CONDITIONAL status]
  conditions:
    - candidate_id: [B]
      conditional_vetoes: [list with details]
      mitigation_required: [actions to address conditions]
      if_mitigated_score: [potential score after mitigation]

  clear_candidates: [list of candidates with CLEAR status]
  ready_to_proceed: [yes, with monitoring]
```

### 4. Check for Survivorship and Analog Bias
Validate that benchmarks and analogs are appropriate.

**Survivorship Bias Check:**
```
Question: Are we comparing to successful existing locations only?

Check:
  1. List any analog locations used for comparison
  2. Verify if failed locations are excluded from comparison set
  3. Assess if success factors of analogs apply to candidate

Bias potential:
  - High: Comparing only to company's existing successful stores
  - Medium: Comparing to industry averages without understanding survivorship
  - Low: Using comprehensive industry data including failures

Mitigation:
  - If high bias potential: Explicitly state survivorship bias risk
  - Adjust confidence rating down if analogies are survivorship-biased
  - Recommend additional research on failure rates
```

**Analog Bias Check:**
```
Question: Are the analog locations truly comparable?

Check criteria:
  1. Demographic similarity (income, age, household composition)
  2. Competitive environment similarity
  3. Physical site similarity (visibility, access, co-tenancy)
  4. Market maturity similarity (greenfield vs. saturated)

Bias assessment:
  - If 3-4 criteria match: Low bias risk, analog valid
  - If 2 criteria match: Medium bias risk, use analog cautiously
  - If 0-1 criteria match: High bias risk, analog may be misleading

Action:
  - Document bias level for each analog
  - Adjust confidence based on bias assessment
  - If high bias, treat analog as qualitative reference only
```

### 5. Recommend Additional Data Collection
Identify data that would significantly improve confidence.

**Data Collection Prioritization:**
```yaml
data_collection_recommendations:
  high_priority:
    - data_type: [zoning confirmation]
      current_quality: [LOW]
      impact_on_confidence: [HIGH -> would resolve veto risk]
      collection_method: [municipal zoning portal or planning department inquiry]
      estimated_effort: [hours to days]
      estimated_cost: [low to moderate]
      urgency: [blocking decision]

    - data_type: [competitive audit]
      current_quality: [LOW or MEDIUM]
      impact_on_confidence: [HIGH -> critical for saturation analysis]
      collection_method: [field survey, online research,商业数据库]
      estimated_effort: [days to weeks]
      estimated_cost: [moderate]
      urgency: [important for accuracy]

  medium_priority:
    - data_type: [traffic count]
      current_quality: [LOW or ESTIMATED]
      impact_on_confidence: [MEDIUM -> improves accessibility scoring]
      collection_method: [manual count, traffic data purchase]
      estimated_effort: [days]
      estimated_cost: [low to moderate]
      urgency: [enhances confidence]

    - data_type: [local demographics update]
      current_quality: [MEDIUM, vintage > 2 years]
      impact_on_confidence: [MEDIUM -> refines demand estimates]
      collection_method: [purchase latest demographic data]
      estimated_effort: [days]
      estimated_cost: [moderate]
      urgency: [nice to have]

  optional_enhancement:
    - data_type: [customer research]
      current_quality: [not currently available]
      impact_on_confidence: [LOW -> nice to have for validation]
      collection_method: [surveys, focus groups, intercept interviews]
      estimated_effort: [weeks]
      estimated_cost: [high]
      urgency: [optional for long-term refinement]
```

**Recommendation Logic:**
```
For each data gap:
  1. Assess current impact on confidence (HIGH/MEDIUM/LOW)
  2. Estimate effort and cost to fill gap
  3. Calculate ROI: confidence gain vs. effort
  4. Prioritize: HIGH impact + LOW effort = immediate action
  5. De-prioritize: LOW impact + HIGH effort = optional enhancement

Output recommendation:
  - Must-have before decision: [list]
  - Nice-to-have before decision: [list]
  - Optional for future refinement: [list]
```

## Output Format

The sub-quality-reviewer outputs a comprehensive quality assessment:

```yaml
quality_review:
  analysis_date: [YYYY-MM-DD]
  reviewer: [sub-quality-reviewer]

  assumption_stress_tests:
    distance_decay_lambda:
      assumption: [value used]
      challenge: [alternative tested]
      sensitivity_result: [robust | fragile]
      if_fragile: [ranking change noted]
      conclusion: [acceptable | needs refinement | critical uncertainty]

    attractiveness_proxy:
      assumption: [proxy used]
      challenge: [alternative tested]
      sensitivity_result: [robust | fragile]
      if_fragile: [ranking change noted]
      conclusion: [acceptable | needs refinement | critical uncertainty]

    spend_per_capita:
      assumption: [value or source used]
      challenge: [alternative tested]
      sensitivity_result: [robust | fragile]
      if_fragile: [ranking change noted]
      conclusion: [acceptable | needs refinement | critical uncertainty]

    trade_area_boundaries:
      assumption: [boundaries defined]
      challenge: [alternative tested]
      sensitivity_result: [robust | fragile]
      if_fragile: [ranking change noted]
      conclusion: [acceptable | needs refinement | critical uncertainty]

    competitive_set_completeness:
      assumption: [completeness asserted]
      challenge: [alternative tested]
      sensitivity_result: [robust | fragile]
      if_fragile: [ranking change noted]
      conclusion: [acceptable | needs refinement | critical uncertainty]

  data_quality_assessment:
    demographic_data:
      source: [citation]
      vintage: [year]
      quality: [HIGH | MEDIUM | LOW]
      gap_impact: [description]
      recommended_action: [specific steps]

    competitor_data:
      source: [citation]
      completeness: [percentage]
      quality: [HIGH | MEDIUM | LOW]
      gap_impact: [description]
      recommended_action: [specific steps]

    traffic_footfall_data:
      source: [citation]
      quality: [HIGH | MEDIUM | LOW]
      gap_impact: [description]
      recommended_action: [specific steps]

    rent_lease_terms:
      source: [citation]
      quality: [HIGH | MEDIUM | LOW]
      gap_impact: [description]
      recommended_action: [specific steps]

    zoning_constraints:
      source: [citation]
      quality: [HIGH | MEDIUM | LOW]
      gap_impact: [description]
      recommended_action: [specific steps]

  overall_confidence_rating: [HIGH | MEDIUM | LOW]
  confidence_rationale: [explanation based on critical data quality]

  veto_execution:
    candidates_vetoed: [list of BLOCKED candidates with reasons]
    candidates_conditional: [list of CONDITIONAL candidates with mitigations]
    candidates_clear: [list of CLEAR candidates]

  bias_check:
    survivorship_bias: [assessed risk level and mitigation]
    analog_bias: [assessed risk level and mitigation]
    overall_bias_risk: [LOW | MEDIUM | HIGH]

  data_collection_recommendations:
    must_have_before_decision: [list of critical gaps]
    nice_to_have_before_decision: [list of useful enhancements]
    optional_for_future_refinement: [list of future improvements]

  final_recommendation:
    ready_to_recommend: [yes | no]
    if_no:
      blocking_issues: [list]
      required_actions: [list]
    if_yes:
      recommended_candidate: [name]
      confidence_level: [HIGH | MEDIUM | LOW]
      conditions: [any conditions or monitoring recommendations]
      caveats: [any remaining uncertainties]

  quality_gates_status:
    assumptions_stress_tested: [yes, count of >= 3]
    data_gaps_flagged: [yes]
    confidence_assigned: [yes]
    vetoes_applied: [yes]
    bias_checked: [yes]
    data_collection_prioritized: [yes]
```

## Quality Gates

The sub-quality-reviewer must pass ALL quality gates:

1. **Assumptions Challenged**: Minimum 3 key assumptions must be stress-tested with sensitivity analysis. More is better.

2. **Confidence Rating Assigned**: Overall confidence (High/Medium/Low) must be stated with rationale tied to data quality.

3. **Data Gaps Flagged**: All data quality issues must be explicitly listed with impact assessment.

4. **Vetoes Applied**: All veto conditions from stakeholder mapper must be executed and reflected in final ranking.

5. **Bias Checked**: Survivorship and analog bias must be assessed and documented.

6. **Data Collection Prioritized**: Recommendations for additional data must be prioritized by impact and effort.

## Error Handling

**All Candidates Vetoed:**
```
If all candidates have BLOCKED veto status:
  1. Return "NO VIABLE CANDIDATES" recommendation
  2. List all veto conditions by candidate
  3. Suggest either:
     - Modify criteria (if user flexibility exists)
     - Search for new candidates
     - Negotiate veto conditions (if conditional)
  4. Do NOT force a recommendation among blocked candidates
```

**Critical Data Gaps:**
```
If critical data quality is LOW across ALL candidates:
  1. Set overall confidence to LOW
  2. Do NOT make definitive recommendation
  3. Recommend data collection before decision
  4. Present preliminary ranking as "preliminary, subject to change with better data"
  5. If user insists on proceeding, explicitly document risks
```

**Fragile Assumptions:**
```
If multiple assumptions show fragility in sensitivity analysis:
  1. Flag as "HIGH UNCERTAINTY" analysis
  2. Present multiple scenarios (optimistic, base, pessimistic)
  3. Recommend conservative approach (select candidate robust across scenarios)
  4. Do NOT present fragile ranking as definitive
```

## Integration Points

- **Calls**: None (analyzes outputs from other sub-skills)
- **Called By**: main.md (retail-location-intelligence)
- **Inputs From**: All other sub-skills (requirements-gatherer, trade-area-modeler, scoring-engine, stakeholder-mapper)
- **Outputs To**: main.md (final recommendation, confidence, caveats)

## Framework Citations

**Decision Quality and Risk Analysis:**
- Hammond, J. S., et al. (1998). "The Hidden Traps in Decision Making." Harvard Business Review.
- Kahneman, D., & Tversky, A. (Eds.). (2000). Choices, Values, and Frames. Cambridge University Press.

**Retail Location Risk Assessment:**
- Hernández, T., & Bennison, D. (2000). "The art and science of retail location decisions." International Journal of Retail & Distribution Management.
