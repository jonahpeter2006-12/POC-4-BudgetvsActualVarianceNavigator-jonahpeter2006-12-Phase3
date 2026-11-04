# REPRESENTATIVENESS ASSESSMENT

## Assessment Overview

- Assessment: **source_coverage_preserved_with_real_world_limitations**
- Source observations: 18
- Canonical records: 72

## Full Assessment Evidence

```json
{
  "assessment_version": "1.0.0",
  "canonical_dataset": "data/canonical/intelligence_data.csv",
  "representativeness_reference": "data/source-sample/source_sample.csv",
  "canonical_record_count": 72,
  "source_observation_count": 18,
  "canonical_source_id_count": 18,
  "transformation_note": "Canonical records are four financial measurements derived from each source observation, not independent transactions.",
  "coverage_comparison": {
    "cost_centres": {
      "source_unique_count": 6,
      "canonical_unique_count": 6,
      "source_values": [
        "CC-101",
        "CC-102",
        "CC-201",
        "CC-202",
        "CC-301",
        "CC-401"
      ],
      "canonical_values": [
        "CC-101",
        "CC-102",
        "CC-201",
        "CC-202",
        "CC-301",
        "CC-401"
      ],
      "all_source_values_preserved": true,
      "missing_from_canonical": [],
      "unexpected_in_canonical": []
    },
    "departments": {
      "source_unique_count": 4,
      "canonical_unique_count": 4,
      "source_values": [
        "Engineering",
        "HR & Ops",
        "Marketing",
        "Sales"
      ],
      "canonical_values": [
        "Engineering",
        "HR & Ops",
        "Marketing",
        "Sales"
      ],
      "all_source_values_preserved": true,
      "missing_from_canonical": [],
      "unexpected_in_canonical": []
    },
    "categories": {
      "source_unique_count": 6,
      "canonical_unique_count": 6,
      "source_values": [
        "Cloud Infrastructure",
        "Events & PR",
        "Paid Ads & Campaigns",
        "Recruitment & Onboarding",
        "Software Licenses",
        "Travel & Client Entertainment"
      ],
      "canonical_values": [
        "Cloud Infrastructure",
        "Events & PR",
        "Paid Ads & Campaigns",
        "Recruitment & Onboarding",
        "Software Licenses",
        "Travel & Client Entertainment"
      ],
      "all_source_values_preserved": true,
      "missing_from_canonical": [],
      "unexpected_in_canonical": []
    }
  },
  "temporal_coverage": {
    "source_month_values": [
      "Feb 2026",
      "Jan 2026",
      "Mar 2026"
    ],
    "canonical_reporting_dates": [
      "2026-01-01T00:00:00Z",
      "2026-02-01T00:00:00Z",
      "2026-03-01T00:00:00Z"
    ],
    "source_month_count": 3,
    "canonical_reporting_period_count": 3
  },
  "source_observation_distributions": {
    "cost_centre": {
      "CC-101": 3,
      "CC-102": 3,
      "CC-201": 3,
      "CC-202": 3,
      "CC-301": 3,
      "CC-401": 3
    },
    "department": {
      "Engineering": 6,
      "Marketing": 6,
      "Sales": 3,
      "HR & Ops": 3
    },
    "category": {
      "Cloud Infrastructure": 3,
      "Software Licenses": 3,
      "Paid Ads & Campaigns": 3,
      "Events & PR": 3,
      "Travel & Client Entertainment": 3,
      "Recruitment & Onboarding": 3
    },
    "month": {
      "Jan 2026": 6,
      "Feb 2026": 6,
      "Mar 2026": 6
    }
  },
  "checks": {
    "all_source_observations_retained": true,
    "four_metrics_per_source_observation": true,
    "cost_centre_coverage_preserved": true,
    "department_coverage_preserved": true,
    "category_coverage_preserved": true
  },
  "all_mapping_coverage_checks_passed": true,
  "limitations": [
    "All supplied observations are synthetic.",
    "All 18 available source observations were retained; this does not prove that the source represents real-world financial activity.",
    "Only January to March 2026 is covered.",
    "The preserved source sample is the available comparison reference, not an independent external population.",
    "The 72 canonical rows must not be interpreted as 72 independent source observations."
  ],
  "assessment": "source_coverage_preserved_with_real_world_limitations"
}
```

## Interpretation

The assessment compares canonical coverage with the supplied source sample.

- All 18 source observations are retained.
- Each source observation expands into four financial measurements.
- Cost-centre, department and category coverage is preserved.
- The reporting period covers January to March 2026.

## Limitations

The source data is synthetic. Matching the supplied sample does not establish representativeness of a real-world population.

The 72 canonical records are derived from 18 source observations and must not be treated as 72 independent source observations.

## Conclusion

**Source coverage is preserved, subject to real-world representativeness limitations.**
