# The owner's reading of the 14 PoBs of the weekly core run 05.10 (2026-10-06 ~22:40)

The owner read the 14 rows of the reading page (run `20261005-1220-gate-20261005`, #586, the PoBs made BEFORE
#575's flask fix). His words are verbatim (Russian); the lead's decision follows each. Row numbers are the
tab's order: 1 winter_orb, 2 physical_dot, 3 spark, 4 ignite_penance_brand, 5 regular_viper_strike,
6 toxic_rain, 7 hit_penance_brand, 8 cold_dot, 9 bleed_bow, 10 summon_raging_spirits, 11 smite,
12 stormbrand, 13 absolution_minions, 14 poison_spectral_throw.

The owner's closing rule: "Все тикеты что я описал - надо создавать и давать сразу в работу, не ждать
чего-то. Единственное чего они могут ждать, это моих уточнений."

## Preface (flasks, movement speed)

> Оговорюсь сразу, я не адрессю фласки и соответственно крафты и прочие бонусы дающие дпс или другие статы за
> фласки + то что где-то могут одеть рф из-за руби фласки и прочее. Фласки мы пофиксили, а тут раны до фикса
> фласок. Касательно мувспида, я предлагаю с дей 1 сделать что на ботинках ролим 30% мув спида. Это будет честно
> и перестанет создавать проблемы с тестами. По факту в игре так и есть что тебе надо 30% мса всегда на
> ботинках, меньше очень слабо.

Decision: flasks: nothing (#575, #589, #596 cover it). Movement speed: **ticket A** "Day-1 boots always
roll 30% increased Movement Speed": the boots template's one fixed line on every day-1 build is
`30% increased Movement Speed` (the owner's number; the ilvl / tier rule of the day-1 rolls still applies to
the tier chosen). Kind A (D113): rail test + trace counter `generated(boots without 30% increased Movement
Speed) = 0` on 6/6 of the smoke six; `EffectiveMovementSpeedMod` per build shown. Parent #424 (rulebook,
`g-boots` / movement cell); the rulebook page gets the owner's line.

## 1 winter_orb (522 %)

> Если не считать фласки то тут выглядит все легально. Ты действительно смог выжать намного больше дпса.
> Единственное что мне не нравится и надо создать тикеты + выполнять их:
> а. Правило с +1 лвл гемов на оружиях должно распространяться и на щиты (в дей 1 лодауте)
> б. Мне кажется я поторопился с кластер джевелами и их не надо было энейблить в дей 1. Я хочу сдвинуть
> правила на 1 лодаут вверх. То есть то что сейчас на дей 1 идет на т16 лодаут. То что было на т16 лодауте
> идет в эндгейм лодаут. Так будет честнее

Decision: **ticket B** "Day-1 shields may carry +1 to Level of Socketed Gems like weapons": the day-1 weapon
rule (`+1 to Level of Socketed Gems`, the prefix as PoB writes it, incl. the `+1 to Level of all Spell Skill
Gems`-style lines the weapon rule already allows) extends to the Shield slot. Kind A: rail test + trace
`generated(shield with the +1 gem-level line) > 0` on a build with a shield (winter_orb) and the line
evaluated > 0. Parent #424.

**Ticket C** "Cluster jewels move one loadout up: none on day 1": the lead's reading of the owner's word:
the CLUSTER JEWEL rules shift one loadout up: day-1's cluster rules become the T16 loadout's, T16's become
the endgame's, day 1 has no cluster jewels. Kind A: `evaluated(cluster jewel) = 0` on every day-1 build
(6/6), the rail tests of the cluster step on `loadout=day1` refuse, the rulebook matrix cells move. A
question for the owner inside the ticket (does not hold the ticket): does the shift apply to the cluster
jewel rules only, or to every day-1 rule that was "enabled early" (name them)? Parent #424.

## 2, 3, 4 (physical_dot, spark, ignite_penance_brand): "ок".

## 5 regular_viper_strike

> Вижу баг на амуле. Там крафт реген лайф и реген мана. Насколько я знаю это невозможно.

Decision: **ticket D** "An item carries one crafted mod unless it has Can have up to 3 Crafted Modifiers":
the amulet of regular_viper_strike-s4 in the run carries two crafted lines (a Life regeneration craft and a
Mana regeneration craft). The worker decodes that PoB (fixture facts by decode), reads PoB's crafted-mod
data (`mod_corpus` / the bench craft list) and names whether the two lines are one hybrid bench craft
(`Regenerate # Life per second, #% increased Mana Regeneration Rate` hybrid exists on amulets in some
leagues: check in PoB's data, never from memory) or two separate crafts; if two, the gear rails forbid a
second crafted line without the multimod craft, and the audit gains the check "crafted lines <= 1 unless
`Can have up to 3 Crafted Modifiers`". Kind: bug-specific test + the audit on the 14 PoBs of the run (count
of items with 2+ crafted lines shown, expected 0 after). Parent #586.

## 6 toxic_rain

> Тут через мана фласку закрыли проблему с маной. Как обсуждали с фласками - если аптайм не 100% то это не
> годится

Decision: **ticket E** "Mana sustain is judged without flasks; a Mana Flask counts only at 100 % Flask
uptime": the mana floor (the unreserved mana / mana cost sustain rail) is measured with every flask's
`active` as #575 derives it (under 100 % uptime = inactive), and the mana rail never treats a Mana Flask
as the sustain source unless PoB prints 100 % uptime for it. Kind A: rail test + trace
`evaluated(mana sustain by an inactive flask) = 0` on 6/6; toxic_rain-s5 shown before/after. Parent #586.

## 7 hit_penance_brand

> Странно почему он не берет хай волтейдж нод. По идее скилл 50% конверт в лайтнин, саппорт на 50% конверта в
> лайтнин, то есть фул лайтнин дмг. Критовый билд, значит при крите шок гарантирован. Значит можно включать шок
> в конфиге. Единственное когда ты не элементалистка, при включении шока как я понимаю он включает на 1% или
> типо того. И надо самому руками ставить шок эффект. Это довольно большая задача, но она касается не только
> шока а всех эйлментов и того как они работают. Вот статья шока https://www.poewiki.net/wiki/Shock . У шока
> прикол что с каждым хитом он стакается. Ударил на 100, получил 10%-ый шок, следующий удар будет 110,
> следовательно и шок от следующего удара если он шокнет тоже выше и шок рампается. А мы высчитываем и рамп
> тоже. Значит мы сможем это считать. Единственный нюанс - это эйлмент трешолды мобов. На вики для этого указан
> сирус. Мы в побе (скрин) считаем по какому-то эвередж гварду/пиннакл боссу дпс, а значит и эйлмент трешолды
> для высчитывания эйлмент эффектов надо считать тоже исходя из этой настройки. Тут надо пойти на поедб и взять
> эйлмент трешолды всех гвардов и пинакл боссов и понять какое, полагаю, среднее число мы возьмем, чтобы это
> было честно. Тут по факту большая задача по имплементации правильного расчета эйлментов (не только
> дефолтных, но и бритл, скорч и прочие). Они все работают от эйлмент трешолдов и нам надо это правильно
> просчитывать. Нужен будет ресерч и код, потом тесты имплементации. Думаю дополнительно не помешает ресерч
> какие вообще эйлменты есть, как работают (факты типо того что эйлменты от крита накладываются 100%-но
> всегда, если есть сорс элемента (или эйлменты заэнейблены как в случае со скорч бритл и тд)). Тебе нужно
> полагаю создать тикет, сперва провести ресерч, потом подумать как имплементировать. Мне нужно чтобы наша
> система идеально считала эйлменты учитывая окно рампа

The screenshot: PoB's enemy config in our runs is `Is the enemy a Boss? = Guardian/Pinnacle Boss`, Enemy
Level 84 (the tooltip's Guardian / Pinnacle row: +50 % Elemental Resistances, +30 % Chaos Resistance, 150 %
monster Armour, 124 % Evasion, 181 % monster Damage of each type, 800 % total, 3 % penetration).

Decision: **ticket F (parent)** "Ailments are computed from boss ailment thresholds and the ramp window"
with **sub-issue F1 (research, ready-for-agent)** "Research: every ailment, its application rule and the
ailment thresholds of the Guardian and Pinnacle bosses": (1) the list of ailments (Shock, Chill, Freeze,
Ignite, Scorch, Brittle, Sap, Poison, Bleed) and for each: the application rule (crit = 100 % for the
element's default ailment when the hit has that damage type; Scorch / Brittle / Sap need their enabling
source), the magnitude formula vs the enemy's ailment threshold, duration, stacking / the strongest-instance
rule, and how PoB models each (which config toggles and which computed values: `conditionShockedEnemy`,
`conditionEnemyShocked`, the "Shock effect" override, `enemyIsBoss`), with file:line in
`vendor/pob/source/src/Modules/CalcOffence.lua` / `CalcSetup.lua` / `ConfigOptions.lua`; (2) the ailment
threshold of every Guardian and Pinnacle boss from poedb (external GPT researcher, the wiki first)
and the number our config's `Guardian/Pinnacle Boss` row implies (PoB's own: the boss ailment threshold is
derived from the enemy's life in PoB, read how); (3) the shock ramp inside our 2.5 s ramp window (every hit
raises the next hit's shock) as a formula we can compute from PoB's per-hit numbers. Output: a research
file under docs/research with the facts and a proposal of what the optimizer sets (config toggles and
effect values are optimizer decisions, principle 2; derived, principle 4) and what the LLM never touches.
Then the lead writes the implementation sub-issues (F2...). Parent of F: #486 (day-1 map: it changes
the number every hit-build is judged by). hit_penance_brand's `High Voltage` is the example the research
explains (why the search did not take it: a shock not configured).

