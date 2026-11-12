"""The platform pick of PoB's native Lua runtime (no PoB starts here).

On Windows the bridge loads the `lua51.dll` PoB ships in the extracted portable runtime and C modules come from
that folder (`?.dll`), exactly as before Linux support. On Linux it loads the LuaJIT built by
`scripts/pob_runtime_linux.sh` (`vendor/pob/runtime-linux/`), C modules come only from that folder (`?.so`), and the
library is opened RTLD_GLOBAL so `lua-utf8.so` resolves the `lua_*` symbols from it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from junkroan.pob.native_runtime import lua_runtime_layout, runtime_fingerprints

RUNTIME = Path("/x/var/cache/pob/v2.67.2/app")
NATIVE = Path("/x/vendor/pob/runtime-linux")


def test_windows_loads_lua51_dll_from_the_pob_runtime() -> None:
    layout = lua_runtime_layout(RUNTIME, platform="win32", native_root=NATIVE)
    assert layout.library == RUNTIME / "lua51.dll"
    assert layout.cpath_lua == f"package.cpath = package.cpath .. ';{RUNTIME.as_posix()}/?.dll'"
    assert layout.load_global is False


def test_linux_loads_the_built_luajit_and_only_its_so_modules() -> None:
    layout = lua_runtime_layout(RUNTIME, platform="linux", native_root=NATIVE)
    assert layout.library == NATIVE / "libluajit-5.1.so.2"
    assert layout.cpath_lua == f"package.cpath = '{NATIVE.as_posix()}/?.so'"
    assert layout.load_global is True


def test_linux_native_root_follows_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JUNKROAN_POB_NATIVE_ROOT", "/opt/pobnative")
    layout = lua_runtime_layout(RUNTIME, platform="linux")
    assert layout.library == Path("/opt/pobnative") / "libluajit-5.1.so.2"


def test_linux_native_root_defaults_to_the_repo_vendor_folder(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JUNKROAN_POB_NATIVE_ROOT", raising=False)
    layout = lua_runtime_layout(RUNTIME, platform="linux")
    assert layout.library.parent.as_posix().endswith("vendor/pob/runtime-linux")


def test_fingerprints_hash_the_library_actually_loaded(tmp_path: Path) -> None:
    runtime, native = tmp_path / "app", tmp_path / "native"
    runtime.mkdir()
    native.mkdir()
    (runtime / "lua51.dll").write_bytes(b"windows")
    (native / "libluajit-5.1.so.2").write_bytes(b"linux")
    (native / "lua-utf8.so").write_bytes(b"utf8")
    win = runtime_fingerprints(runtime, platform="win32", native_root=native)
    assert win == {"lua51_dll_sha256": "340d600392818df2413382dc7d8325c360d83ea49a262d31760348484bbc10b5"}
    lin = runtime_fingerprints(runtime, platform="linux", native_root=native)
    assert lin["lua51_dll_sha256"] == "caf90169eefa5f807d577486b9f795ab86ae2983c5c20806cff959117e90af18"
    assert set(lin) == {"lua51_dll_sha256", "lua_utf8_so_sha256"}
