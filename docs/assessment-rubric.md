# Assessment Rubric

Rubric for the **Mobile App Security** lab (Android). Aligned with the three
course modules: Android Architecture, Static Analysis, Dynamic Analysis.

## Weighting

| Module / Activity             | Weight |
|-------------------------------|--------|
| Module 1 — Recon & Structure  | 20%    |
| Module 2 — Reverse & Extract  | 35%    |
| Module 3 — Runtime & Intercept| 30%    |
| Evidence quality              | 10%    |
| Final report                  | 5%     |
| **Total**                     | **100%** |

## Scoring per category (0–4 scale)

| Score | Level | Description |
|-------|-------|-------------|
| 4 | Excellent | Complete, correct, well-evidenced, minimal/no help needed. |
| 3 | Proficient | Correct result, minor gaps in evidence or rationale. |
| 2 | Developing | Partial result, some errors, help needed. |
| 1 | Beginner | Major gaps, incorrect, needs significant guidance. |
| 0 | No attempt | Not done / no evidence. |

## Category descriptors

### Module 1 — Recon & Structure (20%)
- Decompiled the APK (`jadx`/`apktool`) and read the manifest.
- Identified exported components (activities, provider) and their
  misconfigurations.
- Enumerated resources (strings/assets/raw) and content providers.
- Used `adb`, `aapt2`, and `content query` correctly.
- Stayed in scope.

### Module 2 — Reverse & Extract (35%)
- Located hardcoded secrets in decompiled source.
- Decoded weak encodings (Base64/XOR) and documented the decode.
- Broke the insecure AES-ECB crypto (algorithm, key, ciphertext → plaintext).
- Interpreted a MobSF static-scan report and found the flagged secret.
- Extracted strings from the native library.
- Applied CVSS/OWASP Mobile Top 10 reasoning to each finding.

### Module 3 — Runtime & Intercept (30%)
- Bypassed SSL pinning and intercepted the API call (Burp/mitmproxy + Frida).
- Bypassed root detection and reached the locked vault.
- Hooked a targeted function and dumped a runtime-decrypted secret.
- Monitored `logcat` and caught the leaked flag.
- Pulled and inspected local storage (SQLite/SharedPreferences).
- Could explain *why* each technique worked.

### Evidence quality (10%)
- Screenshots / tool output / Frida sessions / logcat captures for every
  step and finding.
- Evidence saved in a clear, reviewable form (named, organized).

### Final report (5%)
- Completed the `reports/template.md` assessment report.
- Accurate summary, scope, methodology, findings, risk ratings, remediation.

## Final grade

| Total | Grade |
|-------|-------|
| 90–100 | A |
| 80–89  | B |
| 70–79  | C |
| 60–69  | D |
| <60    | F |

## Automated component

CTFd awards points for each challenge flag (the module weight is reflected in
challenge `value`s). The rubric above is for the **delivered evidence and
methodology quality**, which the instructor grades. Suggested mapping: use the
automated CTFd score as a cap and the rubric to assess methodology depth and
the final report.