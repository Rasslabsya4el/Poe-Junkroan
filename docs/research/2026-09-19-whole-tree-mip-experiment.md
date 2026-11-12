# Whole-tree MIP experiment

Finished benchmark exports only. The run files persist their judged stat but not their author-floor object, so this uses the specified fallback `Rails.objective(maximize=<persisted stat>)`; node weights use fast non-cascading PoB what-if trials with KAPPA = 10, and every proposal below is reloaded and judged by real PoB.

## cold_dot

Source: `artifacts/benchmark/20260919-0941-core14-rules/cold_dot-s2.pob.txt`. Objective: `maximize CombinedDPS subject to Life >= 3700, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, FireResist >= 75, ColdResist >= 75, LightningResist >= 75, EffectiveMovementSpeedMod >= 1.2, MoMUnreservedShare >= 0.4, RampBudget >= RampStages, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifePerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup >= 0.85*ESPerSecondCost`. Incumbent: 327,588 CombinedDPS, violation 0.0000, 104 points.

Weights: 3874 fast trials in 31.9s; positive 408, zero 1920, negative 22.

| proposal | predicted gain | actual value | violation | rho | changed points | trunk dropped | solver s | gap | feasible | refused masteries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| proposal (unrestricted) | -0.00% | 327,588 | 0.0000 | - | 0 | 0 | 60.17 | 33.94% | True | - |
| proposal (D=10) | +11.07% | 254,786 | 0.0000 | -2.01 | 10 | 0 | 60.07 | 4.83% | True | - |
| proposal (D=20) | +33.88% | 250,738 | 0.0092 | -0.96 | 20 | 0 | 60.09 | 4.39% | False | - |
| proposal (D=40) | +46.86% | 260,022 | 0.0000 | -0.44 | 41 | 0 | 60.08 | 11.25% | True | - |
| re-linearization | - | no accepted first proposal | - | - | - | - | - | - | - | - |

Total PoB seconds after loading the delivered build: 35.8s (experiment wall time 287.6s, including HiGHS).

## bleed_bow

Source: `artifacts/benchmark/20260919-0941-core14-rules/bleed_bow-s1.pob.txt`. Objective: `maximize CombinedDPS subject to Life >= 3700, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, FireResist >= 75, ColdResist >= 75, LightningResist >= 75, EffectiveMovementSpeedMod >= 1.2, MoMUnreservedShare >= 0.4, RampBudget >= RampStages, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifePerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup >= 0.85*ESPerSecondCost`. Incumbent: 969,206 CombinedDPS, violation 0.0000, 102 points.

Weights: 3876 fast trials in 54.8s; positive 633, zero 1698, negative 19.

| proposal | predicted gain | actual value | violation | rho | changed points | trunk dropped | solver s | gap | feasible | refused masteries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| proposal (unrestricted) | +0.00% | 969,206 | 0.0000 | - | 0 | 0 | 60.07 | 23.93% | True | - |
| proposal (D=10) | +9.00% | 848,674 | 0.0000 | -1.38 | 10 | 0 | 60.10 | 2.11% | True | - |
| proposal (D=20) | +45.08% | 1,054,435 | 0.0486 | -0.88 | 20 | 0 | 60.08 | 2.12% | False | - |
| proposal (D=40) | +96.49% | 1,262,808 | 0.9937 | -9.98 | 40 | 0 | 60.10 | 3.42% | False | - |
| re-linearization | - | no accepted first proposal | - | - | - | - | - | - | - | - |

Total PoB seconds after loading the delivered build: 58.6s (experiment wall time 309.6s, including HiGHS).

## summon_raging_spirits

Source: `artifacts/benchmark/20260919-0941-core14-rules/summon_raging_spirits-s1.pob.txt`. Objective: `maximize FullDPS subject to Life >= 3700, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, FireResist >= 75, ColdResist >= 75, LightningResist >= 75, EffectiveMovementSpeedMod >= 1.2, MoMUnreservedShare >= 0.4, RampBudget >= RampStages, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifePerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup >= 0.85*ESPerSecondCost`. Incumbent: 1,302,190 FullDPS, violation 0.0250, 101 points.

Weights: 3875 fast trials in 90.1s; positive 211, zero 2095, negative 44.

| proposal | predicted gain | actual value | violation | rho | changed points | trunk dropped | solver s | gap | feasible | refused masteries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| proposal (unrestricted) | +885.58% | 400,272 | 0.1062 | -0.17 | 136 | 11 | 60.08 | 3.59% | False | - |
| proposal (D=10) | +20.22% | 1,329,932 | 0.0368 | -0.48 | 10 | 0 | 60.08 | 1.90% | False | - |
| proposal (D=20) | +23.40% | 1,134,771 | 0.0032 | 0.38 | 20 | 0 | 60.17 | 4.15% | False | - |
| proposal (D=40) | +2.83% | 1,181,056 | 0.0428 | -9.56 | 6 | 0 | 60.08 | 8.67% | False | - |
| re-linearization (D=20) | +30.41% | 1,178,626 | 0.0163 | -0.30 | 20 | 5 | 60.12 | 0.31% | False | - |

Total PoB seconds after loading the delivered build: 182.5s (experiment wall time 497.3s, including HiGHS).

## stormbrand

Source: `artifacts/benchmark/20260919-0941-core14-rules/stormbrand-s2.pob.txt`. Objective: `maximize FullDPS subject to Life >= 3700, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, FireResist >= 75, ColdResist >= 75, LightningResist >= 75, EffectiveMovementSpeedMod >= 1.2, MoMUnreservedShare >= 0.4, RampBudget >= RampStages, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifePerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup >= 0.85*ESPerSecondCost`. Incumbent: 2,115,491 FullDPS, violation 0.0000, 100 points.

