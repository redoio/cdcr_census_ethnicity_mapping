# Project Rules

## Reference Repositories

1. Treat everything under `reference_repos/` as immutable reference material.
2. Never edit, format, rename, move, delete, or generate files inside `reference_repos/`.
3. Never execute Python scripts, notebooks, build tasks, or data-processing commands from the reference repositories.
4. Never commit, push, pull, merge, rebase, reset, checkout, stash, tag, or create branches in the reference repositories.
5. Limit inspection to read-only operations such as file listing, text search, text reading, `git status`, `git log`, `git show`, and non-writing schema inspection.

## Data Safety

6. Never run a command that writes to or overwrites `offenses_data`.
7. Never use an `offenses_data` directory as a development output path.
8. Perform all implementation outside `reference_repos/` unless the user explicitly authorizes work in a separate real client checkout.
9. Write generated data only to an explicitly named staging or temporary directory.
10. Do not expose raw CDCR IDs, hashing seeds, environment files, or raw-to-hash dictionaries.
11. Preserve the original `ethnicity` and `cdcno` columns and values.

## Development Process

12. Work in small, reviewable increments.
13. Produce or update documentation before implementation while behavior or category definitions remain under review.
14. Preserve compatibility with the `preprocess -> hash_object -> offenses_data` responsibility split.
15. Place semantic data transformations in preprocessing, not hashing or publication code.
16. Ask before introducing new third-party dependencies.
17. Follow existing style: pandas DataFrames, small functions, lowercase `snake_case` Python names, and lowercase space-separated published columns.
18. Do not silently coerce unseen ethnicity values. Report them as `review_needed` and stop publication until reviewed.
19. Keep the project-defined generic `other` distinct from Census `Some other race alone`.

## Validation And Publication

20. Validate mappings against every distinct source value in each release.
21. Verify row counts, IDs, source ethnicity values, existing columns, and table cardinality before accepting staged output.
22. Produce a dry-run summary before writing full outputs.
23. Require Aparna's review of the mapping dictionary and staged schema before integration with the real processing repository.
24. Require explicit authorization before generating files intended to replace an `offenses_data` release.
25. Publish data, dictionary, category definitions, README changes, and FAQ changes as reviewed artifacts, not through an unreviewed in-place run.

