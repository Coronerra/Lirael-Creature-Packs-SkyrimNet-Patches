# SkyrimNet / OStimNet requirements for animation packs and patches

What SkyrimNet NPCs need from an OStim animation to understand and use it, and how each need is met.
Checked against **OStimNet 2.5.7** (latest, 2026-10-22) and **OStim Navigator 2.2.0 / 2.2.1** (2.2.1 changed only
a prompt location; the description and metadata loaders are identical).

Sources:
- OStimNet README and docs: https://github.com/tetherball88/OStimNet (`docs/Descriptions.md`, `docs/Intents.md`,
  `docs/Phases.md`, `docs/AnimationPacks.md`, `CHANGELOG.md`)
- OStim Navigator source: https://github.com/tetherball88/OStimNavigator (`OStimNetMetaData.cpp`, `SceneDatabase.cpp`,
  `SceneDescriptionData.h`)
- SkyrimNet: https://fateless.ai/ and https://github.com/MinLL/SkyrimNet-GamePlugin. Neither has animation-author
  guidance; animations are handled entirely by OStimNet and OStim Navigator.

## 1. Required mods (users)
SkyrimNet, OStim Standalone, OStimNet, OStim Navigator 2.0.2+ (it supplies all scene data and builds descriptions),
OStim Hot Swap, PapyrusUtil, powerofthree's Papyrus Extender, UIExtensions; OCum Ascended optional.

## 2. Scene data (pack side: the animation author's files)
Navigator reads every OStim scene file (`SKSE/Plugins/OStim/scenes/**.json`). It uses:
- **actors**: count, `intendedSex`, `type` (creature race) and actor tags
- **actions**: `type`, `actor`, `target`, `performer`. Navigator auto-builds a description from these when no
  custom description exists, and OStimNet's thread phases use the OStim action tags they imply
  (`intercourse`, `oral`, `penilestimulation`, `fingering`, `toying`, `clitoralstimulation`).
  Wrong actor/target indexes mean wrong auto descriptions and phases.
- **scene tags**: positions (e.g. `missionary`, `doggystyle`, `cowgirl`) and intents.
- Furniture comes from the scene's furniture field.

How to meet it: correct actions and indexes in each scene, standard position tags. This is the pack author's job,
not a patch's. In Lirael Atelier's packs a few Baka/FlufyFox actions point at the wrong actor; they are listed in
the `data_notes` column of `data/*.csv` for her if she wants them. Nothing here changes them.

## 3. Descriptions
- Folder: `Data/SKSE/Plugins/OStimNet/animationsDescriptions/`. **Every** `*.json` there is loaded
  (not subfolders), so a patch can add its own file without touching anyone else's.
- Format: one JSON object, `{"SceneId": "text"}`. Values must be strings (anything else is skipped).
  Ids are matched case-insensitively. One entry per **scene file**, i.e. per stage (`Name-1`, `Name-2`...).
- Placeholders: `{{scenedata.actors.N}}` = actor N's name.
- Style (from the files OStimNet ships): plain physical description of what the bodies are doing, one or two
  sentences, using the placeholders. No stage numbers or other meta text.
- If two files define the same id, the one loaded **last overwrites** the other (a warning is logged), so a patch
  must never repeat ids the pack already describes.
- The MCM option *Use custom descriptions* (default on) picks custom over auto-generated.

How we meet it: one file per pack named `zz <Pack> SkyrimNet Patch.json` (OCreatures Reforged uses `zz OCreatures Reforged SkyrimNet Patch.json`), only ids with no existing description
(Billyy 2.1.2 is skipped entirely because she ships her own).

## 4. Intents and positions (OStimNetMetaData.json)
- Navigator reads exactly **one** file: `Data/SKSE/Plugins/OStimNet/OStimNetMetaData.json`. There is no add-on
  folder for intents in 2.5.7 / Navigator 2.2.1; the last mod in MO2 that provides it wins.
- Format: `{"sceneid": {"intent": "a,b", "positions": ["..."]}}`. Ids are lowercased. Intent can be a comma list.
- Valid intents: `platonic` (care scenes only, never sex), `romantic`, `lustful`, `transactional`, `dom`,
  `aggressive`. A scene with **no** intent tag is generic and can be picked for any intent.
- Which tagged scenes each thread intent may pick: romantic -> romantic/lustful; lustful -> lustful/romantic;
  transactional -> transactional/lustful/romantic; dom -> dom; aggressive -> aggressive.
  So idles/hubs should stay untagged.
- Valid positions: Navigator's canonical list (missionary, butterfly, matingpress, piledriver, anvil, bridge, seashell,
  cowgirl, reversecowgirl, amazon, doggystyle, prone, standing, bodyguard, nelson, carry, spooning, scissors, pretzel,
  lap, lotus, reverselotus, facesitting, sixtynine, spitroast, wheelbarrow, idle) plus aliases (`doggy` ->
  `doggystyle`, `reverse cowgirl` -> `reversecowgirl`...).
- At startup Navigator adds the intent and position tags to each scene's own JSON and **writes that file back to
  disk** (ids starting `ostim` are skipped). It only adds tags the scene does not already have and never removes
  any. A scene that already has a different intent keeps both, with hers first.

How we meet it: an optional combined file = OStimNet 2.5.7 + Billy v3 + our intents. Her own intent tags are
copied as-is so nothing contradicts them. Positions: Billy v3 already carries Navigator's auto-populated positions for every one of
these scenes that has a position tag; `merge_meta.py` would fill any empty ones the same way Navigator's
*Auto Populate Positions* does (none were empty in this release).

## 5. Install (users)
1. Each description patch directly below its pack.
2. Optional intents below OStimNet and below Billy's Merged Ostimnet Metadata v3 (v3 can be disabled).
3. **If you used Billy v3 before:** its blanket "lustful" was already written into the Billyy scene files (in the pack
   folder or MO2 Overwrite), so some of her aggressive scenes may carry both tags. Reinstall the Billyy pack (and clear
   `SKSE/Plugins/OStim/scenes` from Overwrite) to start clean.

## 6. Notes on creatures
OStimNet 2.5.7 only offers humanoid NPCs for scenes it starts itself (`Nearby actors humanoid only`, default on).
Creature scenes usually come from other mods; OStimNet then evaluates them retroactively. That makes the
description the most useful part, and intents matter mainly when the AI changes position mid-scene.

## 7. Making or updating a patch
See `UPDATING.md`. Keep ids exact, never duplicate an existing description id, only use the six intents, never tag
idles, and ship no files from the pack.
