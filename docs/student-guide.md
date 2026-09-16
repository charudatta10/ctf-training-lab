# Student Guide — Mobile App Security Methodology

This guide explains **how** to approach the lab across its three modules. It
intentionally does **not** reveal flags or full solutions — you must find
those yourself. Work through the modules in order on the CTFd platform.

> Always follow [docs/lab-rules.md](lab-rules.md). Attack only the
> GlowMart Mobile app, the appstore, and the api backend.

---

## 0. Get oriented

- Open **http://localhost:8000/** (or the URL your instructor gives you).
- Read the Module 1 challenge set ("Recon & Structure").
- Download the APK:
  - CTFd attachment, or
  - App store: `http://appstore.<ip>.sslip.io:8080/apk/GlowMartMobile.apk`

### Working environment

Your "attacker workstation" is your **host machine + an Android emulator or
device**:

```bash
# create / start an emulator (Android Studio AVD Manager), then:
adb devices                 # emulator must appear as "device"
adb install GlowMartMobile.apk
adb shell am start -n com.glowmart.mobile/.MainActivity
```

Install the toolchain you need per module:

- Module 1: `jadx` (or `jadx-gui`), `apktool`, `adb` (platform-tools).
- Module 2: `jadx-gui`, `apktool`, MobSF (Docker), `strings`, CyberChef.
- Module 3: Frida (`pip install frida-tools`, `frida-ps -U`), Objection,
  Burp Suite / mitmproxy, a rooted emulator (or a non-rooted one with
  root-detection handled) — see your instructor's setup notes.

> A practical APK decompile:
> ```bash
> jadx -d out/ GlowMartMobile.apk     # decompiled sources + resources
> apktool d GlowMartMobile.apk        # smali + buildable res
> aapt2 dump badging GlowMartMobile.apk   # quick manifest/packgage info
> ```

---

## 1. Module 1 — Android Architecture ("Recon & Structure")

Goal: understand the app's *structure* before attacking behavior.

- **Manifest.** Read `AndroidManifest.xml` in `out/`. List every component:
  - Is any `activity` / `provider` / `service` / `receiver` **exported**?
  - An exported component with no intent-filter is a classic misconfig.
  - Flags hide in `<meta-data>` values and in resource files.
- **Intent contracts.** Decompile an exported activity; what extra keys does
  it read? Launch it with `adb shell am start -n pkg/.Activity --es key value`.
- **Resources.** Browse `out/resources/` (`assets/`, `res/raw/`,
  `res/values/strings.xml`). Look at *unused* entries.
- **Content Providers.** For an exported provider, query it from `adb`:
  ```bash
  adb shell content query --uri content://<authority>/<path>
  ```

Checklist: manifest reviewed · extra contracts found · resources audited ·
providers queried.

---

## 2. Module 2 — Static Analysis ("Reverse & Extract")

Goal: pull secrets out of the code without running it.

- **Hardcoded secrets.** Grep decompiled sources for `key`, `secret`,
  `token`, `password`, `api`. MobSF's "Hardcoded Secrets" finding is a
  shortcut — and this module has a challenge that leans on it.
- **Encoding ≠ encryption.** A string constant that is only Base64/XOR is
  trivially reversible. CyberChef: `From Base64`, `XOR Brute Force`.
- **Crypto review.** Locate `Cipher.getInstance(...)`; note the algorithm
  and mode. `AES/ECB` + a key constant in the same class = broken by design.
  Extract the ciphertext + key and decrypt (CyberChef AES-Decrypt).
- **Native libraries.** `unzip -l` the APK to see `lib/*/lib*.so`. Run
  `strings` on them — plaintext flags survive in native strings.
- **MobSF static scan.** Upload the APK; read the generated **report** —
  findings are the deliverable, and one of them *is* the flag.

Checklist: source greped · MobSF report read · all ciphers enumerated ·
native libs strings'd.

---

## 3. Module 3 — Dynamic Analysis ("Runtime & Intercept")

Goal: instrument the running app.

- **SSL pinning bypass + interception.**
  1. Configure Burp/mitmproxy on the host; install its CA on the emulator.
  2. Proxy the emulator (`adb shell settings put global http_proxy 10.0.2.2:8080`
     or Burp invisible proxy via iptables).
  3. The app's `PinnedApiClient` will reject your CA → bypass with Frida:
     ```js
     Java.perform(function () {
         var P = Java.use("com.glowmart.mobile.PinnedApiClient");
         // neuter the pin check so it never throws CertificateException
     });
     ```
     (Objection: `android sslpinning disable`.)
  4. Re-trigger the app's "Sync" → intercept `/api/v1/mobile/banner` → flag.
- **Root detection bypass.** Hook the check:
  ```js
  Java.perform(function () {
      Java.use("com.glowmart.mobile.RootCheck").isDeviceRooted.implementation = function () { return false; };
  });
  ```
  Then open the vault (MainActivity → "Open vault").
- **Runtime decrypt dump.** Find the class that decrypts at run time, hook
  the method, and `console.log` its return value (call it with the same
  argument the app uses).
- **Logcat.** Read the log stream:
  ```bash
  adb logcat -c && adb shell am start -n com.glowmart.mobile/.MainActivity && adb logcat -d | grep -i flag
  ```
- **Local storage.** Pull the app's data and inspect:
  ```bash
  adb exec-out run-as com.glowmart.mobile cat databases/glowmart.db > db.sqlite   # debuggable builds
  sqlite3 db.sqlite "select * from secrets;"
  ```
  SharedPreferences live in
  `/data/data/com.glowmart.mobile/shared_prefs/*.xml`.

Checklist: proxy configured · pin bypassed · root check bypassed · target
function hooked · logcat reviewed · storage pulled & inspected.

---

## Final deliverable

Complete the **mobile security assessment report** template
([reports/template.md](../reports/template.md)): executive summary, scope,
methodology, per-module findings with evidence, risk ratings, remediation,
and a conclusion. Evidence (screenshots, decompiler output, Frida sessions,
logcat captures) is required for every claim.

## Checklist before you finish

- [ ] Read the rules of engagement and knew your scope.
- [ ] Module 1: manifest, intent extras, resources, providers reviewed.
- [ ] Module 2: sources reversed, MobSF report mined, crypto broken, native strings read.
- [ ] Module 3: pinning bypassed, root check bypassed, secrets dumped, storage pulled.
- [ ] Evidence captured for every finding.
- [ ] Report completed following the template.
- [ ] Stayed **in scope** the entire time.