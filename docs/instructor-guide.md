# Instructor Guide

> **Instructor-only.** This document contains complete solutions, flags, and
> hints. Do not share it with students. Keep flags and solutions out of the
> student-facing material.

---

## 1. Architecture at a glance

- **CTFd** (`ghcr.io/ctfd/ctfd:3.7.4`) + **MariaDB** + **Redis**.
- Mobile targets built locally:
  - `app` — Android source + builder → `GlowMartMobile.apk` (analyzed by students).
  - `appstore` — serves the APK / attachments (`:8001`).
  - `api` — Flask backend, HTTP `:3000` + pinned TLS `:3443`.
- All on the isolated `mobsec-lab-net` bridge (`internal: true`).
- `ctfd` binds loopback `127.0.0.1:8000`; `api` binds loopback `3000`/`3443`.

See [architecture.md](architecture.md).

## 2. Installation

Prereqs: Python 3.8+, Podman 4+ (`podman --version`), a running machine
(`podman machine start` on Windows/macOS), and Podman Compose.

```bash
python scripts/lab.py setup        # first-time: .env, build, start, provision
python scripts/lab.py build-apk    # build the vulnerable APK (needs internet, several GB)
```

The APK builder (`targets/app/Dockerfile`) installs the Android SDK + NDK
inside a container. If you prefer, build `GlowMartMobile.apk` in Android
Studio and drop it at `targets/appstore/www/apk/GlowMartMobile.apk` instead —
`lab.py build-apk` is just a convenience.

## 3. Starting & resetting the lab

```bash
python scripts/lab.py start        # start + (re)provision (idempotent)
python scripts/lab.py stop         # stop, keep DB volume
python scripts/lab.py reset        # DESTROY all data, rebuild, re-provision
python scripts/lab.py health       # status + isolation verification
python scripts/lab.py expose|close # [admin] open/close LAN firewall+portproxy
```

CTFd URL: **http://127.0.0.1:8000/**

Admin (first run): from `.env` → `CTFD_ADMIN_EMAIL` / `CTFD_ADMIN_PASSWORD`.
**Change the admin password and `CTFD_SECRET_KEY` before real use.**

## 4. Student onboarding

1. Provide the lab running and the APK built.
2. Students install on an emulator/device:
   ```bash
   adb install GlowMartMobile.apk
   ```
3. Point them to `docs/student-guide.md` and `docs/lab-rules.md`.
4. Backend reachability for the emulator:
   - HTTP: `http://10.0.2.2:3000`
   - HTTPS (pinned): `https://10.0.2.2:3443`
5. Classroom LAN: `EXPOSE_TARGETS=1` + `SERVICE_DOMAIN=<ip>.sslip.io` +
   `python scripts/lab.py expose`; hand out the hostname URLs
   (`ctfd.`, `appstore.`, `api.` subdomains).

> Suggested: attach `GlowMartMobile.apk` to the first challenge in each
> module so students can get it straight from CTFd too.

## 5. Challenge map, flags & solutions

| # | Challenge | Flag | Module/tool | Solution summary |
|---|-----------|------|-------------|------------------|
| 1 | arch-manifest | `flag{manifest_exported_leak}` | jadx/apktool | Manifest meta-data `com.glowmart.mobile.flag` on exported `.SecretActivity` |
| 2 | arch-intent-leak | `flag{activity_intent_extra_leak}` | jadx + adb | `am start -n com.glowmart.mobile/.DebugLeakActivity --es auth_override grant` (flag also in strings.xml) |
| 3 | arch-resources | `flag{resource_hidden_secret}` | jadx/apktool | `res/raw/secret_codebook.json` → `secret` |
| 4 | arch-provider | `flag{provider_unprotected}` | adb | `adb shell content query --uri content://com.glowmart.mobile.secrets/flag` |
| 5 | static-hb-key | `flag{static_hardcoded_api_key}` | jadx | `AuthTokenProvider.API_KEY` |
| 6 | static-encoded | `flag{weak_encoding_xor_base64}` | CyberChef | Base64-decode `Strings.ENCODED_BANNER = "ZmxhZ3t3ZWFrX2VuY29kaW5nX3hvcl9iYXNlNjR9"` |
| 7 | static-crypto | `flag{static_aes_ecb_key}` | CyberChef | AES-128-ECB, key `0123456789abcdef`, ciphertext `MRGeLCEOn3ijvPto5JaxAB9bj2gCfRBw9AI65EReaZA=` → plaintext |
| 8 | static-mobsf | `flag{mobsf_scan_discovered_secret}` | MobSF | Hardcoded-secret finding; value also in `res/values/secrets.xml` (`api_secret_key`) |
| 9 | static-native | `flag{native_so_string_discovery}` | strings | `strings libglowmart.so \| grep flag` (dump at appstore `/apk/libglowmart.strings.txt`) |
| 10 | dyn-pinning | `flag{ssl_pinning_bypassed}` | Frida + Burp/mitmproxy | Bypass `PinnedApiClient` pin check → intercept `GET https://10.0.2.2:3443/api/v1/mobile/banner` |
| 11 | dyn-root | `flag{root_check_bypassed}` | Frida | Hook `RootCheck.isDeviceRooted→false`; open `VaultActivity` (flag in strings.xml `vault_flag`) |
| 12 | dyn-frida-decrypt | `flag{frida_runtime_decrypt_dump}` | Frida | Hook/call `Vault.getDecryptedSecret(4242)`; blob XOR key = `userId & 0xFF` (0x92) |
| 13 | dyn-logcat | `flag{logcat_debug_leak}` | logcat | `MainActivity` logs `GlowMartDebug ... flag{logcat_debug_leak}` on start |
| 14 | dyn-storage | `flag{local_database_forensics}` | adb pull/sqlite | `databases/glowmart.db` table `secrets`; `shared_prefs/session_data.xml` key `remembered_flag` |

