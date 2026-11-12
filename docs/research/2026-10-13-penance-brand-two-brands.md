# Penance Brand: Two Brands on One Enemy

**Scope.** Regular **Penance Brand**, not Penance Brand of Dissipation or Conduction. Research performed 2026-10-13. I searched the requested wiki pages first: [Penance Brand](https://www.poewiki.net/wiki/Penance_Brand), [Brand](https://www.poewiki.net/wiki/Brand), [Runebinder](https://www.poewiki.net/wiki/Runebinder), and [Brand attachment](https://www.poewiki.net/wiki/Brand_attachment). The wiki's live pages/API were protected by Anubis/Cloudflare during direct retrieval, but live search indexed the current Penance Brand mechanics text. Official forum and patch-note pages were opened directly.

The most relevant official post-change correction is [3.23.1 Patch Notes](https://www.pathofexile.com/forum/view-thread/3480999): GGG fixed a bug in Penance Brand's check of energy on the branded enemy. This means December 2023 player testing of the launch bug is useful as a historical conflict, but should not be treated as the current rule.

## 1. Shared energy, explosion rate, and which brand is removed

### Current wiki

**Source:** [PoE Wiki, “Penance Brand”](https://www.poewiki.net/wiki/Penance_Brand)  
**Date:** 2026-07-26, indexed publication/update date  
**Author:** PoE Wiki contributors; no individual author shown  
**Conditions:** Regular Penance Brand; each brand is attached to the *same enemy* at the same time through an attachment-limit exception such as Runebinder. Each brand activates normally. This does not describe Penance Brand of Dissipation.

> “Penance Brand adds a stack of Energy to the enemy it is attached to each time the brand activates, up to a cap of 20 Energy. Energy is simply a counter on the enemy and not a debuff. When the enemy reaches 20 Energy, the earliest attached Penance Brand will be destroyed and cause an explosion on the target. Immediately after this explosion occurs, Energy is reset to 0, and any other attached Penance Brands will begin to add Energy again.”

> “If multiple Penance Brands are attached to an enemy simultaneously (via Runebinder), each brand will independently add Energy stacks towards the shared 20 Energy cap, accelerating the rate at which the cap is reached. However, only one brand will explode on reaching 20 Energy.”

### Official basis for two simultaneous attachments

**Source:** [GGG, “All Notables and Keystones in Path of Exile: Harvest”](https://www.pathofexile.com/forum/view-thread/2873767)  
**Date:** 2020-06-16  
**Author:** Grinding Gear Games  
**Conditions:** Runebinder allocated; it changes only the number of Brands allowed to attach to one enemy. It does not state a special Penance Brand explosion rule.

> “You can have an additional Brand Attached to an Enemy”

### Official skill lifecycle

**Source:** [GGG, “Content Update 3.23.0 -- Path of Exile: Affliction”](https://www.pathofexile.com/forum/view-thread/3451455)  
**Date:** 2023-11-30  
**Author:** Grinding Gear Games  
**Conditions:** Regular Penance Brand after the 3.23 rework; attached to an enemy; maximum energy reached.

> “It now immediately causes an explosion when the branded enemy reaches maximum energy.”

> “It no longer has an attached duration — instead, it remains attached to the enemy until it reaches maximum energy, then expires immediately once the explosion occurs.”

> “activates every 0.1s while attached”

### Official post-launch bug fix

**Source:** [GGG, “3.23.1 Patch Notes”](https://www.pathofexile.com/forum/view-thread/3480999)  
**Date:** 2024-01-16  
**Author:** Kieren_GGG, Grinding Gear Games  
**Conditions:** Applies to Penance Brand's calculation of energy on its branded enemy. GGG does not disclose the implementation or exact formerly incorrect edge case.

> “Fixed a bug where Penance Brand could get the wrong result when checking the amount of energy on the branded enemy.”

### Historical disagreement: launch-period player test

**Source:** [Path of Exile Bug Reports, “Penance Brand of Dissipation and Runebinder has weird interation”](https://www.pathofexile.com/forum/view-thread/3454612)  
**Date:** 2023-12-10  
**Author:** yazuka#2910, player report  
**Conditions:** Reported launch state before 3.23.1; the author tested both base Penance Brand and Dissipation with Runebinder. This is not a GGG confirmation, and the relevant energy-check bug was subsequently fixed.

> “Base Gem: Applying 2 brands to the same target builds energy from both simultaneously and triggers the first brand when the sum of the two is equal to 20, but only counts the energy on the first brand.”

> “This results in a tiny explosion ... and the removal of the first brand.”

GGG acknowledged the report without defining the intended rule:

**Source:** same thread  
**Date:** 2023-12-12  
**Author:** Jatin_GGG, Grinding Gear Games  
**Conditions:** Acknowledgement of the report, not a mechanics ruling.

> “Thanks for your report, I'll pass this on.”

**What it says:** Two regular Penance Brands on one enemy add to one 20-energy enemy counter, so two equal-rate brands reach 20 in about half the one-brand charging time, but produce **one** explosion, not two. The wiki says that the earliest attached Brand is removed; the other stays attached, energy resets to zero, and it begins the next charge. Thus two brands do **not** double explosion frequency or sustain two hits per cap; they make the single-cap cycle charge twice as fast while two are attached.

## 2. Recast requirement, time cost, and permanent attachment

### Official lifecycle: attached brand is consumed at the explosion

**Source:** [GGG, “Content Update 3.23.0 -- Path of Exile: Affliction”](https://www.pathofexile.com/forum/view-thread/3451455)  
**Date:** 2023-11-30  
**Author:** Grinding Gear Games  
**Conditions:** Regular Penance Brand attached to an enemy after 3.23; it reaches maximum energy.

> “It now immediately causes an explosion when the branded enemy reaches maximum energy.”

> “It no longer has an attached duration — instead, it remains attached to the enemy until it reaches maximum energy, then expires immediately once the explosion occurs.”

### Current gem data

**Source:** [PoE Wiki, “Penance Brand”](https://www.poewiki.net/wiki/Penance_Brand)  
**Date:** 2026-07-26, indexed publication/update date  
**Author:** PoE Wiki contributors; no individual author shown  
**Conditions:** Regular Penance Brand's current unmodified base values. Increases/reductions to cast speed alter both its casting rate and its activation frequency, as stated by the gem.

> “Cast Time: 0.75 sec”

> “Activates every 0.1 seconds while Attached”

> “Increases and Reductions to Cast Speed also apply to this Skill's Activation frequency”

### Community explanation that attached Penance does not expire naturally

**Source:** [Path of Exile Bug Reports, “Penance brand does not work with ‘Recover 10% of Mana when a Brand expires while Attached’”](https://www.pathofexile.com/forum/view-thread/3453533)  
**Date:** 2023-12-12  
**Author:** MonaHuna#6449, player  
**Conditions:** Regular Penance Brand after the 3.23 rework; distinguishes “removed after explosion” from “expires while attached.” This is consistent with the official 3.23 lifecycle text but is not a staff answer.

> “Penance Brand is removed after explosion, not expired. It can expire only while detached.”

### Current community treatment of replacement casts

**Source:** [Path of Exile Gameplay Help, “Penance Brand of Dissipation Question”](https://www.pathofexile.com/forum/view-thread/3818718)  
**Date:** 2025-07-26  
**Author:** Jadian#0111, player  
**Conditions:** The explicit detailed answer uses Penance Brand of Dissipation for its ramp example, so it is not direct evidence for the regular gem's explosion timer. Its statements about brand attachment slots and replacement casts are general Brand mechanics. The player assumes Runebinder and a source of extra maximum Brands.

> “Generally, you don't have to be constantly pressing it. In a bossing situation, with Runebinder and some source of extra Brands, you can place two Brands which attach immediately, and two more which will attach when the first two expire. At that point, you only have to replace the detached ones to maintain uptime on the Brands.”

> “Brands to not last forever, even if they do not attach to an enemy. If you cast a Brand with no enemies are around, it will expire after lasting for its Detached Duration.”

### Timing implication

At base values, one regular Penance Brand needs 20 activations at 0.1 seconds each: about **2.0 seconds from attachment to explosion**. The gem's base cast time is **0.75 seconds**, so one replacement cast is roughly **37.5%** of the one-brand base charge time, before cast-speed modifiers and attachment travel/ticks.

With two equal-rate attached brands, the shared counter receives two energy per 0.1 seconds, so it reaches 20 in about **1.0 second**. One base replacement cast is therefore about **75%** of that dual-attached charge window. The 0.75-second cast-time and 0.1-second activation interval are base gem values; cast speed modifies both, so this comparison remains ratio-like under ordinary increased/reduced cast-speed scaling. It is not a claim that every cast attaches instantly or that server ticks add no timing variance.

**What it says:** The exploded Brand is gone. To restore two attached Brands after the first explosion, the player must eventually supply another Brand, either by recasting or by having an already-cast unattached Brand that can attach. Regular Penance Brand is not permanently attached: the official 3.23 description explicitly makes the explosion terminate its attached lifetime. At base values, a normal cast takes 0.75 seconds versus about 2.0 seconds to one-brand explosion or about 1.0 second to the shared-cap explosion while two equal-rate Brands are attached.

## 3. Spacing, attachment order, and same-moment attachment

### Current wiki: removal order and reset

**Source:** [PoE Wiki, “Penance Brand”](https://www.poewiki.net/wiki/Penance_Brand)  
**Date:** 2026-07-26, indexed publication/update date  
**Author:** PoE Wiki contributors; no individual author shown  
**Conditions:** Regular Penance Brand; multiple Brands remain attached to one enemy after the first reaches the shared cap.

> “When the enemy reaches 20 Energy, the earliest attached Penance Brand will be destroyed and cause an explosion on the target.”

> “Immediately after this explosion occurs, Energy is reset to 0, and any other attached Penance Brands will begin to add Energy again.”

### Player question expressly identifying the simultaneous/server-tick ambiguity

**Source:** [Path of Exile Gameplay Help, “GGG, Penance Brand clarifications?”](https://www.pathofexile.com/forum/view-thread/3452269)  
**Date:** 2023-12-05  
**Author:** inori92#4444, player  
**Conditions:** Two Brands generated by Remarkable and attached to one target. The author specifically distinguishes exact simultaneity from attachment on adjacent server ticks. This is a question, not evidence of a rule.

> “They will both attach (either simultaenously or after the other in server ticks), generate to 20 energy stacks then boom.”

> “Does one ALWAYS boom before the other ... or does both brands attached check for 20 energy and explode on the next available server tick after, causing 2x damage?”

A later player reply gives the shared-rate reading:

**Source:** same thread  
**Date:** 2023-12-06  
**Author:** Draegnarrr#2823, player  
**Conditions:** Two attached Brands; no authoritative source attached.

> “It will be double charge speed to 10”

### Historical, now-superseded player observation

**Source:** [Path of Exile Bug Reports, “Penance Brand of Dissipation and Runebinder has weird interation”](https://www.pathofexile.com/forum/view-thread/3454612)  
**Date:** 2023-12-10  
**Author:** yazuka#2910, player  
**Conditions:** Launch-period base Penance Brand, two brands on one target, prior to the 3.23.1 bug fix for checking enemy energy.

> “Applying 2 brands to the same target builds energy from both simultaneously and triggers the first brand when the sum of the two is equal to 20”

This must be read alongside GGG's later correction:

**Source:** [GGG, “3.23.1 Patch Notes”](https://www.pathofexile.com/forum/view-thread/3480999)  
**Date:** 2024-01-16  
**Author:** Kieren_GGG, Grinding Gear Games  
**Conditions:** Penance Brand energy check generally; patch notes do not identify whether the bug was this exact Runebinder race/order observation.

> “Fixed a bug where Penance Brand could get the wrong result when checking the amount of energy on the branded enemy.”

### Finding for exact same-timestamp behavior

**Not found:** I found no GGG post, patch note, or current wiki passage that states a deterministic tie-breaker when two regular Penance Brands receive *exactly the same attachment timestamp*. I searched the requested wiki pages, `site:pathofexile.com/forum Penance Brand earliest attached energy`, `site:pathofexile.com/forum Penance Brand Runebinder both explode`, `Penance Brand simultaneous server ticks`, and the 3.23/3.23.1 patch notes.

The current wiki resolves the ordinary case by saying “earliest attached,” but does not say how a true timestamp tie is broken. The official sources say the skill is removed at maximum energy, and the wiki says only one Brand explodes; neither publishes a same-tick ordering algorithm.

**What it says:** Explosion timing follows attachment state, not an even alternating schedule. With equal activation rates, two simultaneously active Brands fill the same 20-energy counter together; the first/earliest attached Brand is the one removed, the counter resets, and the survivor starts the next charge from zero. If the Brands were attached at different times, the documented earliest-attached rule determines which goes first. If they were attached at exactly the same moment, the sources establish one explosion rather than two but do not document a deterministic visible tie-break rule.