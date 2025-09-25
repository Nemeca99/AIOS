# Buildozer spec file for UML Calculator Mobile
[app]
title = UML Calculator
package.name = umlcalculator
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1

# (str) Application entry point, default is main.py
entrypoint = main.py

# (list) Permissions
android.permissions = INTERNET

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
android.orientation = portrait

# (str) Android NDK version to use
android.ndk = 23b

# (str) Android SDK version to use
android.sdk = 33

# (str) Minimum API required
android.minapi = 21

# (str) Target API
android.target = 33

# (str) Android entry point, default is org.kivy.android.PythonActivity
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is 'import android' (crashes on some devices)
# android.theme = '@android:style/Theme.NoTitleBar'

# (str) Custom source folders for requirements
# (list) List of inclusions using pattern matching
# (list) List of exclusions using pattern matching
# (str) Presplash of the application
# (str) Icon of the application
# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
# (str) Android NDK version to use
# (str) Android SDK version to use
# (str) Minimum API required
# (str) Target API
# (str) Android entry point, default is org.kivy.android.PythonActivity
# (str) Android app theme, default is 'import android' (crashes on some devices)
