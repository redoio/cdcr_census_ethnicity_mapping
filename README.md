# CDCR Census Ethnicity Mapping

This repository contains the first implementation step for adding a Census-compatible race/ethnicity grouping to CDCR demographics data.

The workflow is CSV-only to match the published `offenses_data` files.

The workflow keeps the original CDCR `ethnicity` column and appends one publication column:

```text
census race ethnicity group
```

The mapping currently covers all 37 ethnicity labels observed across the `12_2023` and `04_2025` `offenses_data` releases. It also includes a guardrail for future datasets: any previously unseen ethnicity label is reported as `review_needed` and blocks output unless explicitly allowed for staging review.

## Repository Contents

```text
mappings/
  cdcr_census_ethnicity_mapping.json
docs/
  CENSUS_TARGET_CATEGORIES.md
  REPO_INTEGRATION_PLAN.md
  RELEASE_WORKFLOW.md
scripts/
  map_cdcr_ethnicity_to_census.py
tests/
  test_ethnicity_mapping.py
DEVELOPMENT_RULES.md
```

## Intended Data Flow

This repo is a small review package. The eventual production home for the mapping logic should be the `preprocess` repository.

Recommended flow:

1. Add the approved mapping dictionary and category documentation to `preprocess`.
2. Add the mapped column during demographics preprocessing.
3. Preserve the new column through `hash_object`.
4. Stage outputs for both `12_2023` and `04_2025`.
5. Update `offenses_data` only after review and approval.

Do not run this script directly against `offenses_data` release files in place. Use
staged output paths as shown in `docs/RELEASE_WORKFLOW.md`.

## Usage

Dry-run a demographics file without writing output:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input path\to\demographics.csv `
  --dry-run
```

Write a staged output file:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input path\to\demographics.csv `
  --output path\to\staging\demographics.csv
```

Include audit columns for internal review only:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input path\to\demographics.csv `
  --output path\to\staging\demographics_audit.csv `
  --include-audit-columns
```

## Approved Mapping Notes

Client-confirmed decisions:

- `Indian` maps to `nh_asian`.
- `Jamaican` maps to `nh_black`.
- `Other` and `Unknown` map to the project-defined `other` category.

The project-defined `other` category is not equivalent to the Census `Some other race alone` category. Downstream population-rate calculations should handle that denominator decision explicitly.

## Future Dataset Workflow

For each new release:

1. Run a dry run against the new demographics file.
2. Review the unique source ethnicity labels and mapped group counts.
3. If new labels appear, update `mappings/cdcr_census_ethnicity_mapping.json`.
4. Re-run validation before staging output.
5. Keep the original ethnicity values unchanged.
