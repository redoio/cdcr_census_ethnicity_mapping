# CDCR Census Ethnicity Mapping

This repository contains a workflow for mapping CDCR ethnicity labels to Census-compatible race/ethnicity groups. The mapped groups are intended for future population-based sentencing analyses using U.S. Census demographic data.

The mapping dictionary is stored in `mappings/cdcr_census_ethnicity_mapping.json` 

The script reads a CSV, preserves the original `ethnicity` column and adds:

```text
census race ethnicity group
```

The current mapping covers all ethnicity labels observed in the 2023 and 2025 CDCR demographics datasets.

## Safety
Generate mapped files in a staging directory for review. Do not overwrite files in `offenses_data` directly.

## Mapping Table

The prefix `nh` stands for **Non-Hispanic**.

| CDCR ethnicity label | Stored value | Meaning |
|---|---|---|
| American Indian | `nh_aian` | Non-Hispanic American Indian or Alaska Native |
| Bangladeshi | `nh_asian` | Non-Hispanic Asian |
| Black | `nh_black` | Non-Hispanic Black |
| Cambodian | `nh_asian` | Non-Hispanic Asian |
| Chinese | `nh_asian` | Non-Hispanic Asian |
| Columbian | `hispanic_latino` | Hispanic or Latino |
| Cuban | `hispanic_latino` | Hispanic or Latino |
| Filipino | `nh_asian` | Non-Hispanic Asian |
| Fijian | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Guamanian | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Guamanian or Chamorro | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Guatemalan | `hispanic_latino` | Hispanic or Latino |
| Hawaiian | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Hispanic | `hispanic_latino` | Hispanic or Latino |
| Hmong | `nh_asian` | Non-Hispanic Asian |
| Indian | `nh_asian` | Non-Hispanic Asian |
| Jamaican | `nh_black` | Non-Hispanic Black |
| Japanese | `nh_asian` | Non-Hispanic Asian |
| Korean | `nh_asian` | Non-Hispanic Asian |
| Laotian | `nh_asian` | Non-Hispanic Asian |
| Mexican | `hispanic_latino` | Hispanic or Latino |
| Nicaraguan | `hispanic_latino` | Hispanic or Latino |
| Other | `other` | Project-defined other category |
| Other Asian | `nh_asian` | Non-Hispanic Asian |
| Other Asian Not Listed | `nh_asian` | Non-Hispanic Asian |
| Other Hispanic Not Listed | `hispanic_latino` | Hispanic or Latino |
| Other Pacific Islander Not Listed | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Pakistani | `nh_asian` | Non-Hispanic Asian |
| Pacific Islander | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Puerto Rican | `hispanic_latino` | Hispanic or Latino |
| Salvadorian | `hispanic_latino` | Hispanic or Latino |
| Samoan | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Thai | `nh_asian` | Non-Hispanic Asian |
| Tongan | `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| Unknown | `other` | Project-defined other category |
| Vietnamese | `nh_asian` | Non-Hispanic Asian |
| White | `nh_white` | Non-Hispanic White |

## Census-Compatible Groups

The mapped values below are the values written to the `census race ethnicity group` column.

| Stored value | Meaning |
|---|---|
| `hispanic_latino` | Hispanic or Latino |
| `nh_white` | Non-Hispanic White (`nh` = Non-Hispanic) |
| `nh_black` | Non-Hispanic Black |
| `nh_aian` | Non-Hispanic American Indian or Alaska Native |
| `nh_asian` | Non-Hispanic Asian |
| `nh_nhpi` | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| `other` | Project-defined category for `Other` and `Unknown`; not the Census "Some other race alone" category |
| `review_needed` | Unmapped label requiring review |

## Usage

Install dependencies:

```powershell
pip install -r requirements.txt
```

Dry-run a CSV without writing output:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input path\to\demographics.csv `
  --dry-run
```

Write a staged output file:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input path\to\demographics.csv `
  --output staging\demographics.csv
```

Include audit columns for review:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input path\to\demographics.csv `
  --output staging\demographics_audit.csv `
  --include-audit-columns
```

By default, the script stops before writing output if it finds an ethnicity label that is not in the mapping dictionary.


## Future Datasets

For each new CDCR release:

1. Run a dry run against the new demographics CSV.
2. Review mapped group counts and any labels reported as needing review.
3. If new labels appear, update `mappings/cdcr_census_ethnicity_mapping.json`.
4. Re-run the dry run until there are no unmapped labels.
5. Write output only to a staging path.
6. Confirm row counts, existing columns and original `ethnicity` values before any release update.

Use `--allow-review` only during manual review of new labels. Do not use `review_needed` as an analysis category.

## Tests

Run the test suite with:

```powershell
python -m unittest
```
