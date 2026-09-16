package com.glowmart.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class VaultActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        if (RootCheck.isDeviceRooted()) {
            tv.setText("Vault locked: root detected.");
        } else {
            tv.setText("Vault unlocked.\nFlag: " + getString(R.string.vault_flag));
        }
        setContentView(tv);
    }
}