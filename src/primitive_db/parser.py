import shlex

from primitive_db.constants import (
    ASSIGNMENT_TOKEN_COUNT,
    BOOLEAN_VALUES,
    INVALID_VALUE_MESSAGE,
    VALUE_PUNCTUATION,
    VALUE_QUOTES,
)


def tokenize(text):
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
    condition = parse_assignments(text)
    if len(condition) != 1:
        raise ValueError(INVALID_VALUE_MESSAGE.format(value=text))
    return condition


def parse_set(text):
    return parse_assignments(text)