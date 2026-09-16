# mobile-security-ctf-lab

A **local, isolated mobile app security CTF laboratory** for the *Network
Security* course (topic: **Android Mobile App Security**).

Everything runs locally via **Podman** and **CTFd** on a private, isolated
container network. Students analyze a deliberately-vulnerable Android app
(**GlowMart Mobile**), a fake app store, and a mobile backend. There are **no
cloud dependencies** and the vulnerable targets are **never exposed to the
public internet or your LAN** by default.

> ⚠️ **Security warning — read this first.**
> This repository intentionally builds *vulnerable* applications for
> educational use only. Attack **only** the systems explicitly in scope
> (`GlowMartMobile.apk`, `appstore`, `api`) and **only** inside the isolated
> lab network. See [docs/lab-rules.md](docs/lab-rules.md).

---

## Purpose

Give students a complete, hands-on Android security course across **three
modules**:

1. **Android Architecture** — APK structure, the manifest, components,
   permissions, signing, app sandboxing.
2. **Static Analysis** — reverse engineering (`jadx`, `apktool`), hardcoded
   secrets, insecure crypto, obfuscation, MobSF, code-signing verification.
3. **Dynamic Analysis** — Frida instrumentation, SSL-pinning bypass,
   root-detection bypass, Burp/mitmproxy interception, logcat monitoring,
   local storage (SQLite / SharedPreferences) forensics.

Students find **flags** embedded in the app's source, manifest, resources,
native library, traffic, and local storage, and deliver a final **mobile
security assessment report**.

## Learning Objectives

1. Decompile the APK and read the AndroidManifest; identify exported
   components and their risks.
2. Enumerate resources (strings/assets/raw) and content providers.
3. Use jadx/apktool, MobSF, `strings`, and CyberChef to extract secrets.
4. Break weak encodings and insecure symmetric crypto.
5. Bypass SSL pinning and root detection with Frida; intercept traffic.
6. Monitor `logcat` leaks and pull/inspect local storage (SQLite,
   SharedPreferences).
7. Produce a professional mobile security assessment report.

---

## Architecture

```
                Host (attacker workstation + emulator)
                adb / jadx / apktool / Frida / MobSF / Burp
                           |
     http://127.0.0.1:8000 |
                           v
                    +-----------+
                    |   CTFd    |   (localhost only)
                    +-----------+
                           |
                 mobsec-lab-net  (isolated, internal, no internet)
                           |
          +---------------+---------------+
          |               |               |
          v               v               v
       appstore         api           (APK target)
       (APK host)   (HTTP + pinned      GlowMartMobile.apk
                     HTTPS backend)      installed on emulator
```

- **CTFd** — the challenge / flag platform (with MariaDB + Redis).
- **appstore** — serves `GlowMartMobile.apk` (and attachment dumps).
- **api** — mobile backend: `:3000` HTTP, `:3443` pinned HTTPS.
- **app** — the vulnerable Android app students reverse and instrument.

All target traffic happens **only** on the isolated `mobsec-lab-net` network.
See [docs/architecture.md](docs/architecture.md) for details and a Mermaid
diagram, including how the emulator reaches `api` via `10.0.2.2`.

---

## Prerequisites

- **Podman** 4.x+ with a running machine (`podman machine start`) and Podman
  Compose support. Windows/macOS use the built-in WSL/VM machine.
- ~6 GB free RAM and ~15 GB disk (more if you build the APK in-container).
- **Android toolchain for the student machine**: `adb`, and per-module tools
  (`jadx`/`apktool`, MobSF, Frida, Burp/mitmproxy). Also an **Android
  emulator/device** (a plain emulator is fine — no root needed for most CTFs).
- The **vulnerable APK** built once:
  ```
  python scripts/lab.py setup      # first-time: .env, build, start, provision
  python scripts/lab.py build-apk  # build the APK (several GB download, needs internet)
  ```

---

## Installation & Startup

Requires Python 3.8+ and Podman. A single cross-platform CLI drives the whole
lab — no Git Bash or WSL needed (run from any terminal/PowerShell/cmd):

```bash
python scripts/lab.py setup      # first-time: creates .env, builds, starts, provisions
python scripts/lab.py start      # subsequent startups (idempotent)
```

Available subcommands: `setup`, `start`, `stop`, `reset`, `health`, `build-apk`,
`expose`, `close` (see `python scripts/lab.py --help`).

The CLI:

1. Creates `.env` from `.env.example` if missing.
2. Build/start all containers on the isolated network.
3. Waits for CTFd to become healthy.
4. Automatically creates the admin account and **provisions every challenge**
   (categories, descriptions, points, hints, flags, attachments).

