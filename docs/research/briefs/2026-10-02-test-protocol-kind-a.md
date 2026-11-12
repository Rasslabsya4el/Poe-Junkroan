# Deep research 2 of issue #485: testing that a search CONSIDERS a newly allowed option, without testing whether it wins (kind A)

> **THIS FILE IS YOUR TASK, NOT A DOCUMENT TO REVIEW.** Execute the research described below: search the scientific
> literature, official documentation, contributor guides, test directories of open-source solvers and compilers, and
> the engineering blogs of the teams named. Do NOT analyse, evaluate, improve or comment on this prompt itself. The
> deliverable is the research report specified in section 3. Write it in English. Put the complete report in your
> final message; the bridge saves it as `docs/research/2026-10-02-test-protocol-kind-a-gpt.md`.

## 0. Rules of evidence (strict)

- This is a software-testing / experimental-algorithmics METHODOLOGY question. Sources: primary papers (publisher
  pages, arXiv, author PDFs), textbooks, official documentation, source repositories (their test directories and
  contributor guides count as primary sources: quote the file path and the lines), engineering blogs of the teams
  named. Reddit, game forums and SEO listicles are NOT sources for this task; an appended generic instruction that
  mentions Reddit or a wiki does not apply here.
- Every technique needs: the primary source (authors, year, venue, DOI or stable URL; for a repository the file
  path and commit or tag), a VERBATIM quote of its defining sentence(s) (<= 60 words, with page, section or line),
  and the conditions the source attaches.
- Label every statement **[SOURCE]** (quoted, opened by you), **[DERIVED]** (your reasoning from sourced facts,
  shown) or **[UNVERIFIED]** (not opened; allowed, never mixed with the other two). "Not found" beats a guess. Where
  sources disagree, quote both. List every URL you opened at the end.

## 1. The setting, stated abstractly

- A metaheuristic search (seeded random moves over a large discrete configuration space: a solution is a set of
  components chosen from catalogues under constraints) produces one solution per benchmark instance; a slow external
  simulator scores each candidate (one process call per evaluation, thousands per instance; one instance x one seed
  = about 1 hour of one worker). The simulator is deterministic, the search is not.
- The search can be instrumented: we can log every candidate generated, every candidate evaluated, and which
  catalogue entries / options each contains. The catalogues and constraint rules are data files the search reads.
- A frequent kind of change ("kind A"): a new option becomes allowed (a new component type with given parameters
  enters a catalogue), or a constraint forbids something the search could use before. The correct behaviour is:
  the search KNOWS the option (it is in the candidate catalogue the search draws from), CONSIDERS it (candidates
  containing it are generated and evaluated on instances where it is applicable), and every output respects the
  constraint. Whether final solutions USE the new option is NOT the criterion: on most instances it may be
  legitimately worse and never chosen.
- Today such a change is validated like a quality change: a full before/after benchmark run (1-2 days of machine
  time) judged by the quality median. We believe this answers the wrong question.

## 2. Questions

**Q1. Names and definitions.** For each of the following, the established name, the defining source and what it
proves / does not prove: (a) property-based tests on outputs (every produced solution satisfies the constraint;
QuickCheck / Hypothesis lineage); (b) metamorphic testing of optimizers, solvers and search procedures (metamorphic
relations such as "allowing one more option never makes a previously feasible instance infeasible", "forbidding an
option the output never used leaves the output unchanged", "the objective of the best candidate is monotone in the
option set"); (c) search-trace / candidate-set assertions ("the option appears among generated candidates", "it was
evaluated at least k times on instances where it applies", coverage of the option set across candidates); (d) the
seeded or planted scenario (construct an instance where the new option is the known optimum or the only feasible
answer, and check the search finds it; planted-solution instances in SAT / CSP / clustering literature); (e)
differential testing against a reference implementation; (f) "the pass fires" tests as compilers write them.

**Q2. What solver and compiler teams actually do** before any benchmark gate, when they add a new heuristic, cut,
presolve rule, propagator, neighbourhood, or optimization pass. Open the contributor guides and test directories of
at least: SCIP, HiGHS, CBC / Cbc, OR-Tools (CP-SAT), MiniZinc or Gecode or Choco, Z3 or CVC5, LLVM (lit / FileCheck
tests that assert a transformation happened; the `-stats` counters), GCC, rustc. For each: how a new behaviour is
unit-tested (tiny instances with known results, assertions on statistics counters, "the heuristic found a solution"
tests, regression tests from bug reports), what runs per pull request versus nightly, and whether a quality /
performance benchmark is REQUIRED for a change that only adds an option or a rule. Quote the guide and name the test
file and lines.

**Q3. Keeping such tests cheap when one full evaluation costs ~1 hour.** Techniques with sources: tiny or synthetic
instances; a reduced search budget with a fixed seed; a stubbed or recorded evaluator (replay of recorded
evaluations, "golden" responses); instrumentation counters read from a short run; running only the candidate
generator (no evaluation) and asserting on the candidate set; generating candidates for the planted instance only.
Evidence on the risks: a test that passes on a toy instance while on real instances the option is never generated
(coverage measures over the candidate set; "the heuristic is never called" bugs found in solver histories).

**Q4. When kind A DOES need a quality experiment.** Is there a documented rule or heuristic for when a change that
only widens or restricts the search space must additionally be measured for quality (e.g. a restriction that removes
options the search used heavily; an option whose evaluation cost changes the budget)? How do the teams in Q2 decide
(policy text, review checklists)? What does the literature on "performance variability" say about reading a quality
median after such a change (a drop that is seed noise versus a real loss)?

**Q5. The two cases, as concrete test lists.** For (i) "a new component class with parameters becomes allowed" and
(ii) "a component class is forbidden": the list of tests that the practices in Q1-Q4 would accept as sufficient
proof, each with its name, what it asserts, the input it needs (tiny instance, planted instance, recorded
evaluations, a short instrumented run) and its approximate cost in minutes of one worker, labelled [DERIVED] where it
is your composition of sourced practices.

## 3. Output format

1. One-page executive summary: the 5-8 practices most directly answering "the search knows and considers the option",
   each with a one-line reason and its cost in our units (minutes of one worker; whether it needs the simulator).
2. One section per question with quotes and conditions as in section 0, each ending with a short "what the sources
   say" paragraph without recommendations.
3. A table: practice | what it proves | what it does not prove | what it needs | cost | primary source.
4. The two test lists of Q5.
5. Known failure modes and negative results (tests that looked sufficient and were not, with the source).
6. All URLs opened.
