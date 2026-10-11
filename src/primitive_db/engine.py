import shlex

import prompt

from primitive_db.constants import (
    COMMAND_PROMPT,
    CREATE_TABLE_COMMAND,
    CREATE_TABLE_MIN_ARGUMENTS,
    DROP_TABLE_ARGUMENTS,
    DROP_TABLE_COMMAND,
    EXIT_COMMAND,
    HELP_COMMAND,
    HELP_TEXT,
    INVALID_VALUE_MESSAGE,
    LIST_TABLES_COMMAND,
    META_FILE,
    UNKNOWN_COMMAND_MESSAGE,
)
from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Выводит справку по доступным командам."""
    print()
    print(HELP_TEXT)
    print()


def run():
    """Запускает цикл ввода команд и управления таблицами."""
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string(COMMAND_PROMPT).strip()

        try:
            tokens = shlex.split(user_input)
        except ValueError:
            print(INVALID_VALUE_MESSAGE.format(value=user_input))
            continue

        if not tokens:
            continue

        command = tokens[0]
        arguments = tokens[1:]
        result = None

        if command == EXIT_COMMAND:
            if arguments:
                print(INVALID_VALUE_MESSAGE.format(value=user_input))
                continue
            break

        elif command == HELP_COMMAND:
            if arguments:
                print(INVALID_VALUE_MESSAGE.format(value=user_input))
                continue
            print_help()

        elif command == LIST_TABLES_COMMAND:
            if arguments:
                print(INVALID_VALUE_MESSAGE.format(value=user_input))
                continue
            list_tables(metadata)

        elif command == CREATE_TABLE_COMMAND:
            if len(arguments) < CREATE_TABLE_MIN_ARGUMENTS:
                print(INVALID_VALUE_MESSAGE.format(value=user_input))
                continue
            table_name = arguments[0]
            columns = arguments[1:]
            result = create_table(metadata, table_name, columns)

        elif command == DROP_TABLE_COMMAND:
            if len(arguments) != DROP_TABLE_ARGUMENTS:
                print(INVALID_VALUE_MESSAGE.format(value=user_input))
                continue
            result = drop_table(metadata, arguments[0])

        else:
            print(UNKNOWN_COMMAND_MESSAGE.format(command=command))

        if result is not None:
            save_metadata(META_FILE, result)