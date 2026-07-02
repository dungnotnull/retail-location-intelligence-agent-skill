---
name: sub-trade-area-modeler
description: Estimates catchment area, demand capture, and competitive saturation per candidate site using the Huff gravity model, Reilly's Law, and Christaller central-place theory.
---

## Purpose
Quantify how much consumer demand each candidate site can realistically capture based on geographic proximity, population distribution, competitor locations, and retail attractiveness factors. This sub-skill transforms demographic and competitive data into actionable demand estimates.

## Inputs
- Geocoded candidate sites (from sub-requirements-gatherer)
- Target customer demographic profile (from sub-requirements-gatherer)
- Retail format and attractiveness factors (from sub-requirements-gatherer)
- External data: census demographics, competitor locations, traffic patterns

## Procedure

### 1. Define Catchment Area
Establish the geographic boundaries from which the site will draw customers.

**Catchment Definition Methods:**

**A. Drive-Time Isochrone (Primary Method)**
```
Parameters:
- Primary catchment: [5, 7, 10] minutes drive time (adjust by format)
- Secondary catchment: [10, 15, 20] minutes drive time
- Tertiary catchment: [20, 30, 45] minutes drive time

Format-specific defaults:
- Convenience/F&B: 3min primary, 7min secondary, 15min tertiary
- Grocery: 5min primary, 10min secondary, 20min tertiary
- Destination retail: 10min primary, 20min secondary, 30min tertiary
- Services: 7min primary, 15min secondary, 30min tertiary
```

**B. Distance Ring (Fallback/Secondary Method)**
```
Parameters:
- Primary: [0.5, 1.0, 1.5] miles or [1, 2, 3] km
- Secondary: [1.5, 2.5, 3.5] miles or [2.5, 4, 6] km
- Tertiary: [3.5, 5.0, 7.5] miles or [6, 8, 12] km

Use when: Drive-time data unavailable, for comparison, or for quick estimates
```

**C. Road Network Buffer (Tertiary Method)**
```
Parameters:
- Buffer distance along road network from site
- Accounts for natural barriers (rivers, highways, railways)
- Use for urban canyon environments or complex topography

Implementation:
  1. Extract road network from site coordinates
  2. Apply buffer distance (e.g., 1km along roads)
  3. Clip to maximum straight-line distance (e.g., 2km Euclidean)
  4. Result = realistic service area
```

**Barriers and Exclusions:**
```
Identify and exclude:
- Natural barriers: rivers, mountains, parks (non-commercial)
- Infrastructure barriers: highways without crossings, railroad lines
- Jurisdictional boundaries: if relevant to concept
- Competitor exclusion zones: if user-specified

Apply barrier reduction:
  - Reduce catchment area by estimated barrier impact (%)
  - Document which barriers and reduction rationale
```

**Catchment Output Format:**
```yaml
catchment:
  method: [drive_time | distance_ring | road_network]
  parameters:
    primary:
      value: [minutes or distance]
      area_sq_km: [calculated]
      population_estimated: [from demographics]
    secondary:
      value: [minutes or distance]
      area_sq_km: [calculated]
      population_estimated: [from demographics]
    tertiary:
      value: [minutes or distance]
      area_sq_km: [calculated]
      population_estimated: [from demographics]
  barriers_identified: [list]
  barrier_adjustments: [reductions applied]
```

### 2. Pull and Process Demographic Data
Extract population and spending power within each catchment ring.

**Data Sources (by region):**
```
North America:
- US Census Bureau: data.census.gov (ACS 5-year estimates)
- Statistics Canada: statcan.gc.ca
- Mexico: INEGI

Europe:
- Eurostat: ec.europa.eu/eurostat
- UK: ONS census data
- National statistics offices (country-specific)

Asia-Pacific:
- Australia: ABS
- Japan: Statistics Bureau
- Singapore: Department of Statistics
- Country-specific census portals

Fallback:
- WorldPop: worldpop.org (global grid population)
- LandScan: high-resolution global population
- Commercial: ESRI Demographics, Nielsen, Claritas (if licensed)
```

**Demographic Variables to Extract:**
```
Required:
- Total population (by catchment ring)
- Population by age (matching target customer)
- Population by household income (matching target customer)
- Household count and average size

Recommended:
- Population by education (for professional services)
- Population by occupation (for B2B services)
- Daytime population (if available, for office/retail)
- Vehicle ownership (for auto-dependent concepts)

Enhanced:
- Consumer spending by category (if available)
- Disposable income (if available)
- Population growth projections (if available)
```