**All flags use case-insensitive static matching in CTFd.**

### Crypto boxes included in the app

- `Strings.ENCODED_BANNER` → `ZmxhZ3t3ZWFrX2VuY29kaW5nX3hvcl9iYXNlNjR9`
- `CryptoBox` → AES-128-ECB, key `0123456789abcdef`, sealed base64
  `MRGeLCEOn3ijvPto5JaxAB9bj2gCfRBw9AI65EReaZA=`
- `Vault.BLOB` → base64 of `flag{frida_runtime_decrypt_dump}` XOR `0x92`
  (`9P7z9en04Pv2883g5/zm+//3zfb38eDr4ubN9uf/4u8=`)

### API backend

- `GET /health`
- `GET /api/v1/mobile/session`
- `GET /api/v1/mobile/banner` → `{"flag": "flag{ssl_pinning_bypassed}", ...}` (HTTPS, pinned)

### The pinned cert

`targets/api/certs/` holds the lab self-signed keypair. The app pins
`PIN_SHA256 = +zSd3zPVaGL3CmRb7lO45beFNK/lw+4D+fb43RZg91Y=`
(sha256 of the SPKI DER). If you regenerate the cert, update both the api
folder and `PinnedApiClient.PIN_SHA256` and rebuild the APK.

## 6. Common student mistakes

1. **Attacking out of scope** (host/LAN/internet/CTFd) — remind them of
   `lab-rules.md`.
2. **Not installing the APK** — some challenges (logcat, storage, pinning)
   need a running app, not just static analysis.
3. **Guessing flags instead of capturing evidence.**
4. **Missing the runtime aspect** — M3 challenges are runtime, not static;
   Frida/emulator needed.
5. **Reusing objects** — e.g., expecting `PinnedApiClient.fetchBanner()` to
   fail "because cleartext" — it is HTTPS with a custom pin; the failure only
   appears once a proxy is in front.
6. **Overcounting / under-documenting findings** in the final report.

## 7. Troubleshooting

| Problem | Resolution |
|---------|-----------|
| CTFd won't start | `podman compose logs ctfd`; machine running; port 8000 free. |
| Challenges not visible | Provisioner needs CTFd ready; re-run `python scripts/lab.py start`. |
| APK missing from appstore | Run `python scripts/lab.py build-apk` (or drop a hand-built APK into `targets/appstore/www/apk/`). |
| Emulator can't reach api | Verify `10.0.2.2:3000` from the emulator; on LAN use the host IP. |
| Pinning bypass "didn't work" | Confirm Burp CA installed AND emulator proxied BEFORE re-triggering "Sync". |
| SQLite pull fails | Use a debuggable build (`app-debug.apk`) + `adb exec-out run-as`, or a rooted emulator. |
| `podman compose` missing | Install a Compose provider; see [README](../README.md). |
| Want a clean class | `python scripts/lab.py reset` (wipes all data). |

## 8. How to add a challenge

1. Add an entry to `challenges/challenges.json` (see `challenges/README.md`):
   `id`, `category`, `name`, `description`, `value`, `difficulty`, `flag`,
   `hints[]`.
2. (Optional) modify the app source in `targets/app` to surface the flag,
   then rebuild the APK.
3. Re-provision: `python scripts/lab.py start` (idempotent).

To change points/hints/descriptions, edit the JSON and re-provision after
deleting the old challenge in the CTFd admin UI (the provisioner only **adds**
missing challenges and skips existing names).