---
name: sub-stakeholder-mapper
description: Maps decision-makers, lease/zoning constraints, and approval paths for a retail site decision. Identifies veto conditions that override analytical scores.
---

## Purpose
Surface the human and structural factors that can veto a site regardless of its analytical score. Many high-scoring sites fail due to lease terms, zoning restrictions, landlord rejection, or franchise approval. This sub-skill ensures these hard constraints are identified and documented early.

## Inputs
- Site profile (from sub-requirements-gatherer)
- Candidate site details (addresses, landlords if known)
- Retail format and requirements
- Organizational context (franchise, independent, chain)

## Procedure

### 1. Identify Decision-Makers
Map all individuals and entities who influence or control the site decision.

**Primary Decision-Makers:**
```yaml
decision_makers:
  owner_founder:
    role: [Final approver, typically]
    priorities: [ROI, risk tolerance, brand fit, lifestyle impact]
    veto_power: [yes | no]
    timeline_influence: [how they affect speed]

  landlord_property_owner:
    role: [Gatekeeper for site access]
    priorities: [Rent level, tenant quality, lease term, creditworthiness]
    veto_power: [yes | no]
    timeline_influence: [can delay or accelerate]

  franchisor_if_applicable:
    role: [Brand protector and system standard maintainer]
    priorities: [Territory integrity, site standards, cannibalization avoidance, brand adjacency]
    veto_power: [yes, typically through approval process]
    timeline_influence: [can add weeks to process]

  lender_if_financing:
    role: [Risk underwriter]
    priorities: [Collateral value, cash flow coverage, borrower experience, market viability]
    veto_power: [yes, through financing approval]
    timeline_influence: [can extend process by months]

  local_authority:
    role: [Permit issuer]
    priorities: [Compliance with zoning, parking, signage, building codes]
    veto_power: [yes, through permit denial]
    timeline_influence: [public notice periods, hearing schedules]
```

**Secondary Influencers:**
```yaml
influencers:
  co_tenants:
    role: [May have exclusivity or co-tenancy clauses]
    priorities: [Traffic generation, compatibility, exclusivity protection]
    veto_power: [sometimes, through lease clauses]

  community_neighbors:
    role: [Can object at permit hearings]
    priorities: [Traffic, noise, character preservation, competition]
    veto_power: [sometimes, through public process]

  commercial_broker:
    role: [Site scout and deal facilitator]
    priorities: [Commission, transaction speed, relationship maintenance]
    veto_power: [no, but can influence]

  architect_builder:
    role: [Feasibility assessor for build-out]
    priorities: [Buildability within budget, code compliance]
    veto_power: [sometimes, if site proves unbuildable]
```

**Decision-Maker Mapping Template:**
```
For each stakeholder:
  - Name/Entity: [if known]
  - Role: [decision or influence type]
  - Priorities: [what matters to them]
  - Veto Power: [can they block the deal?]
  - Timeline Impact: [how they affect speed]
  - Approval Required: [yes/no, what type]
  - Known Positions: [any stated preferences or deal-breakers]
```

### 2. Capture Hard Constraints
Document non-negotiable requirements that can veto a site.

**Zoning Constraints:**
```yaml
zoning_constraints:
  use_code:
    current_zoning: [e.g., C2, B3, Mixed-Use]
    permitted_uses: [list from zoning code]
    conditional_uses: [uses requiring additional approval]
    prohibited_uses: [explicitly not allowed]
    match_assessment:
      format_permitted: [yes | no]
      requires_conditional_use: [yes | no]
      variance_required: [yes | no]
      permit_complexity: [straightforward | moderate | complex | unlikely]

  operational_requirements:
    parking_minimum: [spaces required by code]
    parking_available: [spaces at site]
    parking_deficit: [if deficit exists]
    parking_variance_needed: [yes | no]

    signage_allowed: [type, size, illumination restrictions]
    signage_compatibility: [whether format's needs fit]

    hours_limitation: [if restricted by zoning]
    hours_compatibility: [whether format's needs fit]

    alcohol_license: [if applicable, availability and restrictions]
    outdoor_seating: [if applicable, permits required]

  building_code:
    occupancy_type: [required for format]
    existing_use: [current building occupancy]
    change_of_use_required: [yes | no]
    upgrade_requirements: [if change of use or additions]

    accessibility_compliance: [ADA or local equivalent requirements]
    current_compliance: [existing building status]
    upgrade_required: [yes | no]

    grease_trap_sewer: [for F&B]
    existing_capacity: [yes | no]
    upgrade_required: [yes | no]
```

