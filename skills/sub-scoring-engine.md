---
name: sub-scoring-engine
description: Computes a transparent weighted multi-criteria score per candidate retail site and produces a defensible ranking. Shared across business-operations cluster.
---

## Purpose
Transform heterogeneous evidence—demand estimates, accessibility metrics, competitive positioning, rent efficiency, and constraint fit—into a single, transparent, defensible site ranking. The scoring engine ensures decision criteria are explicit, weights are justified, and no hidden biases drive the recommendation.

## Inputs
- Trade area analysis outputs (from sub-trade-area-modeler)
- Stakeholder constraints (from sub-stakeholder-mapper)
- Site-specific data: accessibility, visibility, footfall, rent, zoning
- User preferences (if any): criteria priorities, weight adjustments

## Procedure

### 1. Define Scoring Criteria
Establish the evaluation dimensions that matter for the specific retail format.

**Core Criteria (Universal):**
```yaml
criteria:
  demand_capture:
    description: "Estimated annual demand from Huff model"
    metric: "Annual revenue estimate ($)"
    source: "sub-trade-area-modeler"
    weight_default: 0.30
    weight_justification: "Primary revenue driver; fundamental to viability"

  competitive_position:
    description: "Competitive saturation and differentiation opportunity"
    metric: "Saturation index (inverted) and gap score"
    source: "sub-trade-area-modeler"
    weight_default: 0.20
    weight_justification: "Market entry difficulty; affects pricing power and market share"

  accessibility_visibility:
    description: "Ease of customer access and storefront visibility"
    metric: "Composite of traffic count, visibility rating, entry/exit ease"
    source: "Site evaluation or traffic data"
    weight_default: 0.15
    weight_justification: "Drive-by traffic and convenience factor; affects volume"

  rent_efficiency:
    description: "Rent cost relative to demand potential"
    metric: "Rent as percentage of estimated demand"
    source: "sub-requirements-gatherer + demand estimate"
    weight_default: 0.15
    weight_justification: "Direct impact on profitability and payback period"

  co_tenancy_quality:
    description: "Presence of complementary anchors and absence of conflicts"
    metric: "Synergy score from co-tenant analysis"
    source: "Site lease document or observation"
    weight_default: 0.10
    weight_justification: "Traffic generation from anchors; avoid cannibalization"

  zoning_fit:
    description: "Permitted use compatibility and ease of permitting"
    metric: "Zoning match score and permit complexity rating"
    source: "sub-stakeholder-mapper"
    weight_default: 0.10
    weight_justification: "Hard constraint; can veto regardless of other factors"
```

**Format-Specific Criteria (conditional):**
```yaml
format_specific:
  # For F&B
  grease_trap_sewer:
    description: "Existing grease trap and sewer capacity"
    weight_if_applicable: 0.05
    condition: "category includes food preparation"

  # For auto-dependent formats
  parking_adequacy:
    description: "Parking spaces relative to expected peak demand"
    weight_if_applicable: 0.05
    condition: "format requires customer parking"

  # For destination retail
  pad_visibility:
    description: "Freestanding visibility from main thoroughfare"
    weight_if_applicable: 0.05
    condition: "format is standalone or pad building"

  # For urban formats
  transit_access:
    description: "Proximity to public transit and pedestrian volume"
    weight_if_applicable: 0.05
    condition: "format is transit-oriented or urban"
```

### 2. Assign and Justify Weights
Each criterion receives a weight reflecting its importance to the specific retail format and situation.

**Default Weight Sets (by Category):**
```yaml
default_weights:
  convenience_f_b:  # Quick service, convenience store
    demand_capture: 0.25
    competitive_position: 0.20
    accessibility_visibility: 0.25  # Higher for convenience
    rent_efficiency: 0.15
    co_tenancy_quality: 0.10
    zoning_fit: 0.05

  destination_restaurant:  # Fine dining, destination retail
    demand_capture: 0.30
    competitive_position: 0.25  # Higher for destination (less foot traffic)
    accessibility_visibility: 0.10
    rent_efficiency: 0.10
    co_tenancy_quality: 0.15  # Synergy matters more
    zoning_fit: 0.10

  grocery:
    demand_capture: 0.35
    competitive_position: 0.25
    accessibility_visibility: 0.15
    rent_efficiency: 0.10
    co_tenancy_quality: 0.05
    zoning_fit: 0.10

  professional_services:
    demand_capture: 0.25
    competitive_position: 0.20
    accessibility_visibility: 0.15
    rent_efficiency: 0.20  # Higher impact on service businesses
    co_tenancy_quality: 0.10
    zoning_fit: 0.10
```

