package com.glowmart.mobile;

import android.util.Base64;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

public final class PinnedApiClient {
    // sha256 of the lab API certificate's SPKI (base64) -- hardcoded pin (M3-C10).
    private static final String PIN_SHA256 = "+zSd3zPVaGL3CmRb7lO45beFNK/lw+4D+fb43RZg91Y=";
    private static final String API_SECURE_BASE = "https://10.0.2.2:3443";

    private PinnedApiClient() {
    }

    public static String fetchBanner() throws Exception {
        URL url = new URL(API_SECURE_BASE + "/api/v1/mobile/banner");
        HttpsURLConnection conn = (HttpsURLConnection) url.openConnection();
        conn.setConnectTimeout(8000);
        conn.setReadTimeout(8000);
        conn.setSSLSocketFactory(createPinningSslSocketFactory());
        conn.setHostnameVerifier((hostname, session) -> true); // pin is the only trust control
        InputStream in = conn.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            sb.append(line);
        }
        reader.close();
        conn.disconnect();
        return sb.toString();
    }

    private static SSLSocketFactory createPinningSslSocketFactory() throws Exception {
        TrustManager tm = new X509TrustManager() {
            @Override
            public void checkClientTrusted(X509Certificate[] chain, String authType) {
            }

            @Override
            public X509Certificate[] getAcceptedIssuers() {
                return new X509Certificate[0];
            }

            @Override
            public void checkServerTrusted(X509Certificate[] chain, String authType)
                    throws CertificateException {
                if (chain == null || chain.length == 0) {
                    throw new CertificateException("empty certificate chain");
                }
                try {
                    byte[] spki = chain[0].getPublicKey().getEncoded();
                    byte[] digest = MessageDigest.getInstance("SHA-256").digest(spki);
                    String pin = Base64.encodeToString(digest, Base64.NO_WRAP);
                    if (!PIN_SHA256.equals(pin)) {
                        throw new CertificateException("certificate pin mismatch: " + pin);
                    }
                } catch (java.security.NoSuchAlgorithmException e) {
                    throw new CertificateException(e);
                }
            }
        };
        SSLContext ctx = SSLContext.getInstance("TLS");
        ctx.init(null, new TrustManager[]{tm}, new SecureRandom());
        return ctx.getSocketFactory();
    }
}