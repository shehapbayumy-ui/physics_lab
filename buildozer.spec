[app]

title = Physics Lab
package.name = physicslab
package.domain = org.physicslab

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

# Android 5.0+
android.minapi = 21

# Android API used for building
android.api = 34

# Support old 32-bit + modern 64-bit phones
android.archs = armeabi-v7a,arm64-v8a

# Accept Android SDK license
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 0
