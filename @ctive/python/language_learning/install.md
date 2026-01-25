# Installation Instructions

## WSL (Ubuntu) quick setup

This repo can be used from WSL. For Kivy on newer Python versions (e.g. 3.14), pip may need to build native extensions.

One-command bootstrap (installs Ubuntu build deps, creates `.venv`, installs `Cython` + `kivy[base]` from `requirements.txt`):

```bash
cd /mnt/c/Users/BenkeHargitai/prog/bencode/@ctive/python/language_learning
./scripts/bootstrap_wsl.sh
```

Recreate the venv from scratch:

```bash
./scripts/bootstrap_wsl.sh --recreate
```

## iOS build setup

Follow the instructions at https://kivy.org/doc/stable/guide/packaging-ios.html to install `kivy-ios`.
After setting up `kivy-ios`, I recommend navigating to the `@ctive/python` directory and running:

```bash
mkdir language_learning_build
cd language_learning_build
toolchain build python3 kivy
toolchain create vocab-learner /absolute/path/to/bencode/.../language_learning/lib
open vocab-learner-ios/vocab-learner.xcodeproj
```

Then navigate to: XCode > clicking `vocab-learner` main folder on the left panel > TARGETS > `vocab-learner`

Under "Signing & Capabilities":
- Edit "Bundle Identifier" to "org.benkex.vocab-learner"
- Set "Team" to your Personal Team (e.g.)

Under "Build Settings > Packaging":
- Edit Package name to "Vocab Learner" under 

In the `vocab-learner-ios` directory, make the following changes:
- Replace default `vocab-learner-ios/icon.png` with the one from `.../language_learning/lib/assets/images/icon.png`

Then, make the following changes to the generated Xcode project:
- Ensure that the app has permission to access the Documents directory by enabling the appropriate Info.plist keys (UIFileSharingEnabled / LSSupportsOpeningDocumentsInPlace) in `vocab-learner-ios/vocab-learner-Info.plist`:
    ```
        ...
        <string>Launch Screen</string>
    +++ <key>UIFileSharingEnabled</key>
    +++ <true/>
    +++ <key>LSSupportsOpeningDocumentsInPlace</key>
    +++ <true/>
        <key>UIStatusBarHidden</key>
        ...
    ```

The app can then be built and run on a connected iOS device using Xcode.