Weights: 3879 fast trials in 64.0s; positive 1138, zero 1193, negative 19.

| proposal | predicted gain | actual value | violation | rho | changed points | trunk dropped | solver s | gap | feasible | refused masteries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| proposal (unrestricted) | -0.00% | 2,115,491 | 0.0000 | - | 0 | 0 | 60.08 | 18.42% | True | - |
| proposal (D=10) | +23.86% | 2,321,865 | 0.2460 | -9.90 | 10 | 0 | 60.10 | 1.13% | False | - |
| proposal (D=20) | +41.69% | 2,306,512 | 0.5831 | -13.77 | 20 | 1 | 60.07 | 2.38% | False | - |
| proposal (D=40) | -0.00% | 2,115,491 | 0.0000 | - | 0 | 0 | 60.09 | 7.77% | True | - |
| re-linearization | - | no accepted first proposal | - | - | - | - | - | - | - | - |

Total PoB seconds after loading the delivered build: 67.1s (experiment wall time 316.9s, including HiGHS).

## impale_ballista

Source: `artifacts/benchmark/20260919-0130-new18-rules/impale_ballista-s1.pob.txt`. Objective: `maximize FullDPS subject to Life >= 3700, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, FireResist >= 75, ColdResist >= 75, LightningResist >= 75, EffectiveMovementSpeedMod >= 1.2, MoMUnreservedShare >= 0.4, RampBudget >= RampStages, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifePerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup >= 0.85*ESPerSecondCost`. Incumbent: 963,133 FullDPS, violation 0.0000, 102 points.

Weights: 3881 fast trials in 108.8s; positive 1515, zero 341, negative 494.

| proposal | predicted gain | actual value | violation | rho | changed points | trunk dropped | solver s | gap | feasible | refused masteries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| proposal (unrestricted) | +175.49% | 264,718 | 1.4361 | -8.60 | 108 | 6 | 60.09 | 2.43% | False | - |
| proposal (D=10) | +27.65% | 435,531 | 0.1987 | -9.17 | 9 | 0 | 34.15 | 0.00% | False | - |
| proposal (D=20) | +41.02% | 459,073 | 0.6484 | -17.08 | 20 | 0 | 60.11 | 1.12% | False | - |
| proposal (D=40) | +63.15% | 476,181 | 1.0408 | -17.28 | 29 | 0 | 60.11 | 2.71% | False | - |
| re-linearization | - | no accepted first proposal | - | - | - | - | - | - | - | - |

Total PoB seconds after loading the delivered build: 112.0s (experiment wall time 337.8s, including HiGHS).

## burning_arrow_snipe

Source: `artifacts/benchmark/20260919-0130-new18-rules/burning_arrow_snipe-s2.pob.txt`. Objective: `maximize CombinedDPS subject to Life >= 3700, PhysicalMaximumHitTaken >= 4700, FireMaximumHitTaken >= 14800, ColdMaximumHitTaken >= 14600, LightningMaximumHitTaken >= 16000, FireResist >= 75, ColdResist >= 75, LightningResist >= 75, EffectiveMovementSpeedMod >= 1.2, MoMUnreservedShare >= 0.4, RampBudget >= RampStages, Str >= ReqStr, Dex >= ReqDex, Int >= ReqInt, ManaUnreserved >= ManaCost, LifeUnreserved >= LifeCost, NetLifeRegen+NetEnergyShieldRegen+SelfCostPerSecond >= 0*Life, ManaRegenRecovery+ManaLeechGainRate+ManaRecoup >= 0.85*ManaPerSecondCost, LifeRegenRecovery+LifeLeechGainRate+LifeRecoup >= 0.85*LifePerSecondCost, EnergyShieldRegenRecovery+EnergyShieldLeechGainRate+EnergyShieldRecoup >= 0.85*ESPerSecondCost`. Incumbent: 1,520,364 CombinedDPS, violation 0.0250, 103 points.

Weights: 3875 fast trials in 67.6s; positive 665, zero 1671, negative 14.

| proposal | predicted gain | actual value | violation | rho | changed points | trunk dropped | solver s | gap | feasible | refused masteries |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| proposal (unrestricted) | +1255.01% | 399,082 | 0.1714 | -0.18 | 134 | 3 | 60.10 | 7.27% | False | - |
| proposal (D=10) | +15.37% | 1,531,592 | 1.0250 | -65.03 | 10 | 0 | 60.12 | 5.35% | False | - |
| proposal (D=20) | +51.46% | 1,390,176 | 1.0000 | -19.11 | 20 | 0 | 60.11 | 9.46% | False | - |
| proposal (D=40) | +318.96% | 1,173,621 | 1.1714 | -3.67 | 40 | 0 | 60.12 | 6.84% | False | - |
| re-linearization | - | no accepted first proposal | - | - | - | - | - | - | - | - |

Total PoB seconds after loading the delivered build: 71.8s (experiment wall time 324.6s, including HiGHS).

## Result

Only summon_raging_spirits improved Score, and no proposal improved an incumbent while feasible.
At D=10, additive-model rho ranges from -65.03 to -0.48, so the additive model is not trustworthy even at the smallest radius.
PoB rejected or made infeasible 18 proposal(s); floors and near-zero-priced connectors break the additive prediction.
