# Lirael Creature Packs - SkyrimNet Patches

> **Disclaimer: This was AI generated.** I'm not into bestiality and won't subject myself to reviewing all of these animations, so if anyone is willing to go through them all and make a proper mod, please be my guest. This is just a crude add-on to help SkyrimNet NPCs understand the scenes, and I'm sure there are mistakes. **These patches are UNTESTED in game.** I haven't run them and I'm not going to. This is merely to help those who are into it.

SkyrimNet / OStimNet scene descriptions and intents for Lirael Atelier's creature animation packs.
By That Guy (Coronerra).

**None of Lirael Atelier's files are included in this repository or in any patch zip.** Nothing of hers is
overwritten or edited. Her packs are required: https://www.patreon.com/LiraelAtelier

| Patch zip | Requires exactly | Contains |
|---|---|---|
| `FluffyFox_SkyrimNet_Patch_for_v0.5.2.zip` | FlufyFox OStim - Creatures v0.5.2 | descriptions |
| `Baka_SkyrimNet_Patch_for_v0.1-dev.zip` | OCreatures - Baka Animation Pack v0.1-dev | descriptions |
| `OCreatures_SkyrimNet_Patch_for_v1.9.zip` | OCreatures Reforged v1.9 | descriptions (idles only) |
| `Lirael_Creature_Packs_SkyrimNet_Intents_OPTIONAL.zip` | the above + Billyy Creatures COMPLETE v2.1.2 | combined intents |

Billyy 2.1.2 already ships her own descriptions, so it only gets intents (for the 225 series she left untagged).

Built against a modified Nolvus 6.0.21 setup (OStim Navigator 2.2.0, OStimNet 2.5.7). Not tested in game.

## Install (MO2)
- Each description patch: its own mod, directly below the pack it is for.
- Optional intents: below OStimNet and below "Billy's Merged Ostimnet Metadata" v3 (it contains everything in
  v3, so v3 may be disabled). OStim Navigator reads only one `OStimNetMetaData.json`, which is why intents
  can't be a per-pack add-on.

## Why separate patches, and why add-ons
See `docs/WHY.md`. Short version: one patch per pack and version, so each can be updated or dropped on its own,
and nothing of hers is shipped, so Lirael can keep releasing without anyone redistributing or overriding her work.

## Requirements
What SkyrimNet/OStimNet need from animations and patches, and how to meet them: [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md).

If you used Billy's Merged Ostimnet Metadata v3 before, reinstall the Billyy pack to clear the old tags Navigator wrote into its scene files (see REQUIREMENTS.md section 5).

## Contents
- `tools/` generator: `common.py` (intent rules), `gen.py` (descriptions, intents, CSV), `merge_meta.py`, `build.py`
- `data/<pack>_scenes.csv` one row per stage: scene id, stage, actions, actors, her tags, intent, `reason`,
  `logic_doc`, conflicts, unsure, data notes, description
- `notes/INTENT_LOGIC.md` the intent rules, how they were applied, tie-breakers and examples
- `docs/UPDATING.md` updating for a new pack version

## License
MIT, for this project's own metadata and scripts only (see LICENSE). The animations and scene files belong to
Lirael Atelier and the original animators.
