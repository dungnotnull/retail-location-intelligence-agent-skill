---
name: sub-requirements-gatherer
description: Captures retail format, target customer, budget, and candidate site coordinates for location analysis through structured intake and geocoding validation.
---

## Purpose
Establish a complete, validated, and geocoded brief before any trade-area modeling or scoring begins. This sub-skill ensures all necessary inputs are collected, addresses are validated, and the retail concept is well-defined.

## Inputs
- User's natural language description of their retail concept and candidate sites
- Optional: existing documents (business plan, site list, market analysis)

## Procedure

### 1. Capture Retail Format
Collect the following structured information:

**Category Classification:**
- F&B (Quick Service, Fast Casual, Casual Dining, Fine Dining)
- Grocery (Supermarket, Specialty Food, Convenience)
- Apparel (Fast Fashion, Boutique, Department Store, Outlet)
- Services (Personal Care, Wellness, Financial, Professional)
- Other (specify)

**Store Specifications:**
- Gross floor area (sq ft / sq m)
- Frontage (linear feet of street presence)
- Parking requirement (spaces)
- Storage/back-of-house needs

**Price Tier:**
- Budget/Economy
- Mid-Market
- Premium/Luxury

**Operating Model:**
- Standalone
- Strip mall
- Enclosed mall
- Lifestyle center
- Mixed-use/Transit-oriented

**Capture Template:**
```
Format:
- Category: [classified]
- Size: [number + unit]
- Frontage: [feet/meters]
- Parking Required: [spaces]
- Price Tier: [tier]
- Model: [type]
```

### 2. Capture Target Customer Profile
Define the primary, secondary, and tertiary customer segments.

**Demographic Dimensions:**
- Age range(s)
- Income bracket(s)
- Household composition (singles, families, retirees)
- Education level
- Occupation patterns

**Behavioral Dimensions:**
- Dayparts served (breakfast, lunch, dinner, late night)
- Trip type (convenience, destination, routine, special occasion)
- Frequency expected (daily, weekly, monthly visits)
- Dwell time (quick stop vs. extended stay)
- Basket size/multi-purpose trip likelihood

**Psychographic Indicators:**
- Value vs. convenience orientation
- Brand sensitivity
- Experience-seeking vs. transaction-focused

**Capture Template:**
```
Target Customer:
Primary Segment:
- Age: [range]
- Income: [bracket]
- Household: [type]
- Daypart: [times]
- Trip Type: [type]
- Frequency: [expected]
- Dwell Time: [duration]

Secondary Segment: [same structure]

Tertiary Segment: [same structure]
```

### 3. Capture and Validate Candidate Sites
For each candidate location, collect comprehensive information and validate.

**Required Information:**
- Full address or coordinates (lat/long)
- Available unit number/suite
- Rent asking price (per sq ft/year or per month)
- Available area (sq ft)
- Lease term available

**Site Characteristics:**
- Visibility (corner, inline, end-cap)
- Accessibility (entry/exit ease, driveway cuts)
- Signage allowance (monument, pole, window)
- Parking (on-site, shared, street)
- Co-tenants (current, planned, vacant)
- Build-out condition (shell, second-generation, turnkey)

**Geocoding Process:**
```
For each candidate address:
1. Parse address into components (street, city, region, postal code, country)
2. Query geocoding service (OpenStreetMap Nominatim, Google Maps API fallback)
3. Validate:
   - Coordinates returned
   - Confidence score ≥ 80%
   - Address type matches (commercial, mixed-use)
4. Reverse-geocode to verify address match
5. Store: original address, normalized address, lat, lng, confidence, data source
6. Flag for manual review if confidence < 80% or address type mismatch
```

**Capture Template:**
```
Candidate [N]:
Address: [original]
Normalized: [validated]
Coordinates: [lat, lng]
Geocode Confidence: [X%]
Unit: [number/suite]
Area Available: [sq ft]
Rent Asking: [per unit / total]
Lease Term: [years/months]
Visibility: [type]
Signage: [allowed types]
Parking: [spaces, type]
Co-tenants: [list]
Build-out: [condition]
Notes: [any relevant observations]
```

