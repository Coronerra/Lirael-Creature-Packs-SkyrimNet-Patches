"""Generate SkyrimNet/OStimNet patch data for Lirael Atelier's creature packs.

usage: python gen.py <pack_key> <extracted_pack_root> <out_dir>
pack_key: fluffyfox | baka | billyy | ocreatures

Writes (never touches the pack itself):
  <out_dir>/<pack>_descriptions.json   OStimNet animationsDescriptions add-on (not for billyy)
  <out_dir>/<pack>_intents.json        {scene_id_lower: intent} for the optional metadata merge
  <out_dir>/<pack>_scenes.csv          per stage: scene id, stage, actions, intent, why
"""
import sys, os, json, csv, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from common import *

NICE = {'AtronachFlame': 'flame atronach', 'AtronachFrost': 'frost atronach', 'AtronachStorm': 'storm atronach',
        'ChaurusFlyer': 'chaurus hunter', 'ChaurusReaper': 'chaurus reaper', 'DwarvenCenturion': 'dwarven centurion',
        'DwarvenSphere': 'dwarven sphere', 'DwarvenSpider': 'dwarven spider', 'DwarvenBallista': 'dwarven ballista',
        'SabreCat': 'sabre cat', 'SpiderGiant': 'giant frostbite spider', 'SpiderLarge': 'large frostbite spider',
        'Spider': 'frostbite spider', 'VampireLord': 'vampire lord', 'Dragonpriest': 'dragon priest',
        'DragonPriest': 'dragon priest', 'BoarMount': 'riding boar', 'Boarmount': 'riding boar', 'Canine': 'canine',
        'IceWraith': 'ice wraith', 'Wispmother': 'wispmother'}
POS = [('matingpress', 'in a mating press'), ('reversecowgirl', 'in reverse cowgirl'), ('cowgirl', 'in cowgirl, on top'),
       ('missionary', 'in missionary'), ('doggystyle', 'doggy style, from behind'), ('doggy', 'doggy style, from behind'),
       ('spooning', 'spooning on their sides'), ('piledriver', 'in a piledriver'), ('69', 'in a sixty-nine'),
       ('kneeling', 'kneeling'), ('sitting', 'sitting'), ('standing', 'standing'), ('laying', 'lying down'),
       ('holding', 'held up off the ground'), ('floating', 'floating')]
ATAG = {'lyingback': 'lies on her back', 'allfours': 'is on all fours', 'kneeling': 'kneels', 'standing': 'stands'}
P = lambda i: '{{scenedata.actors.%d}}' % i


def kind(a):
    t = a.get('type') or ''
    return NICE.get(t, re.sub(r'(?<!^)([A-Z])', r' \1', t).lower())


def her_index(A):
    h = [i for i, a in enumerate(A) if not a.get('type')]
    hf = [i for i in h if a_sex(A[i]) == 'female']
    if hf: return hf[0]
    cf = [i for i, a in enumerate(A) if a.get('type') and a_sex(a) == 'female']
    return cf[0] if cf else (h[0] if h else 0)


def a_sex(a): return (a.get('intendedSex') or '').lower()


def name(A, i):
    return ('the %s %s' % (kind(A[i]), P(i))) if A[i].get('type') else P(i)


