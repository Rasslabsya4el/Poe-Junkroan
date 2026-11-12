# #728 unit 1: where read_proc_table spends its time (2026-10-10, live PC)

488-492 processes (not 917 as in the cProfile; it varies). Machine cpu 83-100 % during the runs, so every number is noisy:
the same read was 2.5 s and 10 s back to back. Each attribute alone via `psutil.process_iter([attr], ad_value=None)`, second run:

| attribute | total s | ms/process |
|---|---|---|
| pid | 0.017 | 0.04 |
| ppid | 0.295 | 0.6 |
| name | 0.029 | 0.06 |
| username | 0.038 | 0.08 |
| cmdline | 5.02 (re-runs 3.06, 2.85) | 10.6 (6.0-6.5) |
| memory_info | 1.64 | 3.5 |
| cpu_times | 1.25 | 2.65 |
| all 7 together | 3.85 (re-run 7.6) | 8.2 |
| whole `read_proc_table()` | 3.80 | 8.1 |
| `_session_of` over 150 processes with username None | 0.0 | ~0 |
| `p.cwd()` over pytest processes (1) | 0.0 | ~0 |

Dominant: `cmdline` (about 5 s of the sum 8.3 s alone; Windows reads the PEB of each process). Then `memory_info` + `cpu_times`
(3 s alone; together with the oneshot they are ~2.5 s when the machine is not saturated, 7-10 s when it is).
`username`, `name`, `pid`, `_session_of`, `cwd` are negligible. `ppid` is small.

Reads the groups' numbers could skip (read from load_groups.py, no code changed):
- `username` / `_session_of`: used only by `_classify` (:190, :117-127) for rows outside job/claude chains; already cheap (0.08 ms), skipping gains nothing.
- `cmdline`: used by `_is_pytest` (:60, :195), `_is_pob_runtime` (:197) and the pytest lists (:200-208) for EVERY row, also rows of the owner/system groups
  (`whole_suite_pytest`, `merge_suite_pytest` count pytests anywhere; `pob_runtime_by_group` counts per group). Skipping it for non-job/claude rows
  would change `whole_suite_pytest`; only a name prefilter (read `cmdline` only when `name` is python/pytest/luajit-like) keeps the numbers, and
  that depends on what the process names of pytest and headless_runtime_worker really are (not measured here).
- `memory_info` / `cpu_times`: summed into `rss_mb` / `cpu_pct` of every group (:192-193), so no row can skip them without changing a group.
- `time.sleep(0.5)` at :146 plus the second `read_proc_table()` at :148 doubles the cost; the answer of `--suite-workers` needs only totals, not the diff.
