# State

As of 2026-11-13.

- The repo was cut from the private archive on 2026-11-12: the product (the PoB harness, the optimizer, the search,
  the corpora, the reference fixtures, the decisions in `docs/adr/`) with its history left behind. CI runs on GitHub
  runners (`docs/ci.md`), heavy runs go through `.github/scripts/heavy_dispatch.py`, PoB runs on Linux.
- On 2026-11-13 the whole project was audited; D119 records what was found and what the owner decided. In short:
  the benchmark path was measured for two months while the request path (`junkroan build`, the product) was barely
  tested and never accepted; the weekly core run counts nothing since 2026-10-17 (flask audit errors on every row);
  one build takes 93-140 minutes, about half of it whole-state reads and XML save/restore.
- The work now, in order (the map issue #14 holds the tickets; later loadouts and parked ideas are under #44 and
  #45; every open issue of the archive has its verdict under #5): one path for requests and references
  on template gear; the weekly core run counting again; what the move left in the archive (four finished branches,
  116 tests, the open day-1 issues); the build's cost; one end-to-end test of a request; then the first three
  requests for the owner's Reading: Earthshatter, Righteous Fire, Penance Brand.
- Nothing runs now. No weekly core run yet in this repo; the first one is its baseline. Two trial heavy runs of
  2026-11-13 measured one Storm Brand row on a hosted 4-core runner: 93 and 111 minutes alone, 105-140 minutes with
  two rows in flight.
- Pending: a dedicated Linux server joining as a self-hosted runner for long PoB runs (no 6-hour cap).
- The old checkout of the archive still holds what this repo needs and does not have: the run output of the old
  weekly core runs, the wiki cache, the PoEDB snapshots. It is not to be deleted until that is saved.
