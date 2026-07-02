"""
Test fixtures for retail location intelligence tests.

This module provides mock data and test fixtures for validating the
retail location intelligence system across various scenarios.
"""

from datetime import date
from typing import Dict, List, Any

# Coffee shop candidates for Scenario 1
COFFEE_SHOP_CANDIDATES = [
    {
        "id": "A",
        "name": "Downtown Corner",
        "address": "123 Main Street, Cambridge, MA 02139",
        "coordinates": {"lat": 42.3736, "lng": -71.1097},
        "unit": "Unit 1",
        "area_available": 1200,
        "area_unit": "sq_ft",
        "rent_asking": 45,
        "rent_unit": "per_sq_ft_year",
        "rent_total_annual": 54000,
        "visibility": "corner",
        "parking_on_site": 5,
        "geocode_confidence": 95,
        "geocode_source": "OSM Nominatim"
    },
    {
        "id": "B",
        "name": "Broadway Inline",
        "address": "456 Broadway, Somerville, MA 02143",
        "coordinates": {"lat": 42.3876, "lng": -71.0892},
        "unit": "Unit 3",
        "area_available": 1000,
        "area_unit": "sq_ft",
        "rent_asking": 38,
        "rent_unit": "per_sq_ft_year",
        "rent_total_annual": 38000,
        "visibility": "inline",
        "parking_on_site": 0,
        "geocode_confidence": 92,
        "geocode_source": "OSM Nominatim"
    },
    {
        "id": "C",
        "name": "Arlington End-cap",
        "address": "789 Massachusetts Ave, Arlington, MA 02476",
        "coordinates": {"lat": 42.4154, "lng": -71.1564},
        "unit": "Unit 2",
        "area_available": 1500,
        "area_unit": "sq_ft",
        "rent_asking": 35,
        "rent_unit": "per_sq_ft_year",
        "rent_total_annual": 52500,
        "visibility": "end_cap",
        "parking_on_site": 12,
        "geocode_confidence": 94,
        "geocode_source": "OSM Nominatim"
    }
]

# Mock demographic data by candidate
MOCK_DEMOGRAPHICS = {
    "A": {
        "primary_population": 8500,
        "target_segment_percentage": 0.42,
        "target_segment_population": 3570,
        "median_income": 95000,
        "household_count": 3200,
        "average_household_size": 2.66,
        "daytime_population": 9500,
        "spending_power_index": 115,
        "data_vintage": 2023,
        "source": "US Census ACS 2019-2023 5-Year Estimates",
        "spatial_resolution": "census_tract"
    },
    "B": {
        "primary_population": 12000,
        "target_segment_percentage": 0.38,
        "target_segment_population": 4560,
        "median_income": 78000,
        "household_count": 4800,
        "average_household_size": 2.50,
        "daytime_population": 15000,
        "spending_power_index": 95,
        "data_vintage": 2023,
        "source": "US Census ACS 2019-2023 5-Year Estimates",
        "spatial_resolution": "census_tract"
    },
    "C": {
        "primary_population": 5200,
        "target_segment_percentage": 0.45,
        "target_segment_population": 2340,
        "median_income": 88000,
        "household_count": 2100,
        "average_household_size": 2.48,
        "daytime_population": 5800,
        "spending_power_index": 108,
        "data_vintage": 2022,
        "source": "US Census ACS 2018-2022 5-Year Estimates",
        "spatial_resolution": "census_tract"
    }
}

# Mock competitor data by candidate
MOCK_COMPETITORS = {
    "A": [
        {
            "name": "Dunkin'",
            "distance_miles": 0.3,
            "attractiveness": 800,
            "attractiveness_proxy": "floor_area",
            "coordinates": {"lat": 42.3760, "lng": -71.1120}
        }
    ],
    "B": [
        {
            "name": "Starbucks",
            "distance_miles": 0.1,
            "attractiveness": 1200,
            "attractiveness_proxy": "floor_area",
            "coordinates": {"lat": 42.3880, "lng": -71.0880}
        },
        {
            "name": "Dunkin'",
            "distance_miles": 0.4,
            "attractiveness": 1000,
            "attractiveness_proxy": "floor_area",
            "coordinates": {"lat": 42.3910, "lng": -71.0850}
        }
    ],
    "C": [
        {
            "name": "Local Cafe",
            "distance_miles": 0.5,
            "attractiveness": 600,
            "attractiveness_proxy": "floor_area",
            "coordinates": {"lat": 42.4190, "lng": -71.1600}
        }
    ]
}

