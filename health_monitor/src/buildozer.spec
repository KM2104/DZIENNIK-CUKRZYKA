[app]
title = Health Monitor
package.name = healthmonitor
package.domain = org.healthmonitor
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 0.1
requirements = python3,kivy==2.3.0,matplotlib,pillow,numpy,reportlab,kivy_garden.graph
# orientation: all = automatyczne obracanie (pion/poziom)
# portrait = tylko pion, landscape = tylko poziom
orientation = all
fullscreen = 0
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

