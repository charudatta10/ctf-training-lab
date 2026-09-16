# target/appstore - GlowMart Mobile download site

Tiny static HTTP server (Python, port 8001) that serves the lab's APK and
module attachments to students. It runs **inside the isolated network**; a
`./www` folder is mounted read-only from the host.

## Contents

- `apk/` - the built APK (`GlowMartMobile.apk`) produced by
  `python scripts/lab.py build-apk`, plus the native strings dump used by
  the M2-C9 stretch challenge.
- `index.html` - a simple landing page for students.

## Reachability

- In-network: `http://appstore:8001/apk/GlowMartMobile.apk`
- Through the reverse proxy (classroom): `http://appstore.<IP>.sslip.io:8080/apk/`
- CTFd also lets the instructor attach the APK directly to challenges.

Most students will simply download the APK from CTFd or the app store,
install it on an emulator with `adb install`, then decompile it with
`jadx`/`apktool` for static analysis.