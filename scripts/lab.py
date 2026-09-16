#!/usr/bin/env python3
"""lab.py - single Python CLI for the mobsec-ctf-lab.

Replaces the bash helpers with one cross-platform command.

Usage (from the project root or anywhere - it finds the project root):
    python scripts/lab.py setup
    python scripts/lab.py start
    python scripts/lab.py stop
    python scripts/lab.py reset
    python scripts/lab.py health
    python scripts/lab.py build-apk       (build the vulnerable Android APK)
    python scripts/lab.py expose          (admin Windows: open firewall+portproxy)
    python scripts/lab.py close           (admin Windows: close firewall+portproxy)

Run as the standard user for everything except `expose`/`close`, which need an
elevated (Administrator) shell on Windows.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
LAB_NET = "mobsec-lab-net"
CTFD_URL = "http://ctfd:8000"
ON_WINDOWS = sys.platform.startswith("win")
APK_BUILDER_IMAGE = "mobsec-lab/apk-builder"
DIST_DIR = PROJECT_ROOT / "targets" / "appstore" / "www" / "apk"


# --------------------------------------------------------------------------- #
# Env / podman helpers
# --------------------------------------------------------------------------- #
def env_val(key: str, default: str = "") -> str:
    """Read a value from .env (last definition wins)."""
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                if k.strip() == key:
                    return v.strip()
    return default


def env_num(key: str, default: int) -> int:
    v = env_val(key)
    try:
        return int(v)
    except ValueError:
        return default


def ensure_env() -> None:
    """Create .env from .env.example on first run."""
    if not ENV_FILE.exists():
        if ENV_EXAMPLE.exists():
            shutil.copy(ENV_EXAMPLE, ENV_FILE)
            print(f"[*] Created .env from .env.example (edit secrets before production use).")
        else:
            print("[!] .env.example missing; cannot create .env.", file=sys.stderr)
            sys.exit(1)


def require_podman() -> str:
    podman = shutil.which("podman")
    if not podman:
        print("Podman is required but was not found. Install Podman first.", file=sys.stderr)
        sys.exit(1)
    return podman


def compose_files() -> list[str]:
    """Return the compose -f args (adds compose.lan.yml overlay when exposed)."""
    if env_val("EXPOSE_TARGETS") == "1":
        return ["-f", "compose.yml", "-f", "compose.lan.yml"]
    return ["-f", "compose.yml"]


def ensure_admin_windows() -> None:
    """Ensure the current process is elevated on Windows (for expose/close)."""
    if not ON_WINDOWS:
        return
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print(
                "[-] This command must be run from an ELEVATED (Administrator) "
                "PowerShell/terminal on Windows.",
                file=sys.stderr,
            )
            print("    Right-click your terminal -> 'Run as administrator', or:", file=sys.stderr)
            print(f"    Start-Process -Verb RunAs -FilePath python -ArgumentList "
                  f"'\"{Path(__file__)}\" {sys.argv[1]}'", file=sys.stderr)
            sys.exit(1)
    except Exception:  # pragma: no cover - defensive
        pass


def run(*args: str, check: bool = True, show: bool = True) -> subprocess.CompletedProcess:
    """Run a command in the project root. `show` hides output (for wait loops)."""
    if show:
        print(f"[*] $ {' '.join(args)}")
    return subprocess.run(list(args), cwd=PROJECT_ROOT, check=check, capture_output=not show)


def wait_ctfd(podman: str, timeout: int = 300) -> bool:
    """Poll CTFd's API from inside a container until it responds."""
    print("[*] Waiting for CTFd to become ready...")
    probe = (
        "import urllib.request,sys;"
        "r=urllib.request.urlopen('http://127.0.0.1:8000/api/v1/challenges',timeout=5);"
        "sys.exit(0 if r.status in (200,401,403) else 1)"
    )
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            p = run(
                podman, "compose", *compose_files(), "exec", "-T", "ctfd",
                "python", "-c", probe,
                check=False, show=False,
            )
            if p.returncode == 0:
                print("[*] CTFd is ready.")
                return True
        except Exception:
            pass
        time.sleep(5)
    print("[!] CTFd did not become ready in time.", file=sys.stderr)
    return False


