# Release Workflow

This document describes the recommended workflow for applying the CDCR-to-Census ethnicity mapping to released demographics datasets.

**Do not write directly to an `offenses_data` release directory.** Always generate and review staged outputs before updating any published release.

The examples below assume a local layout like:

```text
../offenses_data/data/12_2023/demographics.csv
../offenses_data/data/04_2025/demographics.csv
staging/
```

Adjust input paths as needed for your local checkout.
The examples below use PowerShell syntax. Equivalent commands can be used on Linux or macOS.

## 12_2023 Dry Run

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\12_2023\demographics.csv `
  --dry-run
```

## 12_2023 Staged Output

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\12_2023\demographics.csv `
  --output staging\12_2023\demographics.csv
```

## 04_2025 Dry Run

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\04_2025\demographics.csv `
  --dry-run
```

## 04_2025 Staged Output

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\04_2025\demographics.csv `
  --output staging\04_2025\demographics.csv
```

## Future Releases

For a new release, first run a dry run:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\NEW_RELEASE\demographics.csv `
  --dry-run
```

If previously unseen ethnicity labels are detected, update
`mappings/cdcr_census_ethnicity_mapping.json` before rerunning the dry run. Review the mapping summary and confirm that all source ethnicity labels were mapped as expected.

After all labels are mapped, write to staging:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\NEW_RELEASE\demographics.csv `
  --output staging\NEW_RELEASE\demographics.csv
```

Pre-release Checklist:

1. Input and output row counts match.
2. Existing columns and source data remain unchanged.
3. The original `ethnicity` column remains present.
4. The new `census race ethnicity group` column has no `review_needed` values.
5. The staged output has been reviewed and approved before updating any published release.


