# AUTHORIZATION TO TEST — PETITION OF AUTHORITY

**Issue Date:** 2026-09-03
**Valid Through:** 2026-12-31

This document authorizes a mobile application security assessment of the
systems described below. No testing may be performed outside the scope
defined here.

## Client
- **Organization:** GlowMart Inc.
- **Point of contact:** A. Reyes — areyes@glowmart.example (authorizing sponsor)

## Authorized Consultant
- **Engager:** [Student name]
- **Role:** Independent security consultant engaged under the GlowMart Mobile SOW.

## In-Scope Systems (authorized to test)
Only these systems are explicitly authorized:

| Target          | Description                                                    |
|-----------------|----------------------------------------------------------------|
| `GlowMartMobile.apk` | The vulnerable Android app (`com.glowmart.mobile`) installed on the course emulator/device |
| `appstore`      | App store serving the APK and attachments                      |
| `api`           | Mobile backend (`:3000` HTTP, `:3443` pinned HTTPS)            |

- **Authorized network:** the isolated `mobsec-lab-net` only.

## Out-of-Scope Systems (NOT authorized — do not touch)
- Any host on the public Internet.
- The host LAN / Wi-Fi / campus network.
- The CTFd platform (`ctfd`), its database (`db`), and cache (`cache`).
- The emulator/device of any other student.

## Testing Window
- **Start:** 2026-09-07 08:00 local
- **End:** 2026-12-18 17:00 local
- Testing only within course lab hours, Mon–Fri 08:00–17:00.

## Rules of Engagement
1. Attack ONLY the systems explicitly listed as in-scope above.
2. No destructive actions: no data deletion, no denial of service,
   no persistence, no malware — even on your own emulator.
3. No credential harvesting outside the lab.
4. Report any out-of-scope contact immediately; stop testing that vector.
5. All activity is limited to the isolated `mobsec-lab-net` network and your
   own emulator/device.

## Restrictions
- Do NOT scan or access the host machine or other students' devices.
- Do NOT test external/third-party services.
- Capture evidence for every finding; nothing can be claimed without it.

---

**Ann Rei Reyes, Sponsor, GlowMart Inc.**