def provision(podman: str) -> None:
    """Run scripts/provision.py in a throwaway container on the lab network."""
    print("[*] Provisioning challenges into CTFd...")
    env = {
        "CTFD_URL": CTFD_URL,
        "CTFD_ADMIN_EMAIL": env_val("CTFD_ADMIN_EMAIL"),
        "CTFD_ADMIN_PASSWORD": env_val("CTFD_ADMIN_PASSWORD"),
        "CTFD_CTF_NAME": env_val("CTFD_CTF_NAME"),
        "CTFD_CTF_DESCRIPTION": env_val("CTFD_CTF_DESCRIPTION"),
        "CTFD_MODE": env_val("CTFD_MODE"),
        "CHALLENGES_FILE": "challenges/challenges.json",
    }
    try:
        # Use subprocess directly because provisioning needs a host path mount.
        subprocess.run(
            [podman, "run", "--rm",
             "--network", LAB_NET,
             "-e", "CTFD_URL=" + CTFD_URL,
             "-e", "CTFD_ADMIN_EMAIL=" + env["CTFD_ADMIN_EMAIL"],
             "-e", "CTFD_ADMIN_PASSWORD=" + env["CTFD_ADMIN_PASSWORD"],
             "-e", "CTFD_CTF_NAME=" + env["CTFD_CTF_NAME"],
             "-e", "CTFD_CTF_DESCRIPTION=" + env["CTFD_CTF_DESCRIPTION"],
             "-e", "CTFD_MODE=" + env["CTFD_MODE"],
             "-e", "CHALLENGES_FILE=" + env["CHALLENGES_FILE"],
             "-v", f"{PROJECT_ROOT}:/work:ro",
             "-w", "/work",
             "--name", "mobsec-provision",
             "python:3.11-alpine",
             "python", "scripts/provision.py"],
            cwd=PROJECT_ROOT, check=True,
        )
    except subprocess.CalledProcessError:
        print("[!] Provisioning failed.", file=sys.stderr)
        sys.exit(1)


def build_apk(podman: str) -> None:
    """Build the vulnerable Android APK in a container and copy it out."""
    print("[*] Building the vulnerable GlowMart Mobile APK (this downloads the "
          "Android SDK inside the container - it needs internet and several GB)...")
    run(podman, "build", "-t", APK_BUILDER_IMAGE,
        "-f", str(PROJECT_ROOT / "targets" / "app" / "Dockerfile"),
        str(PROJECT_ROOT / "targets" / "app"))
    # Discover the APK inside the built image and copy it out.
    apk_src = "/workspace/app/build/outputs/apk/debug/app-debug.apk"
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    podman_run = ["podman", "run", "--rm"]
    p = run(*podman_run, "--entrypoint", "sh", APK_BUILDER_IMAGE, "-c",
            f"test -f {apk_src} && echo present || echo missing",
            check=False, show=False)
    if p.returncode != 0 or "present" not in p.stdout:
        print("[!] APK not found in the builder image. Check the build logs above.",
              file=sys.stderr)
        sys.exit(1)
    run(podman, "create", "--name", "mobsec-apk-extract", APK_BUILDER_IMAGE,
        "true", show=False)
    try:
        run(podman, "cp", "mobsec-apk-extract:" + apk_src,
            str(DIST_DIR / "GlowMartMobile.apk"), show=False)
    finally:
        run(podman, "rm", "mobsec-apk-extract", check=False, show=False)
    print(f"[*] APK written to {DIST_DIR / 'GlowMartMobile.apk'}")
    print("    Available to students at http://appstore:8001/apk/ (in-network) or")
    print("    http://appstore.<SERVICE_DOMAIN>:<PROXY_PORT>/apk/ when exposed.")


def print_url() -> None:
    addr = env_val("CTFD_BIND_ADDR", "127.0.0.1")
    port = env_num("CTFD_BIND_PORT", 8000)
    api_port = env_num("API_BIND_PORT", 3000)
    print(f"CTFd (local):     http://{addr}:{port}/")
    print(f"API (HTTP loop):  http://10.0.2.2:{api_port}/  (from the Android emulator)")
    print(f"API (HTTPS loop): https://10.0.2.2:{env_num('API_HTTPS_PORT', 3443)}/  (pinned lab)")
    if env_val("EXPOSE_TARGETS") == "1":
        domain = env_val("SERVICE_DOMAIN", "your-ip.sslip.io")
        print(f"CTFd (proxy):     http://ctfd.{domain}:{env_num('PROXY_PORT', 8080)}/")
        print(f"App store:        http://appstore.{domain}:{env_num('PROXY_PORT', 8080)}/")


# --------------------------------------------------------------------------- #
# Windows firewall + portproxy
# --------------------------------------------------------------------------- #
def _open_ports() -> list[int]:
    ports = {
        env_num("CTFD_BIND_PORT", 8000),
        env_num("PROXY_PORT", 8080),
        env_num("API_BIND_PORT", 3000),
        env_num("API_HTTPS_PORT", 3443),
    }
    return sorted(ports)


def _clear_portproxy() -> None:
    """Remove every existing v4tov4 portproxy entry."""
    try:
        out = subprocess.run(["netsh", "interface", "portproxy", "show", "v4tov4"],
                             capture_output=True, text=True).stdout
    except FileNotFoundError:
        return
    for line in out.splitlines():
        t = [tok for tok in re.split(r"\s+", line.strip()) if tok]
        if len(t) >= 4 and re.match(r"^\d+(\.\d+){3}$", t[0]) and t[0] != "Address":
            subprocess.run(["netsh", "interface", "portproxy", "delete", "v4tov4",
                            f"listenaddress={t[0]}", f"listenport={t[1]}"],
                           capture_output=True)


