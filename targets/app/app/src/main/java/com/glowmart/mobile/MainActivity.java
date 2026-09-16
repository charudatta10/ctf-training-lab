package com.glowmart.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

public class MainActivity extends Activity {
    private static final String TAG = "GlowMartDebug";
    static final String FLAG_LOGCAT = "flag{logcat_debug_leak}";
    static final String FLAG_STORAGE = "flag{local_database_forensics}";
    static final int USER_ID = 4242;
    private TextView output;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // M3-C13: debug log leak -- visible in logcat
        Log.v(TAG, "MainActivity initialised. Internal build flag=" + FLAG_LOGCAT);

        // M3-C14: local storage (SharedPreferences + SQLite)
        getSharedPreferences("session_data", MODE_PRIVATE)
                .edit()
                .putString("user", "glotest")
                .putString("remembered_flag", FLAG_STORAGE)
                .apply();
        AppDatabase.getInstance(this).writeFlag(FLAG_STORAGE);

        // M3-C12: runtime decrypt license check -- the full value is only
        // observable through a Frida hook of Vault.getDecryptedSecret().
        String check = Vault.getDecryptedSecret(USER_ID);
        Log.d("VaultLicense", "license check: " + check.substring(0, Math.min(8, check.length())) + "...");

        // Best-effort native init (M2-C9)
        NativeLib.safeSlogan();

        renderUi();
    }

    private void renderUi() {
        ScrollView scroll = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(32, 32, 32, 32);

        TextView title = new TextView(this);
        title.setText("GlowMart Mobile - employee portal");
        title.setTextSize(20f);
        root.addView(title);

        Button sync = new Button(this);
        sync.setText("Sync with backend");
        sync.setOnClickListener(v -> new Thread(() -> {
            final String result;
            try {
                result = PinnedApiClient.fetchBanner();
            } catch (Exception e) {
                runOnUiThread(() -> output.setText("Sync failed: " + e.getMessage()));
                return;
            }
            runOnUiThread(() -> output.setText("Backend: " + result));
        }).start());
        root.addView(sync);

        Button vault = new Button(this);
        vault.setText("Open vault");
        vault.setOnClickListener(v -> startActivity(
                new android.content.Intent(this, VaultActivity.class)));
        root.addView(vault);

        output = new TextView(this);
        output.setText("");
        root.addView(output);

        scroll.addView(root);
        setContentView(scroll);
    }
}