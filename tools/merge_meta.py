"""Build the OPTIONAL combined OStimNetMetaData.json.
usage: python merge_meta.py <OStimNet 2.5.7 OStimNetMetaData.json> <Billy's Merged v3 OStimNetMetaData.json> <out.json> <pack_intents.json>...
Order: OStimNet entries, then Billy v3 entries (v3 already contains every OStimNet entry), then the pack intents.
Pack intents replace the intent of matching ids; positions are always kept. Hub/idle ids are never given an intent."""
import json, sys
base = json.load(open(sys.argv[1], encoding='utf-8-sig'))
v3 = json.load(open(sys.argv[2], encoding='utf-8-sig'))
out = {}
for src in (base, v3):
    for k, v in src.items(): out[k.lower()] = {'intent': v.get('intent', ''), 'positions': list(v.get('positions', []))}
changed = added = 0
for f in sys.argv[4:]:
    for k, it in json.load(open(f)).items():
        if k in out:
            if out[k]['intent'] != it: changed += 1
            out[k]['intent'] = it
        else:
            out[k] = {'intent': it, 'positions': []}; added += 1
missing = [k for k in base if k.lower() not in out] + [k for k in v3 if k.lower() not in out]
assert not missing
json.dump(out, open(sys.argv[3], 'w'), indent=4)
print('entries', len(out), 'base', len(base), 'v3', len(v3), 'changed', changed, 'added', added)