## 8, 9, 10 (cold_dot, bleed_bow, summon_raging_spirits): "ок".

## 11 smite

> Мы не обсуждали тинкчеры. Суть тинкчеров в том что это такая кнопка которую нажимаешь для берст урона. Она
> очень быстро жрет ману и выключается когда маны ноль. Тинкчеры работают только на мили атаках (или
> ренджевых если взять пассивку варден сабкласса). Я считаю что мы должны юзать тинкчеры (и у автора тоже
> включать), но в наших побах важно чтобы тинкчер умещался в дюрейшн рампа (2.5с сейчас). То есть чтобы за эти
> 2.5с мана не улетела в ноль. Тут надо провести ресерч как работают тинкчеры, что такое мана берн у них и тд.
> Чтобы ты мог правильно закодить тинкчеры и то как они будут работать с рампом. На самих тинкчерах как
> айтемах меня устроит если они будут подчиняться тому как в дей 1 все айтемы ролятся по айлвлам. Дей 1 - 0
> полезных модов, то есть тупо база тинкчера с его имплиситом. т16 лодаут - 1 полезный мод на тинкчере.
> Эндгейм и выше - 2 полезных мода. По айлвлам все должно подчиняться правилу айлвлов и роллов, но это и так
> должно работать без моего напоминания. То есть это тоже большая задача на уровне эйлментов, которую надо
> выполнять

