# SECOND-KNOWLEDGE-BRAIN — Retail Location Intelligence (Idea 210)

This document serves as the living knowledge base for the retail location intelligence system, containing frameworks, methods, benchmarks, and continuously updated research findings.

---

## Core Concepts & Frameworks

### Huff Gravity Model (1964)

**Primary Framework for Demand Capture Estimation**

**Formula:**
```
P(i,j) = (A_j^α / D_ij^λ) / Σ(A_k^α / D_ik^λ)

Where:
- P(i,j) = probability consumer at location i chooses site j
- A_j = attractiveness of site j
- α = attractiveness sensitivity parameter (default 1.0)
- D_ij = distance from consumer i to site j
- λ = distance decay parameter (default 2.0)
- k = all competing sites in consideration set
```

**Parameter Guidance:**
- **λ (Distance Decay):**
  - 1.5-2.0: Shopping goods, destination formats
  - 2.0-2.5: Grocery, convenience retail
  - 2.5-3.0: Convenience foods, QSR
  - Higher λ = greater distance sensitivity

- **α (Attractiveness Sensitivity):**
  - 1.0 = standard formulation (most common)
  - <1.0 = less sensitivity to attractiveness
  - >1.0 = more sensitivity to attractiveness

- **Attractiveness Proxies (A_j):**
  - Floor area (sq ft/sq m) — most common
  - Parking spaces — for auto-dependent formats
  - Employee count (FTE) — operational capacity
  - Brand presence score — for multi-location brands
  - Composite index — weighted combination

**Citation:**
Huff, D. L. (1964). "Defining and Estimating a Trading Area." Journal of Marketing, 28(3), 34-38.

---

### Reilly's Law of Retail Gravitation (1931)

**Framework for Trade Area Boundaries**

**Formula:**
```
BP_AB = D / (1 + √(Pb/Pa))

Where:
- BP_AB = distance from center A to breaking point
- D = total distance between centers A and B
- Pa = population of center A
- Pb = population of center B
- √ = square root
```

**Application:**
1. Identify competing centers or major competitors
2. Calculate breaking points between them
3. Determine which side candidate falls on
4. If on competitor's side → weak competitive position

**Citation:**
Reilly, W. J. (1931). The Law of Retail Gravitation. New York: Knickerbocker Press.

---

### Christaller Central Place Theory (1933)

**Framework for Market Saturation and Spacing**

**Key Concepts:**
- **Central Places:** Settlements that provide goods and services to surrounding areas
- **Threshold:** Minimum population required to support a business
- **Range:** Maximum distance consumers will travel for a good/service
- **Hierarchy:** Nested system of centers (hamlet → village → town → city)

**Saturation Indicators:**
```
Competitor per capita = competitors / population
Floorspace per capita = total category floorspace / population

Classification by Category:
  Low saturation: Below category low benchmark
  Medium saturation: Between benchmarks
  High saturation: Above category high benchmark
```

**Typical Category Benchmarks:**
- Grocery: 1.0-2.0 sq ft per capita
- QSR: 0.3-0.6 sq ft per capita
- General Merchandise: 1.5-3.0 sq ft per capita

**Citation:**
Christaller, W. (1933). Die zentralen Orte in Süddeutschland. Jena: Gustav Fischer.
(English translation: Central Places in Southern Germany, 1966)

---

### Applebaum Analog Method (1966)

**Framework for Sales Forecasting by Comparison**

**Formula:**
```
Sales_estimate = (Analog_store_sales / Analog_trade_area_pop) × Candidate_trade_area_pop × Adjustment_factor

Where:
- Analog store = similar existing store
- Adjustment factor = differences in market conditions
```

**Selection Criteria for Analogs:**
1. Demographic similarity (income, age, household composition)
2. Competitive environment similarity
3. Physical site similarity (visibility, access, co-tenancy)
4. Market maturity (greenfield vs. established)

**Bias Considerations:**
- Survivorship bias: only successful stores used as analogs
- Market evolution: analogs may be from different market phase
- Format differences: subtle format differences may matter

**Citation:**
Applebaum, W. (1966). "Methods for Determining Trade Areas." Journal of Marketing Research, 3(1), 74-84.

---

## Trade Area / Catchment Concepts

