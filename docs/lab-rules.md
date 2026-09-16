# Laboratory Rules of Engagement

> ## ⚠️ Attack only the systems explicitly included in this laboratory.

This is an **educational cyber range** for mobile app security. You are
authorized to test **only** the application and backend described below, and
**only** for the duration of the course.

## Authorized targets (in scope)

| Target        | Description                                                    |
|---------------|----------------------------------------------------------------|
| `GlowMartMobile.apk` | The deliberately-vulnerable Android app (`com.glowmart.mobile`) installed on your course emulator/device |
| `appstore`    | The app store that serves the APK / attachments                |
| `api`         | The mobile backend (`:3000` HTTP, `:3443` pinned HTTPS)        |

The isolated network is `mobsec-lab-net`. The authorized corporation is
`glowmart.trust` (fictional).

## Explicitly OUT of scope — do not touch

- The **CTFd** platform (`ctfd`), its database (`db`), and cache (`cache`).
- The **host machine** and anything on your LAN / Wi-Fi / campus network.
- Anything on the **public internet**.
- Other participants' emulators/devices, or their `adb` sessions.

## Hard rules

1. **Attack only in-scope systems.** No exceptions.
2. **No destructive actions.** No data deletion, no denial-of-service, no
   defacement, no persistence, no malware (including on your own emulator).
3. **No credential theft outside the lab.** Do not exfiltrate anything.
4. **No lateral movement** off the isolated `mobsec-lab-net` network
   (or off your own emulator).
5. **Do not expand scope.** If a scan touches an out-of-scope system, stop
   that vector immediately and inform the instructor.
6. **Capture evidence** for every finding. Nothing may be claimed without it.

## Consequences

Violating these rules (e.g., scanning the host/LAN/internet, attacking CTFd)
risks:
- Invalidated lab results and a failing grade for the assessment.
- Administrative/network consequences (your machine may be isolated).

If you are ever unsure whether a target is in scope, **ask the instructor first.**

---

By proceeding you acknowledge this laboratory is authorized, isolated, and
limited to the systems listed above.