**Data Processing:**
```
For each catchment ring:
1. Query demographic data source for defined boundary
2. Extract variables for target customer profile match
3. Normalize to per-capita and per-household metrics
4. Apply data vintage adjustment (if older than 2 years, apply growth factor)
5. Calculate effective market size:
   - Total population × segment match % × spending power index
```

**Vintage Handling:**
```
If data vintage > 2 years:
  - Apply regional growth factor (from projections or recent trends)
  - Flag as "adjusted for growth, base vintage: [year]"
  - Reduce confidence rating accordingly

If only national/regional data available:
  - Apply downscaling based on built-up area or nighttime lights
  - Flag as "scaled from [regional level], low precision"
  - Use only as order-of-magnitude estimate
```

**Demographic Output Format:**
```yaml
demographics:
  data_source: [source name]
  data_vintage: [year]
  confidence: [high | medium | low]
  primary_catchment:
    total_population: [number]
    target_segment_population: [number]
    target_segment_percentage: [calculated]
    median_income: [amount]
    household_count: [number]
    average_household_size: [decimal]
    day_population_if_available: [number]
    spending_power_index: [normalized to 100]
  secondary_catchment: [same structure]
  tertiary_catchment: [same structure]
  adjustments:
    growth_factor_applied: [if applicable]
    scaling_method: [if applicable]
    notes: [any relevant concerns]
```

### 3. Apply Huff Gravity Model
Calculate the probability that consumers in the trade area will choose each candidate site.

**Huff Model Formula:**
```
P(i,j) = (A_j^α / D_ij^λ) / Σ(A_k^α / D_ik^λ)

Where:
- P(i,j) = probability that consumer at location i chooses site j
- A_j = attractiveness of site j
- α = attractiveness sensitivity parameter (default 1.0)
- D_ij = distance from consumer location i to site j
- λ = distance decay parameter (default 2.0)
- k = all competing sites in the consideration set
```

**Parameter Specification:**
```yaml
huff_parameters:
  distance_decay_lambda:
    value: [2.0 is default]
    justification: "[cite Huff 1964 or later calibration]"
    format_specific_adjustments:
      convenience_foods: [2.5-3.0, higher sensitivity to distance]
      grocery: [2.0-2.5]
      destination_restaurant: [1.5-2.0, lower sensitivity]
      shopping_goods: [1.5-2.0]
  attractiveness_sensitivity_alpha:
    value: [1.0 is default]
    justification: "[standard formulation]"
```

**Attractiveness Proxy (A_j):**
```
Choose primary proxy based on available data:
1. Floor area (sq ft) - most common, directly available
2. Number of parking spaces - correlates with capacity
3. Employee count (FTE) - operational capacity proxy
4. Brand presence score (if multi-location brand) - brand equity
5. Composite index = weighted sum of above factors

For new sites (no operational data):
  - Use proposed floor area
  - Adjust for co-tenancy anchor effect (+20% if next to major anchor)
  - Adjust for signage visibility (+10% if prominent)
  - Document all adjustments

For competitive sites:
  - Estimate floor area from observation (satellite, street view)
  - Use industry averages if direct observation unavailable
  - Flag estimation uncertainty
```

**Distance Calculation (D_ij):**
```
Choose metric based on format:
1. Network distance (driving distance) - best for auto-dependent formats
2. Network time (driving time) - best when time matters more than distance
3. Euclidean distance - fallback only, note as approximation
4. Walking time - for urban, pedestrian-oriented formats

Implementation:
  - Use routing service (OSRM, Google Maps, Mapbox)
  - Calculate from population centroids or census block centroids
  - For approximation, use distance decay formula with appropriate barrier adjustment
```

**Consideration Set:**
```
Include in competitive set:
- All direct competitors within extended tertiary catchment
- Major indirect competitors (e.g., supermarket vs. grocery)
- Proposed candidate sites (all, to assess cannibalization if multi-site)

Exclude:
- Competitors outside reasonable trade area
- Failed/closed competitors (unless relevant for saturation analysis)
- Competitors with different target customer (document rationale)
```

