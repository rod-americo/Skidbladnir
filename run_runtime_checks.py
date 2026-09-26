#!/usr/bin/env python3
"""Executa a matriz real; ferramenta ausente ou versão divergente é erro."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

from scaffold_project import CATALOG, RUNTIMES, canonicalize_preset, render_and_write_templates, runtime_commands


def run(command: list[str] | str, cwd: Path, env: dict[str, str], *, expect_failure: bool = False) -> str:
    result = subprocess.run(command, cwd=cwd, env=env, shell=isinstance(command, str), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    if (result.returncode == 0) == expect_failure:
        raise RuntimeError(f"{command}\nexit={result.returncode}\n{result.stdout[-14000:]}")
    return result.stdout


def check_toolchain(runtime: str, env: dict[str, str]) -> None:
    commands = {"python": ["python3", "--version"], "node": ["node", "--version"], "ts": ["node", "--version"], "go": ["go", "version"], "swift": ["swift", "--version"], "csharp": ["dotnet", "--version"], "java": ["java", "-version"], "rust": ["rustc", "--version"]}
    command = commands[runtime]
    if not shutil.which(command[0], path=env["PATH"]):
        raise RuntimeError(f"toolchain obrigatória ausente: {command[0]}; nada foi validado")
    output = run(command, Path.cwd(), env)
    expected = RUNTIMES[runtime]["version"]
    if runtime == "swift":
        pattern = re.escape(expected[:-2]) + r"(?:\.0)?" if expected.endswith(".0") else re.escape(expected)
        valid = re.search(r"Swift version " + pattern + r"(?: |\n)", output)
    else:
        valid = re.search(r"(?<!\d)" + re.escape(expected) + r"(?![\d.-])", output)
    if not valid:
        raise RuntimeError(f"{runtime}: esperado {expected}, recebido {output.strip()}")


def check_frozen_install(runtime: str, repo: Path, env: dict[str, str]) -> None:
    if runtime in {"node", "ts"}:
        path = repo / "package.json"
        original = path.read_text()
        payload = json.loads(original)
        section = "devDependencies" if "typescript" in payload.get("devDependencies", {}) else "dependencies"
        payload.setdefault(section, {})["typescript"] = "5.8.3"
        path.write_text(json.dumps(payload))
        try:
            output = run(["npm", "ci", "--ignore-scripts"], repo, env, expect_failure=True)
            if "lock" not in output.lower():
                raise RuntimeError("npm ci falhou por motivo diferente da divergência do lockfile: " + output)
        finally:
            path.write_text(original)
    elif runtime == "rust":
        path = repo / "Cargo.toml"
        original = path.read_text()
        path.write_text(original.replace('version = "0.1.0"', 'version = "0.2.0"', 1))
        try:
            output = run(["cargo", "build", "--locked", "--offline"], repo, env, expect_failure=True)
            if "lock" not in output.lower():
                raise RuntimeError("Cargo falhou por motivo diferente do lockfile: " + output)
        finally:
            path.write_text(original)
    elif runtime == "python":
        path = repo / "requirements.txt"
        original = path.read_text()
        path.write_text(re.sub(r"--hash=sha256:[a-f0-9]+", "--hash=sha256:" + "0" * 64, original))
        try:
            output = run(["python", "-m", "pip", "install", "--require-hashes", "--force-reinstall", "--no-deps", "-r", "requirements.txt"], repo, env, expect_failure=True)
            if "hash" not in output.lower():
                raise RuntimeError("pip falhou por motivo diferente do hash: " + output)
        finally:
            path.write_text(original)


def check_http(repo: Path, env: dict[str, str]) -> None:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    process = subprocess.Popen(["python", "-m", "runtime_probe"], cwd=repo, env={**env, "SERVER_HOST": "127.0.0.1", "SERVER_PORT": str(port)}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError("serviço HTTP encerrou antes de responder ao probe")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1) as response:
                    assert response.status == 200
                    assert json.load(response)["status"] == "ok"
                    return
            except OSError:
                time.sleep(0.1)
        raise RuntimeError("timeout do healthcheck HTTP")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def check_project(runtime: str, preset: str, repo: Path, env: dict[str, str]) -> None:
    render_and_write_templates(repo, runtime, preset, "Runtime Probe", "runtime_probe", "https://github.com/example/runtime-probe", False, False, True)
    gate = repo / "PROJECT_GATE.md"
    gate.write_text("\n".join(
        line.partition(":")[0] + ": Operação local com contratos explícitos e validação automatizada verificável."
        if line.startswith("- ") and ":" in line and not line.startswith("- runtime escolhido:") else line
        for line in gate.read_text().splitlines()
    ) + "\n")
    commands = runtime_commands(runtime, "runtime_probe", preset)
    if runtime == "python":
        run(["python3", "-m", "venv", ".venv", "--prompt", repo.name], repo, env)
        env = {**env, "PATH": str(repo / ".venv/bin") + os.pathsep + env["PATH"]}
        run(["python", "-m", "pip", "install", "--require-hashes", "-r", "requirements.txt"], repo, env)
    elif runtime != "java":
        run(commands["setup"], repo, env)
    for script in ["check_project_gate.py", "check_deploy_manifest.py"]:
        run([sys.executable, "scripts/" + script], repo, env)
    run(commands["test"], repo, env)
    run(commands["build"], repo, env)
    output = run(commands["smoke"], repo, env)
    if runtime in {"java", "rust"}:
        event = json.loads(output.strip().splitlines()[-1])
        assert event["evt"] == "startup" and event["svc"] == "Runtime Probe"
    if preset == "fastapi":
        check_http(repo, env)
    if preset == "base":
        check_frozen_install(runtime, repo, env)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True, choices=[r for r in RUNTIMES if r != "generic"])
    parser.add_argument("--preset", help="omite para executar todos os presets deste runtime")
    args = parser.parse_args()
    env = dict(os.environ)
    env.update({"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1", "GOTOOLCHAIN": "local"})
    try:
        check_toolchain(args.runtime, env)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    presets = [canonicalize_preset(args.preset)] if args.preset else RUNTIMES[args.runtime]["presets"]
    if any(preset not in RUNTIMES[args.runtime]["presets"] for preset in presets):
        parser.error("preset não suportado pelo runtime")
    failed = []
    for preset in presets:
        print(f"CHECK {args.runtime}/{preset}", flush=True)
        try:
            with tempfile.TemporaryDirectory(prefix=f"skidbladnir-{args.runtime}-{preset}-") as tmp:
                check_project(args.runtime, preset, Path(tmp), env)
            print(f"PASS {args.runtime}/{preset}", flush=True)
        except (RuntimeError, AssertionError, subprocess.TimeoutExpired) as exc:
            print(f"FAIL {args.runtime}/{preset}: {exc}", file=sys.stderr, flush=True)
            failed.append(preset)
    print(f"{len(presets) - len(failed)}/{len(presets)} projetos aprovados ({args.runtime} {RUNTIMES[args.runtime]['version']}; catálogo {CATALOG['reviewed_on']})")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
