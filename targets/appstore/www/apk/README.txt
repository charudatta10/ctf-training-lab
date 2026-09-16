Place the built APK here as GlowMartMobile.apk.

Run:  python scripts/lab.py build-apk   (from the project root)

The build script also drops libglowmart.strings.txt here (a strings(1)
dump of the native library) so the M2-C9 stretch challenge works even
without an NDK build.