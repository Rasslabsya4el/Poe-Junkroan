Saved to `docs/research/2026-10-04-greater-volley-mortar-overlap.md`.

# Greater Volley on Forged Frostbearer Ice Mortars: overlap on one boss

**Research date:** 2026-10-04  
**Game context:** Path of Exile 3.29; the question is the number of Ice Mortar explosion areas that can damage one boss-size target when one Forged Frostbearer fires five mortars with Greater Volley.

## Scope and evidence standard

The sources below distinguish three different claims:

* projectile **shape** (fan versus parallel lanes);
* the PoE projectile rule (simultaneous projectiles do not directly hit one target more than once);
* **area overlap** (several impact explosions can still damage the target).

“Five projectiles” means the base projectile plus Greater Volley's four additional projectiles. A source that reports a multiplier or a PoB setting is recorded as that author's modeled count; it is not silently upgraded to a controlled in-game measurement. No source found during this search states a numeric physical fan width in metres or a boss hitbox measurement for Ice Mortar.

## 1. Ice Mortar, Greater Volley shape, and the overlap rule

### Forged Frostbearer / Ice Mortar — PoE Wiki

**URL:** https://www.poewiki.net/wiki/Forged_Frostbearer  
**Date:** page last updated 2026-03-25 (the page exposes this date in search results; no individual author is credited)  
**Author:** PoE Wiki editors (individual author not credited)  
**Verbatim passage:**

> “Cold Mortar – uses a cold damage mortar skill similar to other monster mortars, dealing area cold damage on impact (Skill:MMSPyromaniacIceMortar)”

The linked internal-skill page gives the underlying skill description:

**URL:** https://www.poewiki.net/wiki/Skill:MMSPyromaniacIceMortar  
**Date:** page last updated 2026-07-11 (no individual author credited)  
**Author:** PoE Wiki editors (individual author not credited)  
**Verbatim passage:**

> “Generic monster mortar skill. Like Monster Projectile but has an impact effect.”

These passages establish an impact area, but do not state its radius, the spread width, or a boss overlap count.

### Greater Volley — PoE Wiki

**URL:** https://www.poewiki.net/wiki/Greater_Volley_Support  
**Date:** current page; no individual publication date or individual author credited  
**Author:** PoE Wiki editors (individual author not credited)  
**Verbatim passage:**

> “Supported Skills fire 4 additional Projectiles”
>
> “Supported Skills also fire Projectiles from up to 4 points on each side of you”

The same page describes the geometry:

> “While the projectiles from Greater Multiple Projectiles fan out from the main projectile, Greater Volley's projectiles shoot out parallel to the main projectile, and originate from points on either side of the player.”

This is a parallel, side-origin pattern, not the GMP fan. The source does not give a width in metres or degrees. “Up to 4 points on each side” is a source-point description, not a stated ground spread width.

### Volley — PoE Wiki

**URL:** https://www.poewiki.net/wiki/Volley_Support  
**Date:** current page; no individual publication date or individual author credited  
**Author:** PoE Wiki editors (individual author not credited)  
**Verbatim passage:**

> “While Multiple Projectiles Support's projectiles fan out from the main projectile, Volley's projectiles shoot out parallel to the main projectile, and originate from points on either side of the player.”

The same page records the distribution rule when more projectiles are added:

> “Additional Projectiles: If additional projectiles are added to a skill supported by Volley Support, they will first begin being fired from two additional points beside the character (for a total of five), then the points will begin launching multiple projectiles.”

This supports the qualitative conclusion that Volley and Greater Volley use parallel lanes. It still does not provide Ice Mortar's physical lane spacing or explosion radius.

### GGG's Greater Volley announcement

**URL:** https://www.pathofexile.com/forum/view-thread/2682345  
**Date:** 2019-11-27  
**Author:** Natalia_GGG, Grinding Gear Games  
**Verbatim passage:**

> “Any Arrow + Barrage + Greater Volley This causes a sequential volley to fire in a line from side to side, damaging a condensed area that can hit enemies many times.”

