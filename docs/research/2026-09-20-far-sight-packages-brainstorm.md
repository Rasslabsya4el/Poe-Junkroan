# Far sight over packages: a brainstorm with the owner (2026-09-20). A frame for the loadout work, not a spec.

## The owner's concern (kept in his terms)

Min-maxing in Path of Exile is not "add or remove one thing at a time": it is trying BUNDLES. The system today thinks in one
kind of bundle only (a unique + some nodes), and only because the owner once named attribute stackers. He does not want special
cases. His examples, none of which a "per X" keyword parse finds:

- **Mageblood**: the strongest belt, worth exactly nothing without magic utility flasks built for it.
- **Darkness Enthroned**: a belt that is two abyss sockets + "increased effect of socketed abyss jewels"; alone it gives zero and
  a screen that ranks items alone culls it. The package = generate two abyss jewels (each base has its own mods). NOT an
  uber-endgame item.
- **Voices**: a cluster jewel whose package is "re-do the tree, generate medium / small clusters".
- **The Adorned** build version: the jewel + many magic corrupted jewels + a tree rebuilt around jewel sockets.
- **Attribute stackers**: never ONE unique; one unique + a changed tree only shows potential and loses to the finished build.
- Radius jewels (Thread of Hope, timeless, Impossible Escape, Split Personality) that reshape the tree, and their crossings.

"Complexity grows exponentially with every loadout, and I do not see how it is solved without dumb brute force."

Also his verdict for DAY 1: little randomness is the goal, so what is strong on gear (accuracy) may well come from the tree there --
it makes day-1 PoBs deterministic and comfortable. The tree-versus-gear question (below) matters for LATER loadouts.

## The frame the lead proposed

1. **An enabler is never evaluated alone.** A human does "equip Mageblood -> redo the flasks -> compare": he knows WHICH SUBSYSTEM
   the item touches. That knowledge is needed at the level of mechanism TYPES (about five), derived from PoB's parsed mods:

   | enabler type | examples | what is re-optimized |
   |---|---|---|
   | scales with a variable | stackers, per charge, per minion | the producers of that variable |
   | changes the effect / uptime of a class of objects | Mageblood (flasks), Darkness Enthroned (abyss jewels), The Adorned (magic jewels) | the objects of that class |
   | opens slots | abyss sockets, Voices (cluster sockets), extra jewel / gem sockets | what fills the slots |
   | changes the tree's allocation rules | Thread of Hope, Intuitive Leap, Impossible Escape, timeless jewels | the tree around it |
   | changes a skill's rules | keystones | links, gear |

   The edges "consumes <-> produces / belongs to class" come from PoB's mod data (PerStat / Multiplier variables, named
   modifiers, item properties) + a SMALL machine-readable table "modifier name -> object class" (30-50 rows, `mechanics/` style).
2. **An optimistic bound before anything expensive** (branch and bound): ONE PoB what-if of the enabler together with an
   IDEALIZED stand-in for what it enables -- Mageblood + four ideal flasks from the mod ladders; Darkness Enthroned + two ideal
   abyss jewels; a stacker item + a temporary "+300 Strength"; Thread of Hope + every strong notable in the ring (the fast what-if
   needs no connectivity, so all sockets x all ring sizes cost seconds). Below the current build even when idealized = dead, known
   in milliseconds. Above = worth a real branch.
3. **Inside a branch plain greed works again.** The hard step is the first: with 800 Strength in the branch every further
   "per Strength" item shows a large value ALONE; with The Adorned equipped every jewel socket becomes expensive and the tree
   reshapes itself toward sockets. So "a package of many uniques" is a seed + ordinary growth. Branches (skeleton variants)
   compete at the end, as variants do today.
4. **A fidelity ladder**: bound (ms) -> a quick conditional fill of the branch (a minute or two) -> the full optimization
   (tens of minutes). Cost ~ (#enablers x cheap bound) + (a dozen branches x full build), not exponential.

## What does not exist yet (the loadout work proper)

Per-class optimizers (flasks; rare / magic / abyss jewels; cluster jewels), the dependency graph from PoB's mods (first fix
`scripts/build_scaling_vectors.py:129`, which truncates provider lists to 50), the bound recipes per enabler type, the ladder.

## Honest limits

Pairs of enablers that fail even the optimistic bound one by one (crossed radius jewels): only pairs the graph links through a
shared variable are affordable (thousands, not hundreds of thousands). Three-link chains and mechanics PoB does not compute: not
found by the machine -- LLM hypotheses and the owner's knowledge propose, PoB judges (the architecture's original split).
Timeless jewels: a table search over seeds against the build's scaling vector, PoB verifies the top seeds -- a subsystem of its
own. Bounds may be too generous: calibrate "promised vs delivered" on the evaluation rows we already log.

