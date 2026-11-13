# 2026-11-13 D119. After the audit: one path for requests and references, template gear only, the main skill ranks, the LLM is the site's request front

Status: Accepted

(D117 and D118 are numbers of the archive's process decisions, which did not come over; they are not used here.)

Why now: on 2026-11-13 the owner asked for a full audit of the project (decisions, code, tests, run output, the move
from the archive, the research). What it found, with the numbers it stands on:

- The path that was measured is not the path the prototype ships. The benchmark rebuilds a reference from the
  author's skeleton (ascendancy, supports, utilities, uniques) on template gear under the author's floors.
  `junkroan build` enumerates ascendancy x damage mode, defaults to loot gear (`search/request.py`,
  `scripts/search.py`) and uses absolute floors; the day-1 trace classes are registered by the replay bench (one of
  them also by the benchmark) and none by the request path. 95.5 % of the PoB test time is the benchmark path and none is the request path.
- Acceptance stands at 0 of 3 (D114 amd 3): the one Reading of request builds (2026-10-16, 7 builds of 3 requests)
  rejected all of them, and product work stopped on 2026-10-18.
- The weekly core run gave no counted answer after 2026-10-13: the run of 2026-10-17 counted 0 of 62 rows, each
  failing the audit on flask errors, and the second trial heavy run of 2026-11-13 (four Storm Brand rows) shows the same
  errors.
  From 2026-09-26 to 2026-10-13 the median of "% of the author" went from 169 % to 138 % over 2,930 commits while
  the rules and the author's number both changed, so the two cannot be told apart.
- One build went from 32-36 minutes (2026-09-21) to between 1 h 33 min and 2 h 20 min; PoB calls per build went
  from about 24,000 to about 53,000. On one measured build of 1 h 58 min, whole-state reads and XML save/restore took about 54 minutes and
  the trials about 36.
- No model is called anywhere in `src/` or `scripts/`; `docs/HYPOTHESES.md` describes an input nothing produces.
- 75 % of the archive's tickets and a third of its commits were agent orchestration.

The owner's answers the same day settle what follows. On the orchestration effort: "это была явная ошибка ... мы
можем полностью сосредоточиться на продукте".

Decision:

1. **One path.** A request and a reference run through the same search code. A reference is a request with every
   skeleton field fixed; what the benchmark adds is only the author's numbers beside ours. A test that passes, or a weekly
   core run that counts its rows, therefore says something about `junkroan build`.
2. **Template gear only** (the owner: "только темплейт"). `junkroan build` builds on template gear (D79); loot gear
   (D19) leaves the product path and stays, if at all, as an experiment's switch.
3. **A request's builds are ranked by the main skill's damage** (the owner: "фул дпс на мейн скилле ... короче по мейн
   скиллу"): the objective of the glossary, the main skill under its damage mode. Damage of other skills in the build
   is reported on its own line and does not rank. Support skills that buff the main skill (a curse, a mine's aura, a
   Vaal skill's buff) are part of the main skill's number, as PoB counts them: "это саппорт скиллы, это норма в пое".
4. **The LLM is the request front of the future site, and the prototype runs without it.** The owner: "ллм будет на
   сайте когда юзер будет давать запрос по билду. Возможно обойдемся без ллм, но с ллм как будто проще и понятнее
   для юзера". It turns a player's plain prompt into a request (a forced unique, "Life 5k" as a floor). Until the
   prototype is accepted the chat does that by hand: the owner says what he wants in his words, the chat writes the
   request and echoes how it understood each part. No hypothesis generator and no prompt parser is built before the
   first accepted request. Principle 2 of `CLAUDE.md` stands unchanged: no model picks a node, an affix or a config.
   The offline proposal step of the bundle catalogue (a model proposes lists of bundle-graph node ids per stand and
   PoB measures only those) is catalogue work, not a call inside `junkroan build`; it stays as designed and waits
   with the bundles (item 8).
5. **Acceptance**: three requests in the owner's words, each read by him with no logical error. No comparison with
   an author is part of it. The first three: Earthshatter, Righteous Fire, Penance Brand, a skill alone, the system
   choosing the rest. This replaces three clauses of D114 and the rest of D114 stands: "in a row, different skills,
   at least one with forced directions" (amd 3, item 6) is dropped; "no new kind of logical error" (amd 3, item 6)
   becomes no logical error, an old kind found again reopening its issue; "in the owner's words" (amd 1) now means
   he says what he wants and the chat writes the request (item 4).
6. **A movement skill is mandatory in every build and is exempt from the dead-gem check** (the owner: "да"): the
   check (#29, not in the audit yet) flags a gem whose removal moves no PoB number, and a movement skill moves none
   by nature.
7. **The red-line marks stay off** until the owner has gone through them with the chat, by red-line kind (the owner:
   "я буду их разбирать с тобой, к этому надо вернуться потом"). Off is to be explicit and tested, not the side
   effect of a missing store file.
8. **Scope and order.** Bundles, the catalogue, ailment thresholds and tinctures are day-1 loadout (the owner: "это
   основы игры по факту, а тинчеры я сам положил в дей1"). The order of work is the chat's, kept in the map issue: the
   foundation (one path, the weekly core run counting again, one end-to-end test of a request, what the move left
   behind); the first three requests and the first weekly core run; the loop defects his Reading of 2026-10-16
   named; the build's cost; then those mechanics, the ones his Readings name first.
9. **Time.** There is still no time line per request (D114 amd 2 and 3). Hours are accepted for the prototype; the
   dedicated server lifts the 6-hour cap of a hosted job. Speed work is justified by what a ticket run costs, not by
   a product deadline.
10. **A second PoB.** The system will later be duplicated for Path of Exile 2, which has another Path of Building,
    in an unscheduled future. Nothing is built for it now. Where a seam's place is open, the choice that lets a
    second PoB sit behind `PobSession` wins; no abstraction layer is added for it.
11. The four request runs of 2026-10-23/24 that nobody read are discarded; their requests are rebuilt after the
    repair if the owner wants them.

Still open, the owner's to decide after a measurement: whether Life 4,500 stays a hard day-1 floor. It is above 24
of the 32 references (median 4,030) and stands on top of three lines per item, uniques T5, one +30 node, no
resistances from the tree, strict mana and no utility flasks; what the rules cost in damage together is in no ADR (#31 measures it).

Consequences: the tickets are under the map issue
[The day-1 prototype after the audit](https://github.com/Rasslabsya4el/Poe-Junkroan/issues/14). Every open issue of
the archive got a verdict (#5): 41 of the old system closed, 35 product issues carried, replaced or placed under
the maps #14, #44 and #45. `docs/STATE.md` rewritten. D114 is marked as amended by this ADR.
`docs/HYPOTHESES.md`, `docs/REQUEST.md`, `docs/ARCHITECTURE.md`, `docs/LAYOUT.md`, `README.md` and the intro and
principle 2 of `CLAUDE.md` describe the LLM's role as it was before this decision until their ticket (#28) lands. Glossary: Hypothesis is a skeleton written by hand or, later, by a model; nothing
produces one today.
