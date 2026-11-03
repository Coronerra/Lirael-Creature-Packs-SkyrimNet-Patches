"""Build the patch zips from data/ (run gen.py first).
usage: python build.py <OStimNet meta json> <Billy v3 meta json> <out_dir>"""
import os, sys, zipfile, subprocess, json
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.dirname(here); data = os.path.join(repo, 'data')
out = sys.argv[3]; os.makedirs(out, exist_ok=True)
LINK = 'https://www.patreon.com/LiraelAtelier'
NOTE = ("This was AI generated. I'm not into bestiality and won't subject myself to reviewing all of these\n"
        "animations, so if anyone is willing to go through them all and make a proper mod, please be my guest.\n"
        "This is just a crude add-on to help SkyrimNet NPCs, and I'm sure there are mistakes.\n"
        "UNTESTED in game: I haven't run these and won't. This is merely to help those who are into it.\n")
PACKS = [('fluffyfox', 'FluffyFox', 'FlufyFox OStim - Creatures', '0.5.2'),
         ('baka', 'Baka', 'OCreatures - Baka Animation Pack', '0.1-dev'),
         ('ocreatures', 'OCreatures', 'OCreatures Reforged', '1.9')]
DT = lambda d: zipfile.ZipInfo(d, date_time=(2026, 11, 2, 0, 0, 0))
def w(z, name, text):
    i = DT(name); i.compress_type = zipfile.ZIP_DEFLATED; i.external_attr = 0o644 << 16; z.writestr(i, text)
for key, short, full, ver in PACKS:
    zp = os.path.join(out, '%s_SkyrimNet_Patch_for_v%s.zip' % (short, ver))
    desc = open(os.path.join(data, key + '_descriptions.json'), encoding='utf-8').read()
    readme = f"""{short} SkyrimNet Patch for v{ver}
by That Guy (Coronerra)

NOTE: {NOTE}
REQUIRES exactly: {full} v{ver} by Lirael Atelier - {LINK}
This patch was generated from that exact version. It may not match other versions
(new, renamed or removed scenes will be missing or wrong). Check for an updated patch first.

Also requires: OStim Standalone, OStimNet, OStim Navigator (descriptions are read by OStim Navigator).

What it is: a pure add-on. It contains ONE file of scene descriptions for SkyrimNet/OStimNet:
  SKSE/Plugins/OStimNet/animationsDescriptions/zz {short} SkyrimNet Patch.json
None of Lirael Atelier's files are included, and none of her files are overwritten or edited.

Install (MO2): install as a new mod and place it directly BELOW {full}.

Intents (optional) are NOT in this zip. They are in
Lirael_Creature_Packs_SkyrimNet_Intents_OPTIONAL.zip - see its README.

Sources, rules and per-scene notes: the Lirael-Creature-Packs-SkyrimNet-Patches repository by Coronerra.
License: MIT for this patch's own metadata only. The animations belong to their authors.
"""
    with zipfile.ZipFile(zp, 'w') as z:
        w(z, 'SKSE/Plugins/OStimNet/animationsDescriptions/zz %s SkyrimNet Patch.json' % short, desc)
        w(z, 'README.txt', readme)
    print(zp, os.path.getsize(zp))
tmp = os.path.join(out, '_meta.json')
subprocess.check_call([sys.executable, os.path.join(here, 'merge_meta.py'), sys.argv[1], sys.argv[2], tmp] +
                      [os.path.join(data, k + '_intents.json') for k in ('fluffyfox', 'baka', 'billyy')])
zp = os.path.join(out, 'Lirael_Creature_Packs_SkyrimNet_Intents_OPTIONAL.zip')
readme = f"""Lirael Creature Packs - SkyrimNet Intents (OPTIONAL)
by That Guy (Coronerra)

NOTE: {NOTE}
Covers exactly: Billyy Creatures COMPLETE v2.1.2, FlufyFox OStim - Creatures v0.5.2,
OCreatures - Baka Animation Pack v0.1-dev (all by Lirael Atelier - {LINK}).
Other versions may not match. Packs you don't have are simply ignored.
OCreatures Reforged 1.9 has only idle/intro scenes, so it gets no intents.

OStim Navigator reads only ONE SKSE/Plugins/OStimNet/OStimNetMetaData.json, so this is a combined
replacement of that file: all OStimNet 2.5.7 entries + all "Billy's Merged Ostimnet Metadata" v3 entries
+ the new creature intents (which replace v3's blanket "lustful" on Billyy creature scenes)
If you used Billy v3 before, reinstall the Billyy pack: Navigator already wrote v3's tags into its scene files.

Install order (MO2), top to bottom:
  OStimNet
  Billy's Merged Ostimnet Metadata v3   (optional; this file already contains it - you may disable it)
  THIS MOD                               (must be BELOW both)
To uninstall, just disable it; the file below it is used again.

Her own intent tags always win: Navigator keeps tags a scene already has and only adds missing ones.
Navigator writes these intent tags into the pack's scene files at runtime. That is normal OStimNet
behaviour (it does the same for every pack); this mod ships none of her files.
License: MIT for this metadata only.
"""
with zipfile.ZipFile(zp, 'w') as z:
    w(z, 'SKSE/Plugins/OStimNet/OStimNetMetaData.json', open(tmp).read()); w(z, 'README.txt', readme)
os.remove(tmp); print(zp, os.path.getsize(zp))
