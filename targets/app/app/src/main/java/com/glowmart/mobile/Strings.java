package com.glowmart.mobile;

import android.util.Base64;

import java.nio.charset.StandardCharsets;

public final class Strings {
    // Weakly encoded private note (M2-C6). Decode manually (CyberChef / base64).
    public static final String ENCODED_BANNER = "ZmxhZ3t3ZWFrX2VuY29kaW5nX3hvcl9iYXNlNjR9";

    private Strings() {
    }

    public static String decodeBanner() {
        return new String(Base64.decode(ENCODED_BANNER, Base64.DEFAULT), StandardCharsets.UTF_8);
    }
}