## The tree-versus-gear exchange (same family: a cross-surface package)

Inside one surface the system compares exactly (node vs node, line vs line); ACROSS surfaces only through order. A floor (hit
chance 95%, resistances, attributes) is paid by whichever surface met it first; afterwards no single-surface move can undo it
(the item line has no value because the floor is met; the nodes cannot leave because the floor would break). Only movement
speed is withheld from tree stages today. Measured prices: an open line on armour / jewellery ~1-2% of value, a tree point ~2-3%,
an accuracy cluster 3-4 points. Plan for later loadouts: (1) measure on delivered builds how many points sit on floor-only
nodes and what PoB gives for the transfer; (2) a "floor transfer" move = one package what-if (item line on the cheapest slot +
those nodes removed + the points re-spent), both directions; (3) a table in the build description: "hit chance 95%: paid by 4
tree points (-7%); gear would pay it for -1.5%".

## Addendum (same day): is it case-by-case work, and can raw compute find multi-link bundles?

The owner's two follow-ups: (1) "so every item's kickstart has to be worked out case by case?" (2) "three or more unremarkable
pieces from different surfaces (a gem + an affix + a mastery / a timeless-only node) that enable each other only together:
impossible to compute, only hard-coded knowledge? Would 'dig this build for a week' find it? What about combining everything in
the game on a universal stand for a month of compute?"

1. **Not per item: per GATE TYPE.** A piece worth nothing alone is almost always behind a gate -- a condition, a variable
   ("per X"), a threshold, a slot, a flag -- and PoB's parser already wrote those gates down for every unique, node and gem in
   its tag language (Condition, ActorCondition, Multiplier, MultiplierThreshold, PerStat, StatThreshold, SkillType, SlotName,
   ...): ten years of the PoB authors' per-item labour, inherited. The kickstart is one generic recipe per tag type: ask PoB
   what the piece gives WITH ITS GATE FORCED OPEN (condition true, the variable at a reference amount, the slot filled with an
   ideal object). Residue: items PoB implements in special Lua code without tags (Mageblood may be one): a few dozen rows.
   FIRST STEP, cheap, no PoB runtime: a census of the tags over the whole corpus -- how many pieces have all their value behind
   a gate, how many gates exist, how many pieces carry no tag. That number says how "mathematical" this can be.
2. **Chains become PATHS.** More time with today's moves finds nothing: every move changes one surface, and a random kick
   proposes "this gem + that affix + that mastery" with a chance of about 1 in 10^10. With the gate graph a chain is a path
   (the gem provides a condition -> the condition opens the affix -> the affix feeds a variable -> the variable opens the
   mastery): a graph search of seconds, each found chain verified by ONE PoB what-if. Out of reach: links PoB does not compute.
3. **Blind enumeration, priced** (about 5,000 pieces -- uniques, notables, masteries, gems, affix groups; 7 ms a fast what-if;
   this PC's 5 workers): all PAIRS 12.5 million = ~5 hours per stand (all pairs on our 58 reference builds ~12 days of the
   machine, once, offline); all TRIPLES 2 x 10^10 = ~11 months per stand -- no; triples built only around pairs that showed a
   non-additive effect (say 1% of pairs) 6 x 10^8 = ~10 days per stand. Four-way blind is beyond a lifetime, and the gates make
   it unnecessary: forcing a gate open turns a hidden k-way bundle into k first-order measurements plus a path. No universal
   stand (the owner is right): the stands are the reference builds per archetype -- and, for "dig THIS build for a week", the
   owner's own build: a week covers all pairs and the pruned triples ON IT ("deep dig" as a product mode). No tree is generated
   per check: the fast what-if needs no connectivity; real trees only for survivors.
4. Caveats: a table of measured interactions per stand echoes v1's "scaling atlases" (forbidden to resurrect) -- those were
   AUTHORED, these are measured PoB deltas (principle 4); re-read LEGACY before the spec. Pieces whose value appears only after
   everything else is rebuilt (Chaos Inoculation) are branches, never what-ifs; the bound only decides which branches to build.

## Two acceptance cases the owner named (a future chain finder must find both BY ITSELF)

1. **Warden + ranged weapon + a tincture.** PoB: `["tincture effects also apply to ranged weapons"] = flag("TinctureRangedWeapons")`
   (ModParser.lua:5191); tincture mods carry `ModFlag.WeaponMelee` (:956). One gate (a flag), one ascendancy node opens it.
