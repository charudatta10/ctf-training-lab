# Reverse proxy (Caddy) - single-entry LAN access

This optional service is the lab's **single network entry point** when the
instructor wants a classroom/30-student setup. It fronts CTFd and the mobile
HTTP services behind ONE exposed port, routing by `Host` header using
`*.sslip.io` hostnames (no DNS / hosts-file setup for students).

- `Caddyfile` - routing config (see file header for the full URL table).

## How it's used

Only active when the `compose.lan.yml` overlay is loaded, i.e. when
`EXPOSE_TARGETS=1` (see [.env.example](../.env.example) and
[README.md](../README.md) -> "LAN / Classroom access").

```bash
# .env
EXPOSE_TARGETS=1
SERVICE_DOMAIN=10.250.12.246.sslip.io   # <your-LAN-IP>.sslip.io
```

Then start with the overlay and open Windows Firewall/proxy:
```bash
python scripts/lab.py start      # reads EXPOSE_TARGETS, loads compose.lan.yml
python scripts/lab.py expose     # admin PowerShell: firewall + portproxy
```

## Student URLs (replace IP)

| Service    | URL |
|------------|-----|
| CTFd       | `http://ctfd.<IP>.sslip.io:8080/` |
| App store  | `http://appstore.<IP>.sslip.io:8080/` |
| API (HTTP) | `http://api.<IP>.sslip.io:8080/` |
| API (HTTPS)| `https://api.<IP>:3443/` (pinned-TLS lab; emulator uses `10.0.2.2:3443`) |

## Emulator access note

The Android emulator reaches the host's loopback through the special alias
`10.0.2.2`. With the default loopback bind, the emulator can use:

- `http://10.0.2.2:3000/` for the plain HTTP backend, and
- `https://10.0.2.2:3443/` for the pinned-TLS endpoint.

When `EXPOSE_TARGETS=1`, those ports are also reachable from LAN devices via
the host's LAN IP (`API_BIND_ADDR=0.0.0.0` overlay).

## Limitations

- **HTTP only on the proxy.** No TLS by default (classroom simplicity, avoids
  self-signed warnings for many students). To enable HTTPS on 443, switch the
  site block to `https://` and remove `auto_https off`.
- The **api HTTPS port is not proxied** (students use it directly); it is
  re-published by the `compose.lan.yml` overlay.