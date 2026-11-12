"""Which native Lua runtime the headless PoB worker loads on this platform.

PoB's Lua sources come from the pinned portable release on every platform (`release_manager`); only the native
part differs. On Windows it is the `lua51.dll` PoB ships next to `Launch.lua`, with C modules (`lua-utf8.dll`)
from the same folder: behaviour exactly as before Linux support. On Linux it is the LuaJIT and `lua-utf8.so` built
by `scripts/pob_runtime_linux.sh` at the commits PoB's own Windows build uses, in `vendor/pob/runtime-linux/`
(or `$JUNKROAN_POB_NATIVE_ROOT`). There `package.cpath` is that folder only, so a system Lua module (an `lpeg`
that dkjson would pick up) never changes PoB's behaviour, and the library is opened RTLD_GLOBAL because Lua C
modules on Linux resolve `lua_*` from the already loaded LuaJIT.
"""

from __future__ import annotations

import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path

NATIVE_ROOT_ENV = "JUNKROAN_POB_NATIVE_ROOT"
LINUX_LUAJIT_NAME = "libluajit-5.1.so.2"
LINUX_NATIVE_MODULES = ("lua-utf8.so",)
_DEFAULT_LINUX_NATIVE_ROOT = Path(__file__).resolve().parents[3] / "vendor" / "pob" / "runtime-linux"


@dataclass(frozen=True)
class LuaRuntimeLayout:
    library: Path  # the LuaJIT shared library the bridge opens
    cpath_lua: str  # the Lua statement that points `package.cpath` at the native modules
    load_global: bool  # open the library RTLD_GLOBAL (Linux: C modules link against it)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _is_windows(platform: str) -> bool:
    return platform.startswith("win")


def linux_native_root(native_root: Path | None = None) -> Path:
    if native_root is not None:
        return native_root
    configured = os.environ.get(NATIVE_ROOT_ENV, "").strip()
    return Path(configured) if configured else _DEFAULT_LINUX_NATIVE_ROOT


def lua_runtime_layout(runtime_root: Path, *, platform: str = sys.platform, native_root: Path | None = None) -> LuaRuntimeLayout:
    if _is_windows(platform):
        return LuaRuntimeLayout(
            library=runtime_root / "lua51.dll",
            cpath_lua=f"package.cpath = package.cpath .. ';{runtime_root.as_posix()}/?.dll'",
            load_global=False,
        )
    root = linux_native_root(native_root)
    return LuaRuntimeLayout(
        library=root / LINUX_LUAJIT_NAME,
        cpath_lua=f"package.cpath = '{root.as_posix()}/?.so'",
        load_global=True,
    )


def runtime_fingerprints(runtime_root: Path, *, platform: str = sys.platform, native_root: Path | None = None) -> dict[str, str]:
    """The launch receipt's hashes of the native runtime. The key `lua51_dll_sha256` keeps its name on every platform
    and hashes the LuaJIT library actually loaded; Linux adds its own C modules."""

    layout = lua_runtime_layout(runtime_root, platform=platform, native_root=native_root)
    fingerprints = {"lua51_dll_sha256": _sha256_file(layout.library)}
    if not _is_windows(platform):
        for name in LINUX_NATIVE_MODULES:
            fingerprints[name.replace("-", "_").replace(".", "_") + "_sha256"] = _sha256_file(layout.library.parent / name)
    return fingerprints


__all__ = ["LuaRuntimeLayout", "NATIVE_ROOT_ENV", "linux_native_root", "lua_runtime_layout", "runtime_fingerprints"]
