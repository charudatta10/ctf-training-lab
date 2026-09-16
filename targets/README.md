# Vulnerable lab targets

The mobile-lab targets, built locally and attached to the isolated
`mobsec-lab-net` network. The `api` service additionally publishes loopback
host ports so an Android emulator can reach it.

| Target    | Directory         | Technology              | In-network services        | Educational role |
|-----------|-------------------|-------------------------|----------------------------|------------------|
| `app`     | `targets/app`     | Android (Gradle + NDK)  | built → `appstore`         | the vulnerable app itself (built with `lab.py build-apk`) |
| `appstore`| `targets/appstore` | Python http.server      | :8001 HTTP (static)        | serves the APK + attachments to students |
| `api`     | `targets/api`     | Flask + self-signed TLS | :3000 HTTP, :3443 HTTPS    | backend the app talks to (Module 3 labs) |

Each directory contains its own `Dockerfile` and application code. The
`app` module produces the actual APK that students analyze; all flags and
their locations are documented in `docs/instructor-guide.md`
(instructor-only).

> **Safety:** these are deliberately vulnerable. Keep them inside the
> isolated network. The committed TLS key in `targets/api/certs/` is a lab
> artifact and must never be used anywhere else.