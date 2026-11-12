# Tinctures and Mana Burn: source report

*Sources are quoted verbatim. Dates and authors are given as displayed by the source or its search result; PoEDB and some wiki pages do not display an individual author or publication date. The mechanic changed after Affliction: official 3.23 descriptions are distinguished below from official 3.25 changes and current item data.*

## 1. Activation, Mana Burn, deactivation, and cooldown

### Sources

- **Official GGG, 3.23 Affliction content reveal** — [Path of Exile: Affliction](https://www.youtube.com/watch?v=pE2D4bgTeIQ), **November 2023** (reveal; uploader/author: **Path of Exile**).  
  > “A Warden of the Maji can learn to use tinctures which coat their weapon, granting various powerful effects. You can equip Tinctures in your flask slots and toggle them on and off at will. You can only have one enabled at a time”  
  **Conditions:** The reveal describes Warden of the Maji Tinctures, equipped in flask slots; only one can be enabled at once.

- **Official GGG, 3.25.0 patch notes** — [Content Update 3.25.0 -- Path of Exile: Settlers of Kalguur](https://www.pathofexile.com/forum/view-thread/3531661), **July 18, 2024**, **Grinding Gear Games**.  
  > “While a Tincture is active it grants you a powerful buff to your melee attacks, but inflicts Mana Burn on you, draining your mana at an increasing rate the longer the Tincture has been active. The Tincture can be manually deactivated, or will automatically deactivate when you run out of mana.”  
  > “You inherently only have one Tincture active at a time. Tinctures also have a cooldown, so once you have deactivated one, no Tincture can be activated for a time.”  
  **Conditions:** These are the post-Affliction core-game rules introduced in 3.25. The same notes add the mastery “Tinctures deactivate when you have 12 or more Mana Burn,” so builds with that mastery can deactivate before reaching zero mana.

- **PoE Wiki, Tincture page** — [Tincture](https://www.poewiki.net/wiki/Tincture), latest edit shown as **March 11, 2026**, page author **not identified on the article** (creator shown on the info page: Blvcksvn).  
  > “Mana Burn causes you to lose 1% of your maximum Mana per stack per second.”  
  > “Can be deactivated manually, or will automatically deactivate when you reach 0 Mana.”  
  **Conditions:** This describes the ordinary Mana Burn wording. For *N* stacks, the quoted rule is *N* × 1% of maximum mana per second; reduced Mana Burn rate changes how quickly stacks are applied, not the quoted per-stack drain.

- **PoE Wiki, Tincture page**, same page/date/author details as above.  
  > “Inflicts Mana Burn every 0.70 Seconds”  
  **Conditions:** 0.70 seconds is the listed interval for a Prismatic Tincture, not a universal interval for every base. For example, the page’s Oakbranch entry says 0.50 seconds and its Ironwood entry says 0.90 seconds.

- **PoEDB** — [Tinctures](https://poedb.tw/us/Tinctures), **date not displayed**, author **not displayed**.  
  > “Inflicts Mana Burn every 0.70 Seconds”  
  > “8 Second Cooldown when Deactivated”  
  **Conditions:** This is the Prismatic base. PoEDB lists different intervals and cooldowns by base: e.g. Oakbranch 0.50 seconds/8 seconds; Ironwood 0.90 seconds/10 seconds; Ashbark and Borealwood 0.60 seconds/7 seconds; Poisonberry and Blood Sap 0.70 seconds/6 seconds.

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “(15—17)% reduced Mana Burn rate”  
  > “(24—26)% reduced Mana Burn rate”  
  > “35% increased effect  
  > (47—51)% increased Mana Burn rate”  
  **Conditions:** PoEDB identifies these as **prefixes**. Increased/reduced Mana Burn rate modifies the rate stacks are inflicted; one prefix trades increased Tincture effect for increased burn rate.

- **Path of Exile forum, player question and reply** — [Does the Manaburn debuff ever drop?](https://www.pathofexile.com/forum/view-thread/3533201), **July 26, 2024**; question by **raV#3445**, answer by **MonaHuna#6449**.  
  > “No, while a tincture is active, it stacks mana burn.”  
  **Conditions:** This answers whether the stacks expire on their own while the Tincture stays active: the reply says they do not.

- **Reddit, r/pathofexile** — [Tincture Theorycrafting - durations/uptime/etc.](https://www.reddit.com/r/pathofexile/comments/1e7hjdl/tincture_theorycrafting_durationsuptimeetc/), **July 2024** (search result gives no exact post date), **u/xLapsed**.  
  > “The description says that they mana burn every 0.7 seconds, with each stack draining 1% more mana. After they expire, there is an 8sec cooldown to reactivate.”  
  **Conditions:** This is a player’s generalization using a 0.7-second example. PoEDB and the wiki show that base intervals and cooldowns vary; the per-stack drain is 1% of *maximum* mana, not 1% of current mana.

### What it says

Mana Burn stacks while the Tincture is active; each stack drains 1% of maximum mana per second. The application interval and cooldown depend on the base and modifiers. A player can deactivate manually, ordinary Tinctures also deactivate at zero mana, and the 3.25 mastery can deactivate them at 12 stacks.

## 2. Which skills receive Tincture effects

### Sources

- **PoEDB, Tinctures** — [Tinctures](https://poedb.tw/us/Tinctures), **date and author not displayed**.  
  > “Tincture effects only apply to hits with weapons. Unarmed skills, shield skills, and non-attack hits like spells are unable to benefit from tincture effects.”  
  **Conditions:** The page further clarifies the effects apply to attacks using the player’s weapon, including qualifying remote weapon skills. It says effects apply to either weapon while dual wielding, but not to minions using the weapon.

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “Seasoned Hunter”  
  > “Tincture Effects also apply to Ranged Weapons”  
  **Conditions:** Seasoned Hunter is a **Warden of the Maji** ascendancy notable. Its wording extends effects to ranged weapons; this is not a general property of Tinctures.

- **Official GGG, 3.25.0 patch notes** — [Content Update 3.25.0](https://www.pathofexile.com/forum/view-thread/3531661), **July 18, 2024**, **Grinding Gear Games**.  
  > “A new Bloodsoaked Blade Keystone Passive Skill … causes Tinctures to inflict Weeping Wounds instead of Mana Burn, draining your life instead of your mana.”  
  **Conditions:** This changes the resource/debuff, not which weapon attacks can receive Tincture effects.

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “The Battle Within Oakbranch Tincture”  
  > “Does not inflict Mana Burn over time”  
  > “Inflicts 1 Mana Burn on you when you Hit an Enemy with a Melee Weapon”  
  **Conditions:** This unique Tincture replaces periodic Mana Burn with hit-triggered stacks. Its listed trigger specifically says **Melee Weapon**.

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “Melee Weapon Damage Penetrates 1% Elemental Resistances per Mana Burn, up to a maximum of 200%”  
  **Conditions:** This is the Sap of the Seasons unique Prismatic Tincture effect; it scales with Mana Burn stacks and has a 200% cap in current PoEDB data.

- **Reddit, r/pathofexile** — [Tincture mods from datamining](https://www.reddit.com/r/pathofexile/comments/1ecgc3d/tincture_mods_from_datamining/), **July 26, 2024**, **u/Keldonv7** (date/author shown in search result).  
  > “Does not inflict Mana Burn over time”  
  > “Inflicts Mana Burn on you when you Hit an Enemy with a Melee Weapon”  
  **Conditions:** The thread discusses datamined Tincture mods; the quoted lines correspond to the unusual hit-triggered unique mechanic rather than normal periodic stacking.

### What it says

By default, Tincture effects apply to weapon attacks, including melee weapon attacks, not spells, unarmed attacks, or shield skills. Warden’s **Seasoned Hunter** extends them to ranged weapons. **The Battle Within** changes periodic Mana Burn to hit-triggered Mana Burn; **Bloodsoaked Blade** changes Mana Burn into life-draining Weeping Wounds.

## 3. How players use Tinctures, uptime, and mana recovery

### Sources

- **Reddit, r/PathOfExileBuilds** — [Trickster CI Ephemeral Edge: what feels good on moderate…](https://www.reddit.com/r/PathOfExileBuilds/comments/1ekq9kt/trickster_ci_ephemeral_edge_what_feels_good_on/), **August 2024** (search result date: October 6, 2024, likely recrawl date), **u/dyfrgi**.  
  > “There's no way to search for this on poe.ninja yet, but it looks like about 90% of Splitting Steel players are using a Prismatic Tincture, usually rolled with reduced mana burn and melee weapon attack speed.”  
  > “The builds tend to get a good amount of mana leech/onhit, way more than they need - e.g. one I sampled uses 116 mana/second to attack between leech and regen recovers 369/second.”  
  > “With 1334 mana, each stack is 13 mana (I think? How does this round?), so the extra lets you sustain up to 19 stacks. With the reduced mana burn prefix, it's about 1 stack/0.94 seconds or 18 seconds to reach 19 stacks. With an 8 second cooldown, that's an average uptime of about 70%. It's a little better than that in practice since you'd only turn it on when you have a DPS window on a big enemy, though.”  
  **Conditions:** The author describes a sampled Splitting Steel build, with 1334 maximum mana and a reduced-burn prefix. The 116 mana/s is attack cost, 369 mana/s is recovery from leech plus regeneration; the 18 seconds and ~70% uptime are the author’s estimate for those assumptions.

- **Reddit, r/PathOfExileBuilds** — [Mana Recoup will combo well with Tinctures and Trauma/Echoes of Creation](https://www.reddit.com/r/PathOfExileBuilds/comments/1echldo/mana_recoup_will_combo_well_with_tinctures_and/), **July 26, 2024**, **u/Razekal**.  
  > “In my DS of Ambi build that swings 6x times a second with Blitz stacks, I generate 380 mana per second from recoup at about 3/4ths my sustainable trauma just from a single 6% mana recoup mod from a Syndicate mod. That much mana recovery sustains 54 stacks of mana burn, or 32 seconds.”  
  > “if I cut that and lower trauma down to 17 stacks (60% of max sustainable trauma) I still generate 200 mana per second which covers 30 mana burn or 18 seconds of uptime.”  
  **Conditions:** These are the author’s Double Strike of Ambidexterity/Berserker calculations at the stated attack rate and Trauma levels, with 6% mana recoup. This is not a universal Tincture uptime figure.

- **Reddit, r/PathOfExileBuilds** — [The Quest for 500M DPS - A Cyclone Story](https://www.reddit.com/r/PathOfExileBuilds/comments/1pcfuer/the_quest_for_500m_dps_a_cyclone_story/), **December 2025**, **u/TheRealDoomWagon**.  
  > “What happens with the tincture during invulnerability phases? You have 14 unreservered mana so it takes only 0.6s until your passive mana regen can't keep up with the mana burns and you are fully reliant on mana leech. If you can't leech for a second it goes on CD for 8 seconds.”  
  **Conditions:** This is a commenter’s build-specific calculation with only 14 unreserved mana; when the boss cannot be leeched from during an invulnerability phase, the commenter says the Tincture reaches cooldown quickly. It illustrates that leech availability matters as well as nominal mana recovery.

- **Reddit, r/PathOfExileBuilds** — [Tinctures on a non warden](https://www.reddit.com/r/PathOfExileBuilds/comments/1oqh1in/tinctures_on_a_non_warden/), **November 6, 2025**, **u/Bitchenmuffins** (author/date shown in search result).  
  > “One tincture is used on most attack melee builds afaik. Its not an uptime type button. Its a burst button. With your run of the mill low attack cost, mana leech build you get like 5-15 seconds (never checked, just by feel) of burst.”  
  **Conditions:** The author explicitly labels 5–15 seconds an unchecked, feel-based estimate for a typical low-attack-cost melee leech build; it is not measured data or a guaranteed duration.

- **Reddit, r/PathOfExileBuilds** — [PoE 3.25 Eviscerate Ignite Elementalist – Energy Blade Edition](https://www.reddit.com/r/PathOfExileBuilds/comments/1gytwcr/poe_325_eviscerate_ignite_elementalist_energy/), **November 24, 2024**, **u/kuro009**.  
  > “The Tincture is only for tough enemies. We don't constantly spam it. It has roughly 4 seconds duration before it get deactivated and goes into cooldown. But the Ignite we create when the tincture is activate do not drop in DPS once the tincture is deactivated.”  
  **Conditions:** This is an Ignite build’s author-described setup and approximate duration. The reported continued Ignite damage is the build-specific reason the Tincture’s deactivation does not immediately end its damage contribution.

- **Reddit, r/PathOfExileBuilds** — [Warden with tinctures and you: Could they be worth it?](https://www.reddit.com/r/PathOfExileBuilds/comments/1e9ea0i/warden_with_tinctures_and_you_could_they_be_worth/), **July 2024** (search result recrawled October 6, 2024), **u/Keyenn**.  
  > “My build needs 26 mana (with 670 max mana) per 10 sec in order to sustain tinctures.”  
  > “Enduring suffision makes it so tinctures linger for 0.5s per manaburn when disabled to a maximum of 6s, so when the tincture is automatically removed due to the mastery, I get 6s effect still, enough to reach the next CD.”  
  **Conditions:** This is a Warden setup using the first-six-stacks mastery, the 12-stack deactivation mastery, and Enduring Suffusion. The 26 mana/10s claim is for the author’s stated 670 maximum mana and setup; linger has a six-second maximum.

### Mana reservation and recovery caveat

The drain rule quoted above is based on **maximum mana**, but Tincture deactivation is described as occurring when the character runs out of mana. Reservation therefore affects the mana available as a buffer for costs and drain; it does not change the quoted “1% of maximum Mana per stack per second” amount. The player examples show why recovery sources matter: leech can sustain stacks while hitting, recoup can continue recovery in the stated Trauma setup, and an invulnerable or otherwise unleechable target can sharply shorten uptime. The Reddit examples do not establish a single typical duration.

### What it says

Players describe both short, manually timed boss bursts and longer uptime when leech, regeneration, or recoup can cover the stack drain. Reported durations range from about 4 seconds in one build, to an explicitly unmeasured 5–15-second estimate, to 18–32 seconds in builds with the stated recovery. Mana reservation, attack costs, and whether the target can be leeched from change those results.

## 4. Tincture implicit and explicit mod pools

### Sources

- **PoEDB, Tinctures** — [Tinctures](https://poedb.tw/us/Tinctures), **date and author not displayed**.  
  > “Prismatic Tincture”  
  > “(70—100)% increased Elemental Damage with Melee Weapons”  
  **Conditions:** This is the Prismatic base’s implicit modifier, displayed separately from the randomized prefix/suffix mod pool.

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “Rosethorn Tincture”  
  > “(100—150)% increased Critical Strike Chance with Melee Weapons”  
  **Conditions:** This is the Rosethorn base’s implicit.

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “Oakbranch Tincture”  
  > “Gain 3 Rage on Melee Weapon Hit”  
  **Conditions:** This is the Oakbranch base’s implicit; its base entry also lists “Inflicts Mana Burn every 0.50 Seconds” and “8 Second Cooldown when Deactivated.”

- **PoEDB, Tinctures**, same URL/date/author details.  
  > “Herbal … Prefix … (11—13)% increased effect”  
  > “Persevering … Prefix … (24—26)% reduced Mana Burn rate”  
  > “of Overpowering … Suffix … Melee Weapon Damage Penetrates (17—19)% Elemental Resistances”  
  > “of Mastery … Suffix … (25—29)% increased Melee Weapon Attack Speed”  
  **Conditions:** These are examples from the listed explicit mod pool. Prefixes also include increased cooldown recovery rate and prefixes trading effect for Mana Burn rate; suffixes include damage over time multiplier, critical strike multiplier, damage against low-life enemies, and other utility mods.

- **PoE Wiki, Prismatic Tincture** — [Prismatic Tincture](https://www.poewiki.net/wiki/Prismatic_Tincture), **page search result dated July 31, 2024**, author **not identified on the article**.  
  > “(70-100)% increased Elemental Damage with Melee Weapons”  
  **Conditions:** This is the base implicit. The same page displays the standard Prismatic interval and cooldown, as well as the later Sap of the Seasons unique’s additional modifiers.

- **Reddit, r/PathOfExileBuilds** — [Trickster CI Ephemeral Edge: what feels good on moderate…](https://www.reddit.com/r/PathOfExileBuilds/comments/1ekq9kt/trickster_ci_ephemeral_edge_what_feels_good_on/), **August 2024** (search result recrawled October 6, 2024), **u/dyfrgi**.  
  > “about 90% of Splitting Steel players are using a Prismatic Tincture, usually rolled with reduced mana burn and melee weapon attack speed.”  
  **Conditions:** The author characterizes this as an estimate from inspecting builds, not a comprehensive measured sample.

**PoEDB count caveat:** PoEDB lists the explicit modifier pool by **Prefix** and **Suffix** categories, and shows a Magic Tincture setup commonly with one prefix and one suffix. The displayed mod pool is much larger than those two affix slots; a normal Magic item does not carry every listed pool entry at once. The base implicit is separate from those explicit affixes.

### What it says

Tincture bases have a base-specific implicit, while their explicit pool has prefix and suffix mods. PoEDB’s useful examples include increased effect and reduced Mana Burn rate prefixes, and damage, penetration, attack speed, and critical multiplier suffixes.