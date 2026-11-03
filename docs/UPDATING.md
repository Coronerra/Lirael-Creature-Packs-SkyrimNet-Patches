# Updating for a new pack version

1. Extract the new pack archive somewhere (it is only read).
2. `python tools/gen.py <fluffyfox|baka|billyy|ocreatures> <extracted pack> data`
3. Review the diff: `git diff --stat data/` then the CSV. Look at new or removed scene ids, the `unsure` and
   `conflict_with_her_tags` columns, and any intent tags she has added (hers always win).
4. Update the version in `tools/build.py` (`PACKS`) and the README tables.
5. `python tools/build.py <OStimNet OStimNetMetaData.json> <Billy v3 OStimNetMetaData.json> <out dir>`
6. Verify: zip lists, JSON loads, description and intent counts match the pack's stages, no files of hers inside.
