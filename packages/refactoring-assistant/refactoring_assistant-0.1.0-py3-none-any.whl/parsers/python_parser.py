import ast
from typing import Any
from .base_parser import BaseParser


class PythonParser(BaseParser):
    """Класс для парсинга Python кода."""

    def parse(self, code: str) -> Any:
        """Разбирает Python код с помощью ast модуля."""
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Ошибка синтаксиса Python: {e}")