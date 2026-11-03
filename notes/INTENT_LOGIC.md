# Intent logic

> WARNING: This is AI generated. I am not personally into this stuff so I am not going to be reviewing by hand every animation to ensure the descriptions and intents are correct. This is to hopefully give a temporary base for people to operate in Skyrimnet with until someone is willing to review each scene individually in game and hopefully make a proper version for everyone who is into this.
>
> These patches are UNTESTED in game.

The code is `tools/common.py` (`stage_signals`, `series_intent`) and `tools/gen.py`. Every stage's row in
`data/<pack>_scenes.csv` has a `reason` column (the rule that fired and the tags or actions that triggered it),
a `logic_doc` column linking to a section below, plus `conflict_with_her_tags`, `unsure` and `data_notes`.

Vocabulary (OStimNet): platonic, romantic, lustful, transactional, dom, aggressive.
Passionate and loving are not in it: **passionate -> lustful**, **loving -> romantic**.

**One intent per scene series.** A series is all stages `Name-1 ... Name-N`. Signals are pooled over every stage,
so "she is in control of anything" means in any stage.

## Evaluation order (tie-breakers)
Rules are checked top to bottom and the first match wins:
1. Werewolf + kiss/kissing + loving tags, not restrained -> romantic (R4)
2. She is in control of anything -> lustful (R2)
3. Werewolf + kissing (no loving tags) -> lustful; if forced -> aggressive (R4)
4. Creature oral on her, with no force or restraint tags -> lustful (R3)
5. Otherwise aggressive, with the reason naming restraint (R5), then egg-laying (R6), then force tags (R1)
6. Final guard: restraint never ends romantic (R5)
7. Her own intent tags always override the rule result (R7)

## R0 idles and hubs
Scenes with no actions (hubs, idle/intro scenes, all of OCreatures Reforged 1.9) get a description only and
**no intent**. An intent tag on an idle would hide it when another intent is selected.
- fluffyfox: `FlufyOAtronachFlameHubFM` (1 stages, actions ``) -> ****. idle/hub (no actions): description only, no intent
- fluffyfox: `FlufyOCanineHubFM` (1 stages, actions ``) -> ****. idle/hub (no actions): description only, no intent
- baka: `BakaOAtronachFrostHubFM` (1 stages, actions ``) -> ****. idle/hub (no actions): description only, no intent
- baka: `BakaOAtronachStormHubFM` (1 stages, actions ``) -> ****. idle/hub (no actions): description only, no intent
- billyy: `BillyyAtronachFlameHubFF` (1 stages, actions ``) -> ****. idle/hub (no actions): description only, no intent
- billyy: `BillyyAtronachFrostHubFM` (1 stages, actions ``) -> ****. idle/hub (no actions): description only, no intent

## R1 default aggressive
Creature sex is aggressive by default. Force tags only change the reason text: forced, rape, defeated, struggle,
conquering, harassing, aggressive, "aggressive default".
- fluffyfox: `FlufyOCatTest` (5 stages, actions `vaginalsex`) -> **aggressive**. creature sex (default)
- fluffyfox: `FlufyODefeatedRiekling` (2 stages, actions `default`) -> **aggressive**. forced: defeated
- baka: `BakaOBearDoggy` (5 stages, actions `vaginalsex`) -> **aggressive**. creature sex (default)
- baka: `BakaOBearHoneySucking` (6 stages, actions `vaginalsex`) -> **aggressive**. creature sex (default)
- billyy: `BillyyAshHopperBehind` (5 stages, actions `vaginalsex`) -> **aggressive**. creature sex (default)
- billyy: `BillyyAshHopperDoggy` (5 stages, actions `vaginalsex`) -> **aggressive**. creature sex (default)

## R2 she is in control
"If she is in control of anything it is lustful." Control is detected per stage from:
- actions where she works him: blowjob, handjob, boobjob, footjob, balljob, thighjob, bodyjob, femalemasturbation.
  It does NOT count if the action's `performer` is a creature, or the stage is tagged facefuck.
  (Baka/FlufyFox list her as the action actor; Billyy lists her as target. Detection is by action type, not index.)
- vaginal/anal sex where the `performer` is her (she moves on him)
- position/role tags: cowgirl, reversecowgirl, femdom, "female domanation", facesit/facesitting, seduce,
  footjob, masturbation.
Control wins over force, restraint and egg tags; those cases are listed in the `unsure` column.
- fluffyfox: `FlufyOFalmerCowGirl` (7 stages, actions `vaginalsex`) -> **lustful**. she is in control: tag cowgirl
- fluffyfox: `FlufyOFdraugBJ` (7 stages, actions `blowjob;handjob`) -> **lustful**. she is in control: she performs blowjob; she performs handjob
- baka: `BakaOBoarRMate` (6 stages, actions `vaginalsex;blowjob;handjob`) -> **lustful**. she is in control: she performs blowjob; she performs handjob
- baka: `BakaOHMAWT` (5 stages, actions `vaginalsex;analsex;blowjob`) -> **lustful**. she is in control: she performs blowjob
- billyy: `BillyyAshHopper3pSpitroast` (5 stages, actions `blowjob`) -> **lustful**. she is in control: she performs blowjob
- billyy: `BillyyAshHopperBlowjob` (5 stages, actions `blowjob`) -> **lustful**. she is in control: she performs blowjob

