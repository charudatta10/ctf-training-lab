#include <jni.h>
#include <android/log.h>

static const char SLOGAN[] = "flag{native_so_string_discovery}";

JNIEXPORT jstring JNICALL
Java_com_glowmart_mobile_NativeLib_slogan(JNIEnv *env, jobject thiz) {
    __android_log_print(ANDROID_LOG_INFO, "GlowMartNative", "slogan: %s", SLOGAN);
    return (*env)->NewStringUTF(env, SLOGAN);
}