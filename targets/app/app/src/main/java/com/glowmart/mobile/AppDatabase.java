package com.glowmart.mobile;

import android.content.ContentValues;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public final class AppDatabase extends SQLiteOpenHelper {
    private static final String DB_NAME = "glowmart.db";
    private static final int DB_VERSION = 1;
    private static volatile AppDatabase instance;

    private AppDatabase(Context context) {
        super(context.getApplicationContext(), DB_NAME, null, DB_VERSION);
    }

    public static AppDatabase getInstance(Context context) {
        if (instance == null) {
            synchronized (AppDatabase.class) {
                if (instance == null) {
                    instance = new AppDatabase(context);
                }
            }
        }
        return instance;
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS secrets ("
                + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "flag TEXT,"
                + "note TEXT)");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
    }

    public void writeFlag(String flag) {
        ContentValues cv = new ContentValues();
        cv.put("flag", flag);
        cv.put("note", "session cache entry");
        getWritableDatabase().insert("secrets", null, cv);
    }
}