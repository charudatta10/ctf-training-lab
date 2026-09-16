package com.glowmart.mobile;

public final class NativeLib {
    static {
        try {
            System.loadLibrary("glowmart");
        } catch (UnsatisfiedLinkError ignored) {
            // native lib is optional in a non-NDK lab build
        }
    }

    private NativeLib() {
    }

    public static native String slogan();

    public static String safeSlogan() {
        try {
            return slogan();
        } catch (UnsatisfiedLinkError e) {
            return "<native lib unavailable>";
        }
    }
}