The condition matters: this example includes Barrage and an arrow skill, so it is not a direct Ice Mortar test. It is official support for Greater Volley's side-to-side/condensed-area behavior, not a numerical Ice Mortar overlap result.

### GGG's Volley clarification

**URL:** https://www.pathofexile.com/forum/view-thread/2034078/filter-account-type/staff  
**Date:** 2017-12-06 (the official announcement thread date)  
**Author:** Grinding Gear Games staff post (announcement; the individual author is not visible in the retrieved extract)  
**Verbatim passage:**

> “This support adds two extra projectiles, and lets a portion of your projectiles be fired from adjacent points. The adjacent projectiles are fired from up to four adjacent points, creating a wide line of projectiles.”

The passage describes Volley, not Greater Volley, and says “wide line” without a width measurement. It is consistent with the PoE Wiki geometry description.

### The official simultaneous-projectile rule — patch 2.0.0

**URL:** https://www.pathofexile.com/forum/view-thread/1304441  
**Date:** 2015-07-10 (Path of Exile 2.0.0: The Awakening patch notes)  
**Author:** Grinding Gear Games patch notes  
**Verbatim passage:**

> “Projectile skills no longer "shotgun". You can't hit the same target with more than one simultaneously-created projectile from the same source any more. They've been rebalanced around this.”

This is the exact rule and the patch it came from. It prohibits multiple direct projectile hits from the same simultaneous cast. It does not say that an impact area created by each projectile cannot overlap.

### Official mortar example: Blazing Salvo

**URL:** https://www.pathofexile.com/forum/view-thread/2934377  
**Date:** 2020-09-11  
**Author:** Bex_GGG, Grinding Gear Games  
**Verbatim passage:**

> “Blazing Salvo releases a torrent of fiery mortars that can hit enemies as they fly and land in rapid succession, with each mortar causing an explosion. When targeting up close, the explosions can hit a target multiple times, while targeting at range causes them to spread out and have a higher explosion radius, giving you a wide damage spread.”

The condition is explicit: up-close targeting can make the explosions hit a target multiple times; at range the mortars spread out and the explosion radius is higher. This is Blazing Salvo, not Ice Mortar, so it establishes the general mortar/area behavior but not Frostbearer's exact count.

### Forum explanation of projectile versus area overlap

**URL:** https://www.pathofexile.com/forum/view-thread/3117972  
**Date:** 2021-05-12  
**Author:** Shagsbeard#3964 and AcrylicHercules#1220  
**Verbatim passages:**

Shagsbeard#3964:

> “The the projectiles have AOE and the AOE overlaps, yes. If not, no.”

AcrylicHercules#1220:

> “Projectile skills were changed way back in the 2.0.0 release to no longer shotgun: ... ‘Projectile skills no longer "shotgun". You can't hit the same target with more than one simultaneously-created projectile from the same source any more.’”
>
> “As Shagsbeard says, the closest you can come to shotgunning now is to have multiple overlapping damage areas.”

The first quote is a concise conditional rule, not an Ice Mortar measurement. It preserves the relevant condition: overlap of the projectile-created area is required.

### What was not found for Question 1

No live source located in this search states a numeric Ice Mortar fan/parallel-lane width in metres or degrees, nor a boss-size target radius, nor a controlled “exactly N of the five” measurement. The wiki and GGG sources establish “impact area,” “parallel lanes/side origins,” and the simultaneous-projectile/overlapping-area distinction.

**What it says:** Greater Volley makes the five Ice Mortars leave side-origin parallel lanes; the mortars' impact areas may overlap and damage one target, but the available sources do not give a physical spread width or prove that all five overlap a boss at every distance.

## 2. Player reports for Forged Frostbearer / Ice Mortar

### Reddit: Forged Frostbearer DPS

