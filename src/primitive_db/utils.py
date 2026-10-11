import json
import os

from primitive_db.constants import (
    DATA_DIR,
    FILE_ENCODING,
    FILE_WRITE_MODE,
    JSON_INDENT,
    TABLE_FILE_EXTENSION,
)


def load_json(filepath, default):
    """Загружает JSON или возвращает default, если файла нет."""
    try:
        with open(filepath, encoding=FILE_ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def save_json(filepath, data):
    """Сохраняет данные в JSON-файл."""
    with open(filepath, FILE_WRITE_MODE, encoding=FILE_ENCODING) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=JSON_INDENT,
        )


def load_metadata(filepath):
    """Загружает метаданные таблиц."""
    return load_json(filepath, {})


def save_metadata(filepath, data):
    """Сохраняет метаданные таблиц."""
    save_json(filepath, data)


def get_table_path(table_name):
    """Формирует путь к файлу таблицы после проверки имени."""
    if not table_name.isidentifier():
        raise ValueError(f"Некорректное имя таблицы: {table_name}")

    filename = f"{table_name}{TABLE_FILE_EXTENSION}"
    return os.path.join(DATA_DIR, filename)


def load_table_data(table_name):
    """Загружает записи таблицы или возвращает пустой список."""
    filepath = get_table_path(table_name)
    return load_json(filepath, [])


def save_table_data(table_name, data):
    """Создаёт папку данных и сохраняет записи таблицы."""
    filepath = get_table_path(table_name)
    os.makedirs(DATA_DIR, exist_ok=True)
    save_json(filepath, data)


def delete_table_data(table_name):
    """Удаляет файл таблицы, если он существует."""
    filepath = get_table_path(table_name)

    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass