from primitive_db.constants import (
    COLUMN_LIST_SEPARATOR,
    COLUMN_SEPARATOR,
    EMPTY_COLUMNS_MESSAGE,
    EMPTY_TABLES_MESSAGE,
    ID_COLUMN_NAME,
    ID_COLUMN_TYPE,
    INVALID_VALUE_MESSAGE,
    TABLE_CREATED_MESSAGE,
    TABLE_DROPPED_MESSAGE,
    TABLE_EXISTS_MESSAGE,
    TABLE_LIST_ITEM,
    TABLE_NOT_FOUND_MESSAGE,
    VALID_TYPES,
)


def build_schema(columns):
    if not columns:
        print(EMPTY_COLUMNS_MESSAGE)
        return None

    schema = {ID_COLUMN_NAME: ID_COLUMN_TYPE}
    provided_names = set()

    for column in columns:
        column_name, separator, data_type = column.partition(COLUMN_SEPARATOR)

        if (
            not separator
            or not column_name.isidentifier()
            or column_name in provided_names
            or data_type not in VALID_TYPES
            or (
                column_name == ID_COLUMN_NAME
                and data_type != ID_COLUMN_TYPE
            )
        ):
            print(INVALID_VALUE_MESSAGE.format(value=column))
            return None

        provided_names.add(column_name)
        schema[column_name] = data_type

    return schema


def format_schema(schema):
    return COLUMN_LIST_SEPARATOR.join(
        f"{column_name}{COLUMN_SEPARATOR}{data_type}"
        for column_name, data_type in schema.items()
    )


def create_table(metadata, table_name, columns):
    if not table_name.isidentifier():
        print(INVALID_VALUE_MESSAGE.format(value=table_name))
        return None

    if table_name in metadata:
        print(TABLE_EXISTS_MESSAGE.format(table_name=table_name))
        return None

    schema = build_schema(columns)
    if schema is None:
        return None

    metadata[table_name] = schema
    print(
        TABLE_CREATED_MESSAGE.format(
            table_name=table_name,
            columns=format_schema(schema),
        )
    )
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(TABLE_NOT_FOUND_MESSAGE.format(table_name=table_name))
        return None

    del metadata[table_name]
    print(TABLE_DROPPED_MESSAGE.format(table_name=table_name))
    return metadata


def list_tables(metadata):
    if not metadata:
        print(EMPTY_TABLES_MESSAGE)
        return

    for table_name in metadata:
        print(TABLE_LIST_ITEM.format(table_name=table_name))