**Lease Constraints:**
```yaml
lease_constraints:
  financial:
    asking_rent: [per sq ft/year or per month]
    rent_type: [base, NNN, modified gross]
    additional_rents: [CAM, taxes, insurance estimates]
    total_occupancy_cost: [sum of all rent obligations]
    lease_term_required: [minimum years viable]
    lease_term_offered: [landlord's requirement]
    term_mismatch: [if mismatch exists]

    personal_guarantee_required: [yes | no]
    guarantee_amount: [if applicable]
    security_deposit: [amount]

  operational:
    use_clause: [permitted uses in lease]
    exclusivity: [any exclusivity granted to other tenants]
    co_tenancy_requirements: [any continuous operation clauses]
    radius_restriction: [any prohibited locations in area]

    expansion_rights: [first refusal on adjacent space]
    relocation: [any relocation clauses]
    demolition: [any demolition or redevelopment rights by landlord]

    build_out_allowance: [if any, amount per sq ft]
    allowance_adequacy: [whether sufficient for needs]

  approval_path:
    landlord_approval_required: [yes | no, for what]
    franchise_approval_required: [yes | no]
    lender_approval_required: [yes | no]
    timeline_estimate: [weeks/months for full approval chain]

  veto_conditions:
    rent_ceiling_exceeded: [yes | no]
    zoning_mismatch: [yes | no]
    parking_deficit_fatal: [yes | no]
    use_clause_incompatible: [yes | no]
    exclusivity_conflict: [yes | no]
    term_mismatch_fatal: [yes | no]
```

**Franchise/System Constraints (if applicable):**
```yaml
franchise_constraints:
  territory_integrity:
    existing_locations: [nearby franchise units]
    territory_overlap: [if candidate infringes]
    cannibalization_risk: [to existing units]
    territorial_veto: [likely | unlikely]

  site_standards:
    minimum_size: [sq ft required]
    maximum_size: [sq ft allowed]
    size_compatibility: [candidate是否符合]

    minimum_frontage: [feet/meters required]
    frontage_available: [at candidate]
    frontage_compatibility: [是否符合]

    parking_minimum: [spaces required]
    parking_available: [at candidate]
    parking_compatibility: [是否符合]

    visibility_minimum: [visibility score required]
    visibility_available: [at candidate]
    visibility_compatibility: [是否符合]

    co_tenancy_requirements: [required or prohibited adjacencies]
    co_tenancy_conflicts: [at candidate]

  approval_process:
    site_approval_required: [yes | no]
    development_timeline: [standard approval duration]
    additional_fees: [if applicable]

  veto_conditions:
    territory_infringement: [yes | no]
    size_non_compliant: [yes | no]
    standard_non_compliant: [yes | no]
    co_tenancy_conflict: [yes | no]
```

### 3. Map Approval Path and Timeline
Document the sequential or parallel approval process and estimated duration.

**Approval Path Analysis:**
```yaml
approval_path:
  sequential_steps:
    1 - loi_submission:
        owner: [who submits]
        recipient: [landlord or broker]
        duration: [days to weeks]
        conditional: [any prerequisites]
        outcome: [LOI signed or rejected]

    2 - lease_negotiation:
        owner: [attorney, broker]
        recipient: [landlord representative]
        duration: [weeks to months]
        conditional: [on LOI acceptance]
        outcome: [lease drafted or terms rejected]

    3 - franchise_application:
        owner: [owner or developer]
        recipient: [franchisor real estate department]
        duration: [weeks, often parallel with lease]
        conditional: [on site identification]
        outcome: [approval, conditions, or rejection]

    4 - permit_application:
        owner: [architect or owner]
        recipient: [local building department]
        duration: [weeks to months, varies by jurisdiction]
        conditional: [on lease execution and franchise approval]
        outcome: [permits issued, conditions, or denial]

    5 - financing_application:
        owner: [owner]
        recipient: [lender]
        duration: [weeks to months]
        conditional: [on lease, permits, franchise approval]
        outcome: [commitment or rejection]

  parallel_opportunities:
    parallel_tracks:
      - track: [franchise + lease]
        duration_saved: [weeks]
      - track: [permit preparation while negotiating]
        duration_saved: [weeks]

  critical_path:
    total_estimate: [weeks from site to opening]
    critical_bottlenecks: [which steps are on critical path]
    delay_risks: [which steps have highest delay risk]
```

