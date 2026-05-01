#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_WRAPPER="$ROOT_DIR/bin/newproj"
TARGET_BIN_DIR="${1:-$HOME/bin}"
TARGET_LINK="$TARGET_BIN_DIR/newproj"
VERSION="$(tr -d '\n' < "$ROOT_DIR/VERSION")"

if [ ! -f "$SOURCE_WRAPPER" ]; then
  echo "wrapper newproj nao encontrado em $SOURCE_WRAPPER" >&2
  exit 1
fi

mkdir -p "$TARGET_BIN_DIR"
chmod +x "$SOURCE_WRAPPER"

SOURCE_REAL="$(python3 - "$SOURCE_WRAPPER" <<'PY'
from pathlib import Path
import sys

print(Path(sys.argv[1]).resolve())
PY
)"
TARGET_REAL="$(python3 - "$TARGET_LINK" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1]).expanduser()
print(path.resolve() if path.exists() else path)
PY
)"

if [ "$SOURCE_REAL" = "$TARGET_REAL" ]; then
  echo "newproj ja aponta para $SOURCE_REAL"
else
  ln -sfn "$SOURCE_REAL" "$TARGET_LINK"
  echo "newproj instalado em $TARGET_LINK"
fi

case ":$PATH:" in
  *":$TARGET_BIN_DIR:"*)
    echo "PATH ok: $TARGET_BIN_DIR"
    ;;
  *)
    echo "Adicione ao PATH se necessario:"
    echo "export PATH=\"$TARGET_BIN_DIR:\$PATH\""
    ;;
esac

echo "Versao do kit: $VERSION"
echo "Verificacao recomendada: $TARGET_LINK --version"