**Weight Justification Template:**
```
For each criterion:
  - State the assigned weight
  - Explain the business rationale
  - Cite relevant framework or research (if applicable)
  - Note any user-provided priorities that influenced the weight

Example:
  Criterion: Accessibility & Visibility
  Weight: 0.25
  Rationale: For convenience formats, foot traffic and visibility are primary drivers of impulse visits. Research shows 65% of convenience store customers are walk-by or drive-by traffic (NACS, 2023). Higher weight reflects this sensitivity.
```

**User Adjustments:**
```
Allow user to:
  1. Adjust weights within ±20% of default (to prevent gaming)
  2. Swap priorities (e.g., prioritize rent efficiency over accessibility)
  3. Add custom criteria with justification
  4. Exclude criteria only if business case provided

Process for adjustment:
  1. User requests change
  2. System explains impact of change
  3. System shows sensitivity (how rankings change)
  4. User confirms or revises
  5. Document adjustment and rationale in output
```

### 3. Normalize Criteria to Common Scale
Convert each criterion to a 0-100 scale for comparability.

**Normalization Methods by Criterion Type:**

**A. Higher-is-Better Metrics (direct normalization):**
```python
def normalize_higher_better(value, min_value, max_value):
    """
    Normalize metric where higher values are better.
    """
    if max_value == min_value:
        return 50  # All equal, return middle score
    return ((value - min_value) / (max_value - min_value)) * 100

# Example: Demand capture
# demand_values = [500000, 750000, 1000000]
# normalized = [0, 50, 100] for candidate with lowest, middle, highest demand
```

**B. Lower-is-Better Metrics (inverse normalization):**
```python
def normalize_lower_better(value, min_value, max_value):
    """
    Normalize metric where lower values are better.
    """
    if max_value == min_value:
        return 50
    return ((max_value - value) / (max_value - min_value)) * 100

# Example: Rent as percentage of demand
# rent_pct_values = [15%, 20%, 25%]
# normalized = [100, 50, 0] for lowest, middle, highest rent burden
```

**C. Categorical Metrics (mapping to scale):**
```python
def normalize_categorical(category, mapping):
    """
    Convert categorical rating to 0-100 score.
    """
    return mapping.get(category, 50)  # Default to middle if unknown

# Example: Zoning fit
# zoning_mapping = {
#     "permitted_by_right": 100,
#     "conditional_use_possible": 70,
#     "variance_required": 40,
#     "not_permitted": 0,
#     "unknown": 50
# }
```

**D. Composite Metrics (weighted sub-criteria):**
```python
def normalize_composite(sub_metrics, weights):
    """
    Calculate composite score from multiple sub-metrics.
    """
    normalized_scores = []
    for metric, weight in zip(sub_metrics, weights):
        normalized = normalize(metric['value'], metric['min'], metric['max'], metric['direction'])
        normalized_scores.append(normalized * weight)
    return sum(normalized_scores)

# Example: Accessibility & Visibility composite
# sub_metrics = [
#     {'value': 12000, 'min': 5000, 'max': 20000, 'direction': 'higher', 'weight': 0.4},  # Daily traffic
#     {'value': 'good', 'mapping': visibility_map, 'weight': 0.3},  # Visibility rating
#     {'value': 2, 'min': 1, 'max': 5, 'direction': 'higher', 'weight': 0.3},  # Entry/exit rating
# ]
```

