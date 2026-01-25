import json
import os
from enum import Enum
from typing import Any, Dict, Optional


class Lang(Enum):
    """Enum representing available languages with their file paths."""

    ENGLISH = "assets/languages/english.json"
    GERMAN = "assets/languages/german.json"
    HUNGARIAN = "assets/languages/hungarian.json"

    def text(self) -> "LangText":
        return LangText(self)


def _abs_lang_path(rel_or_abs_path: str) -> str:
    if os.path.isabs(rel_or_abs_path):
        return rel_or_abs_path
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_or_abs_path)


def _load_json(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return dict(data) if isinstance(data, dict) else {}
    except FileNotFoundError:
        print(f"ERROR: Language file {path} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"ERROR: Language file {path} has invalid JSON.")
        return {}


class LangText:
    """Loads localized UI text from JSON files.

    - Attribute access: `text.close_but_wrong`
    - Fallback: missing keys fall back to English; then to a sentinel string.
    - Formatting helper: `text.menu_languages_fmt(mlang='Latin', learnlang='English')`
    """

    def __init__(self, lang_enum: Lang):
        self._lang = lang_enum
        self._primary_path = _abs_lang_path(lang_enum.value)
        self._fallback_path = _abs_lang_path(Lang.ENGLISH.value)
        self._primary: Dict[str, Any] = _load_json(self._primary_path)
        self._fallback: Dict[str, Any] = (
            self._primary if lang_enum == Lang.ENGLISH else _load_json(self._fallback_path)
        )

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        if key in self._primary:
            return self._primary[key]
        if key in self._fallback:
            return self._fallback[key]
        if default is not None:
            return default
        return f"MISSING TEXT KEY: {key}"

    def fmt(self, key: str, /, *args: Any, **kwargs: Any) -> str:
        val = self.get(key)
        try:
            return str(val).format(*args, **kwargs)
        except Exception:
            return str(val)

    def __getattr__(self, name: str) -> Any:
        # Called only if normal attribute lookup fails.
        if name.startswith("_"):
            raise AttributeError(name)
        return _TextKey(self, name, self.get(name))


class _TextKey(str):
    """A str subclass that is also callable.

    Lets you write:
        text.some_key(foo=123)
    instead of:
        text.fmt('some_key', foo=123)
    """

    __slots__ = ("_lt", "_key")

    def __new__(cls, lt: "LangText", key: str, value: Any):
        obj = super().__new__(cls, str(value))
        obj._lt = lt
        obj._key = key
        return obj

    def __call__(self, /, *args: Any, **kwargs: Any) -> str:
        return self._lt.fmt(self._key, *args, **kwargs)