2. **Pathfinder Master Surgeon + the oil notable Vinespike Cordial + Inextricable Fate boots**: any two of the three give nothing.
   PoB: the boots' line "all damage inflicts poison against enemies affected by at least N grasping vines" is parsed
   (ModParser.lua:2338) behind the multiplier `GraspingVinesAffectingEnemy` (ConfigOptions.lua:1997, "# of Grasping Vines
   affecting enemy"); "during effect of any life flask" = `Condition:UsingLifeFlask` (:1743); "life flask effects are not
   removed when unreserved life is filled" is parsed (:5147); Vinespike Cordial is RED (one fact row: provides Grasping Vines
   on the enemy while a life flask is active, cap 8). The finder's route: force the boots' gate open (vines = 3) -> a large
   value on a poison build -> who provides vines? the Cordial, gated by UsingLifeFlask -> who proves UsingLifeFlask permanent?
   Master Surgeon + flask charges -> the chain closes, ONE PoB what-if verifies it. Backward chaining over "provides <->
   requires": the number of links costs nothing. What is needed is the meaning of each LINE (from PoB's parse, or one approved
   fact row per red line -- the D62 process), never knowledge of which pieces go together; plus uptime / ramp proofs (vines
   reach 3 inside the ramp budget; the flask does not run dry), the same machinery the conservative config lane already uses.
   Out of reach: a payoff PoB does not compute at all; red lines nobody has read yet (hundreds: per-line work, LLM-drafted,
   owner-approved); gateless numeric synergy is not a problem (each piece is positive alone, greed finds it).

## How it fits the way builds are made (the owner's question: "a researcher mode? every build wearing the vines boots?")

Two modes, and the owner guessed the split himself.

**Mode 1, the researcher -- offline, no builds, once per PoB version.** From PoB's parsed data every piece gets three lists:
what it REQUIRES (gates), what it PROVIDES, which stats it touches. Pure data work, minutes. Then, from every PAYOFF (a piece
with a strong effect behind a gate: "all damage can poison", conversions, "X applies to Y") backward along the links until the
chain closes; each closed chain is stored as a RECIPE: payoff, the enabling pieces with their alternatives (any proof of a
permanent life flask, Master Surgeon being one), restrictions (class / ascendancy), and WHO BENEFITS (the payoff's stat tags:
poison scaling). A catalogue of chains, possibly thousands, derived, not authored.

**Mode 2, an ordinary build.** The skeleton generator does not wander the graph. It RETRIEVES from the catalogue the chains
whose payoff stats intersect what the requested skill scales with and whose restrictions fit (dozens, not thousands): a
Fireball Elementalist never sees the vines chain, a poison Pathfinder always does -- no luck involved. Each retrieved chain is
tried WHOLE in one PoB what-if on the rough build (boots + oil + node + the config conditions, gates forced open = an optimistic
bound). A large promise = a skeleton VARIANT built in full and compared at the end with the plain variant; if the plain one
wins, the chain lost honestly. This is today's unique screen with a bundle as the candidate instead of a single item.

**Config ticks** are the second action of a chain, and nobody ticks them by hand in the final build: the conservative lane turns
a condition on only when a line in the build PROVES it (the existing proof rules). "Three vines on the enemy" is proven by the
chain itself -- the oil is allocated, the flask is permanent, the vines reach 3 inside the ramp budget -- given ONE fact row for
the red oil line (a fact about the LINE, never about the bundle). Pieces leave the build -> the proof is gone -> the tick goes.

**On probability**: the owner is right about TODAY's system (it would need a miracle: the pieces landing together by chance).
The catalogue changes the order of things -- the system itself places all pieces of a chain known to be linked side by side and
asks PoB once. A payoff that only pays together with something else (freed poison-chance investment re-spent) shows at the
branch's full build, where the rest is rebuilt around it.

**Research or engineering?** Mostly engineering; the research part is calibrating the optimistic bound (too generous = junk
branches). First step, cheap and checkable: build the graph and require the researcher to find the vines bundle BY ITSELF.

## What PoB's gates look like, and how many there are (counted from `vendor/pob/source`, PoB 2.67.2; no runtime)

The source of gate data is PoB's OWN parser (`PobSession.parse_mods` -> `modLib.parseMod`; `scripts/build_scaling_vectors.py`
already uses it) -- never the legacy GPT-written "potential scalers" parsing, which the owner distrusts and which is not used.