**URL:** https://www.reddit.com/r/pathofexile/comments/12qn3ux/forged_frostbearer_dps/  
**Post date:** 2023-04-18 (the retrieved Reddit search result gives 1:28 PM UTC)  
**Post author:** u/DeepLeg3917  
**Comment author:** the Reddit result identifies the account as u/DeepLeg3917; the comment's display name was not exposed in the retrieved page  
**Verbatim passages:**

> “Youre most likely looking at *one* projectile. They shotgun. +probably missing some pob config”

and:

> “You want volley isntead of GMP, from my testing it results in better overlap.”
>
> “Once you have that overlap you can go ahead and multiply the amount of spectres you have with the amount of projectiles.”
>
> “I have 5 spectres with 5 projectiles, so I hit 25 on the spectre gem in the gem section resulting in ~8Mio DpS.”

Conditions attached by the poster: the statement is a personal test; it compares Volley with GMP; the PoB setting is five spectres times five projectiles, and therefore models 25 total spectre projectiles hitting the target. The post does not state the target's boss size or the distance at which the test was made, and it does not say that the five mortars of one Frostbearer were separately counted on a boss.

### Reddit: Sire of Shards Forged Frostbearer Spectres

**URL:** https://www.reddit.com/r/PathOfExileBuilds/comments/12ntso2/sire_of_shards_forged_frostbearer_spectres/  
**Post date:** 2023-04-16 (the corresponding archived build entry records 2023-04-16; the Reddit result itself is dated 2023-10-03 by the search index)  
**Post author:** u/XstraNinja  
**Verbatim passage:**

> “I discovered that with Sire of Shards & Greater Volley, the Frostbearers still shoot all projectiles straight forward.”
>
> “It's honestly been a blast in t16 maps. With all the projectiles & cast speed, they actually have really good clear.”

A reply in the same thread says:

> “Volley rather than gv will almost certainly be more damage tho, since you already have so many projectiles, and avoiding the pretty big damage penalty.”

Conditions: Sire of Shards is equipped; the claim concerns direction/clear in T16 maps, not a boss-size target; the reply is a qualitative damage opinion and gives no measured per-boss count.

### Reddit: My Spectre League-starter is finally Endgame ready

**URL:** https://www.reddit.com/r/PathOfExileBuilds/comments/12irzdo/my_spectre_leaguestarter_is_finally_endgame_ready/  
**Post date:** 2023-04-18 (the Reddit search result places the thread in the Crucible-era archive; the current search index displays 2023-10-03)  
**Post author:** u/Soulune  
**Verbatim passage:**

> “We now use Greater Volley--it does have less top-end than aGMP, but is far more consistent and you don't need to worry about positioning your spectres (thanks, whensmahvelfgc).”

Earlier build text in the same thread says:

> “FBs are incredible because their Mortar skill can shotgun; on top of the fact that all of their damage is ALREADY Cold ... Larger AOE = more overlap + additional projectiles, Anomalous Faster Projectiles for double damage and double overlap (need to be positioned).”

Conditions: this is a build-guide recommendation based on the author's play/build experience; “more consistent” is compared with anomalous GMP; the quoted text does not state a number of five-mortar hits, a boss size, or a distance. It does attach a positioning condition to the Faster Projectiles overlap claim.

### Official/forum build report: pure Forged Frostbearer spectres

**URL:** https://www.pathofexile.com/forum/view-thread/3583292  
**Post date:** 2024-10-23  
**Author:** Corak_de#4285  
**Verbatim passage:**

> “These projectiles create overlapping AoEs that can all deal damage to a single target if you increase projectile count and the AoE of the spectres.”
>
> “This can be achieved by linking the gem to Greater Volley Support, using the appropriate Minion Mastery and Plaguebringer from the Necromancer Ascendancy for a dmg increase of 4-5 times compared to the dmg displayed in PoB.”

Conditions: the author attaches the overlap to increased projectile count **and** spectre AoE; the 4–5x figure is a comparison with the PoB display, not a direct count of one boss's five impacts; no distance or target-size condition is stated.

### Official/forum build report: 523M Forged Frostbearer spectres

