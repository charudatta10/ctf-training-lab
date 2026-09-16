# CTFd integration

CTFd is the central challenge/flag platform for the lab. This folder is a
thin documentation + data mount point — **we do not fork or modify CTFd
source code**.

## What lives here

- `data/uploads/` — uploaded challenge files (created at runtime, gitignored).
- `data/logs/` — CTFd logs (runtime, gitignored).
- This README.

## How configuration works

CTFd is configured entirely via **environment variables** (see `compose.yml`
and `.env`). Challenge content is provisioned through the **public CTFd API**
by `scripts/provision.py`, driven by `challenges/challenges.json`.

## Key configured options

| Setting | Value | Notes |
|---------|-------|-------|
| Image | `ghcr.io/ctfd/ctfd:3.7.4` | - |
| Mode | `teams` | default |
| DB | MariaDB (in-network) | reachable only on `mobsec-lab-net` |
| Cache | Redis (in-network) | - |
| Host port | `127.0.0.1:8000` | local-only by default |

## Categories ↔ mobile modules

CTFd categories map to the course modules so students can navigate by
methodology:

- **Android Architecture** — Set 1, "Recon & Structure" (4 challenges)
- **Static Analysis** — Set 2, "Reverse & Extract" (5 challenges, incl. MobSF)
- **Dynamic Analysis** — Set 3, "Runtime & Intercept" (5 challenges)

## Re-provisioning

Challenges are created once by name; re-provisioning is idempotent.

```bash
python scripts/lab.py start        # re-syncs challenges each start
```

> The provisioner only **adds** missing challenges and skips existing
> names — edit/delete a challenge in the CTFd admin UI if you need to change
> an existing one.

## Admin

First-run admin is created automatically by `scripts/provision.py` from the
`.env` values (`CTFD_ADMIN_EMAIL` / `CTFD_ADMIN_PASSWORD`).
`CTFD_SECRET_KEY` should be changed before any real use.

## Out of scope

- We do **not** expose CTFd's DB/cache to the host (only CTFd's web port is
  mapped, on localhost).
- CTFd itself is **out of scope** for students (see `docs/lab-rules.md`).