# 01 - Android Architecture (CTF Set 1: "Recon & Structure")

Challenge definitions live in `challenges/challenges.json` (category:
`Android Architecture`).

Objectives for this set:

- Decompile the APK (`jadx`, `apktool`) and read `AndroidManifest.xml`.
- Identify exported components and judge whether they are misconfigured.
- Discover flags in manifest meta-data, Intent extra contracts, resources,
  and content providers.
- Query an unprotected Content Provider via `adb content query`.

The vulnerable app (`com.glowmart.mobile`) is the APK served at
`http://appstore:8001/apk/GlowMartMobile.apk` (in-network) or attached to CTFd.

Tools: `jadx`, `apktool`, `adb`, `aapt2`. See `docs/student-guide.md`.