**Probability Calculation:**
```python
# Pseudo-code for Huff calculation
def calculate_huff_probability(consumer_location, candidate_site, competitors, lambda=2.0, alpha=1.0):
    """
    Calculate Huff probability for a single consumer location.

    Args:
        consumer_location: (lat, lng) of consumer
        candidate_site: site dict with lat, lng, attractiveness
        competitors: list of competitor dicts with lat, lng, attractiveness
        lambda: distance decay parameter
        alpha: attractiveness sensitivity

    Returns:
        Probability value [0, 1] for candidate site
    """
    sites = [candidate_site] + competitors

    def utility(site):
        distance = calculate_network_distance(consumer_location, site['coordinates'])
        return (site['attractiveness'] ** alpha) / (distance ** lambda)

    utilities = [utility(s) for s in sites]
    total_utility = sum(utilities)

    return utilities[0] / total_utility if total_utility > 0 else 0


def aggregate_catchment_probability(candidate_site, population_grid, competitors, params):
    """
    Aggregate Huff probability across all consumer locations in catchment.

    Args:
        candidate_site: site being evaluated
        population_grid: array of (lat, lng, population) tuples
        competitors: all competitors
        params: Huff parameters (lambda, alpha)

    Returns:
        Weighted average capture probability for entire catchment
    """
    total_population = 0
    weighted_probability = 0

    for lat, lng, pop in population_grid:
        prob = calculate_huff_probability(
            (lat, lng), candidate_site, competitors,
            params['lambda'], params['alpha']
        )
        weighted_probability += prob * pop
        total_population += pop

    return weighted_probability / total_population if total_population > 0 else 0
```

**Huff Output Format:**
```yaml
huff_model:
  framework: "Huff Probabilistic Gravity Model (Huff 1964)"
  parameters:
    distance_decay_lambda: [value]
    lambda_justification: [citation or calibration source]
    attractiveness_sensitivity_alpha: [value]
    attractiveness_proxy: [floor_area | parking | composite]
    distance_metric: [network_distance | network_time | euclidean]
  consideration_set:
    candidate_count: [number]
    competitor_count: [number]
    total_sites: [number]
    competitor_details: [list with locations, attractiveness]
  results:
    primary_catchment:
      capture_percentage: [weighted average %]
      population_weighted: [yes | no]
      spatial_distribution: [uniform | clustered | description]
    secondary_catchment: [same structure]
    tertiary_catchment: [same structure]
    overall_capture_probability: [catchment-weighted average]
```

### 4. Estimate Demand Capture
Convert capture probability into monetary demand estimates.

**Spend Per Capita Estimation:**
```
Sources:
1. Census/consumer expenditure surveys (national, regional, local if available)
2. Industry benchmarks (IBISWorld, Euromonitor, Statista, category associations)
3. Company internal data (if existing locations)
4. Analog method: similar stores in similar trade areas

Formula:
  per_capita_annual_spend = [from source above]
  trade_area_spend = catchment_population × per_capita_spend × segment_match_index
  demand_capture = trade_area_spend × huff_capture_percentage
```

**Segment Match Index:**
```
Adjust total population spend by target customer match:

segment_match_index = (
    (target_age_pop / total_pop) × age_weight +
    (target_income_pop / total_pop) × income_weight +
    (target_household_pop / total_pop) × household_weight
)

Where weights sum to 1.0 and reflect category sensitivity.
Default weights: age=0.4, income=0.4, household=0.2
```

**Demand Capture Calculation:**
```yaml
demand_estimation:
  methodology:
    per_capita_spend_source: [source citation]
    per_capita_annual: [amount]
    segment_match_index: [calculated 0-2, where 1.0 = average]
    segment_weights: [age, income, household weights]
  primary_catchment:
    population: [number]
    total_addressable_market: [population × per_capita_spend]
    segment_adjusted_tam: [× segment_match_index]
    huff_capture_percentage: [from Huff model]
    estimated_annual_demand: [final calculated amount]
  secondary_catchment: [same structure]
  tertiary_catchment: [same structure]
  total_demand_estimate: [sum of all catchments]
  confidence: [high | medium | low]
  confidence_factors: [list of what increases/decreases confidence]
```

### 5. Compute Competitive Saturation
Assess market saturation using Reilly's Law and central-place theory.

**Reilly's Law of Retail Gravitation:**
```
Breaking Point Distance (BP) between two centers:

BP_AB = D / (1 + sqrt(Pb/Pa))

Where:
- BP_AB = distance from center A to breaking point
- D = total distance between centers A and B
- Pa = population of center A
- Pb = population of center B
- sqrt = square root

Application:
  1. Identify competing centers (existing clusters or major competitors)
  2. Calculate breaking points
  3. Determine which side of breaking point candidate falls
  4. If on competitor's side, flag as weak competitive position
```

