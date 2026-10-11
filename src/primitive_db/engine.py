import prompt
from prettytable import PrettyTable

from primitive_db import constants, core, utils
from primitive_db.parser import parse_data_command, tokenize


def print_help():
    """Выводит справку по доступным командам."""
    print()
    print(constants.HELP_TEXT)
    print()


def print_records(schema, records):
    """Выводит записи с заголовками столбцов через PrettyTable."""
    table = PrettyTable()
    table.field_names = list(schema)
    table.add_rows(
        [
            [record[column_name] for column_name in schema]
            for record in records
        ]
    )
    print(table)


def print_record_messages(message, records, table_name):
    """Сообщает результат операции для каждой подходящей записи."""
    if not records:
        print(constants.NO_MATCHES_MESSAGE)
        return

    for record in records:
        print(
            message.format(
                record_id=record[constants.ID_COLUMN_NAME],
                table_name=table_name,
            )
        )


def execute_data_command(metadata, command, arguments):
    """Выполняет CRUD-команду и сохраняет успешные изменения."""
    parameters = parse_data_command(command, arguments)
    table_name = parameters["table_name"]
    schema = metadata[table_name]

    if command == constants.INSERT_COMMAND:
        result = core.insert(
            metadata,
            table_name,
            parameters["values"],
        )
        if result is not None:
            utils.save_table_data(table_name, result)
        return

    table_data = utils.load_table_data(table_name)

    if command == constants.INFO_COMMAND:
        print(
            constants.TABLE_INFO_MESSAGE.format(
                table_name=table_name,
                columns=core.format_schema(schema),
                count=len(table_data),
            )
        )
        return

    where_clause = parameters.get("where_clause")
    selected_records = core.select(table_data, where_clause, schema)
    if selected_records is None:
        return

    if command == constants.SELECT_COMMAND:
        print_records(schema, selected_records)
        return

    if command == constants.UPDATE_COMMAND:
        result = core.update(
            table_data,
            parameters["set_clause"],
            where_clause,
            schema,
        )
        message = constants.RECORD_UPDATED_MESSAGE
    else:
        result = core.delete(table_data, where_clause, schema)
        message = constants.RECORD_DELETED_MESSAGE

    if result is not None:
        utils.save_table_data(table_name, result)
        print_record_messages(message, selected_records, table_name)


def execute_command(metadata, user_input):
    """Выполняет команду; возвращает False при завершении работы."""
    tokens = tokenize(user_input)
    if not tokens:
        return True

    command = tokens[0]
    arguments = tokens[1:]
    invalid_message = constants.INVALID_VALUE_MESSAGE.format(
        value=user_input
    )

    simple_commands = (
        constants.EXIT_COMMAND,
        constants.HELP_COMMAND,
        constants.LIST_TABLES_COMMAND,
    )
    if command in simple_commands and arguments:
        raise ValueError(invalid_message)

    result = None

    if command == constants.EXIT_COMMAND:
        return False
    elif command == constants.HELP_COMMAND:
        print_help()
    elif command == constants.LIST_TABLES_COMMAND:
        core.list_tables(metadata)
    elif command == constants.CREATE_TABLE_COMMAND:
        if len(arguments) < constants.CREATE_TABLE_MIN_ARGUMENTS:
            raise ValueError(invalid_message)
        result = core.create_table(
            metadata,
            arguments[0],
            arguments[1:],
        )
    elif command == constants.DROP_TABLE_COMMAND:
        if len(arguments) != constants.DROP_TABLE_ARGUMENTS:
            raise ValueError(invalid_message)
        result = core.drop_table(metadata, arguments[0])
    elif command in constants.DATA_COMMANDS:
        execute_data_command(metadata, command, arguments)
    else:
        print(
            constants.UNKNOWN_COMMAND_MESSAGE.format(command=command)
        )

    if result is not None:
        utils.save_metadata(constants.META_FILE, result)

    return True


def run():
    """Запускает цикл ввода команд базы данных."""
    print_help()

    while True:
        try:
            user_input = prompt.string(constants.COMMAND_PROMPT).strip()
            metadata = utils.load_metadata(constants.META_FILE)
            if not execute_command(metadata, user_input):
                break
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except KeyError as error:
            print(constants.KEY_ERROR_MESSAGE.format(name=error))
        except ValueError as error:
            print(error)
        except OSError as error:
            print(constants.FILE_ERROR_MESSAGE.format(error=error))