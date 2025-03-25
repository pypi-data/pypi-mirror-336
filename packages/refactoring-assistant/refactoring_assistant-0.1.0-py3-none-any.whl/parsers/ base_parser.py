from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """Базовый абстрактный класс для парсеров кода."""

    @abstractmethod
    def parse(self, code: str) -> Any:
        """Разбирает код и возвращает его представление для анализа."""
        pass

