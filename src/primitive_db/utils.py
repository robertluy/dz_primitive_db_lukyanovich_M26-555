import json

from primitive_db.constants import FILE_ENCODING, JSON_INDENT


def load_metadata(filepath):
    try:
        with open(filepath, encoding=FILE_ENCODING) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w", encoding=FILE_ENCODING) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=JSON_INDENT,
        )