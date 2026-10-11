import prompt

from primitive_db.constants import (
    COMMAND_PROMPT,
    EXIT_COMMAND,
    HELP_COMMAND,
    HELP_TEXT,
    UNKNOWN_COMMAND_MESSAGE,
    WELCOME_MESSAGE,
)


def print_help():
    """Выводит список доступных команд."""
    print(HELP_TEXT)


def welcome():
    """Запускает цикл обработки команд пользователя."""
    print(WELCOME_MESSAGE)
    print()
    print("***")
    print_help()

    while True:
        command = prompt.string(COMMAND_PROMPT).strip()

        if command == EXIT_COMMAND:
            break
        elif command == HELP_COMMAND:
            print()
            print_help()
        else:
            print(UNKNOWN_COMMAND_MESSAGE.format(command=command))