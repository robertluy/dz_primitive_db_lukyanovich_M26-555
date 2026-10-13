import shlex

from primitive_db.constants import (
    ASSIGNMENT_TOKEN_COUNT,
    BOOLEAN_VALUES,
    INVALID_VALUE_MESSAGE,
    VALUE_PUNCTUATION,
    VALUE_QUOTES,
)


def tokenize(text):
    """Разбивает команду на токены с сохранением кавычек значений"""
    lexer = shlex.shlex(
        text,
        posix=False,
        punctuation_chars=VALUE_PUNCTUATION,
    )
    lexer.whitespace_split = True
    lexer.commenters = ""

    tokens = []
    for token in lexer:
        if all(character in VALUE_PUNCTUATION for character in token):
            tokens.extend(token)
        else:
            tokens.append(token)
    return tokens


def parse_value(token):
    """Преобразует токен в строку, целое число или логическое значение"""
    if token.startswith(VALUE_QUOTES):
        values = shlex.split(token)
        if len(values) != 1:
            raise ValueError(INVALID_VALUE_MESSAGE.format(value=token))
        return values[0]

    if token.lower() in BOOLEAN_VALUES:
        return BOOLEAN_VALUES[token.lower()]

    try:
        return int(token)
    except ValueError:
        raise ValueError(
            INVALID_VALUE_MESSAGE.format(value=token)
        ) from None


def split_items(tokens):
    """Разделяет токены по запятым и отклоняет пустые элементы"""
    items = []
    current_item = []

    for token in tokens:
        if token == ",":
            if not current_item:
                raise ValueError(
                    INVALID_VALUE_MESSAGE.format(value=",")
                )
            items.append(current_item)
            current_item = []
        else:
            current_item.append(token)

    if not current_item:
        raise ValueError(INVALID_VALUE_MESSAGE.format(value=","))

    items.append(current_item)
    return items


def parse_values(text):
    """Разбирает список значений в скобках для команды insert"""
    tokens = tokenize(text)

    if tokens[:1] != ["("] or tokens[-1:] != [")"]:
        raise ValueError(INVALID_VALUE_MESSAGE.format(value=text))

    value_tokens = tokens[1:-1]
    if not value_tokens:
        return []

    values = []
    for item in split_items(value_tokens):
        if len(item) != 1:
            raise ValueError(INVALID_VALUE_MESSAGE.format(value=text))
        values.append(parse_value(item[0]))

    return values


def parse_assignments(text):
    """Преобразует присваивания через запятую в словарь значений"""
    assignments = {}

    for item in split_items(tokenize(text)):
        if (
            len(item) != ASSIGNMENT_TOKEN_COUNT
            or item[1] != "="
            or not item[0].isidentifier()
            or item[0] in assignments
        ):
            raise ValueError(INVALID_VALUE_MESSAGE.format(value=text))

        column_name = item[0]
        assignments[column_name] = parse_value(item[2])

    return assignments


def parse_where(text):
    """Разбирает одно условие равенства для отбора записей"""
    condition = parse_assignments(text)
    if len(condition) != 1:
        raise ValueError(INVALID_VALUE_MESSAGE.format(value=text))
    return condition


def parse_set(text):
    """Разбирает присваивания значений для обновления записей"""
    return parse_assignments(text)

def parse_optional_where(tokens):
    """Разбирает необязательную часть where."""
    if not tokens:
        return None

    if tokens[0] != "where":
        raise ValueError(
            INVALID_VALUE_MESSAGE.format(value=" ".join(tokens))
        )

    return parse_where(" ".join(tokens[1:]))


def parse_data_command(command, arguments):
    """Разбирает аргументы CRUD-команды и возвращает её параметры."""
    message = INVALID_VALUE_MESSAGE.format(
        value=" ".join([command, *arguments])
    )

    if command == "insert":
        if (
            len(arguments) < 4
            or arguments[0] != "into"
            or arguments[2] != "values"
        ):
            raise ValueError(message)

        return {
            "table_name": arguments[1],
            "values": parse_values(" ".join(arguments[3:])),
        }

    if command in ("select", "delete"):
        if len(arguments) < 2 or arguments[0] != "from":
            raise ValueError(message)

        where_clause = parse_optional_where(arguments[2:])
        if command == "delete" and where_clause is None:
            raise ValueError(message)

        return {
            "table_name": arguments[1],
            "where_clause": where_clause,
        }

    if command == "update":
        if len(arguments) < 9 or arguments[1] != "set":
            raise ValueError(message)

        where_index = next(
            (
                index
                for index in range(2, len(arguments))
                if arguments[index] == "where"
                and arguments[index - 1] not in ("set", ",", "=")
            ),
            None,
        )
        if where_index is None:
            raise ValueError(message)

        return {
            "table_name": arguments[0],
            "set_clause": parse_set(
                " ".join(arguments[2:where_index])
            ),
            "where_clause": parse_where(
                " ".join(arguments[where_index + 1:])
            ),
        }

    if command == "info" and len(arguments) == 1:
        return {"table_name": arguments[0]}

    raise ValueError(message)