# Mock zoning data by candidate
MOCK_ZONING = {
    "A": {
        "current_zoning": "C-2 Commercial",
        "zoning_code": "C-2",
        "use_permitted": True,
        "permitted_uses": ["retail", "restaurant", "services", "F&B"],
        "conditional_use_required": False,
        "variance_required": False,
        "permit_complexity": "straightforward",
        "estimated_timeline_weeks": 4,
        "parking_adequacy": True,
        "parking_variance_needed": False,
        "signage_compatibility": True,
        "hours_compatibility": True,
        "zoning_veto": False
    },
    "B": {
        "current_zoning": "C-2 Commercial",
        "zoning_code": "C-2",
        "use_permitted": True,
        "permitted_uses": ["retail", "restaurant", "services", "F&B"],
        "conditional_use_required": False,
        "variance_required": False,
        "permit_complexity": "moderate",
        "estimated_timeline_weeks": 6,
        "parking_adequacy": False,
        "parking_variance_needed": True,
        "parking_variance_probability": "medium",
        "signage_compatibility": True,
        "hours_compatibility": True,
        "zoning_veto": False
    },
    "C": {
        "current_zoning": "B-3 Business",
        "zoning_code": "B-3",
        "use_permitted": True,
        "permitted_uses": ["retail", "restaurant", "services", "F&B"],
        "conditional_use_required": False,
        "variance_required": False,
        "permit_complexity": "straightforward",
        "estimated_timeline_weeks": 4,
        "parking_adequacy": True,
        "parking_variance_needed": False,
        "signage_compatibility": True,
        "hours_compatibility": True,
        "zoning_veto": False
    }
}

# Saturated market data for Scenario 2
SATURATED_MARKET_DATA = {
    "district_population": 45000,
    "competitor_count": 6,
    "total_competitor_floorspace": 85000,
    "competitor_floorspace_per_capita": 1.89,
    "category_benchmarks": {
        "category": "Grocery",
        "low_saturation_sqft_per_capita": 0.8,
        "high_saturation_sqft_per_capita": 2.5,
        "typical_store_size": 15000,
        "optimal_per_capita_range": [1.0, 1.8]
    },
    "competitors": [
        {"name": "Market Basket", "size": 25000, "distance_miles": 0.8},
        {"name": "Stop & Shop", "size": 22000, "distance_miles": 1.2},
        {"name": "Trader Joe's", "size": 12000, "distance_miles": 1.5},
        {"name": "Whole Foods", "size": 18000, "distance_miles": 2.1},
        {"name": "ALDI", "size": 10000, "distance_miles": 2.8},
        {"name": "Local Co-op", "size": 8000, "distance_miles": 0.5}
    ]
}

# Zoning veto scenario data
ZONING_VETO_DATA = {
    "candidates": [
        {
            "id": "A",
            "name": "Residential Zone Site",
            "address": "50 Oak Street, Residential District",
            "coordinates": {"lat": 42.3600, "lng": -71.0600},
            "mock_score": 85,
            "zoning": {
                "current_zoning": "R-1 Residential",
                "zoning_code": "R-1",
                "use_permitted": False,
                "permitted_uses": ["single-family", "duplex", "parks"],
                "conditional_use_required": False,
                "variance_required": True,
                "variance_probability": "low",
                "permit_complexity": "unlikely",
                "estimated_timeline_weeks": 24,
                "zoning_veto": True,
                "veto_reason": "Commercial use not permitted in R-1 Residential zone"
            }
        },
        {
            "id": "B",
            "name": "Commercial Zone Site",
            "address": "200 Main Street, Commercial District",
            "coordinates": {"lat": 42.3700, "lng": -71.0700},
            "mock_score": 72,
            "zoning": {
                "current_zoning": "C-2 Commercial",
                "zoning_code": "C-2",
                "use_permitted": True,
                "permitted_uses": ["retail", "restaurant", "services", "F&B"],
                "conditional_use_required": False,
                "variance_required": False,
                "permit_complexity": "straightforward",
                "estimated_timeline_weeks": 4,
                "zoning_veto": False
            }
        }
    ]
}

# Weak data scenario mock data
WEAK_DATA_SCENARIO = {
    "candidates": [
        {
            "id": "A",
            "address": "100 Main St, Data-Poor Town, USA"
        }
    ],
    "data_availability": {
        "census_accessible": False,
        "census_reason": "API rate limit",
        "demographic_data": "stale",
        "competitor_data": "partial",
        "traffic_data": "estimated"
    },
    "cached_brain_data": {
        "regional_demographics": {
            "population_estimate": 50000,
            "median_income_estimate": 65000,
            "vintage": 2020,
            "spatial_resolution": "county-level",
            "staleness_flagged": True
        }
    }
}