**Normalization Implementation:**
```yaml
normalization:
  demand_capture:
    method: linear
    direction: higher_is_better
    min: [minimum demand across candidates]
    max: [maximum demand across candidates]
    formula: "(value - min) / (max - min) × 100"

  competitive_position:
    method: categorical_inversion
    saturation_mapping:
      low: 100
      medium: 60
      high: 20
    gap_adjustment: "+20 if significant gap identified"

  accessibility_visibility:
    method: composite
    components:
      daily_traffic_count:
        weight: 0.5
        normalization: linear, higher_is_better
      visibility_rating:
        weight: 0.3
        mapping: {excellent: 100, good: 75, fair: 50, poor: 25}
      entry_exit_ease:
        weight: 0.2
        mapping: {excellent: 100, good: 75, fair: 50, poor: 25}

  rent_efficiency:
    method: linear
    direction: lower_is_better
    metric: "rent_as_pct_of_demand"
    formula: "(max - value) / (max - min) × 100"

  co_tenancy_quality:
    method: composite
    components:
      anchor_quality:
        weight: 0.4
        mapping: {national_anchor: 100, regional: 75, local: 50, none: 25}
      complementarity:
        weight: 0.3
        mapping: {high: 100, medium: 75, low: 50, conflict: 0}
      vacancy_rate:
        weight: 0.2
        direction: lower_is_better
      cannibalization_risk:
        weight: 0.1
        mapping: {none: 100, low: 75, medium: 50, high: 0}

  zoning_fit:
    method: categorical_mapping
    mapping:
      permitted_by_right: 100
      permitted_with minor conditions: 85
      conditional_use_standard: 70
      conditional_use_challenging: 50
      variance_required: 30
      not_permitted: 0
      unknown: 50
```

### 4. Compute Weighted Scores
Calculate final scores and ranking for each candidate.

**Score Calculation:**
```python
def calculate_candidate_score(candidate, criteria, weights):
    """
    Calculate weighted score for a single candidate.

    Args:
        candidate: dict with all normalized criterion scores
        criteria: list of criterion names
        weights: dict of criterion -> weight

    Returns:
        Total score and per-criterion contributions
    """
    total_score = 0
    contributions = {}

    for criterion in criteria:
        normalized_score = candidate.get(f'{criterion}_normalized', 50)  # Default to 50 if missing
        weight = weights.get(criterion, 0)

        contribution = normalized_score * weight
        contributions[criterion] = contribution
        total_score += contribution

    return {
        'total_score': round(total_score, 2),
        'contributions': contributions,
        'rank': None  # To be assigned after all candidates scored
    }


def rank_all_candidates(candidates_with_scores):
    """
    Assign ranks based on total scores.

    Args:
        candidates_with_scores: list of candidate dicts with total_score

    Returns:
        List with ranks assigned (ties get same rank)
    """
    sorted_candidates = sorted(
        candidates_with_scores,
        key=lambda x: x['total_score'],
        reverse=True
    )

    for rank, candidate in enumerate(sorted_candidates, start=1):
        candidate['rank'] = rank

        # Handle ties: if same score as previous, same rank
        if rank > 1 and candidate['total_score'] == sorted_candidates[rank-2]['total_score']:
            candidate['rank'] = sorted_candidates[rank-2]['rank']

    return sorted_candidates
```

**Score Output Format:**
```yaml
candidate_scores:
  - candidate_id: A
    candidate_name: [name]

    normalized_scores:
      demand_capture: [0-100]
      competitive_position: [0-100]
      accessibility_visibility: [0-100]
      rent_efficiency: [0-100]
      co_tenancy_quality: [0-100]
      zoning_fit: [0-100]

    weighted_contributions:
      demand_capture: [score × weight]
      competitive_position: [score × weight]
      accessibility_visibility: [score × weight]
      rent_efficiency: [score × weight]
      co_tenancy_quality: [score × weight]
      zoning_fit: [score × weight]

    total_score: [sum of weighted contributions, 0-100]
    rank: [position]

    strengths: [criteria where score > 75]
    weaknesses: [criteria where score < 40]
    improvement_opportunities: [low-score criteria with potential for improvement]
```

### 5. Show Per-Criterion Contributions
Ensure full transparency—no black box.