def lan_open() -> None:
    ensure_admin_windows()
    ports = _open_ports()
    print("[*] Opening LAN exposure via single-entry reverse proxy...")
    print(f"    Open ports: {', '.join(map(str, ports))}")
    _clear_portproxy()
    for p in ports:
        for name in (f"MobSec proxy {p}", f"CTFd {p}", f"MobSec api {p}"):
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule",
                            f"name={name}"], capture_output=True)
        subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name=MobSec proxy {p}", "dir=in", "action=allow",
             "protocol=TCP", f"localport={p}", "profile=any"])
        subprocess.run(["netsh", "interface", "portproxy", "add", "v4tov4",
                        "listenaddress=0.0.0.0", f"listenport={p}",
                        "connectaddress=127.0.0.1", f"connectport={p}"], check=True)
    print("[*] Done. Ports open on 0.0.0.0 (advertised via SERVICE_DOMAIN hostnames).")


def lan_close() -> None:
    ensure_admin_windows()
    ports = _open_ports()
    print("[*] Closing LAN exposure...")
    _clear_portproxy()
    for p in ports:
        for name in (f"MobSec proxy {p}", f"CTFd {p}", f"MobSec api {p}"):
            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule",
                            f"name={name}"], capture_output=True)
    for name in ("CTFd 8000 LAN", "CTFd 8000 Public"):
        subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule",
                        f"name={name}"], capture_output=True)
    print("[*] Done. Exposed ports closed; lab is localhost-only again.")


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def health(podman: str) -> None:
    print("== Container status ==")
    run(podman, "compose", *compose_files(), "ps")
    print("\n== Lab network ==")
    p = run(podman, "network", "exists", LAB_NET, check=False, show=False)
    if p.returncode == 0:
        run(podman, "network", "inspect", "--format",
            "{{.Name}}  internal={{.Internal}}", LAB_NET)
    else:
        print(f"[!] Network '{LAB_NET}' does not exist. Start the lab first.")
    print("\n== Host port bindings ==")
    run(podman, "ps", "--filter", "name=ctfd", "--format", "table {{.Names}}\t{{.Ports}}")
    print("\n== Isolation check ==")
    mode = "ACTIVE (reachable from your LAN)" if env_val("EXPOSE_TARGETS") == "1" else "isolated to localhost"
    print(f"    EXPOSE_TARGETS={env_val('EXPOSE_TARGETS', '0')} -> {mode}")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="lab.py", description="mobsec-ctf-lab CLI")
    subs = ap.add_subparsers(dest="command", required=True)
    subs.add_parser("setup", help="first-time install: build, start, provision")
    subs.add_parser("start", help="bring the lab up (idempotent, provisions)")
    subs.add_parser("stop", help="stop the lab (keeps the DB volume)")
    subs.add_parser("reset", help="destroy everything (incl. DB volume), rebuild fresh")
    subs.add_parser("health", help="show container/network/port status")
    subs.add_parser("build-apk", help="build the vulnerable GlowMart Mobile APK")
    subs.add_parser("expose", help="[admin Windows] open firewall+portproxy for LAN")
    subs.add_parser("close", help="[admin Windows] close firewall+portproxy")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    if args.command in ("expose", "close"):
        (lan_open if args.command == "expose" else lan_close)()
        return

    podman = require_podman()
    ensure_env()

    if args.command == "build-apk":
        build_apk(podman)
        return

    if args.command == "setup":
        run(podman, "compose", *compose_files(), "up", "-d", "--build")
        if wait_ctfd(podman):
            provision(podman)
        else:
            sys.exit(1)
        print_url()
        print(f"First-time admin: {env_val('CTFD_ADMIN_EMAIL')}")
        print("Change the admin password and CTFd SECRET_KEY after first login.")
        print("Don't forget: python scripts/lab.py build-apk  (build the APK!)")

    elif args.command == "start":
        run(podman, "compose", *compose_files(), "up", "-d")
        if wait_ctfd(podman):
            provision(podman)
        else:
            print("[!] CTFd not ready; skipping provisioning. Check logs.", file=sys.stderr)
        print_url()

    elif args.command == "stop":
        print("[*] Stopping the lab (keeping the CTFd database volume)...")
        run(podman, "compose", *compose_files(), "down")
        print("[*] Stopped.")

    elif args.command == "reset":
        ans = input("This destroys ALL lab data (challenges, accounts, submissions). Continue? [y/N] ")
        if ans.strip().lower() not in ("y", "yes"):
            print("Aborted.")
            return
        print("[*] Removing containers, volumes, and the isolated network...")
        run(podman, "compose", *compose_files(), "down", "-v")
        print("[*] Rebuilding and starting...")
        run(podman, "compose", *compose_files(), "up", "-d", "--build")
        if wait_ctfd(podman):
            provision(podman)
        else:
            print("[!] CTFd not ready after reset; check logs.", file=sys.stderr)
        print("[*] Reset complete.")
        print_url()

    elif args.command == "health":
        health(podman)


if __name__ == "__main__":
    main()