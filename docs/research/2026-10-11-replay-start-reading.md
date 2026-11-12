# #816 row 1: the replay start, four readings (2026-10-11)

Builds: `artifacts/benchmark/20261004-0020-smoke-14-11/<slug>-s4.pob.txt`; one PobSession, 1 slot, 1 min 4 s.
Value = the objective's maximized stat; viol = `Objective.violations` summed (`objective.py:111`), floors named.

- a: scored by the author's objective (`prepare_author`, today's rules) on the build as loaded: no re-lane, no rejudge
- b: after `judging.relane` + `open_contexts` (the full objective has ramp and self-cost), read at the entry of `rejudge`
- c: after `judging.rejudge`
- d: after `recut`, what `replay_one` scores as `before` / `start_violated` (`scripts/replay_bench.py:294-298`)

Rerun: `cd <worktree> && PYTHONPATH=<worktree>/src python tools/rig816/start_reading.py [slug ...]`

| build | a saved config | b relane | c rejudge | d bench start | first violating |
|---|---|---|---|---|---|
| stormbrand | 1,838,009 / viol 1.0648 [FireResist>=FireResistMax, MoMCastsAfterMaxHit, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond>=Life] | 1,957,880 / viol 1.0648 [FireResist>=FireResistMax, MoMCastsAfterMaxHit, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond>=Life] | 1,957,880 / viol 1.0741 [FireMaximumHitTaken, FireResist>=FireResistMax, MoMCastsAfterMaxHit, PhysicalMaximumHitTaken, TotalEHP] | 1,957,880 / viol 1.0741 [FireMaximumHitTaken, FireResist>=FireResistMax, MoMCastsAfterMaxHit, PhysicalMaximumHitTaken, TotalEHP] | a saved config |
| cold_dot | 302,231 / viol 0.1409 [EffectiveMovementSpeedMod] | 302,231 / viol 0.1409 [EffectiveMovementSpeedMod] | 302,231 / viol 0.1409 [EffectiveMovementSpeedMod] | 302,231 / viol 0.1409 [EffectiveMovementSpeedMod] | a saved config |
| burning_arrow_snipe | 1,425,231 / viol 0.6663 [FireMaximumHitTaken, FireResist>=FireResistMax, TotalEHP] | 1,425,231 / viol 0.6663 [FireMaximumHitTaken, FireResist>=FireResistMax, TotalEHP] | 1,425,231 / viol 0.6663 [FireMaximumHitTaken, FireResist>=FireResistMax, TotalEHP] | 1,425,231 / viol 0.6663 [FireMaximumHitTaken, FireResist>=FireResistMax, TotalEHP] | a saved config |

Reading: all three builds already violate in column a (the first one), so none of the bench steps is the first to break them.
stormbrand: a and b differ in value (1,838,009 -> 1,957,880, the re-lane) at the same violation 1.0648 with three floors
(one of them, `NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond>=Life`, is gone from c); the rejudge (c) swaps that for
FireMaximumHitTaken, PhysicalMaximumHitTaken, TotalEHP (viol 1.0741, the bench's known 1.074). c = d.