def describe(j, stage, total):
    A = j['actors']; tags = {t.lower() for t in j.get('tags', [])}
    her = her_index(A); notes = []
    others = [i for i in range(len(A)) if i != her]
    if not j.get('actions'):
        nm = [name(A, i) for i in others]
        who = nm[0] if len(nm) == 1 else ', '.join(nm[:-1]) + ' and ' + nm[-1]
        bits = ['%s %s' % (P(i), ATAG[t]) for i in range(len(A)) for t in A[i].get('tags', []) if t in ATAG][:2]
        s = '%s and %s are together, getting ready before anything starts.' % (name(A, her), who)
        if bits: s += ' ' + ', '.join(bits) + '.'
        return s[0].upper() + s[1:], notes
    sent = []; done = set(); control = False
    for a in j['actions']:
        t = a['type']; act, tgt, perf = a.get('actor'), a.get('target'), a.get('performer')
        valid = lambda i: i is not None and 0 <= i < len(A)
        if t in ('vaginalsex', 'analsex'):
            pen = act if valid(act) else others[0]
            rec = tgt if valid(tgt) and tgt != pen else her
            if a_sex(A[pen]) == 'female' and valid(tgt) and a_sex(A[tgt]) == 'male':
                pen, rec = tgt, pen  # a woman/female creature is listed as actor of penetration: he penetrates her
                notes.append('%s actor is female, target male; described with the male penetrating' % t)
            if valid(tgt) and A[tgt].get('type') and A[pen].get('type') and tgt != her and not A[her].get('type'):
                notes.append('%s target points at a creature; described on the woman' % t); rec = her
            if perf == rec or (tags & {'cowgirl', 'reversecowgirl'} and rec == her): perf = rec
            hole = 'pussy' if t == 'vaginalsex' else 'ass'
            s = ('%s rides %s, taking him in her %s' % (name(A, rec), name(A, pen), hole)) if perf == rec else \
                ('%s fucks %s in the %s' % (name(A, pen), P(rec), hole))
        elif t in SHE_WORKS:
            w = act if valid(act) and (act == her or not A[act].get('type')) else (tgt if valid(tgt) and (tgt == her or not A[tgt].get('type')) else her)
            r = tgt if valid(tgt) and tgt != w else act if valid(act) and act != w else others[0]
            if r == w: r = others[0]
            verb = {'blowjob': 'sucks %s\'s cock', 'handjob': 'strokes %s\'s cock with her hand',
                    'boobjob': 'works %s\'s cock between her breasts', 'footjob': 'works %s\'s cock with her feet',
                    'balljob': 'plays with %s\'s balls', 'thighjob': 'squeezes %s\'s cock between her thighs',
                    'bodyjob': 'rubs her body along %s\'s cock', 'femalemasturbation': 'touches herself for %s'}[t]
            if A[w].get('type'): s = '%s %s' % (name(A, w), verb % name(A, r))
            else: s = '%s %s' % (P(w), verb % name(A, r))
        elif t in ORAL_ON_HER:
            l = act if valid(act) and A[act].get('type') else others[0]
            s = '%s licks %s\'s pussy' % (name(A, l), P(her))
        else:
            s = '%s and %s press their bodies together' % (name(A, others[0]), P(her))
        if s not in done: done.add(s); sent.append(s)
    out = ', while '.join(sent[:2]) if len(sent) <= 2 else ', '.join(sent[:-1]) + ', and ' + sent[-1]
    out = out[0].upper() + out[1:] + '.'
    pos = list(dict.fromkeys(p for k, p in POS if k in tags))
    if pos: out += ' They are ' + (pos[0] if len(pos) == 1 else pos[0] + ', ' + pos[1]) + '.'
    fl = []
    if tags & RESTRAINT: fl.append('%s is restrained and cannot get away' % P(her))
    if 'forced' in tags or 'rape' in tags: fl.append('%s is being taken by force' % P(her))
    elif 'defeated' in tags: fl.append('%s has been defeated and is in no state to resist' % P(her))
    if tags & {'oviposition', 'eggs'}: fl.append('%s pumps its eggs deep inside her' % name(A, others[0]))
    if tags & {'femdom', 'female domanation', 'female domination'}: fl.append('%s is the one in charge' % P(her))
    if tags & KISS: fl.append('they kiss')
    if 'tentacles' in tags or 'tentacle' in tags: fl.append('tentacles wrap around her')
    if 'gangbang' in tags: fl.append('she is shared between them')
    if tags & {'love', 'loving'} and not (tags & FORCE): fl.append('it is tender and affectionate')
    elif 'rough' in tags: fl.append('it is rough')
    clim = [i for i, a in enumerate(A) if 'climaxing' in [t.lower() for t in a.get('tags', [])] and a.get('type')]
    if clim: fl.append('%s is climaxing' % name(A, clim[0]))
    for f in fl: out += ' ' + f[0].upper() + f[1:] + '.'
    return out, notes


