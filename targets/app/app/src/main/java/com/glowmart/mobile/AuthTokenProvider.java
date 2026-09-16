package com.glowmart.mobile;

public final class AuthTokenProvider {
    // Intentionally hardcoded production secret (M2-C5).
    public static final String API_KEY = "flag{static_hardcoded_api_key}";

    private AuthTokenProvider() {
    }

    public static String getApiKey() {
        return API_KEY;
    }
}