**Timeline by Approval Type:**
```
Typical Durations (varies widely by market and complexity):

LOI to Lease: 2-8 weeks
- Simple, small space: 2-4 weeks
- Complex, large space: 6-12 weeks
- Institutional landlord: 4-12 weeks
- Private landlord: 2-6 weeks

Franchise Approval: 2-6 weeks
- Standard package: 2-4 weeks
- Complex or unusual site: 4-8 weeks
- Territory issues: 4-12 weeks

Permitting: 4-16 weeks
- Straightforward, by-right: 4-6 weeks
- Conditional use: 8-12 weeks + public hearing
- Variance required: 12-20 weeks + public hearing
- Historic district or coastal: 16-24+ weeks

Financing: 4-12 weeks
- SBA loan: 6-10 weeks
- Conventional: 4-8 weeks
- Seller financing: 2-4 weeks
- Cash: N/A

Build-Out: 8-24 weeks
- Second-generation, light improvements: 4-8 weeks
- Shell, standard build-out: 12-16 weeks
- Shell, complex build-out: 16-24+ weeks
```

### 4. Flag Veto Conditions
Identify any constraint that could block the site regardless of score.

**Veto Condition Checklist:**
```yaml
veto_assessment:
  zoning_veto:
    condition: [use not permitted]
    flag: [yes | no]
    override_path: [variance, rezoning, or impossible]
    override_probability: [low | medium | high]
    override_timeline: [additional weeks if attempted]

  parking_veto:
    condition: [parking deficit exceeds variance potential]
    flag: [yes | no]
    override_path: [variance, shared parking, or impossible]
    override_probability: [low | medium | high]

  lease_veto:
    condition: [rent above budget ceiling]
    flag: [yes | no]
    override_path: [negotiate, increase budget, or walk]
    override_probability: [depends on landlord flexibility]

  franchise_veto:
    condition: [territorial infringement or non-compliance]
    flag: [yes | no]
    override_path: [rarely possible]
    override_probability: [very low]

  co_tenancy_veto:
    condition: [exclusivity conflict with existing tenant]
    flag: [yes | no]
    override_path: [negotiate with landlord and existing tenant]
    override_probability: [low to medium]

  community_veto:
    condition: [organized opposition likely]
    flag: [yes | no]
    override_path: [address concerns, public hearing, or impossible]
    override_probability: [depends on specific community]

  financial_veto:
    condition: [lender rejection likely due to site or borrower factors]
    flag: [yes | no]
    override_path: [alternative financing or increase down payment]
    override_probability: [depends on alternatives]

  timeline_veto:
    condition: [approval path exceeds required opening date]
    flag: [yes | no]
    override_path: [accelerate (expensive) or delay opening]
    override_probability: [depends on flexibility]
```

**Veto Summary:**
```
For each candidate:
  - List any active veto conditions
  - Note if veto is absolute (no override) or conditional (override possible)
  - If conditional, estimate override probability and cost/timeline impact
  - Overall veto status: [CLEAR | CONDITIONAL | BLOCKED]

Categorical interpretation:
  CLEAR: No veto conditions identified; can proceed
  CONDITIONAL: Veto conditions exist but override possible with additional effort/cost
  BLOCKED: Absolute veto condition exists; site not viable without fundamental change
```

## Output Format

The sub-stakeholder-mapper outputs a comprehensive constraint and stakeholder map:

