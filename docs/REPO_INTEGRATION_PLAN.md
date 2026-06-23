# Repository Integration Plan

This plan is based on a read-only inspection of:

- `redoio/preprocess`
- `redoio/hash_object`
- `redoio/offenses_data`

No scripts from those repositories were executed and no remote files were changed.

## Existing Flow

1. `preprocess` reads the three release files, cleans column names, and derives time fields for demographics.
2. `hash_object` creates/applies the seeded CDCR ID hash and writes publishable CSV/XLSX files.
3. `offenses_data` stores versioned public CSV snapshots such as `data/12_2023/` and `data/04_2025/`.

The current `preprocess` configuration uses the same input and output release directory and overwrites files. Do not run it against `offenses_data` during development.

## Recommended Ownership

The ethnicity mapping belongs in `preprocess` because it is a semantic data-cleaning transformation. It does not require raw identifiers and should not be implemented as hashing behavior.

Suggested tracked files in `preprocess`:

```text
mappings/cdcr_census_ethnicity_mapping.json
mappings/CENSUS_TARGET_CATEGORIES.md
```

Suggested code boundary:

```python
def map_cdcr_ethnicity(
    df,
    source_col="ethnicity",
    target_col="census race ethnicity group",
    mapping=None,
):
    ...
```

## Safe First Change

1. Add the mapping dictionary and target-category documentation to `preprocess`.
2. Add a pure mapping function in `utils.py` or a focused mapping module.
3. Add tests using a tiny in-memory DataFrame covering every known label and one unknown label.
4. Make unknown labels fail validation or receive `review_needed`; never silently coerce them to `other`.
5. Add a dry-run summary showing source labels, mapped labels, counts, and unmapped values.
6. Write only to a separate staging directory during development.
7. Publish only `census race ethnicity group`; keep mapping status and notes in the dictionary or optional audit output.

Do not update `offenses_data` in this step.

## Later Release Step

After Aparna approves the dictionary and staged output:

1. Run preprocessing on a controlled copy of the release files.
2. Confirm row count and `cdcno` values are unchanged.
3. Confirm only demographics receives the new mapping column.
4. Run the existing hash workflow if processing begins from raw/unhashed data.
5. Compare staged files against the current release before any replacement.
6. Update the `offenses_data` README data dictionary with the new column and category definitions.
7. Publish through a reviewed commit or pull request, not direct in-place execution.

## Validation Checks

- Every distinct source ethnicity has exactly one mapping entry.
- No null mapped values are produced.
- Known source labels map to the approved target category.
- Unexpected labels are reported as `review_needed` and stop release publication.
- Input and output row counts match.
- Existing columns retain their values and order, apart from the intentional new column.
- The original `ethnicity` column remains present.
- The mapping dictionary and output report identify the release vintage.