> `expose` and `close` touch the Windows Firewall/portproxy and must be run
> from an elevated (Administrator) PowerShell. Everything else runs as the
> normal user.

### CTFd access

Open **http://127.0.0.1:8000/** in your browser.

- Admin account (first run): the email/password in `.env`
  (`CTFD_ADMIN_EMAIL` / `CTFD_ADMIN_PASSWORD`).
- **Change the admin password and `CTFD_SECRET_KEY`** before real use.

### Manual Podman commands (no helper scripts)

```bash
podman compose up -d --build          # start the whole lab
podman compose down                    # stop (keep DB volume)
podman compose down -v                 # stop + DELETE all data
podman compose ps                      # status
podman compose logs -f ctfd            # CTFd logs
```

---

## LAN / Classroom access (single-entry reverse proxy)

By default the lab is **localhost-only** and safe: targets have no host ports.
To let **30+ students** on your network connect through ONE entry point, use
the bundled Caddy reverse proxy:

1. Edit `.env`:
   - `EXPOSE_TARGETS=1`
   - `SERVICE_DOMAIN=<your-LAN-IP>.sslip.io`  (e.g. `10.250.12.246.sslip.io`)
2. Start with the overlay: `python scripts/lab.py start` (reads `EXPOSE_TARGETS`).
3. Allow inbound ports through Windows Firewall **and** add portproxys
   (run as Administrator PowerShell):
   `python scripts/lab.py expose`

Students use hostname-based URLs (no DNS setup):

```
CTFd:     http://ctfd.<IP>.sslip.io:8080/
App store:http://appstore.<IP>.sslip.io:8080/apk/GlowMartMobile.apk
API:      http://api.<IP>.sslip.io:8080/   (HTTPS pinned endpoint via app :3443)
```

**Important:** This reaches anyone on your LAN. Keep `EXPOSE_TARGETS=0`
(and run `python scripts/lab.py close`) to restore the isolated default.

To disable LAN exposure later:
```powershell
python scripts/lab.py close     # admin: close firewall rules + forwards
# then set EXPOSE_TARGETS=0 in .env and restart: python scripts/lab.py start
```

---

## Student Workflow

1. Open **http://127.0.0.1:8000/** and log in (or register) on CTFd.
2. Install the APK on your emulator/device:
   ```
   adb install GlowMartMobile.apk
   adb shell am start -n com.glowmart.mobile/.MainActivity
   ```
3. Work the three modules in order:
   **Android Architecture → Static Analysis → Dynamic Analysis**.
4. Reach the backend from the emulator at `10.0.2.2` (HTTP `:3000`,
   pinned HTTPS `:3443`).
5. Capture flags + evidence and deliver the final **assessment report**
   (see [reports/template.md](reports/template.md)).

Detailed methodology without flags: [docs/student-guide.md](docs/student-guide.md).

---

## Reset Procedure

To start the class clean (fresh flags, no student accounts/submissions):

```bash
python scripts/lab.py reset
```

This removes containers **and** the database volume, rebuilds, and re-provisions.
It prompts for confirmation first.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| CTFd unreachable | Machine not started / not healthy | `podman machine start`; `podman compose ps`; `podman compose logs ctfd` |
| Challenges missing | Provisioner didn't run / CTFd wasn't ready | `python scripts/lab.py start` again (idempotent) |
| APK missing on appstore | APK not built | `python scripts/lab.py build-apk` (or drop a hand-built APK in `targets/appstore/www/apk/`) |
| Emulator can't reach api | Wrong host alias | Use `http://10.0.2.2:3000` / `https://10.0.2.2:3443` |
| `adb devices` empty | emulator not started / USB off | Start emulator; `adb kill-server && adb devices` |
| SSL-pinning bypass fails | Proxy CA not installed on device | Install Burp/mitmproxy CA on the emulator first, then bypass |
| Port 8000 in use | Another process | Change `CTFD_BIND_PORT` in `.env` |
| `podman compose` not found | Compose provider missing | See `docs/instructor-guide.md` |

---

## Documentation

- [docs/architecture.md](docs/architecture.md) — topology + Mermaid diagram + isolation model
- [docs/student-guide.md](docs/student-guide.md) — methodology without flags (share with students)
- [docs/instructor-guide.md](docs/instructor-guide.md) — full solutions & administration (**instructor only**)
- [docs/lab-rules.md](docs/lab-rules.md) — laboratory rules of engagement (**read first**)
- [docs/assessment-rubric.md](docs/assessment-rubric.md) — grading rubric
- [reports/template.md](reports/template.md) — mobile assessment report template
- [challenges/README.md](challenges/README.md) — challenge registry & how to add challenges

## License

[MIT](LICENSE). This project is an educational tool. The author is not
responsible for misuse.