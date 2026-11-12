#!/usr/bin/env bash
# Build PoB's native Lua runtime for Linux into vendor/pob/runtime-linux/ (the Windows side uses the lua51.dll PoB
# ships in its portable release; the Lua sources come from that release on both systems).
#
# What it builds, pinned to what PoB v2.67.2's own Windows build uses:
#   libluajit-5.1.so.2  LuaJIT v2.1 at 2460b3ff93a1c955de3d62cfc825de7d68dc272e ("LuaJIT 2.1.1784580905", the commit
#                       of PathOfBuilding-SimpleGraphic's vcpkg port luajit/2026-07-20 and of PoB's Dockerfile),
#                       stock Makefile: JIT on, no LUAJIT_ENABLE_LUA52COMPAT, like the Windows msvcbuild.
#   lua-utf8.so         starwing/luautf8 at d65ebfa4a00d6e582970ab729013bb2a629e74c9 (SimpleGraphic's libs/luautf8).
# The only C module the headless wrapper needs: Common.lua and EditControl.lua `require('lua-utf8')`. lcurl is
# stubbed by the wrapper, lzip is only UpdateCheck.lua's, socket nothing headless; zlib (Inflate, timeless jewel
# data) is the system libz.so.1 through LuaJIT's ffi.
#
# Ubuntu packages it needs (all present on ubuntu-latest runners):
#   build-essential git ca-certificates zlib1g
#
# Idempotent: a second run with the same pins finds BUILD-INFO and the libraries and does nothing.
# Usage: scripts/pob_runtime_linux.sh [--force]
set -euo pipefail

LUAJIT_REPO="https://github.com/LuaJIT/LuaJIT.git"
LUAJIT_COMMIT="2460b3ff93a1c955de3d62cfc825de7d68dc272e"
LUAUTF8_REPO="https://github.com/starwing/luautf8.git"
LUAUTF8_COMMIT="d65ebfa4a00d6e582970ab729013bb2a629e74c9"
PACKAGES=(build-essential git ca-certificates zlib1g)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${JUNKROAN_POB_NATIVE_ROOT:-$ROOT/vendor/pob/runtime-linux}"
INFO="luajit=$LUAJIT_COMMIT luautf8=$LUAUTF8_COMMIT"

if [[ "${1:-}" != "--force" && -f "$OUT/BUILD-INFO" && "$(head -n1 "$OUT/BUILD-INFO")" == "$INFO" \
      && -f "$OUT/libluajit-5.1.so.2" && -f "$OUT/lua-utf8.so" ]]; then
  echo "pob_runtime_linux: up to date in $OUT"
  exit 0
fi

missing=()
for pkg in "${PACKAGES[@]}"; do
  dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "install ok installed" || missing+=("$pkg")
done
if ((${#missing[@]})); then
  echo "pob_runtime_linux: installing ${missing[*]}"
  SUDO=""; [[ "$(id -u)" != 0 ]] && SUDO="sudo"
  $SUDO apt-get update -qq
  $SUDO apt-get install -y -qq "${missing[@]}"
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

fetch() {  # fetch <repo> <commit> <dir>: exactly one commit, checked
  git init -q "$3"
  git -C "$3" fetch -q --depth 1 "$1" "$2"
  git -C "$3" -c advice.detachedHead=false checkout -q FETCH_HEAD
  [[ "$(git -C "$3" rev-parse HEAD)" == "$2" ]] || { echo "pob_runtime_linux: $1 is not at $2" >&2; exit 1; }
}

fetch "$LUAJIT_REPO" "$LUAJIT_COMMIT" "$WORK/luajit"
make -C "$WORK/luajit" -j"$(nproc)" >/dev/null  # default BUILDMODE=mixed: libluajit.so plus a static luajit
fetch "$LUAUTF8_REPO" "$LUAUTF8_COMMIT" "$WORK/luautf8"
# no -lluajit: the host opens libluajit RTLD_GLOBAL, as Lua C modules expect on Linux
gcc -O2 -fPIC -shared -I"$WORK/luajit/src" -o "$WORK/lua-utf8.so" "$WORK/luautf8/lutf8lib.c"

mkdir -p "$OUT"
install -m 0755 "$WORK/luajit/src/libluajit.so" "$OUT/libluajit-5.1.so.2"
install -m 0755 "$WORK/lua-utf8.so" "$OUT/lua-utf8.so"
install -m 0755 "$WORK/luajit/src/luajit" "$OUT/luajit"
version="$("$OUT/luajit" -v)"
jit="$("$OUT/luajit" -e 'print(jit.status() and "JIT on" or "JIT off")')"
[[ "$jit" == "JIT on" ]] || { echo "pob_runtime_linux: built LuaJIT has the JIT off" >&2; exit 1; }
{ echo "$INFO"; echo "$version, $jit"; (cd "$OUT" && sha256sum libluajit-5.1.so.2 lua-utf8.so); } > "$OUT/BUILD-INFO"
cat "$OUT/BUILD-INFO"
