# Challenges

All challenges are defined once, in **`challenges/challenges.json`**, which is
the single source of truth. `scripts/provision.py` reads this registry and
creates/updates the challenges inside CTFd (categories, descriptions, points,
hints, flags).

The directories `01-android-architecture/`, `02-static-analysis/`,
`03-dynamic-analysis/` contain the module brief and supporting notes:

- `01-android-architecture/`  — APK structure, manifest, resources, providers.
- `02-static-analysis/`       — jadx/apktool, MobSF, crypto, native inspection.
- `03-dynamic-analysis/`      — Frida, Burp/mitmproxy, logcat, local storage.

## Challenge modules

| Set | CTFd Category           | Challenges | Difficulty |
|-----|-------------------------|-----------|------------|
| 1   | Android Architecture    | 4         | L1-L2      |
| 2   | Static Analysis         | 5         | L2-L3      |
| 3   | Dynamic Analysis        | 5         | L2-L3      |

## Adding a challenge

1. Add an entry to `challenges/challenges.json` with fields:
   `id`, `category`, `name`, `description`, `value`, `difficulty`, `flag`,
   `hints` (array), and optional `file` (path to attach).
2. Re-run the provisioner:
   ```
   python scripts/lab.py start   # idempotent; will create the new challenge
   ```

The provisioner is idempotent: re-running it will not duplicate challenges.

## Flag security note

Flags are stored in `challenges.json` (needed by CTFd for validation). If you
keep it in a shared repository, treat it as instructor-only material, matching
the otherwise-public challenge content.