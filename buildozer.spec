[app]

title = Physics Lab
package.name = physicslab
package.domain = org.physicslab

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 1.0
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.minapi = 21
android.api = 34
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 0
