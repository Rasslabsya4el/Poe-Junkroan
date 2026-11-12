# Community practice report (PoE1, 3.2x-era mechanics)

## 1. Volatile Dead + regular Spell Cascade + Desecrate

Players generally model a hand-cast VD/Cascade cast as nine VD orbs when Desecrate supplies corpses; with DD sharing the corpse pool, reports become “9 VD + 1 DD” or “7 VD + 3 DD,” depending on corpse-consumption order and Undertaker. A Spellslinger setup is usually counted the same per trigger (nine VD if VD is alone), while Desecrate itself is capped at ten corpses; one PoB discussion explicitly says “you’re 3 DD + 7 VD, or 9 VD + 1 DD.” The claim that normal Cascade gives nine VD orbs is therefore common, but not universal when DD competes for corpses.

- Numbers: hand-cast 6–9 reported, practical target ≈9; Spellslinger 7–9 VD when DD is linked, 9 VD if VD-only.
- PoB convention: one-orb damage multiplied by 9 (or by 7 VD + 3 DD in mixed setups).
- Sources: [VD/DD Spellslinger PoB discussion](https://www.reddit.com/r/PathOfExileBuilds/comments/i2gafm/vd_dd_spellslinger_dps_in_pob/) (2 Aug 2020), “you’re 3 DD + 7 VD, or 9 VD + 1 DD”; [Awakened Cascade VD discussion](https://www.reddit.com/r/PathOfExileBuilds/comments/ho5chk/awakened_spell_cascade_with_volatile_dead_spellslinger/) (9 Jul 2020), “maximum number of VD balls…9.”
- Confidence: **high**

## 2. Pyroclast Mine projectile hits and detonation chains

The only detailed player calculation found estimated 18 active mines, about 38 mines in a full chain, and roughly 13 projectiles from the last mines. Using a 36% overlap chance, that post calculated 2.34 projectile hits per mine on average, plus Pyroclast’s guaranteed base nova for about 3.34 total hits per mine. Other players warn that overlap varies strongly with AoE, boss size and positioning; therefore PoB “hits” values are assumptions, not a stable measurement.

- Numbers: conservative 2.3 projectile overlaps/mine; ≈3.3 total hits including nova; last chain mines up to ~13 projectiles.
- Practical range reported: roughly 2–4 projectile hits per mine; optimistic “all projectiles” calculations are rejected.
- Sources: [Pyroclast overlap calculation](https://www.reddit.com/r/PathOfExileBuilds/comments/1gy8ko1/next_upgrades_on_my_homebrew_pyroclast_mines_ascendant/) (23 Nov 2024), “2.34 proj hits per mine…total hits…around 3.34”; [AoE overlap discussion](https://www.reddit.com/r/PathOfExileBuilds/comments/15qpdsq/how_does_aoe_affect_pyroclast_projs_overlap/) (17 Aug 2023), “AoE…slightly reduced the more AoE you have.”
- Confidence: **medium**

## 3. Mines kept before detonation, reservation and unreserved mana

No Reddit/forum post located gives a reliable cross-build measurement for Pyroclast, Exsanguinate, Icicle and Hexblast simultaneously. The Pyroclast calculation used an 18-mine active limit, but that is a build limit rather than evidence that players always preload 18; practical detonations are commonly described as constrained by throw speed, mana and boss movement. No consistent community number was found for “unreserved mana to keep,” and reservation varies with mine skill, Minefield supports, auras and Eldritch Battery/MoM choices.

- Numbers: one detailed example uses 18 active mines and ~38 mines through chaining; per-mine reservation/unreserved-mana targets: **not found** as a shared rule.
- Sources: [Pyroclast mine-limit calculation](https://www.reddit.com/r/PathOfExileBuilds/comments/1gy8ko1/next_upgrades_on_my_homebrew_pyroclast_mines_ascendant/) (23 Nov 2024), “With an active Mine limit of 18”; [Hexblast/Withering Step setup](https://www.reddit.com/r/pathofexile/comments/197k3la/why_not_withering_step_totems_instead_of_wither_totems/) (15 Jan 2024), “skip more reliably…after the initial 18” (illustrating an 18-mine preload, not a universal rule).
- Confidence: **low**

## 4. Shrapnel Ballista + Arrow Nova

Arrow Nova does function with Shrapnel Ballista, and players use it specifically to place the nova on a stationary boss so the shrapnel cone shotguns. Testing is inconsistent on small or moving targets: one user observed roughly two hits (impact plus nova) and concluded “it does not work,” while other builds report multiplying PoB projectile damage by projectile count and totem count. Tuadh’s league-start link is therefore mechanically valid but highly position-dependent.

- Numbers: practical single-target behavior ranges from 1–2 reliable hits to near-all projectiles on a stationary, large target; theoretical PoB multipliers can be 8–14 projectiles per totem, then multiplied by totems.
- Sources: [Arrow Nova testing](https://www.reddit.com/r/pathofexile/comments/ecb217/is_anyone_using_arrow_nova_support/) (18–19 Dec 2019), “I guess its 2 hits…TLDR, it does not work”; [Shrapnel Ballista PoB test](https://www.reddit.com/r/PathOfExileBuilds/comments/176u61w/deadeye_la_shrapnel_ballista_dps_100_test/) (13 Oct 2023), “each totem hits 196 times with Arrow nova.”
- Confidence: **high**

## 5. Perforate bleed: stance and overlap

Blood Stance is intended for bosses, but players repeatedly report unreliable spike placement and frequent overshoot. Each attack is commonly described as about four to five spikes; practical boss overlap is often only one to two, occasionally three or more when positioning and AoE are favorable. PoB users therefore multiply single-spike damage by an assumed overlap count; no consensus input value was found, with 2–3 being the defensible range.

- Numbers: 4–5 spikes spawned; usually 1–2 hit a small boss, ~3 needed to overcome Blood Stance’s 65% less damage, optimistic 3+.
- Sources: [Blood Stance testing](https://www.reddit.com/r/pathofexile/comments/byfzo2/perforate_blood_stance_does_no_significant_more_damage/) (9 Jun 2019), “Each blood stance attack summons about 4-5 spikes”; [PoB overlap question](https://www.reddit.com/r/pathofexile/comments/lifsnq/how_does_perforate_work_in_pob/) (12 Feb 2021), “Multiply the dps…by the amount of spikes.”
- Confidence: **high**

## 6. Imbalanced Guard

A detailed analysis models Imbalanced Guard as doubling armour while capping total physical mitigation at 50%. It reports that hits below roughly one-tenth of armour become worse, the best region is near one-fifth of armour (about 25% net reduction), and benefit declines as hit size approaches armour. Example break-even points were ~800 damage for 8k armour, ~2,700 for a 15k balanced build, and ~17k for a heavily defended Juggernaut.

- Numbers: downside below ~0.1× armour; strongest around ~0.2× armour; practical benefit often 10–25% effective mitigation; hard cap at 50%.
- Sources: [Imbalanced Guard scenarios](https://www.reddit.com/r/pathofexile/comments/halqxn/imbalanced_guard_scenarios/) (17 Jun 2020), “best against hits for 1/5th of your armor”; [re-visualized analysis](https://www.reddit.com/r/pathofexile/comments/q8jncn/imbalanced_guard_re-visualized/) (15 Oct 2021), “with…24% phys damage reduction…cap around 15k armor.”
- Confidence: **high**

## 7. Trauma Support survival and stack counts

Players sustain Trauma through very high physical mitigation plus regeneration, recoup or Divine Shield; without those layers, self-damage quickly becomes lethal. Reports range from only ~25–30 sustainable stacks on underbuilt characters to 60 stacks in tested setups, and historical Juggernaut builds advertised roughly 100–200 stacks with extreme investment. Common breakpoints are about 87–90% effective physical mitigation and enough recovery to cover attack-rate-scaled self-hits.

- Numbers: 25–30 stacks commonly reported while struggling; ~60 sustainable in a solved build; 100–200 only in specialized legacy-style setups.
- Sources: [30+ Trauma stacks](https://www.reddit.com/r/PathOfExileBuilds/comments/1679wra/trying_to_sustain_30_trauma_stacks/) (1 Sep 2023), “at max rage…61 trauma…15.4k damage”; [Trauma-stacking Juggernaut](https://www.reddit.com/r/PathOfExileBuilds/comments/pawzfv/trauma_stacking_j_u_g_g_100_200_stacks/) (15 Sep 2021), “we can reach around 150 stacks.”
- Confidence: **high**

## 8. Accuracy and chance to hit at league start

I found no Reddit/forum post establishing a universal “95% minimum” rule specifically for league-start attack builds. Community advice generally treats 100% chance to hit as ideal for consistent damage, while 95% is an owner-provided heuristic rather than a documented consensus. Because no dated thread with a numerical rule was located, the optimizer should expose accuracy sensitivity instead of hard-coding 95%.

- Numbers: 95% stated by the owner; 100% is the practical perfection target; consensus range **not found**.
- Source: [Defence-layer discussion](https://www.reddit.com/r/PathOfExileBuilds/comments/1usbxud/understanding_defence_layers_and_how_they_are/) (2026), which discusses hit mechanics but gives no league-start accuracy threshold.
- Confidence: **low**

## 9. Sigil of Power stage ramp

Sigil gains one stage per qualifying mana-spending event, so players commonly report four casts/events to reach maximum. Archmage Ball Lightning users describe four casts as routine; low-cost attack builds often cannot reach stage four without deliberately adding an expensive skill or lowering Sigil’s level. Guides that show maximum-stage boss DPS therefore assume setup time and should not be read as instantaneous damage.

- Numbers: one stage per event; four events/casts to stage 4; low-cost attacks may remain at stage 1.
- Sources: [Sigil + Arcane Cloak](https://www.reddit.com/r/pathofexile/comments/j078tf/sigil_of_power_arcane_cloak/) (26 Sep 2020), “it takes 4 casts to max it out”; [mana-spending discussion](https://www.reddit.com/r/pathofexile/comments/1fv3szb/what_are_good_ways_to_spend_mana_for_sigil_of_power/) (3 Oct 2024), “I use a lvl 1 sigil…reach 4 stages.”
- Confidence: **high**

## 10. Withered stacks from Wither Totems / Withering Step

Ordinary Spell Totem + Wither ramps gradually and is often modeled around 10 stacks for realistic boss uptime rather than assuming permanent 15. A Withering Step totem applies nine stacks immediately; two totems can reach the 15-stack cap after cooldowns, while three conventional Wither totems improve ramp speed but still require repeated casts and target contact. Boss movement can cause missed or stale stacks.

- Numbers: conventional Wither PoB assumption ≈10 stacks; 1 Withering Step totem = 9 immediate; 2 = 15 cap after cooldown; 1–3 Wither totems ramp toward 15 over repeated casts.
- Sources: [Withering Step totems](https://www.reddit.com/r/pathofexile/comments/197k3la/why_not_withering_step_totems_instead_of_wither_totems/) (15 Jan 2024), “one totem will instantly get 9…two…15 stacks”; [Wither-stack PoB advice](https://www.reddit.com/r/pathofexile/comments/qh9p3g/does_wither_stack_withering_step_wither_totems_withering_touch/) (27 Oct 2021), “best to leave wither stacks at ~10.”
- Confidence: **high**

## 10-line optimizer summary

1. VD regular Cascade: model 9 VD orbs per cast when VD has the corpses.  
2. Mixed VD/DD corpse use: test 7 VD + 3 DD versus 9 VD + 1 DD.  
3. Pyroclast: use ~2.3 projectile overlaps plus one guaranteed nova (~3.3 hits/mine).  
4. Pyroclast chains can reach ~38 mines total; last mines may fire ~13 projectiles.  
5. Mine preload: 18 is a common active-limit example, not a universal behavior.  
6. Shrapnel Ballista + Arrow Nova works; stationary-boss hit count can approach all projectiles.  
7. Perforate Blood Stance: assume 1–2 overlaps normally, 3 when optimized.  
8. Imbalanced Guard is best near hits ≈0.2× armour and caps at 50% mitigation.  
9. Trauma: budget for 25–60 sustainable stacks unless exceptionally specialized.  
10. Sigil needs four spending events; Wither PoB ≈10 stacks, Withering Step 1–2 totems = 9–15 instantly.