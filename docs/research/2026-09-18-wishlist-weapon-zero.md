# Wishlist Weapon Zero Diagnostic

## Reproduction

Before the fix, this deterministic run failed after gear pass 1:

```powershell
junkroan.exe scripts/benchmark.py bleed_bow --seeds 1 --no-variants --gear wishlist --workers 1 --tag wl-repro
```

`bleed_bow` logged `[Weapon 1] wishlist: Citadel Bow | 0 mods (ilvl 76):
56,277 -> 0 (viol 5.691 -> inf)` and then failed with `item is not valid for
slot Weapon 2`. The same failure was recorded for `impale_ballista` in the
specified `gear-wishlist` run.

The readbacks below reproduce the gear-pass-1 state: reference skeleton,
conservative config lane, empty passive tree, and all rare slots empty. The
`author bare base` is the base named by the skeleton with no explicit mods;
the named comparison base is likewise bare at item level 76.

## PoB Readbacks

### Bleed Bow

| Weapon 1 state | CombinedDPS | Violated objective terms: value < floor |
|---|---:|---|
| empty | 0 | Life 1881 < 4776; FireResist 64 < 75; LightningResist 56 < 75; HitChance omitted < 95; TotalEHP 3361.812 < 12649.462; PhysicalMaximumHitTaken 2329 < 5610.700; FireMaximumHitTaken 4877 < 18992.400; ColdMaximumHitTaken 6793 < 18232.400; LightningMaximumHitTaken 4047 < 19817.950; Str 153 < ReqStr 194; Dex 46 < ReqDex 151; Int 25 < ReqInt 146 |
| author bare Citadel Bow | 19,554.927 | Life 1881 < 4776; FireResist 64 < 75; LightningResist 56 < 75; TotalEHP 3361.812 < 12649.462; PhysicalMaximumHitTaken 2329 < 5610.700; FireMaximumHitTaken 4877 < 18992.400; ColdMaximumHitTaken 6793 < 18232.400; LightningMaximumHitTaken 4047 < 19817.950; Str 153 < ReqStr 194; Dex 46 < ReqDex 185; Int 25 < ReqInt 146 |
| bare Citadel Bow | 19,554.927 | Life 1881 < 4776; FireResist 64 < 75; LightningResist 56 < 75; TotalEHP 3361.812 < 12649.462; PhysicalMaximumHitTaken 2329 < 5610.700; FireMaximumHitTaken 4877 < 18992.400; ColdMaximumHitTaken 6793 < 18232.400; LightningMaximumHitTaken 4047 < 19817.950; Str 153 < ReqStr 194; Dex 46 < ReqDex 185; Int 25 < ReqInt 146 |
| bare Imperial Bow | 16,401.366 | Life 1881 < 4776; FireResist 64 < 75; LightningResist 56 < 75; TotalEHP 3361.812 < 12649.462; PhysicalMaximumHitTaken 2329 < 5610.700; FireMaximumHitTaken 4877 < 18992.400; ColdMaximumHitTaken 6793 < 18232.400; LightningMaximumHitTaken 4047 < 19817.950; Str 153 < ReqStr 194; Dex 46 < ReqDex 212; Int 25 < ReqInt 146 |

### Impale Ballista

| Weapon 1 state | CombinedDPS | Violated objective terms: value < floor |
|---|---:|---|
| empty | 0 | Life 1787 < 3866; FireResist 12 < 75; ColdResist 67 < 75; HitChance omitted < 95; TotalEHP 3845.634 < 14579.234; PhysicalMaximumHitTaken 2798 < 5328.550; FireMaximumHitTaken 2471 < 16446.400; ColdMaximumHitTaken 6247 < 16446.400; LightningMaximumHitTaken 8031 < 16446.400; Str 119 < ReqStr 146; Dex 127 < ReqDex 146; Int 95 < ReqInt 146 |
| author bare Thicket Bow | 862.051 | Life 1787 < 3866; FireResist 12 < 75; ColdResist 67 < 75; HitChance 54 < 95; TotalEHP 3845.634 < 14579.234; PhysicalMaximumHitTaken 2798 < 5328.550; FireMaximumHitTaken 2471 < 16446.400; ColdMaximumHitTaken 6247 < 16446.400; LightningMaximumHitTaken 8031 < 16446.400; Str 119 < ReqStr 146; Dex 127 < ReqDex 179; Int 95 < ReqInt 146; ManaUnreserved 0 < ManaCost 35; ManaRegenRecovery + ManaLeechGainRate + ManaRecoup omitted < ManaPerSecondCost 101.150 |
| bare Imperial Bow | 915.689 | Life 1787 < 3866; FireResist 12 < 75; ColdResist 67 < 75; HitChance 54 < 95; TotalEHP 3845.634 < 14579.234; PhysicalMaximumHitTaken 2798 < 5328.550; FireMaximumHitTaken 2471 < 16446.400; ColdMaximumHitTaken 6247 < 16446.400; LightningMaximumHitTaken 8031 < 16446.400; Str 119 < ReqStr 146; Dex 127 < ReqDex 212; Int 95 < ReqInt 146; ManaUnreserved 0 < ManaCost 35; ManaRegenRecovery + ManaLeechGainRate + ManaRecoup omitted < ManaPerSecondCost 101.150 |
| bare Citadel Bow | 945.979 | Life 1787 < 3866; FireResist 12 < 75; ColdResist 67 < 75; HitChance 54 < 95; TotalEHP 3845.634 < 14579.234; PhysicalMaximumHitTaken 2798 < 5328.550; FireMaximumHitTaken 2471 < 16446.400; ColdMaximumHitTaken 6247 < 16446.400; LightningMaximumHitTaken 8031 < 16446.400; Str 119 < ReqStr 146; Dex 127 < ReqDex 185; Int 95 < ReqInt 146; ManaUnreserved 0 < ManaCost 35; ManaRegenRecovery + ManaLeechGainRate + ManaRecoup omitted < ManaPerSecondCost 101.150 |

