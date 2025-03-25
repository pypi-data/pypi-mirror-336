Библиотека для выявления участков кода, требующих рефакторинга, с предложениями по улучшениям.

## Установка

```bash
pip install refactoring-assistant
```

## Использование

```python
from refactoring_assistant import CodeAnalyzer

# Создаем анализатор с настраиваемыми порогами
analyzer = CodeAnalyzer(
    threshold_complexity=10,  # Максимальная допустимая сложность функции
    max_line_length=100,      # Максимальная длина строки
    max_function_lines=50     # Максимальное количество строк в функции
)

# Анализ отдельного файла
suggestions = analyzer.analyze_file("path/to/your/file.py")
for suggestion in suggestions:
    print(suggestion)

# Анализ всех Python файлов в директории
results = analyzer.analyze_directory("path/to/directory")
for file, file_suggestions in results.items():
    print(f"Файл: {file}")
    for suggestion in file_suggestions:
        print(f"  {suggestion}")
```

## Возможности

- Обнаружение функций с высокой цикломатической сложностью
- Выявление слишком длинных функций
- Поиск дублирующихся участков кода
- Формирование конкретных предложений по рефакторингу
- Поддержка анализа отдельных файлов и целых директорий

## Для разработчиков

```bash
# Клонирование репозитория
git clone https://github.com/username/refactoring-assistant.git
cd refactoring-assistant

# Установка для разработки
pip install -e .

# Запуск тестов
pytest
```

## Лицензия

MIT