**URL:** https://www.pathofexile.com/forum/view-thread/3555198  
**Post date:** 2024-08-15  
**Author:** Dyudan#7048  
**Verbatim passage:**

> “Total 8 spectres shoot 8 projectiles each per cast which shotgun.”

Conditions: this is an endgame Standard build description with eight spectres and eight projectiles each; it gives no target size, distance, or explanation of whether “shotgun” means direct projectile hits or overlapping mortar areas. It is therefore a stated build assumption/report, not a controlled five-mortar measurement.

### Official/forum build report: 12L Forged Frostbearer

**URL:** https://www.pathofexile.com/forum/view-thread/3521991  
**Post date:** 2024-05-09  
**Author:** lllolll15#3688  
**Verbatim passages:**

> “Boss Damage is 10 out of 10 since the Ice Mortar can shotgun easily achieving 300m guardian dps”
>
> “DPS on pob is per projectiles”
>
> “8 projectile per spectre”
>
> “up to 104 projectiles hitting the same enemy”

Conditions: the author is describing a high-investment 12L Standard showcase; the 104 figure is the author's PoB/build calculation, apparently 13 spectres × 8 projectiles, and is not an in-game count of five mortars on a boss. No boss distance, hitbox size, or controlled overlap test is stated.

### Maxroll 3.29 guide

**URL:** https://maxroll.gg/poe/build-guides/forged-frostbearer-spectre-necromancer-league-starter  
**Date:** last updated 2026-09-17  
**Author:** Helm Breaker  
**Verbatim passage:**

> “The Forged Frostbearers cast Cold mortar projectiles that scale very well when supported by Greater Volley Support, since the projectiles overlap (an effect known as shotgunning).”

The guide also specifies the support setup:

> “Raise Spectre  
> Greater Volley Support  
> Spell Echo Support”

Conditions: the overlap statement is a build-guide explanation; it does not give a numeric count for one boss, a boss size, or a distance. The guide's later advice about the Minion Offence Mastery explicitly refers to increasing the mortar explosions' area of effect, which is consistent with area overlap rather than direct projectile shotgunning.

### What was not found for Question 2

The live Reddit/forum reports found do not provide a repeatable “at X distance, Y of the five mortars hit this boss-size target” measurement. They report qualitative overlap or PoB assumptions: five projectiles per spectre, eight projectiles per spectre, or 8 projectiles × 13 spectres. They also disagree on support choice in the sense that one Frostbearer player reports better overlap with Volley, while later guides describe Greater Volley as more consistent and current 3.29 guidance uses Greater Volley.

**What it says:** player reports treat Frostbearer mortars as overlapping impact areas and commonly model all available projectiles, but none of the located reports supplies the requested controlled boss-distance count; support choice is reported qualitatively as Volley giving better overlap in one test and Greater Volley giving more consistent coverage in later build guides.

## 3. General mortar overlap and PoB community settings

### Forged Frostbearer PoB setting: 25 total projectiles

