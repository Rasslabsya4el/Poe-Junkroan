# Issue #606 unit 1: how PoB (v2.67.2) models ailments

Paths are under vendor/pob/source/src. CO = Modules/CalcOffence.lua, CP = Modules/CalcPerform.lua, CFG = Modules/ConfigOptions.lua, D = Modules/Data.lua. Version: vendor/pob/source/manifest.xml:3.

## Headline findings

1. The formula "50 * (damage / threshold)^0.4 * effectMod" (CO:5224, 5230) is used ONLY to fill the breakdown table (val.effect is called once, CO:5323, inside "if breakdown then"). It never sets ShockVal / CurrentShock. Search for ".effect(" in Modules/*.lua: one hit, CO:5323.
2. The shock the enemy actually carries comes from: (a) config ShockVal (CFG:1922, only when the player types "Effect of Shock:"), (b) modDB ShockBase / ShockOverride / ShockMinimum (CP:3500-3540: guaranteed sources, Shocked Ground CP:1352-1355, Skitterbots CP:1362-1364). ShockVal is written nowhere else (search for Val" in Classes and Modules: only CFG writes, CP reads, CalcSections display).
3. So PoB does not derive the shock a build own hits earn. This contradicts the comment at src/junkroan/optimizer/config_rules.py:103-105 ("PoB applies by itself: ChillVal/ShockVal from the hit") and src/junkroan/mechanics/pending_facts.json around line 147-149 ("applies the shock its own hits earn (CalcPerform ShockVal)"). Places searched for any other writer: CalcOffence, CalcPerform, CalcSetup, CalcDefence, CalcActiveSkill, Calcs, ConfigOptions, ModParser, Classes/. None.
4. Toggle on, no value typed: no tiny shock (see Q2). "Is the enemy Shocked?" only sets Condition:Shocked; no DamageTaken mod, CurrentShock absent.

## Q1. Per ailment

### Chance to apply (CO:4106-4138)
- Generic loop over Ignite, Chill, Freeze, Shock, Scorch, Brittle, Sap: chance = Sum BASE "Enemy<A>Chance" + enemyDB "Self<A>Chance" (CO:4108), times avoid (immune / Avoid mods, CO:4109, 4113). Chill chance is forced to 100 (CO:4110-4112).
- ChanceOnCrit = 100 for Ignite, Chill, Freeze, Shock (CO:4125). Not for Scorch, Brittle, Sap: ailmentData[a].alt = true (D:422-424), so ChanceOnCrit = ChanceOnHit (CO:4121-4123) unless flag CritAlwaysAltAilments. Flag CritsDontAlways<A> (Painseeker) does the same for the others. So "crit = 100% for the element default ailment" holds for Ignite/Chill/Freeze/Shock only; Scorch/Brittle/Sap need their own Enemy<A>Chance mods.
- Warden Oath of Summer: IgniteCanScorch gives Scorch chance and 100 on crit (CO:4115-4118, 4132-4134).
- skillFlags["inflict"..A] = true when ChanceOnHit + (NeverCrit ? 0 : ChanceOnCrit) > 0 (CO:4135-4137). These are the "can inflict" flags that gate config vars via ifFlag inflictScorch, inflictBrittle, inflictSap (CFG:1858, 1905, 1932). The Shock/Chill config vars have no ifFlag.
- Hit required: skillFlags.hit and not Cannot<A>, else chance 0 (CO:4119, 4127-4129). ailmentMode CRIT zeroes ChanceOnHit (CO:4165-4170); AilmentsAreNeverFromCrit CO:4175-4179.
- Source damage of an ailment: the associated type unless <type>Cannot<A>; other types only with flag <type>Can<A> (CO:4191-4206). Associated types: Chill/Freeze/Brittle = Cold, Shock/Sap = Lightning, Scorch = Fire (D:419-424). Damage = output[type.."HitAverage"] / CritAverage, weighted by non-crit vs crit chance (CO:4209-4218).
- Bleed: needs attack and not CannotBleed; BleedChance (+ enemy SelfBleedChance) capped 100 (CO:4073-4076, 4094-4098). Poison: needs hit and not CannotPoison; PoisonChance (CO:4078-4081, 4099-4105); ChaosPoisonChance adds for chaos damage (CO:4104, 4590-4592).

### Magnitude vs threshold (CO:5221-5252, "ailments" table, verbatim formulas)
    Chill  : 50 * ((damage / enemyThreshold) ^ 0.4) * effectMod      (effList 10,20; ramping = HasBonechill)
    Shock  : 50 * ((damage / enemyThreshold) ^ 0.4) * effectMod      (effList 10,20,40; ramping = true)
    Scorch : 50 * ((damage / enemyThreshold) ^ 0.4) * effectMod      (5,10,20)
    Brittle: 10 * ((damage / enemyThreshold) ^ 0.4) * effectMod      (2,4)
    Sap    : (100 / 3) * ((damage / enemyThreshold) ^ 0.4) * effectMod   (5,10; ramping = false)
Inverse (threshold for a target effect): damage * ((50 * effectMod / value) ^ 2.5) (CO:5225). effectMod = calcLib.mod(skillModList, cfg, "Enemy<A>Effect") * calcLib.mod(enemyDB, nil, "Self<A>Effect") (CO:5314). The formula has no clamp to the in-game minimum; the minimum (D:419-424 min) is only added as a table row (CO:5319-5321). Caps (max): Chill 30, Shock 50, Scorch 30, Brittle 6, Sap 20 (D:419-424), raised by <A>Max mods (CP:3532-3539). damage must be > 0 or nothing is flagged (CO:5308).
- Freeze: no effect formula. Only FreezeChance, FreezeDurationMod = 1 + inc/100 (CO:5284) and a breakdown line "for freeze to apply for the minimum of 0.3 seconds, target must have no more than baseVal * 20 * FreezeDurationMod Ailment Threshold" (CO:5286). D:420: min 0.3, max 3. Freeze duration versus a hit is not computed numerically.
- Ignite (CO:4880-5122): DPS = calcAilmentDamage * IgnitePercentBase (0.9, Data/Misc.lua:260) * effectMod * rateMod * activeIgnites * effMult (CO:5062, 5083-5090). Outputs IgniteDPS, IgniteDamage, IgniteDuration, IgniteChancePerHit (CO:4890), IgniteStacksMax, TotalIgniteDPS (only with IgniteCanStack, CO:5119-5122). Without IgniteCanStack maxStacks = 1 (CO:4895-4897): the strongest single ignite.
- Poison (CO:4561-4775): stacks = HitChance * poisonChance * additionalPoisonStacks * dpsMultiplier * stackMultiplier * quantityMultiplier * PoisonDuration * hit rate (CO:4603-4607); single poison DPS = base * PoisonPercentBase 0.30 (Data/Misc.lua:258) * effectMod * rateMod * effMult (CO:4719, 4741-4746); TotalPoisonDPS = singlePoisonDPS * PoisonStacks, capped by DotDpsCap (CO:4769-4773). PoisonStackLimit at CO:4602-4618.
- Bleed (CO:4289-4559): stacks = HitChance * bleedChance * dpsMultiplier * duration * hit rate (x totems), config Multiplier:BleedStacks overrides (CO:4309-4333); BleedStacksMax; BleedDPS = base * BleedPercentBase 70 (Data/Misc.lua:256) * effectMod * rateMod * min(stacks, max) * effMult (CO:4444-4475); BleedRollAverage models the strongest-roll (CO:4363-4372).

### Duration (CO:5310-5312)
output[A.."Duration"] = ailmentData[A].duration * (1 + incDur/100) * moreDur * debuffDurationMult. Base: Chill 2, Shock 2, Scorch 4, Brittle 4, Sap 4 (D:419-424); Ignite 4, Bleed 5, Poison 2 (Data/Misc.lua:257, 259, 261; CO:4313, 4585, 4894).

### Stacking / strongest instance (CP:3431-3546)
- CP:3499-3502 loop for Chill, Shock, Scorch, Brittle, Sap runs only if enemyDB "<A>Val" sum > 0 or modDB has <A>Base/Override/Minimum, and the enemy is not immune or avoiding 100%.
- Current<A> = floor(min(max(override, enemyDB <A>Val sum), Maximum<A>) * 10^precision) / 10^precision (CP:3540): the strongest of the configured value and the guaranteed sources, capped. The tooltip says so too (CFG:1921).
- Default is one instance: DamageTaken INC num under Condition Shocked (CP:3464). With flag ShockCanStack (ModParser:3029 "you can apply up to N shocks"; ShockStacksMax default 1, CalcSetup:61): CurrentShock = num * min(Multiplier:ShockStacks, ShockStacksMax) (CP:3457-3459); Scorch likewise (CP:3473-3475, CalcSetup:62). Stack count typed in config ShockStacks (CFG:1925, placeholder 1) / ScorchStacks (CFG:1866). Chill, Brittle, Sap: one instance.
- Effect applied: Chill = ActionSpeed INC -num (+ cold/all DamageTaken for Bonechill, Ahuana Bite etc., CP:3437-3449); Shock = DamageTaken INC num; Scorch = ElementalResist BASE -num; Brittle = SelfCritChance BASE num; Sap = Damage MORE -num (CP:3453-3496).

### Outputs
<A>ChanceOnHit, <A>ChanceOnCrit, <A>Chance (CO:4120-4129, 4215); <A>EffectMod (CO:5314; shown CalcSections:1215, 1246, 1283, 1312, 1344); <A>Duration; Maximum<A> and Current<A> (CP:3539-3540; CalcSections:1237, 1261-1264, 1305, 1336-1339, 1366); ChillSourceEffect (non-hit chill, CO:5262); FreezeDurationMod; CurrentShock / CurrentScorch in stacking mode; Multiplier:ChillEffect and Multiplier:ShockEffect mirror Current (CP:3549-3556). Damage ailments: IgniteDPS, TotalIgniteDPS, PoisonDPS, TotalPoisonDPS, BleedDPS, BleedStacks, BleedStackPotential, IgniteStackPotential. Multi-pass averaging CO:5553-5567.

## Q2. Config side (ConfigOptions.lua line, var, label verbatim)
Enemy side:
- 1917 conditionEnemyShocked, check "Is the enemy Shocked?": Condition:Shocked + Condition:ShockedConfig on enemy.
- 1921 conditionShockEffect, count "Effect of Shock:" (ifOption conditionEnemyShocked): ShockVal BASE val (cond ShockedConfig) and DesiredShockVal (breakdown only).
- 1925 ShockStacks, count "Shock Stacks" (ifFlag ShockCanStack, placeholder 1). 1928 conditionEnemyOnShockedGround "Is the enemy on Shocked Ground?".
- 1858 conditionEnemyScorched "Is the enemy Scorched?" (ifFlag inflictScorch); 1862 conditionScorchedEffect "Effect of Scorched:"; 1866 ScorchStacks "Scorch Stacks"; 1869 conditionEnemyOnScorchedGround.
- 1873 conditionEnemyChilled "Is the enemy Chilled?"; 1881 conditionEnemyChilledEffect "Effect of Chill:"; 1877 multiplierChilledByYouSeconds "Seconds of chill on enemy?"; 1885 conditionEnemyChilledByYourHits "Is the enemy Chilled by your Hits?".
- 1905 conditionEnemyBrittle "Is the enemy Brittle?" (ifFlag inflictBrittle); 1909 conditionBrittleEffect "Effect of Brittle:".
- 1932 conditionEnemySapped "Is the enemy Sapped?" (ifFlag inflictSap); 1936 conditionSapEffect "Effect of Sap:".
- 1944 multiplierFreezeShockIgniteOnEnemy "# of Freeze / Shock / Ignite on enemy:". No effect override exists for Freeze/Ignite/Bleed/Poison; stacks via Multiplier:BleedStacks (read CO:4309) and multiplierPoisonOnEnemy (CO:4620).
- 2060 enemyIsBoss, list "Is the enemy a Boss?": None "No", Boss "Standard Boss", Pinnacle "Guardian/Pinnacle Boss", Uber "Uber Pinnacle Boss"; defaultIndex = 3 (Pinnacle). 2056 enemyLevel "Enemy Level:". 210 ailmentMode "Ailment calculation mode:" (Average / Crits Only).
Player side: conditionShocked 1199 "Are you Shocked?", conditionPlayerShockEffect 1202 "Effect of Shock:", conditionChilled 1187, conditionChilledEffect 1190, conditionScorched 1184, conditionBrittle 1196, conditionSapped 1205. Player shock without a value DOES default to 15 (CP:851, "or ailmentData.Shock.default"); that default exists only for the player, not for the enemy.

### Toggle on, no value: the "tiny ~1% shock" claim (owner)
Not found in the code; the code path gives no shock:
- ConfigTab apply loop (Classes/ConfigTab.lua:1086-1093): a count var is applied only if the input is non-zero or a placeholder exists. conditionShockEffect has no defaultPlaceholderState, so with an empty box apply is not called and ShockVal is never added.
- CP:3500: the shock block needs enemyDB ShockVal > 0 or ShockBase/Override/Minimum in modDB. With neither: no CurrentShock, no DamageTaken INC from Shock. Only Condition:Shocked is true, so "against Shocked enemies" mods apply (this may be what the owner saw).
- Elementalist-type guaranteed sources (ShockMinimum ModParser:2768; ShockBase conditionals ModParser:2936, 3690-3740) add a fixed value (default 15 times effect mods); none is 1%.
- Inference (not read): a 1% would come from a build with such a source or from a stale value. The check that settles it: run the build with the toggle on and no value, read CurrentShock and the enemy DamageTaken from the headless worker.

## Q3. Ailment threshold (CO:5208-5218)
    isBoss = env.configInput["enemyIsBoss"] ~= "None"
    enemyAilmentThreshold = data.monsterAilmentThresholdTable[env.enemyLevel]      -- Data/Misc.lua, by level
    if env.enemyLevel >= 66 then
        enemyMapLifeMult = isBoss and data.mapLevelBossLifeMult[lvl] or data.mapLevelLifeMult[lvl]
        enemyMapAilmentMult = isBoss and data.mapLevelBossAilmentMult[lvl] or 1
    enemyTypeMult = isBoss and 7.68 or 1
    enemyThreshold = Threshold * enemyTypeMult * enemyMapLifeMult * enemyDB:More(nil,"Life") * enemyMapAilmentMult * enemyDB:More(nil,"AilmentThreshold")
Boss presets add enemy AilmentThreshold MORE: Standard Boss 488 (CFG:2096), Guardian/Pinnacle 404 (CFG:2131), Uber 404 (CFG:2165); factor 1 + v/100 = 5.88 / 5.04 / 5.04. Default level: Pinnacle 84 (CFG:2141), Standard Boss 83 (CFG:2106), Uber 85 (CFG:2175). No boss preset sets enemy Life MORE (search NewMod("Life" in ConfigOptions: none).
Values at level 84 (table [84] = 16265; mapLevelBossLifeMult[84] = 21.46; mapLevelBossAilmentMult[84] = 0.47; mapLevelLifeMult[84] = 2.17; from Data/Misc.lua:470-473, products computed by me):
- Guardian/Pinnacle, level 84: 16265 * 7.68 * 21.46 * 0.47 * 5.04 = about 6,350,000.
- Standard Boss, level 84 (if forced): 16265 * 7.68 * 21.46 * 0.47 * 5.88 = about 7,408,000.
- Not a boss, level 84: 16265 * 2.17 = about 35,300 (level 83: 15319 * 2.09 = 32,017).
Shock on Pinnacle L84, effectMod 1 (computed from the formula): hit 100k gives 9.5%; 1M gives 23.9%; 5M gives 45.4%; 10M gives 60.0% (capped at Maximum Shock 50).

## Q4. Ramp, and iterating hits outside PoB
- No ramp in PoB. One hit shock only: ramping = true (CO:5232, 5238, 5244) feeds only the breakdown label "with a X% shock on the enemy" (CO:5334). A hit raising the next hit shock is not modelled. ShockCanStack stacks multiply the same num (CP:3459); they do not add per-hit magnitudes.
- Per-hit input: damage = calcAilmentDamage(A, CritChance, calcAverageSourceDamage(A)) * More("<A>AsThoughDealing") (CO:5306): chance-weighted average of output.<Type>HitAverage / CritAverage of the types allowed to apply it (CO:4191-4218). Inference from the names: these are pre-enemy-mitigation hit averages.
- Outside PoB: effect_k = min(Maximum<A>, 50 * (hit_k / threshold)^0.4 * <A>EffectMod); threshold from the Q3 formula; feed the result back as conditionShockEffect (integer count; CP:3540 floors to precision 0 for Shock). PoB applies only the number typed (or the larger guaranteed source). Needed per-build outputs: ShockEffectMod, MaximumShock, hit averages.

## Q5. Our repo today
- Worker defaults: src/junkroan/pob/headless_runtime_worker.py:55 enemyIsBoss "Pinnacle", :59 conditionEnemyShocked False, :61 conditionShockEffect None; XML inputs written only when non-default (:3959-3960, :3977-3981); read back :5602-5655 (enemy_state.is_shocked, shock_effect); shock_effect requires is_shocked (:3945-3950 region).
- No caller outside the worker sets shock_effect / is_shocked (searched src, scripts, config).
- Lane gating: src/junkroan/optimizer/config_rules.py:103-108 (OTHER_SKILL_AILMENTS, "Shocked": "lightning"); :2044-2055 (a conditionEnemy<X> var is allowed only if a second skill of that element exists, else "the main skill own ailment PoB applies by itself"); :1566 lane.inputs["enemyIsBoss"] = boss; :1815 AILMENT_DURATIONS; :1861-1881 _ailment_evidence. src/junkroan/optimizer/judging.py:38, 59, 119 keep enemyIsBoss out of preserved user inputs.
- Consequence (from headline 3): a Lightning build own shock is never put into PoB, and the stated reason "PoB applies by itself" is not backed by the CP/CO code read above.
- Corpus: src/junkroan/pob/corpus_data/config_surfaces.json:10269-10303 (conditionEnemyShocked, conditionShockEffect, ifOption).
