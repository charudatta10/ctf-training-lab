package com.glowmart.mobile;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;

public class FlagProvider extends ContentProvider {
    public static final String AUTHORITY = "com.glowmart.mobile.secrets";

    @Override
    public boolean onCreate() {
        return true;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection,
                        String[] selectionArgs, String sortOrder) {
        String path = uri.getLastPathSegment();
        MatrixCursor cursor = new MatrixCursor(new String[]{"flag"});
        if ("flag".equals(path)) {
            cursor.addRow(new Object[]{getContext().getString(R.string.provider_flag)});
        } else {
            cursor.addRow(new Object[]{""});
        }
        return cursor;
    }

    @Override
    public String getType(Uri uri) {
        return "text/plain";
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        return null;
    }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        return 0;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        return 0;
    }
}