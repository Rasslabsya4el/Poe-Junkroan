"""Throwaway: on delivered builds, remove every removable leaf of the tree (one at a time, PoB what-if) and see what moves.

dead      = nothing the objective reads moves (every key within 0.05%)
near-dead = the judged DPS moves < 0.2% and no defensive key moves >= 0.5%
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from junkroan.optimizer.tree_graph import TreeGraph  # noqa: E402
from junkroan.pob.session import PobSession  # noqa: E402

KEYS = ("CombinedDPS", "FullDPS", "Life", "EnergyShield", "Mana", "ManaUnreserved", "LifeUnreserved", "TotalEHP",
        "PhysicalMaximumHitTaken", "FireMaximumHitTaken", "ColdMaximumHitTaken", "LightningMaximumHitTaken", "ChaosMaximumHitTaken",
        "FireResist", "ColdResist", "LightningResist", "ChaosResist", "EffectiveMovementSpeedMod", "Str", "Dex", "Int",
        "LifeRegenRecovery", "ManaRegenRecovery", "NetLifeRegen", "LifeLeechGainRate", "ManaPerSecondCost", "LifePerSecondCost",
        "ReqStr", "ReqDex", "ReqInt", "Speed", "HitChance")
DEF = ("Life", "EnergyShield", "TotalEHP", "PhysicalMaximumHitTaken", "FireMaximumHitTaken", "ColdMaximumHitTaken", "LightningMaximumHitTaken",
       "ChaosMaximumHitTaken", "FireResist", "ColdResist", "LightningResist", "ChaosResist", "EffectiveMovementSpeedMod", "ManaUnreserved",
       "LifeRegenRecovery", "ManaRegenRecovery", "NetLifeRegen", "Str", "Dex", "Int")


def rel(a, b):
    a, b = float(a or 0), float(b or 0)
    if a == b:
        return 0.0
    return abs(b - a) / max(abs(a), 1e-9)


files = [Path(p) for p in sys.argv[2:]]
graph = TreeGraph.load()
out = []
with PobSession() as pob:
    for f in files:
        pob.load_import_code(f.read_text(encoding="utf-8").strip())
        base = pob.stats(KEYS)
        stat = "FullDPS" if float(base.get("FullDPS") or 0) > float(base.get("CombinedDPS") or 0) else "CombinedDPS"
        tree = pob.tree_light()
        allocated = {int(n) for n in tree["user_allocated_node_ids"]}
        start = graph.class_starts.get(str(tree.get("class_id") or ""))
        if start is not None:
            allocated.add(start)
        leaves = [n for n in graph.removable_leaves(allocated) if n in graph.allocatable]
        trials = pob.trial_stats([{"remove": [n]} for n in leaves], KEYS, mode="fast")
        rows = []
        for n, t in zip(leaves, trials):
            st = t.get("stats") if isinstance(t, dict) and "stats" in t else t
            node = graph.node(n)
            moved = {k: (base.get(k), st.get(k)) for k in KEYS if rel(base.get(k), st.get(k)) > 0.0005}
            dps = rel(base.get(stat), st.get(stat))
            dps_signed = (float(st.get(stat) or 0) - float(base.get(stat) or 0)) / max(float(base.get(stat) or 0), 1e-9)
            defensive = max((rel(base.get(k), st.get(k)) for k in DEF), default=0.0)
            kind = "dead" if not moved else ("near-dead" if dps < 0.002 and defensive < 0.005 else ("harmful" if dps_signed > 0.002 else "live"))
            rows.append({"id": n, "name": node.name if node else str(n), "kind": node.kind if node else "?", "class": kind,
                         "dps_change_if_removed": round(dps_signed, 5), "moved": {k: [round(float(a or 0), 2), round(float(b or 0), 2)] for k, (a, b) in moved.items()}})
        n_alloc = len([n for n in allocated if n in graph.allocatable])
        summary = {c: sum(1 for r in rows if r["class"] == c) for c in ("dead", "near-dead", "harmful", "live")}
        out.append({"file": f.name, "stat": stat, "value": base.get(stat), "allocated": n_alloc, "leaves": len(leaves), **summary, "rows": rows})
        print(f"{f.name}: allocated {n_alloc}, leaves {len(leaves)}, {summary}", flush=True)
        for r in rows:
            if r["class"] != "live":
                print(f"    {r['class']:9s} {r['kind']:8s} {r['name'][:44]:44s} dps {r['dps_change_if_removed']:+.4f}  moved: {list(r['moved'])[:6]}", flush=True)
Path(sys.argv[1]).write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
