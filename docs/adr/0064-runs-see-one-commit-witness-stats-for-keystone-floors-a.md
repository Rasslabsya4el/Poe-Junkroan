# 2026-09-18 D64. Runs see one commit; witness stats for keystone floors; a random-element skill is the mean over its parts

Status: Accepted

1. *Removed with the old local run queue: every long run executed from a snapshot of one commit, so a merge
   during a run could not change its code. Heavy runs now run on CI runners at a named ref (`docs/ci.md`).*
2. **A floor that binds only while a keystone is allocated needs a witness in every readback**,
   real or what-if (45d8dd0, `optimizer/keystone_floors.py`). Mind over Matter has PoB's own
   `sharedMindOverMatter`; Elemental Overload has none -- a tree keystone reaches the mod DB only
   as a Keystone LIST mod -- so the headless wrapper publishes `HaveElementalOverload` from PoB's
   `env.keystonesAdded` after every `calcs.perform`, the one call every lane and every calculator
   goes through. `ElementalOverloadUptime` = 1.0 without the keystone, else 1 - (1 - c)^(8 r),
   with c = PoB's effective `CritChance` (which already carries the accuracy roll: CalcOffence
   multiplies it by `AccuracyHitChance`, so the crit-recently rule no longer multiplies by
   HitChance a second time) and r = hits per second; 0 for a minion main skill; floor 0.9
   (`with_skill_floors`). burning_arrow_snipe's author build: 10.6% crit at 0.97 hits/s = 58%
   uptime, so the keystone is refused there.
3. **A skill whose element is random per hit is scored as the mean over its element parts**
   (d4fd350; corpus tag `random_element`: Elemental Hit, Wild Strike). `PobSession.mean_parts`
   makes `stats()` and every fast `trial_stats` evaluate each listed part -- the main gem
   instance's `skillPart` switched around each what-if evaluation and restored -- and report the
   mean of every numeric stat; the groups come from PoB's own part names with the element word
   removed (Fire / Cold / Lightning Attack -> one group; Wild Strike's secondaries stay single).
   The pipeline's part pick scores a group by its mean, the benchmark's author row and the audit
   use the same mean, so both sides are judged alike. The author's elemental_hit: fire part
   607,051, cold 404,273, lightning 660,233, mean 557,186 (21 ms for the three).

Also this morning (cdd83eb): `multiplierRage` became ramp arithmetic (`ramp_inputs.rage_stacks`:
the build's own rage sources x the 2.5 s budget at PoB's throttle of one rage-gaining hit per
0.5 s, Rage Support's 3 per hit, warcries, "after spending N mana", PoB's signed
`RageRegenRecovery`, minus `RageCost` x `Speed`; on-kill, when-hit, flask and retaliation sources
count for nothing on the boss lane). Smite 5 of 30 where the rails typed 15, bleed_perforate
2 of 30 (its Sand-stance number 480,654 instead of 601,832 with the typed 15).