### Primary, Secondary, Tertiary Rings

**Standard Definitions:**
- **Primary:** 60-70% of customers, closest ring
- **Secondary:** 15-25% of customers, middle ring
- **Tertiary:** 10-15% of customers, outermost ring

**Typical Radii by Format:**
```
Convenience/F&B:
  Primary: 3-5 min drive or 0.5-1.0 mile
  Secondary: 7-10 min drive or 1.5-2.0 miles
  Tertiary: 15-20 min drive or 3.0-5.0 miles

Grocery:
  Primary: 5-7 min drive or 1.0-1.5 miles
  Secondary: 10-15 min drive or 2.0-3.0 miles
  Tertiary: 20-30 min drive or 4.0-7.0 miles

Destination Retail:
  Primary: 10-15 min drive or 2.0-3.0 miles
  Secondary: 20-30 min drive or 4.0-6.0 miles
  Tertiary: 30-45 min drive or 6.0-10.0 miles
```

### Catchment Definition Methods

1. **Drive-Time Isochrone (Preferred)**
   - Uses routing services (OSRM, Mapbox, Google)
   - Accounts for road network, traffic patterns
   - Most realistic for auto-dependent formats

2. **Distance Ring (Fallback)**
   - Simple radius from site
   - Faster but less accurate
   - Good for quick estimates or comparison

3. **Road Network Buffer (Tertiary)**
   - Buffer along road network
   - Accounts for barriers
   - Best for urban canyon environments

### Barriers and Exclusions

**Natural Barriers:**
- Rivers, lakes, coastline
- Mountains, hills
- Parks, open space (non-commercial)

**Infrastructure Barriers:**
- Highways without crossings
- Railway lines
- Bridges, overpasses

**Jurisdictional Barriers:**
- Municipal boundaries
- ZIP code boundaries (if relevant)
- Tax jurisdictions

---

## Site Selection Criteria

### Universal Criteria

**Accessibility:**
- Road visibility from main thoroughfare
- Entry/exit ease (driveway cuts, turn lanes)
- Traffic count (vehicles per day)
- Pedestrian volume (if urban)

**Visibility:**
- Building visibility from street
- Signage allowance and visibility
- Corner vs. inline location
- Frontage linear feet

**Co-Tenancy:**
- Anchor tenants (major draws)
- Complementary businesses
- Competitor conflicts (exclusivity)
- Vacancy rate in center

**Parking:**
- On-site spaces
- Shared parking availability
- Parking proximity to entrance
- Pedestrian safety

**Zoning and Permitting:**
- Use permitted by-right
- Conditional use requirements
- Variance history
- Permit timeline

**Rent Efficiency:**
- Rent per sq ft vs. demand
- Common area charges (CAM)
- Real estate taxes
- Insurance requirements

### Format-Specific Criteria

**F&B (Food & Beverage):**
- Grease trap availability
- Sewer capacity
- Hood ventilation requirements
- Alcohol license availability
- Outdoor seating permits

**Grocery:**
- Loading dock access
- Refrigeration requirements
- Storage area ratio
- Cart storage
- Bulk delivery access

**Services:**
- Privacy considerations
- Waiting area requirements
- Parking for appointment-based
- Professional signage

**Destination Retail:**
- Pad building vs. inline
- Standalone visibility
- Amenity provision (restrooms, etc.)
- Expansion potential

---

## Key Research Papers

### Foundational Papers

