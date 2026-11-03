# Lirael Creature Packs - SkyrimNet Patches

> **WARNING: This is AI generated. I am not personally into this stuff so I am not going to be reviewing by hand every animation to ensure the descriptions and intents are correct. This is to hopefully give a temporary base for people to operate in Skyrimnet with until someone is willing to review each scene individually in game and hopefully make a proper version for everyone who is into this.**
>
> **These patches are UNTESTED in game.**

By That Guy (Coronerra). SkyrimNet / OStimNet scene descriptions and intents for Lirael Atelier's creature
animation packs. None of her files are included.

## 1. Requirements for installing

Core (install these first):
- [SKSE64](https://skse.silverlock.org/)
- [Address Library for SKSE Plugins](https://www.nexusmods.com/skyrimspecialedition/mods/32444)
- [OStim Standalone](https://www.nexusmods.com/skyrimspecialedition/mods/98163) and its requirements
- [SkyrimNet](https://github.com/MinLL/SkyrimNet-GamePlugin) ([fateless.ai](https://fateless.ai/))
- [OStimNet 2.5.7](https://github.com/tetherball88/OStimNet/releases/tag/v2.5.7) by tetherball88
- [OStim Navigator 2.2.0+](https://github.com/tetherball88/OStimNavigator/releases/latest) by tetherball88
- OStimNet's own requirements: [OStim Hot Swap](https://www.nexusmods.com/skyrimspecialedition/mods/174565), [PapyrusUtil SE](https://www.nexusmods.com/skyrimspecialedition/mods/13048),
  [powerofthree's Papyrus Extender](https://www.nexusmods.com/skyrimspecialedition/mods/22854), [UIExtensions](https://www.nexusmods.com/skyrimspecialedition/mods/17561)
- For the creature packs: [JContainers](https://github.com/ryobg/JContainers) (https://www.nexusmods.com/skyrimspecialedition/mods/16495),
  Animated Beast's Cocks (ABC), and a behavior engine (Pandora or Nemesis), as listed on her posts

Lirael Atelier's packs, at these exact versions (other versions may not match):

| Pack | Version | Download |
|---|---|---|
| OCreatures Reforged | 1.9 | https://www.patreon.com/LiraelAtelier/posts/o-creatures-169001577 |
| OCreatures - Billyy Animation Pack COMPLETE | 2.1.2 | https://www.patreon.com/LiraelAtelier/posts/billyy-creatures-169281449 |
| FlufyFox OStim - Creatures | 0.5.2 | https://www.patreon.com/posts/171158464 |
| OCreatures - Baka Animation Pack | 0.1-dev | https://www.patreon.com/LiraelAtelier/posts/baka-creature-166350081 |

## 2. Thought process for the labeling

Every scene series (`Name-1 ... Name-N`) gets one intent from OStimNet's list. The rules, in order:

1. **Creature sex is aggressive by default.**
2. **If she is in control of anything, it is lustful.** "In control" means she works him (blowjob, handjob,
   boobjob, footjob...) and the scene data does not say the creature drives it (no creature `performer`, no
   `facefuck` tag), she moves on him (`performer` is her), or the scene is tagged cowgirl, reverse cowgirl,
   femdom, facesitting, seduce or masturbation.
3. **Creature oral on her is lustful**, unless the series is tagged forced or restrained.
4. **Werewolf scenes with kissing** are passionate or loving. Those words are not OStimNet intents, so
   loving (also tagged loving/love/romantic/cute) -> **romantic**, passionate -> **lustful**; forced -> aggressive.
5. **Bondage, yoke and restraint are never romantic.**
6. **Egg-laying and breeding are aggressive** unless she is clearly in control.
7. **Her own tags are kept.** Where Lirael Atelier already tagged a scene, hers is used even if the rules disagree;
   the disagreement is written in the CSV.
8. **Idle/hub scenes get no intent** (a tag would hide them from other intents), only a description.
9. **Unsure scenes are flagged**, e.g. she is in control but the scene is also tagged forced, or a female creature
   with a human man. They are in the `unsure` column.

Details, tie-breakers and examples per pack: [notes/INTENT_LOGIC.md](notes/INTENT_LOGIC.md).
Every stage with its actions, intent and `reason`: [data/fluffyfox_scenes.csv](data/fluffyfox_scenes.csv),
[data/baka_scenes.csv](data/baka_scenes.csv), [data/billyy_scenes.csv](data/billyy_scenes.csv),
[data/ocreatures_scenes.csv](data/ocreatures_scenes.csv).

## 3. Warning: clean up old mods first

OStim Navigator copies intents and positions from `OStimNetMetaData.json` **into each scene's own JSON file and
saves it**. It only ever adds tags and **never removes them**. "Billy's Merged Ostimnet Metadata" v3 tagged every
Billyy creature scene `lustful`, so if you ran it, those scene files already contain `lustful` permanently, even on
scenes she tagged `aggressive`. Removing v3 does not undo that.

To clean up (MO2):
1. Disable "Billy's Merged Ostimnet Metadata" v3 (this patch's optional file already contains everything in it).
2. Open MO2's **Overwrite** and delete anything under `SKSE/Plugins/OStim/scenes/` there
   (stale scene files written by Navigator). Leave other Overwrite content alone.
3. Reinstall each of her packs from the original zip (right-click the mod > Reinstall), so the scene files inside
   the mod folders are back to her originals.
4. Install these patches (section 4) and start the game. Navigator writes the correct tags again on first load.

## 4. How to install, and load order

Download from [Releases](https://github.com/Coronerra/Lirael-Creature-Packs-SkyrimNet-Patches/releases/latest).
In MO2, install each zip as its own mod (Install a new mod from archive), then arrange the left pane:

```
OStim Standalone
SkyrimNet
OStimNet
OStim Navigator
(Billy's Merged Ostimnet Metadata v3 - DISABLED)
OCreatures Reforged 1.9
OCreatures_SkyrimNet_Patch_for_v1.9          <- directly below its pack
OCreatures - Billyy Animation Pack COMPLETE 2.1.2
FlufyFox OStim - Creatures 0.5.2
FluffyFox_SkyrimNet_Patch_for_v0.5.2          <- directly below its pack
OCreatures - Baka Animation Pack 0.1-dev
Baka_SkyrimNet_Patch_for_v0.1-dev             <- directly below its pack
Lirael_Creature_Packs_SkyrimNet_Intents_OPTIONAL  <- below OStimNet (and below v3 if you keep it)
```

Billyy needs no description patch. Then run Pandora/Nemesis as her packs require, and launch.
To remove the optional intents, disable it (the tags Navigator already wrote stay; see section 3).

## 5. How to properly create files for OStimNet

As of November 2nd 2026, this is how to properly tag OSTIM animations for OSTIM net. Make sure to check if these rules have changed in the future builds.

- **Descriptions** go in `Data/SKSE/Plugins/OStimNet/animationsDescriptions/`. Every `*.json` in that folder is
  loaded (not subfolders), so a patch can ship its own file next to everyone else's. Format: one JSON object,
  `{"SceneId": "description text"}`, one entry per scene file (per stage), string values only.
  Navigator's in-game Dev Editor (OStim Options > OStim Navigator Options > Show Dev Editor > OStimNet tab) can also
  write them; it saves to `animationsDescriptions/<PackName>.json`.
- **Intents and positions** go in one single file: `Data/SKSE/Plugins/OStimNet/OStimNetMetaData.json`. There is no
  add-on folder for it, so whichever mod provides it lowest in MO2 wins; patches must merge into one file.
  Format: `{"sceneid": {"intent": "lustful", "positions": ["doggystyle"]}}`. Ids are lowercase. `intent` may be a
  comma list or empty.
- **How Navigator merges:** at startup it reads every scene, looks the id up in `OStimNetMetaData.json`, and appends
  the intent(s) then the positions to the scene's `tags`, skipping tags already there, then writes the scene file
  back to disk. Scenes whose id starts with `ostim` are skipped. Existing tags come first, so the author's own tags
  win. Positions are also read straight from scene tags using the alias list.

Full write-up: [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md).

## 6. The rules

- **Allowed intents** ([docs/Intents.md](https://github.com/tetherball88/OStimNet/blob/main/docs/Intents.md)):
  - `platonic` - non-sexual care (hugs, comfort). Care scenes only, never sex.
  - `romantic` - emotional connection; picks romantic/lustful scenes.
  - `lustful` - physical desire, no emotional investment needed; picks lustful/romantic scenes.
  - `transactional` - sex as an exchange; picks transactional/lustful/romantic scenes.
  - `dom` - consensual dominant/submissive; picks dom scenes.
  - `aggressive` - non-consensual; picks aggressive scenes.
  - No intent = generic, can be picked for any intent.
- **The 27 positions** (Navigator `SceneDescriptionData.h`): missionary, butterfly, matingpress, piledriver, anvil,
  bridge, seashell, cowgirl, reversecowgirl, amazon, doggystyle, prone, standing, bodyguard, nelson, carry, spooning,
  scissors, pretzel, lap, lotus, reverselotus, facesitting, sixtynine, spitroast, wheelbarrow, idle.
- **Aliases:** mating-press / mating press -> matingpress; pile-driver / pile driver -> piledriver;
  reverse-cowgirl / reverse cowgirl / rcg -> reversecowgirl; girl on top -> cowgirl; doggy / doggy-style /
  doggy style -> doggystyle; prone bone / prone-bone -> prone; full nelson / fullnelson -> nelson; spoon -> spooning;
  scissoring -> scissors; lap dance / lapdance -> lap; lotus position -> lotus; reverse lotus -> reverselotus;
  face-sitting / face sitting -> facesitting; and a few more in the source.
- **Ids are case-insensitive** in both descriptions and metadata.
- **Last loaded wins:** if two description files define the same id, the later one overwrites it (a warning is
  logged), so never repeat an id another file already describes.
- **Placeholder:** `{{scenedata.actors.N}}` is replaced with actor N's name.
- **Description style:** plain physical description of what the bodies are doing, one or two sentences, using the
  placeholders, as in the files OStimNet ships. No stage numbers or meta text.
- **Pack side** (the animation author's job, not a patch's): correct `actors` (`intendedSex`, creature `type`),
  correct `actions` with right `actor`/`target`/`performer` indexes (Navigator builds auto descriptions from them,
  and OStimNet's phases use the action tags intercourse, oral, penilestimulation, fingering, toying,
  clitoralstimulation), and standard position tags.

Sources: OStimNet [README](https://github.com/tetherball88/OStimNet), [Descriptions.md](https://github.com/tetherball88/OStimNet/blob/main/docs/Descriptions.md),
[Intents.md](https://github.com/tetherball88/OStimNet/blob/main/docs/Intents.md), [Phases.md](https://github.com/tetherball88/OStimNet/blob/main/docs/Phases.md),
[AnimationPacks.md](https://github.com/tetherball88/OStimNet/blob/main/docs/AnimationPacks.md); OStim Navigator source
`OStimNetMetaData.cpp`, `SceneDatabase.cpp`, `SceneDescriptionData.h` ([repo](https://github.com/tetherball88/OStimNavigator)).

## 7. What was changed and why

| Pack | Added | Why |
|---|---|---|
| FlufyFox 0.5.2 | 247 descriptions; intents for 229 stages (lustful 161, aggressive 68) | ships no descriptions and few intents |
| Baka 0.1-dev | 509 descriptions; intents for 469 stages (aggressive 417, lustful 52) | ships no descriptions; only 67 stages had intents |
| Billyy 2.1.2 | intents only, 1218 stages in the 225 series she left untagged; her 1062 tagged stages copied as-is | she ships her own descriptions for every stage, so none are added |
| OCreatures Reforged 1.9 | 84 descriptions, no intents | the pack's scenes are all idle/intro scenes with no actions |

- All intents for packs you don't have are ignored. The optional file also carries every OStimNet 2.5.7 and Billy v3
  entry, and replaces v3's blanket "lustful" on Billyy scenes with the rule results.
- **v1.0.1 style fix:** descriptions no longer end with "(Stage x of y.)", matching the style of the descriptions
  OStimNet ships.
- **Data errors in her scene files:** 41 Baka and 37 FlufyFox stages point an action at the
  wrong actor, or list the woman/female creature as the penetrating actor. Descriptions are written as the scene
  plays; each is listed in the CSV `data_notes` column. Her files were not changed.
- Unsure series: FlufyFox 11, Baka 1, Billyy 15. Series where the rules disagree with
  her tags (hers kept): Billyy 127, FlufyFox 3.
- Why separate add-on patches: [docs/WHY.md](docs/WHY.md).

## 8. Credits and additional information

- **Lirael Atelier** - the creature packs and conversions: https://www.patreon.com/LiraelAtelier (and the original
  animators credited in her packs: Billyy, FlufyFox, BakaFactory and others).
- **tetherball88** - [OStimNet](https://github.com/tetherball88/OStimNet) and [OStim Navigator](https://github.com/tetherball88/OStimNavigator).
- **The SkyrimNet team** - [SkyrimNet](https://github.com/MinLL/SkyrimNet-GamePlugin), [fateless.ai](https://fateless.ai/).
- **OStim Standalone** team.
- Patches, scripts and docs: That Guy (Coronerra).

License: MIT ([LICENSE](LICENSE)), covering only this project's own scripts, descriptions, intent metadata and
docs. **None of Lirael Atelier's files are included** in this repo or the zips, and none are overwritten or edited.

Updating for a new pack version: re-run `tools/gen.py` on the new pack, review the CSV diff, rebuild with
`tools/build.py`. Steps: [docs/UPDATING.md](docs/UPDATING.md).

Repo layout: `tools/` (generator and build scripts), `data/` (per-pack CSVs and generated JSON), `notes/`, `docs/`.

## 9. Other projects by Coronerra

- [Werewolf-Overhaul-Proof-of-Concept](https://github.com/Coronerra/Werewolf-Overhaul-Proof-of-Concept)
- [Beast-Aware](https://github.com/Coronerra/Beast-Aware)
- [OCum-Tull-Liquid-Softbody-Patch](https://github.com/Coronerra/OCum-Tull-Liquid-Softbody-Patch)
- [OCum-Werewolf-Shot](https://github.com/Coronerra/OCum-Werewolf-Shot)
- [OStim-Beast-Form](https://github.com/Coronerra/OStim-Beast-Form)
