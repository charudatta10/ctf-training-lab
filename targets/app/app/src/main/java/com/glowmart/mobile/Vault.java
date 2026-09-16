package com.glowmart.mobile;

import android.util.Base64;

import java.nio.charset.StandardCharsets;

public final class Vault {
    // XOR-obfuscated blob; the key is derived from a runtime argument (M3-C12).
    private static final String BLOB = "9P7z9en04Pv2883g5/zm+//3zfb38eDr4ubN9uf/4u8=";

    private Vault() {
    }

    public static String getDecryptedSecret(int userId) {
        byte[] raw = Base64.decode(BLOB, Base64.DEFAULT);
        int key = userId & 0xFF;
        for (int i = 0; i < raw.length; i++) {
            raw[i] ^= (byte) key;
        }
        return new String(raw, StandardCharsets.UTF_8);
    }
}