def rule_anchor(why, conflict, it_final, acts):
    if not acts: return 'r0-idles-and-hubs'
    if conflict or (it_final is None): return 'r7-her-own-tags'
    for k, a in [('werewolf', 'r4-werewolf-kissing'), ('in control', 'r2-she-is-in-control'), ('oral', 'r3-creature-oral-on-her'),
                 ('restraint', 'r5-restraint-and-bondage'), ('egg', 'r6-egg-laying-and-breeding'), ('forced', 'r1-default-aggressive')]:
        if k in why: return a
    return 'r1-default-aggressive'


def main(key, root, outd):
    os.makedirs(outd, exist_ok=True)
    sc = load(root)
    ser = collections.defaultdict(list)
    for sid, (rel, j) in sc.items():
        b, n = series_of(sid); ser[b].append((n, sid, rel, j))
    desc, intents, rows, positions = {}, {}, [], {}
    existing = set()
    dd = os.path.join(root, 'SKSE', 'Plugins', 'OStimNet', 'animationsDescriptions')
    if os.path.isdir(dd):
        for f in os.listdir(dd):
            if f.endswith('.json'): existing |= set(json.load(open(os.path.join(dd, f), encoding='utf-8-sig')))
    for b in sorted(ser):
        st = sorted(ser[b]); js = [x[3] for x in st]
        acts = any(j.get('actions') for j in js)
        hers = her_intents(js)
        herset = sorted({t for h in hers for t in h})
        if acts:
            it, why, unsure = series_intent(js)
            conflict = ''
            if herset:
                if herset != [it]: conflict = 'her tag %s vs rule %s (kept hers)' % ('/'.join(herset), it)
                it_final = herset[0] if len(herset) == 1 else None
            else:
                it_final = it
        else:
            it, why, unsure, conflict, it_final = '', 'idle/hub (no actions): description only, no intent', '', '', None
        for n, sid, rel, j in st:
            d, notes = ('', [])
            if key != 'billyy' and sid not in existing:
                d, notes = describe(j, n, len(st)); desc[sid] = d
            if j.get('actions') and nav_positions(j): positions[sid.lower()] = nav_positions(j)
            stage_hers = [t for t in j.get('tags', []) if t in INTENTS]
            if acts and j.get('actions'):
                if stage_hers: intents[sid.lower()] = stage_hers[0]
                elif it_final: intents[sid.lower()] = it_final
                else: intents[sid.lower()] = it
            rows.append({'scene_id': sid, 'series': b, 'stage': n, 'stages': len(st),
                         'actions': ';'.join(a['type'] for a in j.get('actions', [])),
                         'actors': ';'.join((a.get('type') or 'human') + '/' + (a.get('intendedSex') or '?') for a in j['actors']),
                         'her_intent_tags': ';'.join(stage_hers), 'rule_intent': it,
                         'shipped_intent': intents.get(sid.lower(), ''), 'reason': why, 'logic_doc': 'notes/INTENT_LOGIC.md#' + rule_anchor(why, conflict, it_final, acts),
                         'conflict_with_her_tags': conflict, 'unsure': unsure, 'data_notes': ';'.join(sorted(set(notes))),
                         'description': d, 'source_file': rel.replace('\\', '/')})
    if key != 'billyy':
        json.dump(desc, open(os.path.join(outd, key + '_descriptions.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    json.dump(intents, open(os.path.join(outd, key + '_intents.json'), 'w'), indent=2, sort_keys=True)
    json.dump(positions, open(os.path.join(outd, key + '_positions.json'), 'w'), indent=2, sort_keys=True)
    with open(os.path.join(outd, key + '_scenes.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(key, 'scenes', len(sc), 'series', len(ser), 'descriptions', len(desc), 'intents', len(intents),
          dict(collections.Counter(intents.values())))


if __name__ == '__main__':
    main(*sys.argv[1:4])