```yaml
stakeholder_analysis:
  candidate_id: [A, B, C, ...]
  candidate_name: [name]

  decision_makers:
    - role: [owner_founder | landlord | franchisor | lender | local_authority]
      known_entity: [if available]
      priorities: [list]
      veto_power: [yes | no]
      approval_required: [yes | no]
      timeline_impact: [description]
      known_positions: [any stated preferences]

  zoning_constraints:
    current_code: [zoning designation]
    use_permitted: [yes | conditional | no]
    conditional_use_required: [yes | no]
    variance_required: [yes | no]
    permit_complexity: [straightforward | moderate | complex | unlikely]
    parking_adequacy: [yes | no, variance needed]
    signage_compatibility: [yes | no]
    hours_compatibility: [yes | no]
    special_permits: [list if applicable]
    zoning_veto: [yes | no]
    veto_details: [if veto, explain]

  lease_constraints:
    financial_terms:
      asking_rent: [amount]
      rent_type: [type]
      total_occupancy_cost: [amount]
      rent_vs_budget: [under | at | over ceiling]
      lease_term_offered: [years]
      term_adequacy: [yes | no]

    use_restrictions:
      permitted_uses: [list]
      exclusivity_conflicts: [if any]
      co_tenancy_requirements: [if any]

    build_out:
      allowance_offered: [amount if any]
      allowance_adequacy: [yes | no]

    lease_veto: [yes | no]
    veto_details: [if veto, explain]

  franchise_constraints:
    applicable: [yes | no]
    if_applicable:
      territory_clear: [yes | no]
      size_compliant: [yes | no]
      standards_compliant: [yes | no]
      approval_required: [yes | no]
      franchise_veto: [yes | no]

  approval_path:
    sequential_steps: [list with durations]
    parallel_opportunities: [list with time savings]
    critical_path_duration: [weeks estimate]
    critical_bottlenecks: [list]
    delay_risks: [list]

  veto_assessment:
    overall_status: [CLEAR | CONDITIONAL | BLOCKED]
    veto_conditions: [list of any active vetoes]
    conditional_vetoes: [list with override paths and probabilities]
    timeline_feasibility: [yes | no vs. required opening date]

  recommendations:
    if_clear:
      - "No veto conditions; proceed to lease negotiation"
    if_conditional:
      - "Address conditional vetoes before committing:"
      - [specific veto and suggested action]
    if_blocked:
      - "Site not viable due to veto conditions:"
      - [specific veto and why it's blocking]
```

## Quality Gates

The sub-stakeholder-mapper must pass ALL quality gates:

1. **Lease Constraints Captured**: Rent, term, use clause, and any exclusivity must be documented for each candidate.

2. **Zoning Constraints Captured**: Current zoning, permitted use, and permit requirements must be documented. Missing zoning information must be flagged.

3. **Veto Conditions Identified**: Any condition that could block the site must be explicitly listed and classified as absolute or conditional.

4. **Approval Path Mapped**: The sequential steps to site approval must be listed with estimated durations.

5. **Timeline Compared to Requirements**: If the user provided a target opening date, the approval path must be compared and feasibility assessed.

## Error Handling

**Missing Information:**
```
If critical stakeholder information unknown (e.g., landlord identity, zoning status):
  1. Flag as "unknown - high priority to verify"
  2. Proceed with conservative assumptions (assume worst case)
  3. Recommend immediate verification step
  4. Note that analysis is preliminary pending confirmation
```

**Conflicting Information:**
```
If provided information conflicts (e.g., broker says permitted but zoning code suggests otherwise):
  1. Document both sources
  2. Flag conflict clearly
  3. Proceed with more restrictive interpretation
  4. Recommend verification before relying on permissive interpretation
```

**Complex Regulatory Environment:**
```
If site in complex jurisdiction (historic district, coastal zone, overlay zone):
  1. Flag as "complex regulatory environment"
  2. Note additional approval layers
  3. Extend timeline estimates accordingly
  4. Recommend specialized legal/professional review
```

## Integration Points

- **Calls**: WebSearch (zoning codes, municipal portals), WebFetch (permitting guidelines)
- **Called By**: main.md (retail-location-intelligence)
- **Inputs From**: sub-requirements-gatherer (site details, budget)
- **Outputs To**: sub-scoring-engine (zoning fit criterion), sub-quality-reviewer (constraints for veto analysis)

## Framework Citations

**Retail Lease Analysis:**
- AICPA. Audit and Accounting Guide: Retail Leases.
- International Council of Shopping Centers (ICSC). Leasing Standards and Practices.

**Zoning and Land Use:**
- Mandelker, D. R., et al. Planning and Control of Land Development. (LexisNexis, current edition).

**Franchise Site Approval:**
- International Franchise Association (IFA). Franchise Relationship Guide.
