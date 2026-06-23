# IMPLEMENTATION GUIDELINES

This document outlines the implementation guidelines for the CDCR-to-Census ethnicity mapping workflow prior to integration into the production preprocessing pipeline.

## Data Safety

1. Do not write directly to an `offenses_data` release directory.
2. Write generated files only to an explicit staging directory.
3. Preserve the original `ethnicity` column and values.
4. Add the mapped Census-compatible group as a separate column.
5. Do not commit or expose raw CDCR identifiers, hashing seeds, environment files, or raw-to-hash mapping tables.

## Mapping Rules

1. Do not silently coerce unseen ethnicity labels.
2. Stop processing before writing release output when unmapped labels are found.
3. Use `review_needed` only to flag labels requiring manual review. It must not be used as a final analytical category.
4. Keep the project-defined `other` category distinct from Census `Some other race alone`.
5. Update the mapping dictionary before processing new source labels.

## Release Rules

1. Run a dry run before writing staged outputs.
2. Validate row counts before accepting staged output.
3. Confirm that existing columns and source ethnicity values are unchanged.
4. Require review and approval before updating any published release files.
5. All data and documentation changes should be reviewed before being merged into the production workflow.

## Scope

This repository focuses only on the ethnicity mapping workflow and supporting documentation.

Integration into `preprocess` and updates to `offenses_data` will occur only after review and approval.

