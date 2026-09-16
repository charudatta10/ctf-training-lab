# GlowMart Mobile — Statement of Work (SOW)

**Project:** Mobile Application Security Assessment of the GlowMart Mobile App
**SOW Ref:** GLOW-2026-MOB-01

## 1. Client
- **Name:** GlowMart Inc.
- **Contact:** A. Reyes, Security Director — areyes@glowmart.example

## 2. Consultant
- **Name:** [Student]
- **Engagement Manager:** Course Instructor

## 3. Objectives
1. Reverse-engineer the Android application (manifest, resources, source).
2. Identify stored, encoded, and crypto-hidden secrets via static analysis.
3. Demonstrate runtime weaknesses (pinning, root detection, logging,
   storage) with dynamic instrumentation.
4. Produce a professional mobile security assessment report.

## 4. Scope
- Targets: `GlowMartMobile.apk`, `appstore`, `api`.
- Secondary material: `libglowmart.so` (native library) and the
  `glowmart.db` / SharedPreferences data the app creates.
- All other systems are OUT OF SCOPE (see the authorization document).

## 5. Scope Exclusions
- Public Internet, host LAN, campus/Wi-Fi, the CTFd platform, and other
  participants' emulators/devices.

## 6. Deliverables
- A written mobile security assessment report using the course template.
- A findings register with risk ratings and evidence.
- Evidence files (decompiler output, MobSF report, Frida sessions,
  logcat captures, pulled databases) supporting each finding.

## 7. Timeline
- Testing window: **2026-09-07 to 2026-12-18** (see authorization doc).
- Final report due: **2026-12-18 17:00**.

## 8. Testing Restrictions
- Lab hours only, Mon–Fri 08:00–17:00.
- No destructive or denial-of-service testing.
- No out-of-scope scanning.
- No persistence, malware, or lateral movement off `mobsec-lab-net` or your
  own emulator.

## 9. Assumptions
- The environment is a fully authorized, contained lab.
- Testers have credentials to access the CTFd platform and lab network,
  plus terminal/adb access to the course emulator.
- A rooted/emulated test device and the interception tools (Frida, Burp/
  mitmproxy) are provided by the course.

## 10. Reporting Requirements
- Follow the course report template (all sections).
- Rate every finding with a severity (CVSS v3.1 base score + qualitative).
- Provide remediation for each finding.
- Submit the report and evidence before the deadline.

---

**Signature (Client):** Ann Rei Reyes · Date: 2026-09-03
**Signature (Consultant):** ____________________ · Date: ____________