**Contribution Breakdown Table:**
```yaml
scoring_transparency:
  weights_applied:
    demand_capture: [weight and justification]
    competitive_position: [weight and justification]
    accessibility_visibility: [weight and justification]
    rent_efficiency: [weight and justification]
    co_tenancy_quality: [weight and justification]
    zoning_fit: [weight and justification]

  ranking_table:
    | Rank | Candidate | Demand | Competition | Access | Rent | Co-tenancy | Zoning | Total |
    |------|-----------|--------|-------------|--------|------|------------|--------|-------|
    | 1    | A         | 85     | 72          | 90     | 65   | 80         | 95     | 81.2  |
    | 2    | B         | 90     | 65          | 70     | 85   | 75         | 95     | 79.8  |
    | 3    | C         | 70     | 85          | 80     | 90   | 70         | 40     | 72.5  |

    # Legend: Numbers are normalized scores (0-100) before weighting
```

**Score Interpretation Guide:**
```
90-100: Excellent position, clear leader
75-89: Strong position, viable candidate
60-74: Adequate position, some concerns
40-59: Weak position, significant concerns
<40: Poor position, not recommended without major mitigations
```

### 6. Analyze Sensitivity
Identify which weight or assumption changes would flip the ranking.

**Sensitivity Analysis:**
```python
def sensitivity_analysis(candidate_scores, criteria, weights, threshold=5.0):
    """
    Identify which criteria, if weights changed, would flip ranking.

    Args:
        candidate_scores: list of candidates with scores
        criteria: list of criterion names
        weights: current weights
        threshold: minimum score difference to analyze (default 5 points)

    Returns:
        Dict of criteria where weight change would flip rank 1/2
    """
    sensitivity_report = []

    # Sort candidates by current score
    sorted_candidates = sorted(candidate_scores, key=lambda x: x['total_score'], reverse=True)

    # Check if top 2 are close
    if len(sorted_candidates) >= 2:
        score_gap = sorted_candidates[0]['total_score'] - sorted_candidates[1]['total_score']

        if score_gap < threshold:
            # For each criterion, calculate required weight change to flip
            for criterion in criteria:
                # Calculate score difference on this criterion
                criterion_gap = (
                    sorted_candidates[0].get(f'{criterion}_normalized', 50) -
                    sorted_candidates[1].get(f'{criterion}_normalized', 50)
                )

                # Required weight change = score_gap / criterion_gap
                if criterion_gap != 0:
                    required_change = abs(score_gap / criterion_gap)
                    current_weight = weights[criterion]

                    sensitivity_report.append({
                        'criterion': criterion,
                        'current_weight': current_weight,
                        'required_change': required_change,
                        'new_weight_if_increased': current_weight + required_change,
                        'new_weight_if_decreased': current_weight - required_change,
                        'would_flip': required_change < 0.1  # If <10% change needed, flag as sensitive
                    })

    return sensitivity_report
```

**Sensitivity Output:**
```yaml
sensitivity_analysis:
  score_gap_rank_1_2: [points]
  sensitive_criteria:
    - criterion: [name]
      current_weight: [value]
      weight_change_to_flip: [points]
      new_weight_if_flipped: [value]
      interpretation: "[Small/Medium/Large] change required; ranking [is/is not] fragile"

  robust_interpretation:
    if score_gap > 15:
      message: "Ranking is robust. Large (>15 point) gap between top candidates."
    elif score_gap > 5:
      message: "Ranking moderately stable. Moderate gap between top candidates."
    else:
      message: "Ranking fragile. Small gap between top candidates; small weight changes could flip."

  recommendations:
    if fragile:
      - "Collect additional data on [sensitive criteria] to reduce uncertainty"
      - "Consider joint development or phased entry if both sites viable"
    else:
      - "Proceed with top-ranked candidate with confidence"
```

## Output Format

The sub-scoring-engine outputs a comprehensive ranking with full transparency:

