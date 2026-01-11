Arch Linux: Yes, it’s a good environment for building APKs.
Install deps (`python`, `pip`, `jdk17-openjdk`, `git`, `cython`, `wget`, `unzip`, `zip`, `make`, `gcc`, `libffi`, `openssl` etc.).
`pip install --user buildozer`
Run `buildozer -v android debug` from the project folder; it will download SDK/NDK automatically.