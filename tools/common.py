"""Shared loader + intent rules for the Lirael creature pack SkyrimNet patches.
Reads her scene JSONs (never copies them) and returns per-stage records."""
import json, glob, os, re, collections

INTENTS = ['platonic', 'romantic', 'lustful', 'transactional', 'dom', 'aggressive']

# ---- tag sets used by the intent rules (see docs/INTENT_RULES.md) ----
RESTRAINT = {'bound', 'bondage', 'restraints', 'restraint', 'restrained', 'yoke', 'pillory', 'pillorylow',
             'armbinder', 'cuffed', 'cuffs', 'tied', 'frozen', 'stocks', 'chained', 'shackles'}
FORCE = {'forced', 'rape', 'defeated', 'struggle', 'conquering', 'harassing', 'aggressive', 'aggressive default'}
BREED = {'oviposition', 'eggs', 'egg', 'breeding'}
LOVING = {'loving', 'love', 'romantic', 'cute'}
KISS = {'kiss', 'kissing'}
CONTROL_TAGS = {'cowgirl', 'reversecowgirl', 'femdom', 'female domanation', 'female domination', 'facesit',
                'facesitting', 'seduce', 'footjob', 'masturbation', 'masturbating'}
SHE_WORKS = {'blowjob', 'handjob', 'boobjob', 'footjob', 'balljob', 'thighjob', 'bodyjob', 'femalemasturbation'}
ORAL_ON_HER = {'lickingvagina', 'cunnilingus', 'analinggus'}


def load(root):
    """Return {scene_id: (relative_path, json)} for every scene file under root."""
    out = {}
    for f in glob.glob(os.path.join(root, '**', 'scenes', '**', '*.json'), recursive=True):
        out[os.path.basename(f)[:-5]] = (os.path.relpath(f, root), json.load(open(f, encoding='utf-8-sig')))
    return out


def series_of(sid):
    m = re.match(r'(.*)-(\d+)$', sid)
    return (m.group(1), int(m.group(2))) if m else (sid, 1)


def humans(j):
    return [i for i, a in enumerate(j['actors']) if not a.get('type')]


def stage_signals(j):
    """What the stage data says about who is doing what (used for intents and descriptions)."""
    A = j['actors']; tags = {t.lower() for t in j.get('tags', [])}
    H = humans(j)
    s = {'control': [], 'oral_on_her': False, 'notes': []}
    for a in j.get('actions', []):
        t = a['type']
        perf = a.get('performer')
        if t in SHE_WORKS:
            # she works him (Baka/FlufyFox put her as actor, Billyy as target); a performer that is a
            # creature means the creature drives it (e.g. facefuck)
            if perf is not None and perf < len(A) and A[perf].get('type'):
                s['notes'].append('%s driven by creature (performer %d)' % (t, perf))
            elif 'facefuck' in tags:
                s['notes'].append('%s tagged facefuck' % t)
            else:
                s['control'].append('she performs ' + t)
        if t in ORAL_ON_HER:
            s['oral_on_her'] = True
        if t in ('vaginalsex', 'analsex') and perf is not None and perf in H:
            s['control'].append('she moves on him (%s, performer is her)' % t)
    for t in sorted(tags & CONTROL_TAGS):
        s['control'].append('tag ' + t)
    if tags & {'cunnilingus', 'analinggus'}:
        s['oral_on_her'] = True
    return s


def series_intent(stages):
    """stages: list of scene json for one series. Returns (intent, reason, unsure_note)."""
    tags = set()
    for j in stages:
        tags |= {t.lower() for t in j.get('tags', [])}
    sig = [stage_signals(j) for j in stages]
    control = sorted({c for s in sig for c in s['control']})
    oral = any(s['oral_on_her'] for s in sig)
    ww = any((a.get('type') or '').lower().startswith('werewolf') for j in stages for a in j['actors'])
    restr = tags & RESTRAINT; force = tags & FORCE; breed = tags & BREED
    unsure = []
    if ww and tags & KISS and tags & LOVING and not restr:
        it, why = 'romantic', 'werewolf scene with kissing and loving tags (%s)' % ','.join(sorted(tags & LOVING))
        if force: unsure.append('also tagged ' + ','.join(sorted(force)))
    elif control:
        it, why = 'lustful', 'she is in control: ' + '; '.join(control[:3])
        if force or restr or breed:
            unsure.append('she is in control but scene is also tagged ' + ','.join(sorted(force | restr | breed)))
    elif ww and tags & KISS:
        it, why = 'lustful', 'werewolf scene with kissing (passionate, no loving tags)'
        if force: it, why = 'aggressive', 'werewolf kissing but tagged ' + ','.join(sorted(force))
    elif oral and not force and not restr:
        it, why = 'lustful', 'creature oral on her'
        if breed: unsure.append('oral plus ' + ','.join(sorted(breed)))
    else:
        it = 'aggressive'
        why = 'creature sex (default)'
        if restr: why = 'restraint: ' + ','.join(sorted(restr))
        elif breed: why = 'egg-laying/breeding: ' + ','.join(sorted(breed))
        elif force: why = 'forced: ' + ','.join(sorted(force))
        if oral: why += '; creature oral on her but tagged ' + ','.join(sorted(force | restr))
        if tags & LOVING and not restr: unsure.append('tagged ' + ','.join(sorted(tags & LOVING)) + ' but no sign she is in control')
    fem_creature = any(a.get('type') and (a.get('intendedSex') or '').lower() == 'female' for j in stages for a in j['actors'])
    male_human = any(not a.get('type') and (a.get('intendedSex') or '').lower() == 'male' for j in stages for a in j['actors'])
    if fem_creature and male_human:
        unsure.append('female creature with a human man: the rules are written for a woman with a creature')
    if restr and it == 'romantic':  # never romantic
        it = 'lustful'
    return it, why, '; '.join(unsure)


def her_intents(stages):
    return [[t for t in j.get('tags', []) if t in INTENTS] for j in stages]