**Central Place Theory - Saturation Index:**
```
Threshold and Range Analysis:

For each retail category:
  - Threshold = minimum population to support one outlet
  - Range = maximum distance consumers will travel
  - Ideal spacing = range (or 2× range for some categories)

Saturation Metrics:
1. Competitor Density = competitors / sq km or / 1000 people
2. Floorspace Density = total category floorspace / population
3. Herfindahl-Hirschman Index (HHI) = sum of squared market shares

Interpretation:
  - Low density + low HHI = greenfield opportunity
  - High density + low HHI = fragmented, room for consolidation
  - High density + high HHI = saturated, dominant competitors
```

**Competitive Intensity Score:**
```python
def calculate_saturation_index(candidate_location, competitors, population, category):
    """
    Calculate multiple saturation metrics.

    Returns:
        Dict with various saturation indices
    """
    # Count competitors in each catchment ring
    primary_competitors = count_competitors_in_radius(
        candidate_location, competitors, primary_radius
    )
    secondary_competitors = count_competitors_in_radius(
        candidate_location, competitors, secondary_radius
    )

    # Competitor per capita
    competitor_per_capita_primary = primary_competitors / primary_population
    competitor_per_capita_secondary = secondary_competitors / secondary_population

    # Estimate total floorspace (if available)
    total_floorspace = sum(c.get('floorspace_est', 5000) for c in competitors)
    floorspace_per_capita = total_floorspace / primary_population

    # HHI (if market share data available, otherwise proxy by floorspace)
    if any('market_share' in c for c in competitors):
        shares = [c['market_share'] for c in competitors]
        hhi = sum(s**2 for s in shares)
    else:
        # Proxy by floorspace
        floor_shares = [c['floorspace_est'] / total_floorspace for c in competitors]
        hhi = sum(s**2 for s in floor_shares)

    # Classify saturation
    if competitor_per_capita_primary < category['low_saturation_threshold']:
        saturation_level = 'low'
    elif competitor_per_capita_primary < category['high_saturation_threshold']:
        saturation_level = 'medium'
    else:
        saturation_level = 'high'

    return {
        'primary_competitor_count': primary_competitors,
        'secondary_competitor_count': secondary_competitors,
        'competitor_per_capita_primary': competitor_per_capita_primary,
        'competitor_per_capita_secondary': competitor_per_capita_secondary,
        'floorspace_per_capita': floorspace_per_capita,
        'hhi': hhi,
        'saturation_level': saturation_level,
        'category_benchmarks': category['saturation_benchmarks']
    }
```

**Saturation Output Format:**
```yaml
competitive_saturation:
  framework:
    reilly_law: [breaking point analysis results]
    central_place_theory: [threshold/range analysis]
  metrics:
    primary_catchment:
      competitor_count: [number]
      competitor_per_1000_people: [calculated]
      total_estimated_floorspace: [sq ft or sq m]
      floorspace_per_capita: [calculated]
      herfindahl_index: [0-10,000 scale]
    secondary_catchment: [same structure]
  saturation_classification:
    level: [low | medium | high]
    justification: [compared to category benchmarks]
    dominant_competitors: [list with estimated market share]
  competitive_position:
    breaking_point_analysis: [candidate relative to competitors]
    market_gap_opportunity: [yes | no, with rationale]
    entry_barriers: [any structural barriers identified]
```

### 6. State Parameters and Assumptions
Document all model choices, parameters, and their justification.

**Required Documentation:**
```yaml
model_transparency:
  catchment_method: [method chosen and why]
  distance_metrics: [network vs euclidean and rationale]
  huff_parameters:
    lambda: [value and justification]
    alpha: [value and justification]
    attractiveness_proxy: [chosen proxy and alternatives considered]
  demographic_data:
    source: [citation]
    vintage: [year]
    spatial_resolution: [census block, tract, etc]
    adjustments: [any scaling or growth adjustments]
  competitive_data:
    sources: [how competitors identified and located]
    completeness: [estimated % of real competitors captured]
    estimation_methods: [how missing data was estimated]
  assumptions:
    critical_assumptions: [list with impact rating]
    sensitivity_factors: [which assumptions most affect results]
    caveats: [known limitations]
```

## Output Format

The sub-trade-area-modeler outputs a comprehensive analysis per candidate site:

