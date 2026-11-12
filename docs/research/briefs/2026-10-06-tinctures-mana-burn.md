# Brief: how Tinctures and Mana Burn work, and how players use them on melee builds (#607)

Context: Path of Exile 3.23+ (Tinctures came with Affliction, 3.23). Our optimizer measures builds in Path of
Building (PoB) over a 2.5 s ramp window (the first 2.5 s of a boss fight). The owner's understanding: a Tincture is a
button for burst damage; while active it applies stacking Mana Burn that drains mana fast, and it turns off when
mana reaches zero; Tinctures affect only melee attacks (ranged ones too with the Warden's ascendancy passive). We
need the exact mechanics to decide when a build may keep a Tincture on inside the 2.5 s window.

Questions (each answer: the source URL, date, author and a short verbatim quote; "not found" is allowed; keep every
condition the source attaches):
1. Tincture activation and Mana Burn: how Mana Burn stacks (one stack per what interval, the base interval, what
   changes it: "Mana Burn rate", "#% reduced Mana Burn rate", "Mana Burn per second"), how much mana one stack
   drains per second (the exact formula: % of maximum mana or flat), what ends the Tincture (mana reaches 0?
   deactivated manually?), and the cooldown after it ends. Sources: poewiki "Tincture" and "Mana Burn" pages,
   poedb Tincture base pages, GGG's 3.23 announcement and patch notes.
2. Which skills a Tincture's effects apply to: "melee weapon attacks" only, the Warden's ascendancy notable that
   extends it to ranged / bow attacks (its exact name and wording), and any unique Tincture or support that
   changes it.
3. How players use Tinctures in practice on melee builds (Reddit r/PathOfExileBuilds or r/pathofexile, maxroll,
   poe-vault): kept on for the whole boss fight or toggled for burst, how many seconds a typical build holds one
   before running out of mana, and how mana regeneration / leech / reservation interact with it. Quote the
   numbers and the conditions.
4. The implicit and the explicit mod pools on Tincture bases (prefix / suffix count, typical "useful" mods such as
   increased effect, reduced Mana Burn rate, damage), quoted from poedb.

Report: `docs/research/2026-10-06-tinctures-mana-burn.md`, every answer with URL, date, author, verbatim quote and
the attached conditions, then one "what it says" line per question. At least one reddit.com URL is required.