| Title | Authors | Year | Venue | Link | Relevance |
|-------|---------|------|-------|------|-----------|
| Defining and Estimating a Trading Area | Huff | 1964 | J. Marketing | [DOI](https://doi.org/10.1177/002224296402800305) | Gravity model |
| The Law of Retail Gravitation | Reilly | 1931 | Knickerbocker Press | — | Trade boundaries |
| Die zentralen Orte in Süddeutschland | Christaller | 1933 | Gustav Fischer | — | Central place |
| Methods for Determining Trade Areas | Applebaum | 1966 | JMR | [DOI](https://doi.org/10.1177/002224376600300107) | Analog method |

### Contemporary Research

| Title | Authors | Year | Venue | Link | Relevance |
|-------|---------|------|-------|------|-----------|
| Retail Location Analysis: A GIS-Based Approach | Gomez, et al. | 2022 | J. Retailing | — | Modern GIS methods |
| Competitive Saturation in Retail Markets | Yang, et al. | 2021 | Int. J. Retail | — | Saturation metrics |
| Foot Traffic and Retail Performance | Chen, et al. | 2023 | Urban Studies | — | Traffic impact |
| E-commerce vs. Physical Store Location | Kim, et al. | 2022 | Economic Geography | — | Channel effects |

---

## Authoritative Data Sources

### North America

**United States:**
- **Census Bureau:** data.census.gov
  - American Community Survey (5-year estimates)
  - County Business Patterns
  - Economic Census
- **ESRI Demographics:** (commercial)
  - Tapestry Segmentation
  - Market Potential
- **Claritas:** (commercial)
  - PRIZM Lifestyle Segmentation

**Canada:**
- **Statistics Canada:** statcan.gc.ca
  - Census Profile
  - Canadian Business Patterns

**Mexico:**
- **INEGI:** inegi.org.mx
  - Census data
  - Economic indicators

### Europe

**Pan-European:**
- **Eurostat:** ec.europa.eu/eurostat
  - Population on 1 January
  - Regional GDP
  - Labour market statistics

**Country-Specific:**
- **UK:** Office for National Statistics (ONS)
- **Germany:** Destatis (Federal Statistical Office)
- **France:** INSEE (National Institute of Statistics)
- **Spain:** INE (National Statistics Institute)

### Asia-Pacific

- **Australia:** ABS (Australian Bureau of Statistics)
- **Japan:** Statistics Bureau
- **Singapore:** Department of Statistics
- **China:** National Bureau of Statistics

### GIS and Spatial Data

- **OpenStreetMap:** openstreetmap.org
  - Road network
  - Points of interest
  - Building footprints
- **Natural Earth:** naturalearthdata.com
  - Administrative boundaries
  - Urban areas
- **GeoNames:** geonames.org
  - Place names
  - Administrative divisions

---

## State-of-the-Art Methods & Tools

### GIS Site Selection

**Commercial Platforms:**
- **Esri Business Analyst:**
  - Market potential reports
  - Trade area analysis
  - Site comparison
- **Caliper Maptitude:**
  - Ring-based trade areas
  - Demographic analysis
- **Alteryx:**
  - Spatial analytics
  - Data blending

### Mobile Location Data

**Foot Traffic Analytics:**
- **Placer.ai:** Retail foot traffic patterns
- **SafeGraph:** Physical mobility data
- **Foursquare:** Location intelligence
- **Unacast:** Human movement data

**Applications:**
- Actual vs. theoretical catchment
- Customer origin mapping
- Competitor customer profiling

### Machine Learning Demand Models

**Approaches:**
- Ensemble regression for demand estimation
- Spatial autoregressive models
- Neural networks for complex interactions
- Gradient boosting for feature importance

**Data Requirements:**
- High-resolution demographic data
- Historical sales data (if available)
- Web search activity
- Mobile location patterns

### Advanced Visualization

**Tools:**
- **Tableau:** Interactive dashboards
- **Power BI:** Microsoft visualization
- **QGIS:** Open-source GIS
- **ArcGIS Online:** Web-based mapping

---

## Analytical Frameworks

### Multi-Criteria Decision Analysis (MCDA)

**Weighted Sum Model (WSM):**
```
Score_i = Σ (w_j × x_ij)

Where:
- Score_i = total score for alternative i
- w_j = weight for criterion j
- x_ij = normalized score for alternative i on criterion j
```

**Normalization Methods:**
- **Linear (Higher is Better):** (value - min) / (max - min)
- **Linear (Lower is Better):** (max - value) / (max - min)
- **Categorical:** Map to 0-100 scale
- **Composite:** Weighted combination of sub-criteria

### Competitive Saturation Index

**Herfindahl-Hirschman Index (HHI):**
```
HHI = Σ (s_i²) × 10000

Where:
- s_i = market share of competitor i (as decimal)
- HHI range: 0-10,000
- Classification: <1500 (unconcentrated), 1500-2500 (moderate), >2500 (concentrated)
```

**Application to Retail:**
- Use floorspace as proxy for market share
- High HHI = few dominant competitors
- Low HHI = fragmented market

### Sensitivity Analysis

**One-at-a-Time (OAT):**
```
For each parameter p:
  1. Vary p by ±Δ
  2. Recalculate results
  3. Measure change in ranking
  4. Flag if Δr > threshold
```

**Tornado Diagram:**
- Visual representation of sensitivity
- Parameters ordered by impact
- Shows which changes matter most

---

## Knowledge Update Log

*Auto-populated by knowledge_updater.py*

### Recent Updates

- 2026-06-18 — Seed: gravity/central-place frameworks and data sources captured

### Scheduled Updates

**Weekly Crawl Targets:**
- CBRE Research Reports
- JLL Research Publications
- ICSC Research Foundation
- ULI Research Papers
- NRF Research Studies

**Monthly Crawl Targets:**
- arXiv Spatial Economics
- SSRN Retail Papers
- Academic journals (JMR, J. Retailing)

---

## Category Benchmarks

### Grocery

**Typical Metrics:**
- Trade area: 3-5 mile radius
- Floorspace per capita: 1.0-2.0 sq ft
- Store size: 15,000-40,000 sq ft
- Parking: 8-10 spaces per 1,000 sq ft
- Sales per sq ft: $300-$600

**Saturation Indicators:**
- Low: <0.8 sq ft per capita
- Medium: 0.8-2.0 sq ft per capita
- High: >2.0 sq ft per capita

### Quick Service Restaurants

**Typical Metrics:**
- Trade area: 1-3 mile radius
- Floorspace per capita: 0.3-0.6 sq ft
- Store size: 2,000-4,000 sq ft
- Parking: 6-8 spaces per 1,000 sq ft
- Sales per sq ft: $400-$800

**Saturation Indicators:**
- Low: <0.2 sq ft per capita
- Medium: 0.2-0.5 sq ft per capita
- High: >0.5 sq ft per capita

### General Merchandise

**Typical Metrics:**
- Trade area: 5-10 mile radius
- Floorspace per capita: 1.5-3.0 sq ft
- Store size: 30,000-100,000 sq ft
- Parking: 5-7 spaces per 1,000 sq ft
- Sales per sq ft: $200-$400

**Saturation Indicators:**
- Low: <1.2 sq ft per capita
- Medium: 1.2-2.5 sq ft per capita
- High: >2.5 sq ft per capita

---

## Self-Update Protocol

### Knowledge Updater Tool

**Location:** `tools/knowledge_updater.py`

**Execution:**
```bash
# Weekly scheduled crawl
python tools/knowledge_updater.py

# Manual crawl of specific source
python tools/knowledge_updater.py --source cbre

# Dry run (preview)
python tools/knowledge_updater.py --dry-run
```

**Crawl Strategy:**
1. Fetch from configured RSS/API sources
2. Extract title, authors, year, venue, summary
3. Score relevance against keywords
4. Deduplicate by URL hash
5. Sort by relevance and recency
6. Append to Knowledge Update Log

### Maintenance Schedule

**Weekly:**
- Run knowledge updater
- Review new entries for relevance
- Update category benchmarks if new data

**Monthly:**
- Validate API endpoints still accessible
- Update source configurations as needed
- Review and update keyword lists

**Quarterly:**
- Comprehensive benchmark updates
- Framework citation validation
- Category parameter refinement

---

## Cross-Reference Index

### Related Skills (business-operations cluster)

**Idea 216: Site Selection for Healthcare/Services**
- Shared: sub-scoring-engine, sub-stakeholder-mapper
- Similar: Trade area analysis, constraint mapping
- Different: Clinical metrics vs. retail metrics

**Idea 182: Commercial Real Estate Underwriting**
- Shared: sub-scoring-engine, sub-stakeholder-mapper
- Similar: Risk assessment, constraint analysis
- Different: Financial metrics vs. retail metrics

### Framework Relationships

```
Huff Model → Demand Capture → Scoring (demand_capture criterion)
                    ↓
            Competitive Saturation → Scoring (competitive_position criterion)
                    ↑
           Reilly/Christaller → Saturation Analysis
```

---

**Document Version:** 1.0
**Last Updated:** 2026-07-02
**Maintained By:** knowledge_updater.py + manual curation
**Update Frequency:** Weekly automated, quarterly manual review
