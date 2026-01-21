[app]

# (str) Title of your application
title = Vocab Learner

# (str) Version of the app
version = 1.0.3

# (str) Package name
package.name = vocab_learner

# (str) Package domain (needed for Android package ID)
package.domain = org.benkex

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (leave empty to include most)
# source.include_exts = py,png,jpg,kv,atlas,json,txt

# (str) The entry point; Buildozer expects main.py by default.
# Use main.py for this project.
entrypoint = main.py

# (list) Application requirements
# Kivy is required; add any other deps you import.
requirements = python3,kivy

# (str) Android API/NDK settings
android.api = 33
android.minapi = 21

# (list) Permissions (add if you later need storage/network etc.)
android.permissions = 

# (list) Include your data files
# This ensures kits/, languages/, and your txt files are bundled.
source.include_exts = py,kv,json,txt

# (list) Files or directories to exclude
source.exclude_dirs = __pycache__,.git,.venv

# (str) Supported orientation (portrait, landscape)
orientation = portrait, landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Icon (optional)
# icon.filename = ./assets/images/icon.png

# (str) Presplash (optional)
# presplash.filename = 

# (str) Supported hardware: keyboard, touchscreen, etc.
# android.manifest.intent_filters = 

# (str) Log level for kivy
log_level = 2

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (str) Buildozer build directory
build_dir = .buildozer

# (str) Buildozer default command
defaultcommand = android debug
