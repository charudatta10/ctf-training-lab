# 03 - Dynamic Analysis (CTF Set 3: "Runtime & Intercept")

Challenge definitions live in `challenges/challenges.json` (category:
`Dynamic Analysis`).

Objectives for this set:

- Bypass SSL/TLS certificate pinning with Frida and intercept the app's API
  call in Burp Suite / mitmproxy.
- Bypass root detection so a locked vault screen unlocks.
- Hook a function with Frida and dump a runtime-decrypted secret.
- Catch a debug-log flag in `logcat`.
- Pull and inspect local storage (`SharedPreferences` + SQLite) at runtime.

The app's backend (`api` target) serves the pinned endpoint at
`https://10.0.2.2:3443` from the emulator.

Tools: Frida + Objection, Burp Suite/mitmproxy, `adb`, rooted emulator/device.
See `docs/student-guide.md`.