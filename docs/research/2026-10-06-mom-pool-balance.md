# Mind over Matter: how PoB pools a hit, the balance point, casts after the biggest hit (#608 unit 1)

Facts are PoB source (vendor/pob/source/src/Modules/CalcDefence.lua, "CD") read 2026-10-06; marked "inference" where not read.

## 1. How PoB splits a hit
- Keystone line in tree 3_29: "40% of Damage is taken from Mana before Life" (TreeData/3_29/tree.lua:40257, node 34098). Parsed to `DamageTakenFromManaBeforeLife` BASE (ModParser.lua:414-416). `sharedMindOverMatter = min(Sum BASE, 100)` (CD:2306); per-type `<Type>MindOverMatter` adds on top (CD:2347).
- Mana that counts is `ManaUnreserved` only: `mana = max(output.ManaUnreserved, 0)` (CD:2308).
- Pool, verbatim (CD:2307-2318), p = MoMEffect, L = life pool:
  `maxMoMPool = L/(1-p) - L`; `maxManaUsable = floor(min(mana, maxMoMPool))`; `manaUsed = floor(min(maxMoMPool - maxESUsable, maxManaUsable))`; returns `L + manaUsed + maxESUsable`.
  Stored as `sharedManaEffectiveLife` (from LifeRecoverable, CD:2324) and `sharedMoMHitPool` (from LifeHitPool, CD:2326); per type `<Type>TotalHitPool = <Type>MoMHitPool` (CD:2538), and without Eldritch Battery the non-bypassed ES is simply ADDED to it (CD:2549-2550).
- Eldritch Battery = flag `EnergyShieldProtectsMana` ("Energy Shield protects Mana instead of Life", ModParser.lua:2312; node 56075 text in tree 3_29:67101). With it, ES joins the MoM pool: `maxESUsable = floor(min(EnergyShieldRecoveryCap, maxMoMPool*(1-esBypass), (L+maxManaUsable)/(1-(1-esBypass)p) - (L+maxManaUsable)))` (CD:2311-2316). So ES sits in the same p-share as mana: ES is spent before mana, but only from the p part of the hit (CD:330-345); life never loses less than (1-p) of a hit. Without EB: ES takes the whole hit first (CD:319-327), then MoM splits the rest (CD:328+).
- `<Type>MaximumHitTaken` is computed in reverse from the pools (CD:3258-3264, breakdown text CD:3297-3299 "calculated in reverse from health pools"). `TotalEHP = TotalNumberOfHits * totalEnemyDamageIn` (CD:2908). CD:3432 and CD:3674 `takenFromMana` are the DEGEN (damage over time) split, not the hit split: life gets (1-takenFromMana/100), mana takenFromMana/100.

## 2. Balance point (derived from the pool formula)
Pool absorbs D total damage: Life takes (1-p)D, Mana pD while mana lasts; once mana is gone the rest hits Life 1:1. Ignoring other layers (reductions, ES):
- Mana runs out first: Life dies at D = L + M. Valid while M <= pD, i.e. M <= p/(1-p) * L (= `maxMoMPool`).
- Mana never runs out first: Life dies at D = L/(1-p); extra mana is unused.
- **Max hit = L + min(M, L*p/(1-p))**. Not `min(L/(1-p), M/p)` as proposed in the brief: that gives the wrong value left of the balance (it would say M/p, but PoB and the real game give L+M). PoB's `manaUsed = min(maxMoMPool, mana)` is exactly this min.
- p = 0.4: balance M = (0.4/0.6) L = 2/3 L; pool split Life 60 % / Mana 40 %. Below it each unreserved Mana adds +1 to max hit; above it +0. Life adds 1/(1-p) = 1.667 per point above balance, 1 below (plus raises the balance mana need).
- With EB: replace M by (ES + M): balance ES + M = 2/3 L (CD:2315 has the same bound). Below it each ES or Mana point is worth +1.
- Check on stormbrand-s4 (section 5): L 4194, ES 770, ManaUnreserved 358; L+ES+M = 5322 vs PoB PhysicalMaximumHitTaken 5315 (0.13 % apart; the gap is LifeRecoverable/hit-pool details, inference). ES+M = 1128 vs balance 2796: far below, every mana point counts.

## 3. Casts after the biggest hit (proposal, not read from the repo)
Hit D (in the damage type's own units). Mana drained by the MoM part: without EB `max(0, p*(D - ES))`; with EB `max(0, p*D - ES)` (ES takes its bite from the p share first, CD:330-345). Then:
- `ManaLeft = max(0, ManaUnreserved - ManaDrained)` (also valid only for D <= L + min(M, pL/(1-p)); at larger D life is already 0).
- `Casts = ManaLeft / ManaCost`, ManaCost = the main skill's `ManaCost` output (61 in stormbrand-s4; with EB PoB charges ES first, CalcOffence.lua:5795-5800, so then use ES+Mana left; inference on exact accounting).
- Rail: `ManaUnreserved - max(0, p*D - ES_EB) >= N * ManaCost`, with p = `sharedMindOverMatter/100`, D = f * `PhysicalMaximumHitTaken` (all of these are PoB outputs, so it works on what-if trials like the existing floor).
- Proposal: f = 0.8 (a hit that leaves Life > 0 with margin: 20 % below the max), N = 3 casts. Reasoning: the owner wants "some % more mana for casts after a very strong hit"; one cast is no margin (one regen tick short), 3 gives one cast per second-ish for the next few seconds while life recovers; both numbers are a PROPOSAL, no data behind them. The settling check: a PoB sweep of N in {1,3,5} on builds with MoM, counting how many builds go infeasible.
- Stormbrand-s4 under this rule (f 0.8, EB, p 0.4): D = 4252, drained = 0.4*4252 - 770 = 931 > 358, so ManaLeft = 0, Casts = 0: it fails, while the current rule passes it (0.50 >= 0.40).

## 4. Current rule
`keystone_floors.py:56-66`: `MoMUnreservedShare = ManaUnreserved / Mana` (1.0 when `sharedMindOverMatter` is 0, 0.0 when Mana <= 0); `rails_default.json:31` floors it at 0.4. It checks only how much mana is not reserved, not Life:Mana balance, hit size, ES, or casts. Its docstring (keystone_floors.py:6-7) says keystone gives 30 %; tree 3_29 says 40 % (tree.lua:40257): stale comment.

## 5. stormbrand-s4 (decoded artifacts/benchmark/20261005-1220-gate-20261005/stormbrand-s4.pob.txt, decode_import_code)
- Spec treeVersion 3_29; allocated node ids include 34098 (Mind over Matter) and 56075 (Eldritch Battery): both YES. Elemental Overload, CI not allocated.
- PlayerStat: Life 4194, LifeUnreserved 4138, Mana 716, ManaUnreserved 358, ManaUnreservedPercent 50, EnergyShield 770, EnergyShieldRecoveryCap 770, ManaCost 61, PhysicalMaximumHitTaken 5315, TotalEHP 12161.9. `sharedMindOverMatter` is NOT in the XML stats (not a PlayerStat), so p = 0.4 is from the node text, not a stat.
- Pools: Life 4194 / ES 770 / Mana 716 (50 % reserved). ES+ManaUnreserved = 1128 = 40 % of balance need.
