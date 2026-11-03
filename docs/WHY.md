# Why these patches exist and why they are separate

SkyrimNet NPCs understand an OStim scene through OStimNet: a text description per scene, plus an intent
(romantic, lustful, aggressive...) used to pick scenes. Most of Lirael Atelier's creature packs ship without
descriptions, and many scenes have no intent, so NPCs had nothing to go on.

**Add-on, not edit.** OStim Navigator loads every `*.json` in `SKSE/Plugins/OStimNet/animationsDescriptions/`,
so descriptions can sit in their own file (`zz <Pack> SkyrimNet Patch.json`) next to her pack. No description id
she already has is duplicated. Her scene files stay untouched, so she can keep working and releasing; when she
does, the patch is regenerated, not merged by hand.

**Intents.** Navigator reads a single `OStimNetMetaData.json` and at runtime writes the intent tags into each
scene's own file. That is normal OStimNet behaviour for every pack, not something this patch ships. Because
only one metadata file is read, the intents are one optional combined file. Tags she set herself always win.

**Separate per pack.** Each zip is tied to one exact pack version, so a new release of one pack only means
rebuilding that one patch.
