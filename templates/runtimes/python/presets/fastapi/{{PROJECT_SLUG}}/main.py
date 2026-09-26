
from __future__ import annotations

import argparse
import os
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Executa o servico HTTP")
    parser.add_argument("--host", default=os.getenv("SERVER_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("SERVER_PORT", "8000")))
    args = parser.parse_args([] if argv is None else argv)

    import uvicorn

    uvicorn.run(
        "{{PROJECT_SLUG}}.interfaces.http.app:create_app",
        factory=True,
        host=args.host,
        port=args.port,
        reload=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
