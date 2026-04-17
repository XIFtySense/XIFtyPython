#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_VERSION="${XIFTY_RUNTIME_VERSION:-$(cat "$ROOT/runtime-version.txt")}"
RUNTIME_CACHE_ROOT="${XIFTY_RUNTIME_CACHE_DIR:-$ROOT/.xifty-runtime}"

uname_s="$(uname -s)"
uname_m="$(uname -m)"

case "${uname_s}:${uname_m}" in
  Darwin:arm64)
    TARGET="macos-arm64"
    ;;
  Linux:x86_64)
    TARGET="linux-x64"
    ;;
  *)
    echo "unsupported host for XIFty runtime: ${uname_s} ${uname_m}" >&2
    exit 1
    ;;
esac

RUNTIME_DIR="${RUNTIME_CACHE_ROOT}/xifty-runtime-${TARGET}-v${RUNTIME_VERSION}"
ASSET_NAME="xifty-runtime-${TARGET}-v${RUNTIME_VERSION}.tar.gz"
DOWNLOAD_URL="${XIFTY_RUNTIME_URL:-https://github.com/XIFtySense/XIFty/releases/download/v${RUNTIME_VERSION}/${ASSET_NAME}}"

if [[ -f "${RUNTIME_DIR}/manifest.json" ]]; then
  echo "Prepared XIFty runtime at ${RUNTIME_DIR}"
  exit 0
fi

mkdir -p "${RUNTIME_CACHE_ROOT}"
TMP_ARCHIVE="${RUNTIME_CACHE_ROOT}/${ASSET_NAME}"
rm -f "${TMP_ARCHIVE}"
rm -rf "${RUNTIME_DIR}"

curl -L --fail -o "${TMP_ARCHIVE}" "${DOWNLOAD_URL}"
tar -xzf "${TMP_ARCHIVE}" -C "${RUNTIME_CACHE_ROOT}"
rm -f "${TMP_ARCHIVE}"

if [[ ! -f "${RUNTIME_DIR}/manifest.json" ]]; then
  echo "runtime artifact did not unpack correctly at ${RUNTIME_DIR}" >&2
  exit 1
fi

echo "Prepared XIFty runtime at ${RUNTIME_DIR}"
