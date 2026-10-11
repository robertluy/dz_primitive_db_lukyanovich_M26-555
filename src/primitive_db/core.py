from primitive_db.constants import (
    COLUMN_LIST_SEPARATOR,
    COLUMN_SEPARATOR,
    EMPTY_COLUMNS_MESSAGE,
    EMPTY_TABLES_MESSAGE,
    ID_COLUMN_NAME,
    ID_COLUMN_TYPE,
    ID_STEP,
    INITIAL_ID,
    INVALID_VALUE_MESSAGE,
    PYTHON_TYPES,
    RECORD_INSERTED_MESSAGE,
    TABLE_CREATED_MESSAGE,
    TABLE_DROPPED_MESSAGE,
    TABLE_EXISTS_MESSAGE,
    TABLE_LIST_ITEM,
    TABLE_NOT_FOUND_MESSAGE,
    VALID_TYPES,
    VALUE_TYPE_MESSAGE,
    VALUES_COUNT_MESSAGE,
)
from primitive_db.utils import (
    delete_table_data,
    load_table_data,
    save_table_data,
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

    save_table_data(table_name, [])
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

    delete_table_data(table_name)
    del metadata[table_name]
    print(TABLE_DROPPED_MESSAGE.format(table_name=table_name))
    return metadata


def list_tables(metadata):
    if not metadata:
        print(EMPTY_TABLES_MESSAGE)
        return

    for table_name in metadata:
        print(TABLE_LIST_ITEM.format(table_name=table_name))


def validate_values(schema, values):
    """Проверяет существование столбцов и точное совпадение типов."""
    for column_name, value in values.items():
        data_type = schema[column_name]
        expected_type = PYTHON_TYPES[data_type]

        if type(value) is not expected_type:
            raise ValueError(
                VALUE_TYPE_MESSAGE.format(
                    column_name=column_name,
                    data_type=data_type,
                    value=value,
                )
            )


def insert(metadata, table_name, values):
    """Проверяет значения и добавляет запись с автоматическим ID."""
    schema = metadata[table_name]
    column_names = [
        column_name
        for column_name in schema
        if column_name != ID_COLUMN_NAME
    ]

    if len(values) != len(column_names):
        raise ValueError(
            VALUES_COUNT_MESSAGE.format(
                expected=len(column_names),
                actual=len(values),
            )
        )

    record_values = dict(zip(column_names, values))
    validate_values(schema, record_values)

    table_data = load_table_data(table_name)
    record_id = max(
        (record[ID_COLUMN_NAME] for record in table_data),
        default=INITIAL_ID,
    ) + ID_STEP

    record = {ID_COLUMN_NAME: record_id}
    record.update(record_values)
    table_data.append(record)

    print(
        RECORD_INSERTED_MESSAGE.format(
            record_id=record_id,
            table_name=table_name,
        )
    )
    return table_data