**URL:** https://www.reddit.com/r/PathOfExileBuilds/comments/1eeorcf/325_forged_frostbearers_spectres_low_budget_pob/  
**Post date:** 2024-07-29 (the indexed build/source page gives this date; Reddit's current search result is dated 2024-10-03)  
**Author:** u/BendicantMias / “Doominated” in the quoted build text  
**Verbatim passage:**

> “I have set spectre count to 25 to simulate all 5 spectres hitting with all 5 projectiles.”
>
> “I use void sphere to compact mob packs, making it easier for Forged Frostbearers to hit with all of their projectiles.”

Conditions: this is a PoB simulation setting for five spectres and five projectiles; Void Sphere is used to compact **mob packs**, so it is not proof of five impacts on an isolated boss; the author says “simulate,” not “measured.”

### Mortar-type spectre comparison: Perfect Serpent Warriors

**URL:** https://pobarchives.com/build/bKmt4RWN  
**Date:** 2024-08-20  
**Author:** Laudie (build attribution shown by the archive)  
**Verbatim passage:**

> “The more projectiles you can get, the more overlap you achieve with their mortars, resulting in better clear and damage output. With 10 projectiles per minion and up to 7 minions, you can potentially reach 70 overlapping projectiles, creating massive damage spikes!”

Conditions: this is another monster's mortar skill, Perfect Serpent Warriors, and the passage says “potentially”; it is not Forged Frostbearer and gives no isolated boss distance or measured count. It is corroborating evidence for the general mortar-overlap model.

### General area-overlap evidence: Blazing Salvo

**URL:** https://www.pathofexile.com/forum/view-thread/2934377  
**Date:** 2020-09-11  
**Author:** Bex_GGG, Grinding Gear Games  
**Verbatim passage:**

> “When targeting up close, the explosions can hit a target multiple times, while targeting at range causes them to spread out and have a higher explosion radius, giving you a wide damage spread.”

Conditions: Blazing Salvo, not Ice Mortar; the count varies with targeting distance and explosion radius. This is a general official mortar precedent, not a Frostbearer number.

### General area-overlap evidence: Magma Orb discussion

**URL:** https://www.pathofexile.com/forum/view-thread/1961549  
**Date:** 2017-10-08 (thread date shown by the forum search result; individual reply dates vary)  
**Author:** multiple forum participants; names vary by reply  
**Verbatim passages:**

> “Both. If a mob is within the area of effect of multiple hits, they'll take damage from all of them. It's different to the usual shotgunning rules because this is area damage, not damage caused by a projectile hitting the mob.”

and:

> “Magma orb will NOT shotgun with additional projectiles, like from GMP.”

The thread also contains a contrary practical report:

> “Area damage has always been able to overlap and Im not aware of any change to that behavior. Last league I played with Magma orb ... area damage from one salvo were definitely able to overlap. It was perfectly noticeable against bosses.”

Conditions and disagreement: the first statement distinguishes direct projectile hits from overlapping area damage; the second says extra projectiles from a GMP salvo do not shotgun; the final quoted player claims to have seen area overlap against bosses. This is about Magma Orb, not Ice Mortar, and the thread does not give a reproducible boss size/distance protocol.

### General projectile/area distinction: Explosive Arrow forum explanation

**URL:** https://www.pathofexile.com/forum/view-thread/1249629  
**Date:** 2015 (thread date in the forum archive; individual author/date not exposed in the retrieved extract)  
**Author:** forum participants; individual author not identified in the retrieved extract  
**Verbatim passage:**

> “All arrow skills are working as intended in the core game right now. This change basically only affects spells. So yes, if you stick 3 guys right next to each other with EA from LMP or extra arrows, they will take damage from all the explosions if they are close enough together. You can also just shoot a wall and the explosions will still overlap.”

Conditions: Explosive Arrow, not mortar; the targets must be close enough for the explosions to overlap. It is a general example of why the 2.0.0 direct-projectile rule does not imply that secondary area explosions are single-target capped.

### Syndicate Operatives: a contrary spectre precedent

**URL:** https://www.pathofexile.com/forum/view-thread/3186634  
**Date:** 2021-08-17 (3.15-era discussion; exact individual post dates vary)  
**Author:** forum participants discussing GGG's spectre fix  
**Verbatim passage:**

> “Certain projectile abilities used by Incursion Architects, Syndicate Operatives and bosses based on Lunaris have a bug that causes them to hit a target multiple times simultaneously when firing additional projectiles.”

and a player interpretation:

> “My understanding is this change completely removes the ability to shotgun, making GMP and Volley apply no benefit to single target.”

Conditions: this is specifically the Syndicate Operative/architect projectile bug, not a mortar explosion; it is important contrary evidence because it shows that not every spectre projectile can be assumed to overlap in single-target damage. It does not refute separately overlapping Ice Mortar impact areas.

### Summary of Question 3 evidence

The community PoB convention found is “set the projectile/spectre count to every projectile the author assumes can overlap”: 25 for five Frostbearers × five projectiles, 8 per Frostbearer in the 12L report, and 70 potential mortar projectiles for another spectre. These are modeled or potential counts, not measurements of a boss-size target. The general game evidence supports overlap of secondary area explosions while retaining the 2.0.0 ban on direct simultaneous projectile hits.

**What it says:** community PoB practice commonly assumes all mortar impact areas can overlap when AoE, projectile count, and positioning support it; no located source validates a universal five-of-five Ice Mortar count on an isolated boss, and spectre projectile behavior is skill-specific.

## Source count table

| Source | URL | Count on one boss | Condition attached by the source |
|---|---|---:|---|
| DeepLeg3917 Reddit reply | https://www.reddit.com/r/pathofexile/comments/12qn3ux/forged_frostbearer_dps/ | **5 per spectre modeled**; 25 for 5 spectres | Personal Volley-over-GMP test; PoB setting; no boss size or distance stated |
| XstraNinja Reddit thread | https://www.reddit.com/r/PathOfExileBuilds/comments/12ntso2/sire_of_shards_forged_frostbearer_spectres/ | Not stated | Sire of Shards + Greater Volley; “all projectiles straight forward”; T16 clear, not a boss count |
| Soulune Reddit build | https://www.reddit.com/r/PathOfExileBuilds/comments/12irzdo/my_spectre_leaguestarter_is_finally_endgame_ready/ | Not stated | Greater Volley described as more consistent than aGMP; Faster Projectiles overlap requires positioning |
| Corak_de forum guide | https://www.pathofexile.com/forum/view-thread/3583292 | Not stated; says overlapping AoEs can all damage one target | Requires increased projectile count and spectre AoE; no distance/size |
| Dyudan forum build | https://www.pathofexile.com/forum/view-thread/3555198 | **8 per spectre stated** | 8 spectres × 8 projectiles per cast; “shotgun” is not mechanically disambiguated |
| lllolll15 forum build | https://www.pathofexile.com/forum/view-thread/3521991 | **8 per spectre stated**; **104 total stated** | High-investment PoB/build calculation; no boss distance/size |
| Doominated Reddit/PoB report | https://www.reddit.com/r/PathOfExileBuilds/comments/1eeorcf/325_forged_frostbearers_spectres_low_budget_pob/ | **5 per spectre modeled**; 25 for 5 spectres | Explicit PoB simulation; Void Sphere compacts mob packs |
| Helm Breaker Maxroll 3.29 guide | https://maxroll.gg/poe/build-guides/forged-frostbearer-spectre-necromancer-league-starter | Not stated | Greater Volley; says projectile overlap/shotgunning; no numeric boss count |
| GGG Blazing Salvo announcement | https://www.pathofexile.com/forum/view-thread/2934377 | “Multiple” (no number) | Up close explosions can hit a target multiple times; range spreads mortars and increases radius |
| GGG 2.0.0 patch notes | https://www.pathofexile.com/forum/view-thread/1304441 | **1 direct simultaneous projectile** | Same source and simultaneously created; secondary areas are not addressed in this sentence |
| PoE forum projectile rule explanation | https://www.pathofexile.com/forum/view-thread/3117972 | No number; overlapping areas can all contribute | Requires projectile AoE overlap; otherwise no multiple hit |
| Perfect Serpent Warrior mortar archive | https://pobarchives.com/build/bKmt4RWN | **10 per minion potential**; 70 for 7 minions | Other mortar spectre; “potentially”; no isolated boss measurement |

## Bottom line of the evidence

The evidence supports modeling Ice Mortar as a projectile-created area explosion: Greater Volley supplies four additional parallel-lane mortars, and overlapping impact areas can all damage a target. It does **not** support claiming that a particular boss always receives exactly five explosions without specifying distance, target hitbox, projectile travel/impact placement, and the build's AoE. The strongest directly relevant player/PoB evidence found uses **five per Frostbearer as a simulation assumption**, while the strongest general official evidence says mortar explosions can hit multiple times up close and spread at range.