WELCOME_MESSAGE = "Первая попытка запустить проект!"
COMMAND_PROMPT = "Введите команду: "

HELP_COMMAND = "help"
EXIT_COMMAND = "exit"

HELP_TEXT = """<command> exit - выйти из программы
<command> help - справочная информация"""

UNKNOWN_COMMAND_MESSAGE = "Функции {command} нет. Попробуйте снова."

META_FILE = "db_meta.json"
FILE_ENCODING = "utf-8"
JSON_INDENT = 4


VALID_TYPES = ("int", "str", "bool")
ID_COLUMN_NAME = "ID"
ID_COLUMN_TYPE = "int"
COLUMN_SEPARATOR = ":"
COLUMN_LIST_SEPARATOR = ", "

INVALID_VALUE_MESSAGE = "Некорректное значение: {value}. Попробуйте снова."
EMPTY_COLUMNS_MESSAGE = "Ошибка: Необходимо указать хотя бы один столбец."
TABLE_EXISTS_MESSAGE = 'Ошибка: Таблица "{table_name}" уже существует.'
TABLE_NOT_FOUND_MESSAGE = 'Ошибка: Таблица "{table_name}" не существует.'
TABLE_CREATED_MESSAGE = (
    'Таблица "{table_name}" успешно создана со столбцами: {columns}'
)
TABLE_DROPPED_MESSAGE = 'Таблица "{table_name}" успешно удалена.'
TABLE_LIST_ITEM = "- {table_name}"
EMPTY_TABLES_MESSAGE = "Таблиц пока нет."