# Demand capture scenario data
DEMAND_CAPTURE_SCENARIO = {
    "candidate": {
        "id": "A",
        "address": "100 Main St, Test Town, USA",
        "coordinates": {"lat": 42.3601, "lng": -71.0589}
    },
    "catchment": {
        "method": "drive_time",
        "primary_minutes": 5,
        "primary_radius_miles": 1.5,
        "population": 80000,
        "households": 32000,
        "target_segment_match": 0.40
    },
    "spend": {
        "category_annual_spend_per_capita": 1500,
        "source": "Consumer Expenditure Survey 2023",
        "vintage": 2023
    },
    "huff_parameters": {
        "lambda": 2.0,
        "alpha": 1.0,
        "attractiveness": 1200,
        "attractiveness_proxy": "floor_area",
        "distance_metric": "network_distance"
    },
    "competitors": [
        {
            "id": "C1",
            "name": "Competitor 1",
            "attractiveness": 1000,
            "attractiveness_proxy": "floor_area",
            "distance_miles": 1.2,
            "coordinates": {"lat": 42.3720, "lng": -71.0700}
        },
        {
            "id": "C2",
            "name": "Competitor 2",
            "attractiveness": 800,
            "attractiveness_proxy": "floor_area",
            "distance_miles": 2.5,
            "coordinates": {"lat": 42.3800, "lng": -71.0800}
        }
    ]
}

# Expected Huff calculation results for Scenario 6
EXPECTED_HUFF_RESULTS = {
    "utilities": {
        "candidate": 1200,  # A_j^α / D_ij^λ = 1200^1 / 1.0^2 = 1200
        "competitor_1": 694,  # 1000^1 / 1.2^2 ≈ 694
        "competitor_2": 128,  # 800^1 / 2.5^2 ≈ 128
        "total": 2022
    },
    "capture_probability": 0.593,  # 1200 / 2022 ≈ 59.3%
    "addressable_market": 48000000,  # 80000 × $1500 × 0.40
    "estimated_capture": 28464000,  # $48M × 0.593
    "parameters": {
        "lambda": 2.0,
        "alpha": 1.0,
        "attractiveness_proxy": "floor_area",
        "distance_metric": "network_distance"
    }
}

# Quality review stress test data
STRESS_TEST_DATA = {
    "assumptions_to_test": [
        {
            "name": "distance_decay_lambda",
            "base_value": 2.0,
            "alternatives": [1.5, 2.5],
            "impact_threshold": 5  # points difference in ranking
        },
        {
            "name": "attractiveness_proxy",
            "base_value": "floor_area",
            "alternatives": ["parking_spaces", "composite_index"],
            "impact_threshold": 5
        },
        {
            "name": "spend_per_capita",
            "base_value": 1500,
            "alternatives": [1200, 1800],  # -20%, +20%
            "impact_threshold": 5
        },
        {
            "name": "catchment_boundaries",
            "base_value": "5 minutes drive time",
            "alternatives": ["3.75 minutes", "6.25 minutes"],  # -25%, +25%
            "impact_threshold": 5
        },
        {
            "name": "competitive_set_completeness",
            "base_value": "identified competitors",
            "alternatives": ["+30% competitor floorspace", "+50% competitor count"],
            "impact_threshold": 5
        }
    ]
}

# Helper function to generate mock analysis results
def generate_mock_analysis_result(candidate_id: str, scenario: str = "standard") -> Dict[str, Any]:
    """
    Generate a mock analysis result for testing.

    Args:
        candidate_id: The candidate identifier
        scenario: The test scenario type

    Returns:
        Mock analysis result dictionary
    """
    base_result = {
        "candidate_id": candidate_id,
        "candidate_name": f"Candidate {candidate_id}",
        "trade_area_analysis": {
            "catchment_method": "drive_time",
            "primary_population": MOCK_DEMOGRAPHICS.get(candidate_id, {}).get("primary_population", 10000),
            "huff_gravity_model": {
                "framework": "Huff Probabilistic Gravity Model (Huff 1964)",
                "parameters": {
                    "distance_decay_lambda": 2.0,
                    "attractiveness_sensitivity_alpha": 1.0,
                    "attractiveness_proxy": "floor_area",
                    "distance_metric": "network_distance"
                },
                "results": {
                    "primary_capture_percentage": 35.0,
                    "weighted_average_capture": 32.0
                }
            },
            "estimated_annual_demand": 350000,
            "demographics": MOCK_DEMOGRAPHICS.get(candidate_id, MOCK_DEMOGRAPHICS["A"])
        },
        "competitive_saturation": {
            "competitor_count": len(MOCK_COMPETITORS.get(candidate_id, [])),
            "saturation_level": "medium",
            "floorspace_per_capita": 1.5
        },
        "zoning_constraints": MOCK_ZONING.get(candidate_id, MOCK_ZONING["A"]),
        "veto_status": "CLEAR"
    }

    if scenario == "veto":
        base_result["veto_status"] = "BLOCKED"
        base_result["zoning_constraints"] = ZONING_VETO_DATA["candidates"][0]["zoning"]

    if scenario == "saturated":
        base_result["competitive_saturation"] = {
            "competitor_count": 6,
            "saturation_level": "high",
            "floorspace_per_capita": 1.89
        }

    return base_result


