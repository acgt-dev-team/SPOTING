import json
import os
from pathlib import Path
from typing import Any


DEFAULT_LOCALE = os.getenv("APP_LOCALE", "mly")
CATALOGUE_DIR = Path(__file__).resolve().parent
_catalogues: dict[str, dict[str, Any]] = {}


def _load_catalogue(locale: str) -> dict[str, Any]:
    if locale not in _catalogues:
        path = CATALOGUE_DIR / f"{locale}.json"
        if not path.exists():
            return {}

        with path.open(encoding="utf-8") as catalogue_file:
            _catalogues[locale] = json.load(catalogue_file)

    return _catalogues[locale]


def _read_path(catalogue: dict[str, Any], key: str) -> Any:
    value: Any = catalogue
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def t(key: str, locale: str | None = None, **params: Any) -> str:
    selected_locale = locale or DEFAULT_LOCALE
    value = _read_path(_load_catalogue(selected_locale), key)

    if value is None and selected_locale != DEFAULT_LOCALE:
        value = _read_path(_load_catalogue(DEFAULT_LOCALE), key)

    if not isinstance(value, str):
        return key

    return value.format_map(_TranslationParams(params))


class _TranslationParams(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"