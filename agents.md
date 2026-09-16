## Module 1: Android Architecture 
Covers APK structure, Manifest, components (Activities, Services, Broadcast Receivers, Content Providers), permission model, app sandboxing, signing.

**CTF Set 1 — "Recon & Structure" (4 challenges, ~45 min)**
- Decompile an APK and find a hidden flag in `AndroidManifest.xml` (exported component misconfig)
- Identify an exported Activity that leaks data via Intent extras
- Find a flag hidden in resources (`strings.xml`, assets, raw)
- Extract and read a flag from an unprotected Content Provider (via `adb` or `content query`)

Tools: `apktool`, `jadx`, `adb`

---

## Module 2: Static Analysis 
Covers reverse engineering (jadx, apktool), hardcoded secrets, insecure crypto, obfuscation basics, MobSF static scan, manifest/permission review, code signing verification.

**CTF Set 2 — "Reverse & Extract" (4-5 challenges, ~45 min)**
- Hardcoded API key / secret hidden in decompiled Java/Kotlin source
- Base64/XOR-encoded flag requiring manual decoding from a string constant
- Insecure crypto: flag encrypted with weak/static key (ECB mode, hardcoded IV)
- MobSF automated scan — find flag in a flagged vulnerability report
- (Stretch) Flag hidden in native `.so` library, requiring basic string/strings-tool inspection

Tools: `jadx-gui`, `apktool`, MobSF, `strings`, CyberChef

---

## Module 3: Dynamic Analysis 
Covers Frida basics, SSL pinning bypass, runtime instrumentation, intercepting traffic with Burp/mitmproxy, logcat monitoring, root detection bypass, local storage/SQLite inspection at runtime.

**CTF Set 3 — "Runtime & Intercept" (4-5 challenges, ~60 min)**
- Bypass SSL pinning to intercept an API call containing the flag (Frida + Burp/mitmproxy)
- Bypass a root-detection check to unlock a hidden screen with a flag
- Use Frida to hook a function and dump a runtime-decrypted flag
- Inspect logcat output during app use to catch a leaked flag in debug logs
- Pull and inspect a SQLite DB / SharedPreferences file at runtime for a stored flag (`adb pull`)

Tools: Frida + Objection, Burp Suite/mitmproxy, `adb`, Android emulator/rooted device

