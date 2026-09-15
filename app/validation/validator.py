"""Validador simples usado nos DTOs de entrada: acumula mensagens de erro e
lança ValidationException se houver alguma.
"""

from __future__ import annotations

import re
from typing import Any, Optional
from urllib.parse import urlparse

from app.exceptions import ValidationException

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _is_positive_int(value: Any) -> bool:
    if isinstance(value, bool):
        return False

    if isinstance(value, int):
        return value > 0

    if isinstance(value, float):
        return value.is_integer() and value > 0

    if isinstance(value, str):
        try:
            number = float(value)
        except ValueError:
            return False

        return number.is_integer() and number > 0

    return False


def _is_valid_url(value: str) -> bool:
    parsed = urlparse(value)

    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def not_blank(self, value: Any, message: str) -> "Validator":
        if not isinstance(value, str) or value.strip() == "":
            self.errors.append(message)

        return self

    def max_length(self, value: Any, max_length: int, message: str) -> "Validator":
        if isinstance(value, str) and len(value) > max_length:
            self.errors.append(message)

        return self

    def email(self, value: Any, message: str) -> "Validator":
        if not isinstance(value, str) or not _EMAIL_RE.match(value):
            self.errors.append(message)

        return self

    def url(self, value: Any, message: str, optional: bool = False) -> "Validator":
        if optional and (value is None or value == ""):
            return self

        if not isinstance(value, str) or not _is_valid_url(value):
            self.errors.append(message)

        return self

    def not_null(self, value: Any, message: str) -> "Validator":
        if value is None:
            self.errors.append(message)

        return self

    def positive(self, value: Any, message: str) -> "Validator":
        if not _is_positive_int(value):
            self.errors.append(message)

        return self

    def positive_list(self, value: Optional[list], message: str) -> "Validator":
        if value is None:
            return self

        if not isinstance(value, list):
            self.errors.append(message)

            return self

        for item in value:
            if not _is_positive_int(item):
                self.errors.append(message)
                break

        return self

    def validate(self) -> None:
        if self.errors:
            raise ValidationException(self.errors)