Decision: **ticket G (research + spec, ready-for-agent)** "Tinctures: research Mana Burn and the ramp
window, then the rule": (1) how a Tincture works (activation, Mana Burn: rate, stacking, what ends it,
melee-only and the Warden exception), how PoB models it (flask slot, `active`, uptime, Mana Burn in
CalcPerform / the flask code, file:line), (2) the owner's rule to spec: a Tincture is used when the build's
unreserved Mana survives the 2.5 s ramp window under Mana Burn plus skill costs (the number: Mana after
2.5 s > 0, computed from PoB's mana cost per second and the Mana Burn rate); the author's PoB gets the same
switch; (3) the item rule by loadout: day 1 = the base with its implicit only (0 useful mods), T16 = 1
useful mod, endgame and above = 2, always under the ilvl / roll rule of the loadout. Output: research file
+ the implementation sub-issue drafted with numbers for the lead. Parent #424 (rulebook cell for
flasks / tinctures gets the owner's three lines).

## 12 stormbrand

> Важное замечание по тому как работает МоМ кистоун. Когда юзают МоМ, всегда стараются держать хп пул таким,
> чтобы он был 60%, а мана (или ес+мана в случае с энерджи блейд) 40%. Таким образом не получится ситуации что
> тебя убили, а мана осталась. + оставляют какое-то количество %-ов в ману побольше, чтобы хватало еще на
> касты в случае когда к примеру очень сильно ударили и осталось мало маны. Чтобы не было ситуации что
> ударили так сильно, что нет маны. Короче мое хардкод правило о 50% МоМа было не совсем корректным. Нужно
> чтобы мана резерв в случае мома (+ес в случае ЭБ) считался на основе того как это заимпактит ехп пул.
> Потому что если баланс не будет соблюдаться, мы просто теряем ехп в моменты смерти/около смерти. Тоже нужна
> задача и выполнять ее. Сделать ресерч как это работает с математической точки зрения если тебе не ясно о
> чем я говорил. Ну и к примеру когда играешь на мом не важно с эб или без, нужно балансно гнать ехп пул.
> Слишком много маны при хорошем регене могут не давать ничего по ехп посути, пока хп не разогнан до момента
> когда соблюдается баланс. Мне тяжело описать все кейсы, сам не до конца догоняю. Это довольно сложный и
> тонкий момент

Decision: **ticket H** "Mind over Matter: the mana pool is sized by PoB's EHP, not by a 50 % rule": the
hand rule "50 % of Mana unreserved under Mind over Matter" goes (principle 1: PoB already computes
`TotalEHP` / `PhysicalMaximumHitTaken` with Mind over Matter and Eldritch Battery); the optimizer judges
the Life : Mana (+ES with Eldritch Battery) split by those numbers, and a new rail keeps casting possible
after the biggest hit: unreserved Mana left after `PhysicalMaximumHitTaken` is taken through MoM >= N casts
of the main skill (N researched: the owner's "some % more for casts"; the research names the number from
the 60/40 practice and the math of MoM damage split). First unit: a short research note (the MoM math:
damage taken from Mana = 40 % (or the build's %), the pool balance where Life and Mana run out together,
with Eldritch Battery ES first) with the formula; then the rail + the removal of the 50 % rule. Kind A for
the rail (trace `evaluated(MoM build with Mana left < N casts) = 0`) and the removal shown on stormbrand-s4
(TotalEHP, PhysicalMaximumHitTaken, Life, Mana before/after). Parent #424 (rulebook `c-keystones` /
reservation cell).

## 13 absolution_minions: "ок".

## 14 poison_spectral_throw

> Если я все правильно понимаю, то тут мы сталкиваемся с проблемой того как мы считаем дпс. У автора
> спектрал троу х4. Но дпс идет не с хитов, а с пойзна. Который прибавляется от каждого хита в фул дпс. Тут мы
> либо автора считаем по другому, убираем х4 хитов. Либо сами делаем х4 но фул дпс. Насколько я помню фул дпс
> мод вызывал проблемы с тем что он очень долго считается. Поэтому я полагаю имеет смысл спускать автора в
> целях тестов? Кстати не знаю почему у него х4 у ст

Decision: **ticket I** "Poison DPS is read under one hit-count rule for the author and the search": the
worker decodes the author's PoB of poison_spectral_throw (the import code, XML; which setting gives "x4":
a skill-part / projectile-count / `Spectral Throw` hit count in the skill's config, by name as PoB writes
it) and our finalist; the rule: the author and our builds are read under the same hit-count setting for
poison-per-hit; the owner's choice for tests: lower the author (read it with the multiplicity setting our
search uses) rather than make the search compute `FullDPS` with x4 (FullDPS mode was slow). Kind: a
bug-specific test on that reference (the author's number before/after, our 75 % re-read) + the benchmark
reading rule written in the reference's notes. Parent #586. The lead keeps the question "why x4 on
Spectral Throw" open inside the ticket for the decode to answer.

## Off-topic: overleech

> есть всякие пассивки которые дают что-то вайл личинг. У слеера (и еще других механик в игре) есть
> возможность получать оверлич. У трикстера соул дринкер к примеру. Или уник белт по-моему был (нужен ресерч
> всех оверлич сорсов в игре, не помню точно). Если есть оверлич - значит мы всегда личим. Следовательно
> всякие вайл личинг эффекты на билд работают всегда. Это важно добавить в систему, нужен тикет и выполнять
> его

Decision: **ticket J** "Overleech sources switch 'while Leeching' on for the whole fight": retrieval, not
recall: the worker finds every source of "Leech effects are not removed at Full Life" / overleech in PoB's
parsed data (`mod_corpus` / `tag_corpus` / `game_corpus`: ascendancy notables such as Slayer's, Trickster's
`Soul Drinker`, uniques), writes them as a derived list (a machine-readable fact in `src/junkroan/mechanics/`
only if PoB cannot derive it itself; check PoB's own `Condition:Leeching` handling first), and the optimizer
sets the config `Are you Leeching?` (the toggle as PoB names it) when the build has an overleech source and
any leech. Kind A: rail test + trace `evaluated(overleech build with Leeching off) = 0`; the list's length
and the toggles set shown. Parent #424 (`c-ascendancy` / leech cell).

## Tickets, in one table

| id | title | labels | parent |
|---|---|---|---|
| A | Day-1 boots always roll 30% increased Movement Speed | ready-for-agent, area:builds | #424 |
| B | Day-1 shields may carry +1 to Level of Socketed Gems like weapons | ready-for-agent, area:builds | #424 |
| C | Cluster jewels move one loadout up: none on day 1 | ready-for-agent, area:builds | #424 |
| D | An item carries one crafted mod unless it has Can have up to 3 Crafted Modifiers | ready-for-agent, area:builds | #586 |
| E | Mana sustain is judged without flasks; a Mana Flask counts only at 100 % Flask uptime | ready-for-agent, area:builds | #586 |
| F | Ailments are computed from boss ailment thresholds and the ramp window | area:builds (holder, no triage label) | #486 |
| F1 | Research: every ailment, its application rule and the ailment thresholds of the Guardian and Pinnacle bosses | ready-for-agent, area:builds | F |
| G | Tinctures: research Mana Burn and the ramp window, then the rule | ready-for-agent, area:builds | #424 |
| H | Mind over Matter: the mana pool is sized by PoB's EHP, not by a 50 % rule | ready-for-agent, area:builds | #424 |
| I | Poison DPS is read under one hit-count rule for the author and the search | ready-for-agent, area:builds | #586 |
| J | Overleech sources switch 'while Leeching' on for the whole fight | ready-for-agent, area:builds | #424 |

Every ticket quotes the owner's words of its section verbatim in its agent block, states the lead's
decision above as the rule, names its kind (D113) and its numbers, and ends with "Not in this ticket".
Questions to the owner stay inside the ticket and hold nothing (his rule).
