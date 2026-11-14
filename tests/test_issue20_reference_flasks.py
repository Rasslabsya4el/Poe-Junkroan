"""#20: a rebuilt reference wears no flask the day-1 rails forbid, and the report marks every row the counted total leaves out.

The reference's own flasks reach the skeleton through `skeleton_from_xml`; with `gear.flasks.flask_utility_crafting` off the
day-1 flask step trials Flask 1 only, so a magic utility flask of the author's in Flask 2..N was delivered as it came in and
the audit judged it ours (`flask-utility-crafted`, `flask-uptime`). Now the skeleton drops it (`worn_flask_forbidden`), the
flask step counts any such carried flask (trace class `flask-forbidden-carried`, evaluated 0 once nothing is carried), and the
author's own build is judged as before (D115). PoB-free: decoded fixtures, a fake session for the flask step.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import junkroan.optimizer.pipeline as pipeline_mod  # noqa: E402
from benchmark import fixture_path, render_report  # noqa: E402
from build_from_skeleton import skeleton_from_xml  # noqa: E402
from conftest import needs_skill_source  # noqa: E402
from junkroan.optimizer.audit import audit_flask_bases  # noqa: E402
from junkroan.optimizer.flask_lines import worn_flask_forbidden  # noqa: E402
from junkroan.optimizer.flask_trace import CARRIED_FORBIDDEN_CLASS  # noqa: E402
from junkroan.optimizer.pipeline import BuildPipeline  # noqa: E402
from junkroan.optimizer.rails import Rails  # noqa: E402
from junkroan.optimizer.trace import TRACE  # noqa: E402
from junkroan.pob.session import decode_import_code  # noqa: E402
from junkroan.search.skeleton import Skeleton  # noqa: E402
from tests.test_benchmark_counted_rows import full_row  # noqa: E402
from tests.test_flask_step import FakeProbe  # noqa: E402


def _rails(utility: bool) -> Rails:
    base = Rails.load()
    assert base.gear.flasks.flask_utility_crafting is False  # the shipped day-1 rails
    return dataclasses.replace(base, gear=dataclasses.replace(base.gear, flasks=dataclasses.replace(base.gear.flasks, flask_utility_crafting=utility)))


def _xml(slug: str) -> str:
    return decode_import_code(fixture_path(slug).read_text(encoding="utf-8").strip())


def _names(flasks: dict[str, str]) -> dict[str, str]:
    return {slot: text.splitlines()[1] for slot, text in flasks.items()}


# ---- the skeleton: the reference's utility flasks leave it on day 1, stay with the rail on ----------------------------

@needs_skill_source
def test_day1_stormbrand_skeleton_keeps_no_utility_flask() -> None:
    logged: list[str] = []
    sk = skeleton_from_xml(_xml("stormbrand"), rails=_rails(False), log=logged.append)
    assert _names(sk.flasks) == {
        "Flask 1": "Ebullient Divine Life Flask of Quelling",
        "Flask 4": "Condensed Divine Life Flask of Sealing",
        "Flask 5": "Terrified Divine Life Flask of Entropy",
    }
    assert sum("Medic's Diamond Flask of the Narwhal" in m or "Apprentice's Ruby Flask of the Plover" in m for m in logged) == 2


@needs_skill_source
def test_rail_on_stormbrand_skeleton_keeps_every_author_flask() -> None:
    sk = skeleton_from_xml(_xml("stormbrand"), rails=_rails(True))
    assert set(sk.flasks) == {"Flask 1", "Flask 2", "Flask 3", "Flask 4", "Flask 5"}
    assert _names(sk.flasks)["Flask 2"] == "Medic's Diamond Flask of the Narwhal"


@needs_skill_source
def test_day1_unique_flask_stays_and_magic_utility_leaves() -> None:
    sk = skeleton_from_xml(_xml("spark"), rails=_rails(False))  # Flask 2 Blood of the Karui (unique), Flask 3 a magic Ruby Flask
    assert _names(sk.flasks).get("Flask 2") == "Blood of the Karui"
    assert "Flask 3" not in sk.flasks
    assert not [s for s, t in sk.flasks.items() if worn_flask_forbidden(t.splitlines(), _rails(False).gear.flasks)]


# ---- delivery: the session that held the author's build wears what the skeleton holds -----------------------------------

class _HeldSession:
    """A PoB session stand-in that already wears the author's items (the benchmark loads the author's build first): `equip`
    writes or (None) empties a slot, every other call `Skeleton.apply` makes is a no-op."""

    def __init__(self, held: dict[str, str]) -> None:
        self.held = dict(held)

    def equip(self, items: dict[str, str | None], **_kw) -> dict:
        for slot, raw in items.items():
            if raw is None:
                self.held.pop(slot, None)
            else:
                self.held[slot] = raw
        return {}

    def unique_item(self, name: str) -> dict:
        return {"raw": f"Rarity: UNIQUE\n{name}"}

    def __getattr__(self, _name: str):
        return lambda *a, **k: {}


def _delivered(monkeypatch, slug: str, utility: bool) -> dict[str, str]:
    xml = _xml(slug)
    author = skeleton_from_xml(xml, rails=_rails(True)).flasks  # every Flask slot the author wears
    sk = skeleton_from_xml(xml, rails=_rails(utility))
    monkeypatch.setattr(Skeleton, "apply_skills", lambda *a, **k: None)
    pob = _HeldSession(author)
    sk.apply(pob)
    return {slot: raw for slot, raw in pob.held.items() if slot.startswith("Flask ")}


@needs_skill_source
def test_day1_session_that_held_the_author_build_wears_no_utility_flask(monkeypatch) -> None:
    worn = _delivered(monkeypatch, "stormbrand", False)
    assert sorted(worn) == ["Flask 1", "Flask 4", "Flask 5"]
    assert not [s for s, raw in worn.items() if worn_flask_forbidden(raw.splitlines(), _rails(False).gear.flasks)]


@needs_skill_source
def test_rail_on_session_keeps_the_author_utility_flasks(monkeypatch) -> None:
    worn = _delivered(monkeypatch, "stormbrand", True)
    assert _names(worn)["Flask 2"] == "Medic's Diamond Flask of the Narwhal"
    assert _names(worn)["Flask 3"] == "Apprentice's Ruby Flask of the Plover"


@needs_skill_source
def test_output_count_of_forbidden_flasks_in_the_delivered_build() -> None:
    from junkroan.optimizer.trace_output import trace_output_from_xml

    assert trace_output_from_xml(_xml("stormbrand"))[CARRIED_FORBIDDEN_CLASS] == 2  # the author's own: Flask 2, Flask 3
    xml = ('<PathOfBuilding><Items activeItemSet="1"><Item id="1">Rarity: MAGIC\nCondensed Divine Life Flask of Sealing</Item>'
           '<Item id="2">Rarity: UNIQUE\nBottled Faith\nSulphur Flask</Item>'
           '<ItemSet id="1"><Slot name="Flask 1" itemId="1"/><Slot name="Flask 2" itemId="2"/></ItemSet></Items></PathOfBuilding>')
    assert trace_output_from_xml(xml)[CARRIED_FORBIDDEN_CLASS] == 0


# ---- the author's own build is judged as before (D115) -----------------------------------------------------------------

@needs_skill_source
def test_author_build_is_still_audited_on_its_utility_flasks() -> None:
    found = audit_flask_bases(_xml("stormbrand"), _rails(False))
    assert sorted(f.detail.split(":")[0] for f in found) == ["Flask 2", "Flask 3"]
    assert {f.check for f in found} == {"flask-utility-crafted"}
    assert audit_flask_bases(_xml("stormbrand"), _rails(True)) == []


# ---- the flask step's trace counter: a forbidden flask carried into Flask 2..N -----------------------------------------

UTILITY_RAW = "Rarity: MAGIC\nMedic's Diamond Flask of the Narwhal\nItem Level: 68"
LIFE_RAW = "Rarity: MAGIC\nCondensed Divine Life Flask of Sealing\nItem Level: 68"


def _carried(monkeypatch, utility: bool, held: dict[str, str]) -> dict:
    TRACE.reset()
    monkeypatch.setattr(pipeline_mod, "PobFlaskProbe", lambda pob, objective, *, item_level: FakeProbe(lambda c: 1.0))
    pob = SimpleNamespace(
        stats=lambda keys: {"CombinedDPS": 100.0, "Life": 3000.0, "EnergyShield": 100.0},
        equip=lambda items, **_kw: None, equipped_item_raws=lambda: dict(held),
    )
    objective = SimpleNamespace(stat_keys=["CombinedDPS"], score=lambda s: SimpleNamespace(value=s["CombinedDPS"]))
    gear = SimpleNamespace(flasks=_rails(utility).gear.flasks, item_level=68, wishlist=SimpleNamespace(base_level_max=70))
    me = SimpleNamespace(
        pob=pob, rails=SimpleNamespace(gear=gear), objective=objective, log=lambda _l: None,
        _step_start=lambda *a, **k: None, _record=lambda *a: None, judging=SimpleNamespace(rejudge=lambda sk: None),
    )
    BuildPipeline._flask_step(me, None, SimpleNamespace(pure_es=False))
    return TRACE.considered().get("flask", {})[CARRIED_FORBIDDEN_CLASS]


@needs_skill_source
def test_day1_counter_is_zero_when_nothing_forbidden_is_carried(monkeypatch) -> None:
    assert _carried(monkeypatch, False, {"Flask 4": LIFE_RAW}) == {"generated": 0, "evaluated": 0}


@needs_skill_source
def test_day1_counter_counts_a_carried_utility_flask(monkeypatch) -> None:
    held = {"Flask 2": UTILITY_RAW, "Flask 3": UTILITY_RAW, "Flask 4": LIFE_RAW}
    assert _carried(monkeypatch, False, held) == {"generated": 0, "evaluated": 2}


@needs_skill_source
def test_rail_on_counter_is_zero_every_slot_is_trialled(monkeypatch) -> None:
    assert _carried(monkeypatch, True, {"Flask 2": UTILITY_RAW})["evaluated"] == 0


# ---- the report: the "not counted" mark on every row the counted total leaves out --------------------------------------

def test_variant_row_with_an_audit_error_is_marked_not_counted() -> None:
    chosen = full_row("ref", 4, 0.90)
    variant = full_row("ref", 4, 0.95, variant="b", audit=["[error] flask-utility-crafted: Flask 2"], audit_errors=1)
    report = render_report([chosen, variant], stamp="fixture")
    assert "ref s4 (b) (audit error, not counted)" in report
    assert "**ref s4**" in report and "ref s4 (audit error" not in report
    assert "| ref | 1 | 90% |" in report  # the counted total: the chosen row only
