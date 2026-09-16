package com.glowmart.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class DebugLeakActivity extends Activity {
    private static final String EXPECTED_OVERRIDE = "grant";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        String override = getIntent().getStringExtra("auth_override");
        if (EXPECTED_OVERRIDE.equals(override)) {
            tv.setText("Debug session granted.\nFlag: " + getString(R.string.debug_leak_flag));
        } else {
            tv.setText("Debug session denied.\nSupply the 'auth_override' intent extra with value 'grant'.");
        }
        setContentView(tv);
    }
}