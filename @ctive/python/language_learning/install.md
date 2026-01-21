Arch Linux: Yes, it’s a good environment for building APKs.
Install deps (`python`, `pip`, `jdk17-openjdk`, `git`, `cython`, `wget`, `unzip`, `zip`, `make`, `gcc`, `libffi`, `openssl` etc.).
`pip install --user buildozer`
Run `buildozer -v android debug` from the project folder; it will download SDK/NDK automatically.

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