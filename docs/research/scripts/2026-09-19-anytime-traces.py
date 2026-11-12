import json, math, statistics as st
from pathlib import Path
rows = []
for run in ('20260919-0130-new18-rules', '20260919-0941-core14-rules'):
    rows += [r for r in json.loads(Path('artifacts/benchmark', run, 'results.json').read_text(encoding='utf-8')) if r.get('ok')]
def trace(r):
    t, out = 0.0, []
    for s in r['stages']:
        t += float(s.get('seconds') or 0)
        out.append((s['name'], t, float(s.get('value') or 0)))
    return out
by = {}
for r in rows:
    by.setdefault(r['slug'], []).append(r)
def checkpoint(r, name):
    tr = trace(r)
    hit = [x for x in tr if x[0].startswith(name)]
    return hit[-1] if hit else None
def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    sx = sum((a - mx) ** 2 for a in x) ** .5; sy = sum((b - my) ** 2 for b in y) ** .5
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float('nan')
total = [trace(r)[-1][1] for r in rows]
print(f'{len(rows)} builds, {len(by)} references; median build {st.median(total)/60:.0f} min, p90 {sorted(total)[int(.9*len(total))]/60:.0f} min')
for name in ('tree rebuilt on gear', 'loop pass 1', 'loop pass 2', 'loop pass 3'):
    share_t, share_v, xa, xb, same, n = [], [], [], [], 0, 0
    for slug, rs in by.items():
        cps = [(checkpoint(r, name), trace(r)[-1]) for r in rs]
        if len(cps) < 3 or any(c is None or c[2] <= 0 for c, _ in cps):
            continue
        a = [math.log(c[2]) for c, _ in cps]; b = [math.log(f[2]) for _, f in cps]
        xa += [v - st.mean(a) for v in a]; xb += [v - st.mean(b) for v in b]
        same += a.index(max(a)) == b.index(max(b)); n += 1
        share_t += [c[1] / f[1] for c, f in cps]; share_v += [c[2] / f[2] for c, f in cps]
    print(f'{name:22s}: at {st.median(share_t):4.0%} of the build time the value is {st.median(share_v):4.0%} of final; seed residual corr with final r = {pearson(xa, xb):+.2f}; leader-at-checkpoint is the final best seed on {same} of {n} refs (chance {n/3:.0f})')
# within-reference run-to-run noise, log space, pooled over both campaigns' rules rows
res = []
for slug, rs in by.items():
    v = [math.log(float(r['ratio_lane'])) for r in rs]
    if len(v) == 3:
        res += [x - st.mean(v) for x in v]
sd = (sum(x * x for x in res) / (len(res) - len(by))) ** .5
print(f'pooled within-reference sd of one run: {sd:.3f} in log space = about {math.expm1(sd):.0%} of the value')
for n_ref, label in ((6, 'smoke six'), (32, 'full 32')):
    for k in (3,):
        se_med = 1.2533 * sd / (k ** .5) * (1.16)  # median of 3 normal draws: sd ~ 0.67 sigma => 1.16 * sigma/sqrt(3)
        se_delta_ref = (2 ** .5) * 0.67 * sd
        se = 1.2533 * se_delta_ref / (n_ref ** .5)
        print(f'  {label}: median over refs of (median-of-3 B - median-of-3 A): sd about {math.expm1(se):.1%}; an effect must be about {math.expm1(2*se):.0%} to stand out at 2 sd')

print('--- early kill of trailing seeds: keep only the checkpoint leader, what does the delivered best-of-3 lose?')
for name in ('tree rebuilt on gear', 'loop pass 1', 'loop pass 2'):
    loss, cost = [], []
    for slug, rs in by.items():
        cps = [(checkpoint(r, name), trace(r)[-1]) for r in rs]
        if len(cps) < 3 or any(c is None for c, _ in cps):
            continue
        lead = max(range(3), key=lambda i: cps[i][0][2])
        best = max(f[2] for _, f in cps)
        loss.append(1 - cps[lead][1][2] / best)
        full = sum(f[1] for _, f in cps)
        cost.append((sum(c[1] for c, _ in cps) + cps[lead][1][1] - cps[lead][0][1]) / full)
    loss.sort()
    print(f'{name:22s}: time {st.median(cost):.0%} of three full seeds; delivered value lost: 0 on {sum(l < 1e-9 for l in loss)} of {len(loss)} refs, median {st.median(loss):.1%}, mean {st.mean(loss):.1%}, worst {loss[-1]:.0%}; keep TWO leaders:', end=' ')
    loss2, cost2 = [], []
    for slug, rs in by.items():
        cps = [(checkpoint(r, name), trace(r)[-1]) for r in rs]
        if len(cps) < 3 or any(c is None for c, _ in cps):
            continue
        order = sorted(range(3), key=lambda i: -cps[i][0][2])[:2]
        best = max(f[2] for _, f in cps)
        loss2.append(1 - max(cps[i][1][2] for i in order) / best)
        full = sum(f[1] for _, f in cps)
        cost2.append((sum(c[1] for c, _ in cps) + sum(cps[i][1][1] - cps[i][0][1] for i in order)) / full)
    print(f'time {st.median(cost2):.0%}, lost mean {st.mean(loss2):.1%}, worst {max(loss2):.0%}, zero on {sum(l < 1e-9 for l in loss2)}')
one = [max(float(r["ratio_lane"]) for r in rs) / st.median(float(r["ratio_lane"]) for r in rs) - 1 for rs in by.values() if len(rs) == 3]
print(f'for scale: best-of-3 over the median seed is worth median {st.median(one):.1%}, mean {st.mean(one):.1%}')