| level | game line | what PoB wrote | how it opens |
|---|---|---|---|
| 0 | "10% increased Fire Damage" | a mod, no tag | always on |
| 1 condition | "while on low life" | `Condition: LowLife` | config checkbox declared with `ifCond = "LowLife"` (shown only when the build holds such a mod); some conditions PoB sets itself (a flask is active, low life from reservation) |
| 2 variable | "per 10 Strength" | `PerStat: Str, div 10` | no checkbox: PoB counts the build's Strength (the stackers' gate) |
| 3 threshold | Inextricable Fate | `PoisonChance +100`, `FireCanPoison`, `ColdCanPoison` under `MultiplierThreshold: GraspingVinesAffectingEnemy >= 3` | config counter "# of Grasping Vines affecting enemy" (`ifMult`) |
| 4 rule flag | Master Surgeon; Warden tinctures | `flag("LifeFlaskEffectNotRemoved")`, `flag("TinctureRangedWeapons")` | read by PoB's calculation code; what it changes is seen only there |
| 5 special code | Mageblood | `LeftActiveMagicUtilityFlasks = 4`, a number for special code that activates flasks | no tag gate: the small table "modifier name -> object class" |
| red | Vinespike Cordial | the parser returns nothing | one fact row of ours |

Counts: 4,209 parser patterns; tag uses Condition 1,114 (293 distinct variables), SkillName 338, SkillType 281, Multiplier 255
(109 variables), ActorCondition 239 (49), PerStat 152 + StatThreshold 95 (83 stats), MultiplierThreshold 112, SocketedIn 90,
GlobalEffect 57; 325 distinct flags; 578 config options, of which `ifCond` 165, `ifMult` 52, `ifFlag` 106, `ifSkill` 217.
The link gate -> config input is EXPLICIT in PoB (`ifCond` / `ifMult` / `ifFlag`); our `config_options(predicates)` already reads it.

**The asymmetry (the real limit):** PoB knows almost completely what a piece REQUIRES (it needs it to calculate) and only partly
what a piece PROVIDES: it sets a condition itself for skill buffs, active flasks, reservation; for many conditions the only
provider PoB knows is "the player ticked the box" (it has the flag of Master Surgeon, not the fact that it makes UsingLifeFlask
permanent). The PROVIDES side is ours: proof rules "this condition is proven by this line" -- what `config_rules` already does
for the conservative lane (D77) -- built per LINE, never per bundle.

**Making the debugging measurable:** (1) a known-answer set of 20-30 famous bundles the owner knows by heart; the researcher
must find them itself, the share found = its recall (the vines boots are test 1); (2) the ORPHAN list -- gates with no provider
found: either player behaviour ("killed recently") or a missing fact -- a ready work list that makes the unknown visible;
(3) the owner skims the top found chains: a real bundle is recognised in a second, junk too.

## The owner's plan: a BRIDGE TABLE (he is "100% sure there is broken stuff nobody has guessed")

Sizes (ModParser.lua by table): `specialModList` 2,088 patterns (the special lines of uniques, ascendancies, keystones; ~1,100
carry a flag / tag / condition -- the vines boots, Master Surgeon and Mageblood live here), `modTagList` 666 (the gates
themselves), `modNameList` 723 (stat names: generic, dropped), the rest ~730 (number forms, weapon flags, ~130 radius-jewel
functions: a topic of its own). So the owner's guess holds: about a THOUSAND lines to review, plus PoB's red lines.

1. The first cut is MECHANICAL (a line with no tag, no flag, no rule drops by structure), never by the model's memory; the model
   drafts the second step: the BRIDGE of a line -- what it provides, UNDER WHICH CONDITION, what it requires.
2. The condition field is mandatory. The owner's own correction is the pattern: Master Surgeon does not give an endless life
   flask, it gives a mechanic under which 100% uptime becomes POSSIBLE (while life is not being lost; with flask charges). A
   digested answer that loses its condition has burnt us before (D62: "9 orbs" hid "only without DD"). Row format: line pattern
   | provides | condition | requires | source (wiki) | confidence | the owner's verdict; approved in batches from one table.
3. Tags on bridges are the rails of the combinatorics: humans (and a drafting model) describe LINES; the researcher assembles
   the 3+ link bundles from described lines by itself. Nobody writes combinations.
4. Per league: patch notes + a diff of `specialModList` between PoB versions -- new lines show up mechanically.
Limits: the payoff must be computed by PoB; the per-class optimizers (flasks, jewels, ...) come first. Cheap first step after
the limits reset: the mechanical filter + an export of those ~1,100 lines with their gates into a table -- the real size of the
manual work, and the share of lines whose bridge follows from PoB's data without a human.