def generate_mock_scoring_result(candidate_ids: List[str]) -> Dict[str, Any]:
    """Generate mock scoring results for multiple candidates."""
    candidates_ranked = []
    for i, cid in enumerate(candidate_ids):
        candidates_ranked.append({
            "candidate_id": cid,
            "candidate_name": f"Candidate {cid}",
            "rank": i + 1,
            "total_score": 80 - (i * 8),  # 80, 72, 64...
            "normalized_scores": {
                "demand_capture": 75 - (i * 5),
                "competitive_position": 70 - (i * 8),
                "accessibility_visibility": 80 - (i * 3),
                "rent_efficiency": 85 - (i * 10),
                "co_tenancy_quality": 75 - (i * 5),
                "zoning_fit": 90 - (i * 2)
            },
            "weighted_contributions": {
                "demand_capture": (75 - (i * 5)) * 0.30,
                "competitive_position": (70 - (i * 8)) * 0.20,
                "accessibility_visibility": (80 - (i * 3)) * 0.15,
                "rent_efficiency": (85 - (i * 10)) * 0.15,
                "co_tenancy_quality": (75 - (i * 5)) * 0.10,
                "zoning_fit": (90 - (i * 2)) * 0.10
            },
            "strengths": ["rent_efficiency"] if i == 0 else [],
            "weaknesses": ["competitive_position"] if i > 0 else []
        })

    return {
        "criteria_and_weights": {
            "demand_capture": {"weight": 0.30, "justification": "Primary revenue driver"},
            "competitive_position": {"weight": 0.20, "justification": "Market entry difficulty"},
            "accessibility_visibility": {"weight": 0.15, "justification": "Drive-by traffic factor"},
            "rent_efficiency": {"weight": 0.15, "justification": "Profitability impact"},
            "co_tenancy_quality": {"weight": 0.10, "justification": "Traffic generation"},
            "zoning_fit": {"weight": 0.10, "justification": "Constraint satisfaction"}
        },
        "candidates_ranked": candidates_ranked,
        "sensitivity_analysis": {
            "score_gap_rank_1_2": candidates_ranked[0]["total_score"] - candidates_ranked[1]["total_score"],
            "fragile": candidates_ranked[0]["total_score"] - candidates_ranked[1]["total_score"] < 5
        }
    }


def generate_mock_quality_review() -> Dict[str, Any]:
    """Generate mock quality review results."""
    return {
        "assumption_stress_tests": {
            "distance_decay_lambda": {
                "assumption": "λ = 2.0",
                "challenge": "Tested λ = 1.5 and λ = 2.5",
                "sensitivity_result": "robust",
                "conclusion": "Ranking stable across ±0.5 lambda variation"
            },
            "attractiveness_proxy": {
                "assumption": "Floor area as proxy",
                "challenge": "Tested parking spaces and composite index",
                "sensitivity_result": "robust",
                "conclusion": "Ranking stable across alternative proxies"
            },
            "spend_per_capita": {
                "assumption": "$1,500 annual spend",
                "challenge": "Tested ±20% variation",
                "sensitivity_result": "fragile",
                "conclusion": "10% demand change would flip ranking at 5-point gap"
            }
        },
        "overall_confidence": "MEDIUM",
        "confidence_rationale": "Demographic data recent but competitor data partial",
        "data_gaps": [
            {"type": "competitor_verification", "impact": "MEDIUM", "recommendation": "Field audit recommended"}
        ],
        "veto_execution": {
            "candidates_vetoed": [],
            "candidates_conditional": [],
            "candidates_clear": ["A", "B", "C"]
        }
    }


# Export all fixtures
__all__ = [
    'COFFEE_SHOP_CANDIDATES',
    'MOCK_DEMOGRAPHICS',
    'MOCK_COMPETITORS',
    'MOCK_ZONING',
    'SATURATED_MARKET_DATA',
    'ZONING_VETO_DATA',
    'WEAK_DATA_SCENARIO',
    'DEMAND_CAPTURE_SCENARIO',
    'EXPECTED_HUFF_RESULTS',
    'STRESS_TEST_DATA',
    'generate_mock_analysis_result',
    'generate_mock_scoring_result',
    'generate_mock_quality_review'
]
