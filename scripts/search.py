"""Search: a request in, ranked optimized builds out. The search itself is `junkroan.search.flow` (#16).

    python scripts/search.py Fireball                       # every ascendancy, blanks filled by PoB
    python scripts/search.py Fireball --hypotheses h.json   # LLM/human hypotheses (docs/HYPOTHESES.md)
    python scripts/search.py Fireball --ascendancies Elementalist,Inquisitor --top 2 --workers 3

Output: `$OUT_DIR/search-<skill>/<stamp>/` when OUT_DIR is set, else `artifacts/search-<skill>/<stamp>/`.
Exit code: 0 delivered, 1 a refused request or no candidates, 2 a finalist lost every seed (or nothing delivered).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from junkroan.search.flow import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
