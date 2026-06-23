# Development Rules

This repository is for reviewing and staging the CDCR-to-Census ethnicity mapping workflow.

## Data Safety

1. Do not write directly to an `offenses_data` release directory.
2. Write generated files only to an explicit staging directory.
3. Preserve the original `ethnicity` column and values.
4. Add the mapped Census-compatible group as a separate column.
5. Do not expose raw CDCR identifiers, hashing seeds, environment files, or raw-to-hash dictionaries.

## Mapping Rules

1. Do not silently coerce unseen ethnicity labels.
2. Stop processing before writing release output when unmapped labels are found.
3. Use `review_needed` only as a review safeguard, not as a final analytical category.
4. Keep the project-defined `other` category distinct from Census `Some other race alone`.
5. Update the mapping dictionary before processing new source labels.

## Release Rules

1. Run a dry run before writing staged outputs.
2. Validate row counts before accepting staged output.
3. Confirm that existing columns and source ethnicity values are unchanged.
4. Require review and approval before updating any published release files.
5. Publish data and documentation changes through reviewed commits or pull requests.