```yaml
trade_area_analysis:
  candidate_id: [A, B, C, ...]
  candidate_name: [from requirements]

  catchment_definition:
    method: [drive_time | distance_ring | road_network]
    primary:
      radius: [minutes or distance]
      area_sq_km: [calculated]
      population: [from demographics]
    secondary: [same structure]
    tertiary: [same structure]
    barriers: [identified and applied]

  demographics:
    data_source: [citation]
    vintage: [year]
    primary:
      total_population: [number]
      target_segment: [number, %]
      median_income: [amount]
      spending_power_index: [normalized]
    secondary: [same structure]
    tertiary: [same structure]

  huff_gravity_model:
    framework: "Huff Probabilistic Gravity Model (Huff 1964)"
    parameters:
      distance_decay_lambda: [value with justification]
      attractiveness_proxy: [proxy choice]
      distance_metric: [type]
    consideration_set_size: [total competitors evaluated]
    results:
      primary_capture_percentage: [0-100]
      secondary_capture_percentage: [0-100]
      tertiary_capture_percentage: [0-100]
      weighted_average_capture: [0-100]

  demand_estimate:
    per_capita_spend_source: [citation]
    per_capita_annual: [amount]
    segment_adjustment_factor: [calculated]
    primary_addressable_market: [amount]
    estimated_annual_capture: [amount]
    confidence: [high | medium | low]

  competitive_saturation:
    primary_competitor_count: [number]
    competitor_per_capita: [number]
    saturation_level: [low | medium | high]
    saturation_justification: [vs category benchmarks]
    competitive_position: [assessment]

  parameters_and_assumptions:
    # Full transparency as documented above

  quality_flags:
    data_quality_concerns: [any issues]
    estimation_uncertainty: [high | medium | low]
    recommended_next_steps: [if applicable]
```

## Quality Gates

The sub-trade-area-modeler must pass ALL quality gates:

1. **Model Named and Cited**: Framework must be explicitly named (e.g., "Huff Probabilistic Gravity Model (Huff 1964)") with citation.

2. **Parameters Stated**: λ (distance decay), α (attractiveness sensitivity), attractiveness proxy, and distance metric must all be explicitly stated with justification.

3. **Data Source and Vintage**: Demographic and competitive data sources must be cited with year of data. Vintage > 2 years must be flagged.

4. **Consideration Set Defined**: All competitors included in Huff calculation must be listed with locations and attractiveness values.

5. **Confidence Rated**: Each demand estimate must include a confidence rating (High/Medium/Low) with factors affecting confidence.

6. **Transparency Complete**: Parameters, assumptions, and caveats must be documented in model_transparency section.

## Error Handling

**Insufficient Demographic Data:**
```
If catchment demographic data unavailable at required resolution:
  1. Attempt fallback to lower resolution (state vs county vs city)
  2. Apply scaling based on land use or built-up area
  3. Flag as "low confidence, scaled from [level]"
  4. Reduce confidence rating to Low
  5. Do not proceed without at least order-of-magnitude estimate
```

**Competitor Data Gaps:**
```
If significant competitors cannot be located:
  1. Document known competitors and estimate for unknown
  2. Apply saturation estimate based on partial data
  3. Flag as "partial competitor data, saturation estimate uncertain"
  4. Recommend competitive audit as next step
  5. Use conservative saturation assumption (assume additional competitors)
```

**Extreme Parameter Sensitivity:**
```
If results are highly sensitive to parameter choice (e.g., small λ change flips ranking):
  1. Document sensitivity explicitly
  2. Provide results under multiple parameter scenarios
  3. Flag for quality review attention
  4. Recommend parameter calibration if possible
  5. Do not present single-point estimate as definitive
```

## Integration Points

- **Calls**: WebSearch (for competitor discovery), WebFetch (for demographic data), geocoding/routing services (for distance calculations)
- **Called By**: main.md (retail-location-intelligence)
- **Outputs To**: sub-scoring-engine (demand capture, saturation), sub-quality-reviewer (parameters, assumptions)
- **Data Dependencies**: Census/demographic APIs, routing APIs, competitor databases, SECOND-KNOWLEDGE-BRAIN.md (framework citations)

## Framework Citations

**Huff Gravity Model:**
- Huff, D. L. (1964). "Defining and Estimating a Trading Area." Journal of Marketing, 28(3), 34-38.

**Reilly's Law:**
- Reilly, W. J. (1931). The Law of Retail Gravitation. New York: Knickerbocker Press.

**Central Place Theory:**
- Christaller, W. (1933). Die zentralen Orte in Süddeutschland. Jena: Gustav Fischer. (English translation: Central Places in Southern Germany, 1966)

**Analog Method:**
- Applebaum, W. (1966). "Methods for Determining Trade Areas." Journal of Marketing Research, 3(1), 71-74.