### 4. Capture Budget and Constraints
Establish financial and operational boundaries.

**Capital Budget:**
- Build-out allowance available
- Equipment budget
- Opening inventory budget
- Working capital reserve

**Operating Budget:**
- Monthly rent ceiling (absolute and per sq ft)
- CAM/taxes/insurance budget
- Labor budget
- Marketing budget

**Timeline Constraints:**
- Desired opening date
- Lease negotiation deadline
- Build-out duration available
- Seasonal considerations (e.g., avoid holiday rush)

**Non-Financial Constraints:**
- Geographic boundaries (must serve/won't serve)
- Exclusion zones (competitor proximity restrictions)
- Brand adjacency requirements (do/don't co-locate with)
- Operational requirements (delivery access, grease trap, etc.)

**Capture Template:**
```
Budget & Constraints:
Capital:
- Build-out: [amount]
- Equipment: [amount]
- Inventory: [amount]
- Working Capital: [amount]

Operating (Monthly):
- Rent Ceiling: [amount]
- CAM/Taxes/Insurance: [amount]
- Labor: [amount]
- Marketing: [amount]

Timeline:
- Target Open: [date]
- Lease Deadline: [date]
- Build-out Available: [weeks]

Geographic:
- Must Serve Areas: [boundaries]
- Won't Serve Areas: [exclusions]
- Competitor Buffer: [distance, if applicable]

Operational Requirements: [list]
```

### 5. Capture Success Metrics
Define measurable objectives for the location.

**Revenue Metrics:**
- Target first-year revenue
- Break-even monthly sales
- Year-over-year growth expectation
- Comparison to similar locations (if any)

**Footfall/Traffic Metrics:**
- Target daily transactions
- Target peak-hour throughput
- Conversion rate expectation (if applicable)

**Market Share Metrics:**
- Target capture of trade area (percentage)
- Target rank in local competitive set

**ROI Metrics:**
- Payback period target
- IRR hurdle rate
- Maximum acceptable payback period

**Capture Template:**
```
Success Metrics:
Revenue:
- Year 1 Target: [amount]
- Monthly Break-even: [amount]
- YoY Growth: [percentage]

Footfall:
- Daily Transactions: [target]
- Peak-hour Throughput: [target]

Market:
- Trade Area Capture: [percentage]
- Competitive Rank: [position]

ROI:
- Payback Period: [months/years]
- IRR Hurdle: [percentage]
```

### 6. List Unknowns and Flag Follow-Ups
Identify information gaps that require additional research or user input.

**Common Unknowns:**
- Demographic data quality for trade area
- Competitor sales volumes (proprietary)
- Future development plans in trade area
- Traffic pattern seasonality
- Local regulatory changes pending

**Capture Template:**
```
Unknowns Requiring Follow-Up:
1. [Unknown] → [Why it matters] → [How to obtain]
2. [Unknown] → [Why it matters] → [How to obtain]
...

Follow-up Questions for User:
1. [Question]
2. [Question]
...
```

## Output Format

The sub-requirements-gatherer outputs a structured profile object:

```yaml
retail_profile:
  format:
    category: [classified category]
    size_gross_floor_area: [number]
    size_unit: [sq_ft | sq_m]
    frontage: [linear feet/meters]
    parking_required: [spaces]
    price_tier: [budget | mid_market | premium]
    operating_model: [standalone | strip_mall | enclosed_mall | lifestyle_center | mixed_use]

  target_customer:
    primary:
      age_range: [min-max]
      income_bracket: [range]
      household_composition: [type]
      dayparts: [list]
      trip_type: [convenience | destination | routine | special_occasion]
      expected_frequency: [daily | weekly | monthly]
      dwell_time: [duration]
      value_orientation: [value | convenience | balanced]
    secondary: [same structure if applicable]
    tertiary: [same structure if applicable]

  candidates:
    - id: [A, B, C, ...]
      address_original: [user-provided]
      address_normalized: [validated]
      coordinates:
        lat: [decimal]
        lng: [decimal]
      geocode_confidence: [percentage]
      geocode_source: [service used]
      unit: [identifier]
      area_available: [number + unit]
      rent_asking: [amount per unit per period]
      rent_total_annual: [calculated]
      lease_term_available: [description]
      visibility: [corner | inline | end_cap]
      signage_allowed: [types]
      parking:
        on_site: [spaces]
        type: [surface | structured | street]
      co_tenants: [list]
      build_out_condition: [shell | second_generation | turnkey]
      build_out_allowance: [if available]
      notes: [free text]
      data_quality_flags: [any concerns]

  budget:
    capital:
      build_out: [amount]
      equipment: [amount]
      inventory: [amount]
      working_capital: [amount]
    operating_monthly:
      rent_ceiling: [amount]
      cam_taxes_insurance: [amount]
      labor: [amount]
      marketing: [amount]
    timeline:
      target_opening: [YYYY-MM-DD]
      lease_deadline: [YYYY-MM-DD]
      build_out_duration_available: [weeks]
    constraints:
      geographic_must_serve: [boundaries]
      geographic_wont_serve: [boundaries]
      competitor_exclusion_buffer: [distance, if applicable]
      operational_requirements: [list]

  success_metrics:
    revenue:
      year1_target: [amount]
      monthly_break_even: [amount]
      yoy_growth_expectation: [percentage]
    footfall:
      daily_transactions_target: [number]
      peak_hour_throughput: [number]
    market:
      trade_area_capture_target: [percentage]
      competitive_rank_target: [position]
    roi:
      payback_period_target: [months]
      irr_hurdle: [percentage]

  unknowns:
    data_gaps: [list of identified gaps]
    follow_up_questions: [list for user]
    research_requirements: [list for further investigation]

  quality_indicators:
    completeness_score: [percentage of required fields filled]
    geocode_success_rate: [percentage of candidates successfully geocoded]
    data_freshness: [date of data collection]
    flags: [any quality concerns]
```

## Quality Gates

The sub-requirements-gatherer must pass ALL quality gates before proceeding:

1. **Geocode Completeness**: ALL candidate addresses must be successfully geocoded with confidence ≥ 80%. Candidates below threshold must be flagged for manual review or excluded.

2. **Target Customer Definition**: At minimum, the primary segment must be defined with age, income, and trip type. Missing secondary/tertiary is acceptable with flag.

3. **Success Metric Specification**: At least one quantifiable success metric must be defined (revenue, footfall, or ROI). "General awareness" or similar is insufficient.

4. **Budget Clarity**: Rent ceiling (absolute or per sq ft) must be specified. Missing capital budget is acceptable with flag.

5. **Candidate Viable Count**: Minimum 1 candidate must pass geocode validation. Zero viable candidates triggers error and user intervention.

6. **Data Quality Flags**: Any data quality concerns must be explicitly listed in the output (geocoding issues, incomplete fields, conflicting information).

## Error Handling

**Geocoding Failures:**
```
If candidate fails geocoding:
  - Return specific error (address not found, ambiguous, no commercial match)
  - Suggest corrections (missing postal code, misspelling, wrong city)
  - Request alternate format (coordinates instead of address)
  - Do NOT proceed with candidate until resolved
```

**Incomplete Information:**
```
If critical field missing (format, target customer, any candidate):
  - List specific missing fields
  - Explain why each is critical for downstream analysis
  - Provide examples of acceptable values
  - Request completion before proceeding
```

**Contradictory Information:**
```
If user provides conflicting data (e.g., rent ceiling lower than all candidates):
  - Flag specific contradiction
  - Present both values
  - Request clarification or priority
  - Allow proceeding with flag (downstream will filter)
```

## Integration Points

- **Calls**: None (intake sub-skill starts the harness)
- **Called By**: main.md (retail-location-intelligence)
- **Outputs To**: sub-stakeholder-mapper (site details), sub-trade-area-modeler (coordinates), sub-scoring-engine (rent, constraints)
- **Data Dependencies**: Geocoding service (OSM Nominatim primary, Google Maps fallback), local address validation libraries
