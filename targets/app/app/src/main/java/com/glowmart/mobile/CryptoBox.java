package com.glowmart.mobile;

import android.util.Base64;

import java.nio.charset.StandardCharsets;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public final class CryptoBox {
    // AES-128-ECB with a static key and no IV - insecure by design (M2-C7).
    private static final String STATIC_KEY = "0123456789abcdef";
    private static final String SEALED_FLAG_BASE64 = "MRGeLCEOn3ijvPto5JaxAB9bj2gCfRBw9AI65EReaZA=";

    private CryptoBox() {
    }

    public static String decryptSecret() throws Exception {
        SecretKeySpec key = new SecretKeySpec(STATIC_KEY.getBytes(StandardCharsets.UTF_8), "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] plain = cipher.doFinal(Base64.decode(SEALED_FLAG_BASE64, Base64.DEFAULT));
        return new String(plain, StandardCharsets.UTF_8);
    }
}