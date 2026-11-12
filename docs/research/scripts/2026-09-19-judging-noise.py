import json, re, random, statistics as st
from pathlib import Path
import itertools
# frozen campaign: table 1 of the seed-divergence note
frozen = {}
for line in Path('docs/research/2026-09-18-seed-divergence.md').read_text(encoding='utf-8').splitlines():
    m = re.match(r'\|\s*\*?\s*\|\s*(\w+)\s*\|\s*(new18|core14)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|', line)
    if m and m.group(1) not in frozen:
        frozen[m.group(1)] = [float(m.group(i)) for i in (3, 4, 5)]
rules = {}
for run in ('20260919-0130-new18-rules', '20260919-0941-core14-rules'):
    for r in json.loads(Path('artifacts/benchmark', run, 'results.json').read_text(encoding='utf-8')):
        if r.get('ok') and r.get('ratio_lane'):
            rules.setdefault(r['slug'], {})[int(r['seed'])] = float(r['ratio_lane']) * 100
refs = sorted(k for k in frozen if k in rules and len(rules[k]) == 3)
print(len(frozen), 'frozen refs,', len(rules), 'rules refs,', len(refs), 'with 3 + 3 seeds')
def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    sx = sum((a - mx) ** 2 for a in x) ** 0.5; sy = sum((b - my) ** 2 for b in y) ** 0.5
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)
# 1. does the SAME seed carry over between code versions? residuals inside a reference, in log space
import math
xa, xb = [], []
same_best = 0
for k in refs:
    a = [math.log(v) for v in frozen[k]]; b = [math.log(rules[k][s]) for s in (1, 2, 3)]
    ma, mb = st.mean(a), st.mean(b)
    xa += [v - ma for v in a]; xb += [v - mb for v in b]
    same_best += (a.index(max(a)) == b.index(max(b)))
print(f'seed residual correlation frozen vs rules (n={len(xa)} pairs, log space): r = {pearson(xa, xb):+.3f}')
print(f'the best seed is the same seed in both campaigns on {same_best} of {len(refs)} references (chance = {len(refs)/3:.1f})')
# permutation reference: shuffle seeds inside each reference
random.seed(1); perm = []
for _ in range(2000):
    yb = []
    for k in refs:
        b = [math.log(rules[k][s]) for s in (1, 2, 3)]; mb = st.mean(b); random.shuffle(b); yb += [v - mb for v in b]
    perm.append(pearson(xa, yb))
perm.sort(); print(f'  permutation null: 2.5% {perm[50]:+.3f}, 97.5% {perm[1950]:+.3f}')
# 2. within-reference seed noise vs between-version change, per reference (median of 3)
d = {k: st.median(rules[k].values()) - st.median(frozen[k]) for k in refs}
noise = {k: (max(frozen[k]) - min(frozen[k]) + max(rules[k].values()) - min(rules[k].values())) / 2 for k in refs}
full = st.median(d.values())
print(f'median-of-3 change frozen -> rules: median over {len(refs)} refs {full:+.1f} pts; refs up {sum(v > 0 for v in d.values())}, down {sum(v < 0 for v in d.values())}; median seed spread {st.median(noise.values()):.1f}')
# 3. how well does a six-reference subset estimate the 32-reference median change?
smoke = ['cold_dot', 'bleed_bow', 'summon_raging_spirits', 'impale_ballista', 'stormbrand', 'burning_arrow_snipe']
print('smoke six present:', [k for k in smoke if k in d], 'their changes:', [round(d[k], 1) for k in smoke if k in d])
sm = st.median(d[k] for k in smoke if k in d)
random.seed(2); est = sorted(st.median(d[k] for k in random.sample(refs, 6)) for _ in range(200000))
q = lambda p: est[int(p * len(est))]
print(f'full-{len(refs)} median change {full:+.1f}; our smoke six says {sm:+.1f}; a random six says: 5% {q(.05):+.1f}, 25% {q(.25):+.1f}, 50% {q(.5):+.1f}, 75% {q(.75):+.1f}, 95% {q(.95):+.1f}')
print(f'share of random six-subsets with the WRONG SIGN of the campaign change: {sum((e > 0) != (full > 0) for e in est) / len(est):.1%}')
for n in (6, 10, 14, 20):
    e = sorted(st.median(d[k] for k in random.sample(refs, n)) for _ in range(50000))
    print(f'  subset of {n:2d}: 90% band of the estimate {e[int(.05*len(e))]:+.1f} .. {e[int(.95*len(e))]:+.1f}')
