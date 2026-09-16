# target/app - GlowMart Mobile (vulnerable Android app)

This is the **vulnerable Android application** under test. It contains every
flag the lab's challenges expect, placed inside real app constructs that
students must reverse-engineer or instrument at runtime.

## Build the APK

The lab builds it in a container (no host Android SDK needed):

```bash
python scripts/lab.py build-apk
```

The build downloads the Android SDK + NDK *inside* the container (needs
internet and several GB) and deposits the APK at:

```
targets/appstore/www/apk/GlowMartMobile.apk
```

Students can also open this folder directly in Android Studio
(`build.gradle` project) and build/install (`app-debug.apk`) themselves.

## Challenge flag map

| Module / Set | Challenge            | Artifact that contains the flag                          |
|--------------|----------------------|----------------------------------------------------------|
| M1-C1        | Manifest flag        | `AndroidManifest.xml` meta-data on `.SecretActivity`     |
| M1-C2        | Intent-extra leak    | `DebugLeakActivity` + `res/values/strings.xml`           |
| M1-C3        | Resource flag        | `res/raw/secret_codebook.json` / `assets/`               |
| M1-C4        | Content Provider     | `FlagProvider` (query `content://com.glowmart.mobile.secrets/flag`) |
| M2-C5        | Hardcoded key        | `AuthTokenProvider.API_KEY`                              |
| M2-C6        | Encoded flag         | `Strings.ENCODED_BANNER` (base64)                        |
| M2-C7        | Weak crypto          | `CryptoBox` AES-128-ECB, static key `0123456789abcdef`   |
| M2-C8        | MobSF finding        | `res/values/secrets.xml` + `MobSfSecret`                 |
| M2-C9        | Native `.so` string  | `src/main/cpp/glowlib.c` (embedded in `libglowmart.so`)  |
| M3-C10       | SSL pinning          | `PinnedApiClient` pin vs `api` HTTPS endpoint            |
| M3-C11       | Root detection       | `VaultActivity` + `RootCheck`                            |
| M3-C12       | Runtime decrypt      | `Vault.getDecryptedSecret(userId)`                       |
| M3-C13       | Logcat leak          | `MainActivity` `Log.v(...)`                              |
| M3-C14       | Local storage        | `SharedPreferences session_data` + `AppDatabase` SQLite  |

## Layout

```
app/
  build.gradle               # AGP 8.2.2, SDK 34, NDK cmake native lib
  src/main/
    AndroidManifest.xml
    java/com/glowmart/mobile/*.java
    res/values/              # strings, themes, secrets
    res/raw/secret_codebook.json
    assets/private_notes.txt
    cpp/                     # native glowmart lib (M2-C9)
Dockerfile                   # containerized APK builder
```

## Notes for the instructor

- `lab.py build-apk` runs the builder **outside** the isolated network because
  the SDK download needs internet access; the resulting APK is then served to
  students from the isolated `appstore` service.
- If a student rebuilds in Android Studio with a different certificate or
  package name, the launcher/component names must stay
  `com.glowmart.mobile` for every challenge to hold.
- The native library is deliberately optional: the app loads it
  best-effort. If the NDK build is skipped, students can still solve M2-C9
  against the built `libglowmart.so` or the strings dump at
  `appstore/www/apk/libglowmart.strings.txt`.