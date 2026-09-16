package com.glowmart.mobile;

import android.os.Build;

import java.io.File;

public final class RootCheck {
    private static final String[] SU_PATHS = {
            "/system/bin/su", "/system/xbin/su", "/sbin/su", "/vendor/bin/su"
    };

    private RootCheck() {
    }

    public static boolean isDeviceRooted() {
        for (String path : SU_PATHS) {
            if (new File(path).exists()) {
                return true;
            }
        }
        return Build.TAGS != null && Build.TAGS.contains("test-keys");
    }
}