### Why The Empty State Is Infinite

The infinite objective term is `HitChance`. With no weapon, PoB has no attack
number for the main skill and omits `HitChance`, not a numeric zero. `Objective`
turns a missing floored stat into negative infinity, so `HitChance >= 95` adds
an infinite shortfall. A bare bow gives the skill a number and PoB emits
`HitChance` again (Bleed Bow's readback clears the term; Impale Ballista reads
54), so the violation is finite.

Burning Arrow has the same empty-weapon shape (`CombinedDPS = 0`, omitted
`HitChance`) but its bare Imperial Bow already reads `CombinedDPS =
92,565.480`. A pre-tree pipeline probe after the fix produced its normal
four-mod weapon summary unchanged:

```text
[Weapon 1] wishlist: Imperial Bow (22% increased Elemental Damage with Attack Skills) | 4 mods (ilvl 76): 182,220 -> 145,805 (viol 8.387 -> 8.375)
```

## Fix And Proof

The filler now reads `CombinedDPS` alongside the active objective. If an empty
slot has no main-skill number and at least one candidate restores a positive
number, candidates that leave it at zero cannot win and the completed positive
candidate is never dropped just because its complete `Score` is worse than the
item present before the pass. This applies when the objective maximizes either
`CombinedDPS` or `FullDPS`.

Invalid item trial results (`ok: false`) and real equip errors containing
`item is not valid for slot` are skipped. The filler restores the slot to its
prior item state, logs one invalid-item line per slot, and continues; unrelated
exceptions still raise. An externally equipped item has no raw-text readback,
so its failure-only recovery uses its pre-fill XML state.

Focused verification:

```text
python -m pytest -q -p no:cacheprovider -p no:faulthandler tests/test_wishlist_gear.py tests/test_wishlist_gear_pob.py tests/test_gear_slot_order.py
55 passed in 73.66s
```

Full suite: 692 passed, 6 deselected in 768.18s.

The added pinned-PoB test constructs Bleed Bow's pipeline-equivalent gear-pass-1
state, fills `Weapon 1` followed by `Weapon 2`, and asserts both items are
non-empty and `CombinedDPS > 0`.

The fake-session regressions also cover an author item preceding `fill_slot`
with every trial invalid, every real equip invalid, an invalid trial followed
by a valid candidate, and a later joint reroll whose deliberately empty slot
must not restore a stale author item. Each full fill writes one invalid-item
log line.

## Final Acceptance

Completed run `20260918-2321-wl-fix-final`:

```powershell
junkroan.exe scripts/benchmark.py bleed_bow impale_ballista --seeds 1 --no-variants --gear wishlist --workers 2 --loop-seconds 600 --tag wl-fix-final
```

| build | stat | author under our lane | ours | ratio | benchmark audit |
|---|---|---:|---:|---:|---|
| bleed_bow | CombinedDPS | 587,787 | 612,256 | 104% | 0 errors / 4 warnings |
| impale_ballista | FullDPS | 806,537 | 522,701 | 65% | 0 errors / 1 warning |

Both builds completed, neither failed, and both stopped only on the 600-second
loop time budget. That is an audit warning, not an error.

Gear pass 1 restored the main-hand number before its Weapon 2 item:

```text
[Weapon 1] wishlist: Citadel Bow | 4 mods (ilvl 76): 56,277 -> 78,492 (viol 5.691 -> 5.952)
[Weapon 2] wishlist: Light Quiver (+35 to Dexterity) | 4 mods (ilvl 76): 78,492 -> 78,492 (viol 5.952 -> 4.618)
[Weapon 1] wishlist: Imperial Bow (22% increased Elemental Damage with Attack Skills) | 4 mods (ilvl 76): 15,570 -> 8,408 (viol 7.058 -> 7.160)
[Weapon 2] wishlist: Two-Point Arrow Quiver (25% increased Global Accuracy Rating) | 4 mods (ilvl 76): 8,408 -> 9,616 (viol 7.160 -> 5.350)
```

The independent audit found Bleed Bow clean of errors with three warnings, all
pre-existing unsupported PoB mechanics; Impale Ballista had zero findings.

Short compatibility run `20260918-2351-wl-burning-compat` stopped after gear
pass 1 and preserved this exact first weapon line:

```text
[Weapon 1] wishlist: Imperial Bow (22% increased Elemental Damage with Attack Skills) | 4 mods (ilvl 76): 182,220 -> 145,805 (viol 8.387 -> 8.375)
```