```yaml
scoring_results:
  analysis_date: [YYYY-MM-DD]
  retail_format: [from requirements]

  criteria_and_weights:
    demand_capture:
      weight: 0.25
      justification: "[rationale]"
      source: "sub-trade-area-modeler"
      normalization: "linear, higher_better"
    competitive_position:
      weight: 0.20
      justification: "[rationale]"
      source: "sub-trade-area-modeler"
      normalization: "categorical_inversion"
    # ... all criteria with full documentation

  candidates_ranked:
    - rank: 1
      candidate_id: A
      candidate_name: [name]
      total_score: [0-100]

      normalized_scores:
        demand_capture: [score]
        competitive_position: [score]
        accessibility_visibility: [score]
        rent_efficiency: [score]
        co_tenancy_quality: [score]
        zoning_fit: [score]

      weighted_contributions:
        demand_capture: [score × weight]
        competitive_position: [score × weight]
        accessibility_visibility: [score × weight]
        rent_efficiency: [score × weight]
        co_tenancy_quality: [score × weight]
        zoning_fit: [score × weight]

      strengths:
        - criterion: [name]
          score: [value]
          interpretation: [why this is a strength]
      weaknesses:
        - criterion: [name]
          score: [value]
          interpretation: [why this is a weakness and how to address]

    - rank: 2
      # Same structure for all candidates

  ranking_summary:
    leader: [candidate name]
    leader_score: [value]
    runner_up: [candidate name]
    runner_up_score: [value]
    score_gap: [leader_score - runner_up_score]
    interpretation: [robust | fragile]

  sensitivity_analysis:
    score_gap_rank_1_2: [points]
    fragile: [boolean]
    sensitive_criteria: [list where small weight changes would flip]
    recommendations: [based on fragility]

  transparency:
    weights_justified: [yes | no]
    per_criterion_contributions_shown: [yes | no]
    sensitivity_analyzed: [yes | no]
    data_sources_cited: [yes | no]
```

## Quality Gates

The sub-scoring-engine must pass ALL quality gates:

1. **Weights Justified**: Every criterion weight must have a written justification linking to business impact or research.

2. **Per-Criterion Contributions Shown**: Output must include a breakdown table showing each criterion's contribution to the total score.

3. **Sensitivity Stated**: If the top two candidates are within 5 points, sensitivity analysis must identify which criteria could flip the ranking.

4. **No Hidden Criteria**: All criteria used in scoring must be explicitly listed and documented. No "gut feel" adjustments.

5. **Normalization Documented**: The method for converting raw metrics to 0-100 scale must be stated for each criterion.

6. **Data Sources Cited**: Each criterion's source (which sub-skill or external data) must be cited.

## Error Handling

**Missing Criterion Data:**
```
If a candidate lacks data for a criterion:
  1. Assign score of 50 (neutral) if data truly unavailable
  2. Flag as "missing data, neutral score assigned"
  3. Note in output which criteria used neutral scores
  4. If critical criterion (weight > 0.25) missing, flag as high uncertainty
  5. Recommend data collection before final decision
```

**Extreme Outliers:**
```
If one candidate dominates on a single criterion (e.g., 3x demand of others):
  1. Check for data errors or estimation issues
  2. If valid, note as "outlier" in interpretation
  3. Verify ranking is robust and not solely driven by one criterion
  4. If single criterion dominates ranking, flag for quality review
  5. Present alternative ranking with outlier criterion capped
```

**Tie Scores:**
```
If two or more candidates have identical or near-identical total scores:
  1. Assign same rank (e.g., both Rank 1)
  2. Compare per-criterion scores to identify differentiators
  3. Note qualitative differences not captured in scoring
  4. Present both as "co-leaders" with trade-offs
  5. Recommend deeper analysis or pilot testing if both viable
```

## Integration Points

- **Calls**: None (receives data from other sub-skills)
- **Called By**: main.md (retail-location-intelligence)
- **Inputs From**: sub-requirements-gatherer (rent, site details), sub-trade-area-modeler (demand, competition), sub-stakeholder-mapper (zoning, constraints)
- **Outputs To**: main.md (ranking table), sub-quality-reviewer (scores for validation)

## Framework Citations

**Multi-Criteria Decision Analysis (MCDA):**
- Saaty, T. L. (1980). The Analytic Hierarchy Process. New York: McGraw-Hill.
- Keeney, R. L., & Raiffa, H. (1976). Decisions with Multiple Objectives. New York: Wiley.

**Retail Site Selection Criteria:**
- Jones, K., & Simmons, J. (1993). Location, Location, Location. Nelson Canada.
- Hernández, T., & Bennison, D. (2000). "The art and science of retail location decisions." International Journal of Retail & Distribution Management.
