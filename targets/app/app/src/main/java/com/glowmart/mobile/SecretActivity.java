package com.glowmart.mobile;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.widget.TextView;

public class SecretActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        try {
            ActivityInfo ai = getPackageManager().getActivityInfo(
                    getComponentName(), PackageManager.GET_META_DATA);
            String flag = ai.metaData != null
                    ? ai.metaData.getString("com.glowmart.mobile.flag")
                    : "no meta-data";
            tv.setText("Secret component accessed.\nEmbedded flag: " + flag);
        } catch (PackageManager.NameNotFoundException e) {
            tv.setText("Unable to read component metadata.");
        }
        setContentView(tv);
    }
}