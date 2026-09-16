# Mobile Application Security Assessment Report

|                     |                                             |
|---------------------|---------------------------------------------|
| **Client**          | GlowMart Inc.                               |
| **Engagement**      | GLOW-2026-MOB-01                            |
| **Consultant**      | [Student name]                              |
| **Report date**     | [YYYY-MM-DD]                                |
| **Testing window**  | 2026-09-07 to 2026-12-18                    |
| **Application**     | GlowMart Mobile (`com.glowmart.mobile`) v1.3.0 |

---

## 1. Executive Summary
[2–4 sentence summary of the engagement outcome, key risks, and top priorities — written for non-technical readers.]

## 2. Scope
[List the authorized in-scope assets: GlowMartMobile.apk, appstore, api — and the authorized network mobsec-lab-net.]

## 3. Rules of Engagement
[Summarize the constraints you operated under: lab-only, no destructive actions, no out-of-scope testing.]

## 4. Methodology
[Describe your process per module: Android Architecture → Static Analysis → Dynamic Analysis. Name tools used (jadx, apktool, adb, MobSF, Frida, Burp, sqlite3, etc.).]

## 5. Module 1 — Android Architecture ("Recon & Structure")
[Manifest review, exported components, resources audit, content providers. Include evidence.]

## 6. Module 2 — Static Analysis ("Reverse & Extract")
[Hardcoded secrets, encoded values, crypto weaknesses, MobSF findings, native strings. Include evidence.]

## 7. Module 3 — Dynamic Analysis ("Runtime & Intercept")
[Pinning, root detection, runtime decryption, logging, storage. Include evidence.]

## 8. Findings
[Document each finding. Map to a severity (e.g., OWASP Mobile Top 10 / CWE).]
| # | Finding | Module | Severity | Evidence |
|---|---------|--------|----------|----------|
| 1 | Exported component (manifest) | 1 | ... | ... |
| 2 | Intent-extra leak / exported activity | 1 | ... | ... |
| 3 | Unprotected content provider | 1 | ... | ... |
| 4 | Hardcoded API key | 2 | ... | ... |
| 5 | Weak encoding | 2 | ... | ... |
| 6 | Insecure crypto (static AES key) | 2 | ... | ... |
| 7 | Secret in resources / MobSF finding | 2 | ... | ... |
| 8 | Native library secret | 2 | ... | ... |
| 9 | SSL pinning bypassable | 3 | ... | ... |
| 10 | Root detection bypassable | 3 | ... | ... |
| 11 | Debug logging (logcat leak) | 3 | ... | ... |
| 12 | Sensitive data in local storage | 3 | ... | ... |

## 9. Risk Rating
[For each finding, provide severity and rationale; use CVSS v3.1 base scores where appropriate.]

## 10. Evidence
[Attach screenshots, decompiler output, MobSF report excerpts, Frida sessions, logcat captures, and pulled data files.]

## 11. Business Impact
[Translate technical findings into business risk for GlowMart.]

## 12. Remediation
[Provide concrete, prioritized remediation for every finding.]
1. ...
2. ...

## 13. Limitations
[Define what was out of scope and any constraints that limited testing (e.g., non-rooted device, missing ABI).]

## 14. Conclusion
[Closing summary and recommended next steps.]