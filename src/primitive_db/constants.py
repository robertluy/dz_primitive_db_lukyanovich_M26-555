WELCOME_MESSAGE = "Первая попытка запустить проект!"
COMMAND_PROMPT = "Введите команду: "

HELP_COMMAND = "help"
EXIT_COMMAND = "exit"

HELP_TEXT = """***База данных***

Управление таблицами:
<command> create_table <имя_таблицы> <столбец:тип> ... - создать таблицу
<command> list_tables - показать список таблиц
<command> drop_table <имя_таблицы> - удалить таблицу

Операции с данными:
<command> insert into <имя_таблицы> values (<значение1>, ...) - добавить запись
<command> select from <имя_таблицы> - показать все записи
<command> select from <имя_таблицы> where <столбец> = <значение> - отобрать записи
<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить записи
<command> info <имя_таблицы> - показать информацию о таблице

Общие команды:
<command> help - справочная информация
<command> exit - выход из программы"""

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

CREATE_TABLE_COMMAND = "create_table"
DROP_TABLE_COMMAND = "drop_table"
LIST_TABLES_COMMAND = "list_tables"

CREATE_TABLE_MIN_ARGUMENTS = 2
DROP_TABLE_ARGUMENTS = 1

DATA_DIR = "data"
TABLE_FILE_EXTENSION = ".json"
FILE_WRITE_MODE = "w"

PYTHON_TYPES = {
    "int": int,
    "str": str,
    "bool": bool,
}

INITIAL_ID = 0
ID_STEP = 1

VALUES_COUNT_MESSAGE = (
    "Ожидалось значений: {expected}, получено: {actual}. "
    "Значение ID задавать не нужно."
)
VALUE_TYPE_MESSAGE = (
    'Столбец "{column_name}" должен иметь тип {data_type}. '
    "Получено: {value!r}."
)
RECORD_INSERTED_MESSAGE = (
    'Запись с ID={record_id} успешно добавлена в таблицу "{table_name}".'
)

EMPTY_SET_MESSAGE = "Необходимо указать значения для обновления."
EMPTY_WHERE_MESSAGE = "Необходимо указать условие отбора записей."
ID_UPDATE_MESSAGE = "Столбец ID генерируется автоматически и не изменяется."

VALUE_PUNCTUATION = "(),="
VALUE_QUOTES = ('"', "'")
BOOLEAN_VALUES = {"true": True, "false": False}
ASSIGNMENT_TOKEN_COUNT = 3

INSERT_COMMAND = "insert"
SELECT_COMMAND = "select"
UPDATE_COMMAND = "update"
DELETE_COMMAND = "delete"
INFO_COMMAND = "info"

DATA_COMMANDS = (
    INSERT_COMMAND,
    SELECT_COMMAND,
    UPDATE_COMMAND,
    DELETE_COMMAND,
    INFO_COMMAND,
)

RECORD_UPDATED_MESSAGE = (
    'Запись с ID={record_id} в таблице "{table_name}" успешно обновлена.'
)
RECORD_DELETED_MESSAGE = (
    'Запись с ID={record_id} успешно удалена из таблицы "{table_name}".'
)
NO_MATCHES_MESSAGE = "Записи по указанному условию не найдены."

TABLE_INFO_MESSAGE = (
    "Таблица: {table_name}\n"
    "Столбцы: {columns}\n"
    "Количество записей: {count}"
)
KEY_ERROR_MESSAGE = "Ошибка: Таблица или столбец {name} не найден."
FILE_ERROR_MESSAGE = "Ошибка работы с файлами: {error}"