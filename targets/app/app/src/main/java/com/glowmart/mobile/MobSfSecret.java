package com.glowmart.mobile;

public final class MobSfSecret {
    // Exposed credential - flagged by MobSF static scans (M2-C8).
    public static final String ANALYTICS_PASSWORD = "flag{mobsf_scan_discovered_secret}";

    private MobSfSecret() {
    }
}