## R3 creature oral on her
lickingvagina action, or cunnilingus/analinggus tags -> lustful, unless the series is tagged forced or restrained.
- fluffyfox: `FlufyOCanineMiss` (7 stages, actions `vaginalsex;lickingvagina`) -> **lustful**. creature oral on her
- fluffyfox: `FlufyODogMiss` (7 stages, actions `vaginalsex;lickingvagina`) -> **lustful**. creature oral on her
- baka: `BakaOGoaty` (5 stages, actions `vaginalsex;lickingvagina`) -> **lustful**. creature oral on her
- billyy: `BillyyAshHopper3pDoublePen` (5 stages, actions `analsex`) -> **lustful**. creature oral on her
- billyy: `BillyyAshHopperCrab` (5 stages, actions `lickingvagina`) -> **lustful**. creature oral on her

## R4 werewolf kissing
A series with a Werewolf actor and kiss/kissing tags is read as either:
- loving -> **romantic**, when it also has loving, love, romantic or cute tags
- passionate -> **lustful**, otherwise
Forced kissing scenes stay aggressive. Restrained ones are never romantic.
- billyy: `BillyyWerewolf3pHoldingDP` (6 stages, actions `analsex`) -> **lustful**. werewolf scene with kissing (passionate, no loving tags)
- billyy: `BillyyWerewolf4pGangbang1` (6 stages, actions `analsex`) -> **lustful**. werewolf scene with kissing (passionate, no loving tags)

## R5 restraint and bondage
Tags bound, bondage, restraints, yoke, pillory, pillorylow, armbinder, cuffed, tied, frozen, stocks, chained, shackles.
Never romantic; aggressive unless she is in control.
- baka: `BakaOHorseRidingGirl01` (5 stages, actions `vaginalsex`) -> **aggressive**. restraint: restraints
- baka: `BakaOHorseTraining` (5 stages, actions `vaginalsex`) -> **aggressive**. restraint: restraints
- billyy: `BillyyCaninePilloryLowDoggy` (5 stages, actions `vaginalsex`) -> **aggressive**. restraint: pillorylow
- billyy: `BillyyCaninePilloryLowDoggyAnal` (5 stages, actions `analsex`) -> **aggressive**. restraint: pillorylow

## R6 egg-laying and breeding
oviposition, eggs, breeding -> aggressive unless she is in control (e.g. cowgirl).
- baka: `BakaOAHOvi` (5 stages, actions `vaginalsex`) -> **aggressive**. egg-laying/breeding: eggs
- baka: `BakaOCHOviposition02` (5 stages, actions `vaginalsex`) -> **aggressive**. egg-laying/breeding: egg,oviposition
- billyy: `BillyyChaurusInsectStyle` (6 stages, actions `vaginalsex`) -> **aggressive**. egg-laying/breeding: eggs,oviposition
- billyy: `BillyyGiantSpiderDoggy` (6 stages, actions `vaginalsex`) -> **aggressive**. egg-laying/breeding: eggs,oviposition

## R7 her own tags
If any stage already carries an intent tag from Lirael Atelier, her tag is kept for that stage and the series
gets her tag. A rule result that disagrees goes in `conflict_with_her_tags` ("kept hers"). OStim Navigator does
the same at runtime: tags a scene already has come first and are never replaced.
Billyy 2.1.2: 205 of 430 series are hers; the rules only filled the 225 untagged series.
- fluffyfox: `FlufyOFGiantForcedBJ` (5 stages, actions `blowjob`) -> **aggressive**. she is in control: she performs blowjob; tag femdom Conflict: her tag aggressive vs rule lustful (kept hers).
- fluffyfox: `FlufyOFdraugcowgirl` (6 stages, actions `vaginalsex`) -> **aggressive**. she is in control: tag femdom Conflict: her tag aggressive vs rule lustful (kept hers).
- billyy: `BillyyAshHopperFacefuck` (5 stages, actions `blowjob`) -> **aggressive**. she is in control: she performs blowjob Conflict: her tag aggressive vs rule lustful (kept hers).
- billyy: `BillyyAshHopperLayingAnal` (5 stages, actions `analsex`) -> **lustful**. creature sex (default) Conflict: her tag lustful vs rule aggressive (kept hers).

## Female creature with a human man
A few FlufyFox scenes (female draugr, giantess, flame atronach, falmer) pair a female creature with a man.
The rules were applied with the female creature as "her". All are flagged in `unsure`.

## Known data quirks
Some Baka/FlufyFox actions point their target at another creature, or list the female as the penetrating
actor. Descriptions are written as the scene obviously plays; each case is in `data_notes`.
