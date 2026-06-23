# CDCR to Census Race/Ethnicity Mapping Categories

This document describes the Census-compatible race and ethnicity categories used to map CDCR ethnicity labels. These categories are intended to support future comparisons between CDCR populations and county-level demographic data from the U.S. Census.

| Code | End-user label | Census alignment |
|---|---|---|
| `hispanic_latino` | Hispanic or Latino | `B03002_012E`: Hispanic or Latino, of any race |
| `nh_white` | Non-Hispanic White | `B03002_003E`: Not Hispanic or Latino, White alone |
| `nh_black` | Non-Hispanic Black | `B03002_004E`: Not Hispanic or Latino, Black or African American alone |
| `nh_aian` | Non-Hispanic American Indian or Alaska Native | `B03002_005E` |
| `nh_asian` | Non-Hispanic Asian | `B03002_006E` |
| `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander | `B03002_007E` |
| `nh_other` | Non-Hispanic some other race | `B03002_008E` |
| `nh_two_or_more` | Non-Hispanic two or more races | `B03002_009E` and its detailed subcategories |
| `other` | Other or unknown CDCR category | Project-defined category; not a direct Census category |
| `review_needed` | Unmapped value requiring review | Processing safeguard; not an analytical category |

`nh_other` and `nh_two_or_more` are included here for Census completeness. They are
not currently produced by the approved CDCR mapping dictionary.

## Interpretation Notes

- Census treats Hispanic or Latino as an ethnicity that can coexist with any race.
- The mapping uses mutually exclusive broad groups suitable for denominators from `B03002`.
- CDCR source labels do not separately encode race and Hispanic origin. Mapping broad CDCR labels such as `White` and `Black` to non-Hispanic Census groups assumes that Hispanic individuals are represented separately by CDCR Hispanic or national-origin labels.
- `other` must not be compared directly with `B03002_008E`. A denominator policy for this project-defined fallback category still needs to be decided.
- Keep the original `ethnicity` column alongside the mapped column for transparency and auditability.

## Limitations

This mapping represents the current best alignment between CDCR ethnicity labels and available Census race/ethnicity categories. Some source labels do not have an exact Census equivalent and therefore require project-specific mapping decisions.