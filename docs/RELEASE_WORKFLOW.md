# Release Workflow

Use this workflow to review mappings and create staged demographics outputs. Do not
write directly into an `offenses_data` release directory.

The examples below assume a local layout like:

```text
../offenses_data/data/12_2023/demographics.csv
../offenses_data/data/04_2025/demographics.csv
staging/
```

Adjust input paths as needed for your local checkout.

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

If new ethnicity labels are reported, update
`mappings/cdcr_census_ethnicity_mapping.json` and rerun the dry run.

After all labels are mapped, write to staging:

```powershell
python scripts\map_cdcr_ethnicity_to_census.py `
  --input ..\offenses_data\data\NEW_RELEASE\demographics.csv `
  --output staging\NEW_RELEASE\demographics.csv
```

Before any release update, confirm:

1. Input and output row counts match.
2. Existing columns and values are unchanged.
3. The original `ethnicity` column remains present.
4. The new `census race ethnicity group` column has no `review_needed` values.
5. Aparna has reviewed and approved the staged output.
