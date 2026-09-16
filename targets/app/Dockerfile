# ============================================================================
# GlowMart Mobile - vulnerable APK builder.
#
# Builds the intentionally-vulnerable Android APK inside a container so the
# lab has no host-side Android SDK requirement. The build needs INTERNET at
# container build time (SDK downloads) - it is NOT part of the isolated lab
# network. Run via:  python scripts/lab.py build-apk
# ============================================================================

FROM gradle:8.5-jdk17 AS build

USER root

ENV ANDROID_HOME=/opt/android
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools"
ENV NDK_VERSION=25.2.9519653

WORKDIR /workspace

# --- Android command line tools ---------------------------------------------
RUN mkdir -p "${ANDROID_HOME}/cmdline-tools" \
 && curl -fsSL \
    https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \
    -o /tmp/cmdtools.zip \
 && unzip -q /tmp/cmdtools.zip -d "${ANDROID_HOME}/cmdline-tools" \
 && mv "${ANDROID_HOME}/cmdline-tools/cmdline-tools" "${ANDROID_HOME}/cmdline-tools/latest" \
 && rm /tmp/cmdtools.zip

# --- SDK / NDK / CMake components ------------------------------------------
RUN yes | sdkmanager --licenses > /dev/null
RUN sdkmanager \
      "platform-tools" \
      "platforms;android-34" \
      "build-tools;34.0.0" \
      "ndk;${NDK_VERSION}" \
      "cmake;3.22.1" > /dev/null

# --- Build ------------------------------------------------------------------
COPY . .

RUN gradle --no-daemon :app:assembleDebug

# Output: /workspace/app/build/outputs/apk/debug/app-debug.apk