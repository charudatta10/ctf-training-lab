# 02 - Static Analysis (CTF Set 2: "Reverse & Extract")

Challenge definitions live in `challenges/challenges.json` (category:
`Static Analysis`).

Objectives for this set:

- Reverse the app's Java/Kotlin sources (`jadx-gui`) and smali (`apktool`).
- Find hardcoded API keys / credentials in decompiled source.
- Manually decode Base64/XOR-encoded constants (CyberChef).
- Break insecure crypto: AES-128-ECB with a hardcoded key, no IV.
- Validate findings with an automated MobSF static scan.
- (Stretch) Run `strings(1)` on the packaged native `libglowmart.so`.

Remember: maybe the flag has to be extracted from the *report* MobSF
generates, not just the source.

Tools: `jadx-gui`, `apktool`, MobSF, `strings`, CyberChef.
See `docs/student-guide.md`.