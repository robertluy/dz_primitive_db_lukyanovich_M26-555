import json

from primitive_db.constants import (
    COLUMN_LIST_SEPARATOR,
    COLUMN_SEPARATOR,
    DELETE_RECORDS_ACTION,
    DROP_TABLE_ACTION,
    EMPTY_COLUMNS_MESSAGE,
    EMPTY_SET_MESSAGE,
    EMPTY_TABLES_MESSAGE,
    EMPTY_WHERE_MESSAGE,
    ID_COLUMN_NAME,
    ID_COLUMN_TYPE,
    ID_STEP,
    ID_UPDATE_MESSAGE,
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
from primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)
from primitive_db.utils import (
    delete_table_data,
    load_table_data,
    save_table_data,
)

cache_select = create_cacher()


def build_schema(columns):
    """ Проверят столбцы и создает схему с автоматическим ID"""
    if not columns:
        raise ValueError(EMPTY_COLUMNS_MESSAGE)

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
            raise ValueError(INVALID_VALUE_MESSAGE.format(value=column))

        provided_names.add(column_name)
        schema[column_name] = data_type

    return schema


def format_schema(schema):
    """Преобразвет схему таблицы в строку со столбцами и типами"""
    return COLUMN_LIST_SEPARATOR.join(
        f"{column_name}{COLUMN_SEPARATOR}{data_type}"
        for column_name, data_type in schema.items()
    )


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает файл таблицы и добавляет ее схему в метаданные"""
    if not table_name.isidentifier():
        raise ValueError(INVALID_VALUE_MESSAGE.format(value=table_name))

    if table_name in metadata:
        raise ValueError(TABLE_EXISTS_MESSAGE.format(table_name=table_name))

    schema = build_schema(columns)

    save_table_data(table_name, [])
    metadata[table_name] = schema
    cache_select.clear()
    print(
        TABLE_CREATED_MESSAGE.format(
            table_name=table_name,
            columns=format_schema(schema),
        )
    )
    return metadata


@handle_db_errors
@confirm_action(DROP_TABLE_ACTION)
def drop_table(metadata, table_name):
    """Удаляет файл таблицы и ее схему из метаданных"""
    if table_name not in metadata:
        raise ValueError(TABLE_NOT_FOUND_MESSAGE.format(table_name=table_name))

    delete_table_data(table_name)
    del metadata[table_name]
    cache_select.clear()
    print(TABLE_DROPPED_MESSAGE.format(table_name=table_name))
    return metadata


@handle_db_errors
def list_tables(metadata):
    """Выводит список таблиц или сообщение об их отсутствии"""
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


@handle_db_errors
@log_time
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
    cache_select.clear()

    print(
        RECORD_INSERTED_MESSAGE.format(
            record_id=record_id,
            table_name=table_name,
        )
    )
    return table_data


def validate_clauses(table_data, clauses, schema=None):
    """Проверяет столбцы и типы значений в условиях."""
    if schema is None:
        if not table_data:
            return

        schema = {
            column_name: type(value).__name__
            for column_name, value in table_data[0].items()
        }

    for clause in clauses:
        if clause is not None:
            validate_values(schema, clause)


def matches_where(record, where_clause):
    """Проверяет совпадение записи со всеми условиями."""
    if where_clause is None:
        return True

    return all(
        type(record[column_name]) is type(value)
        and record[column_name] == value
        for column_name, value in where_clause.items()
    )


@handle_db_errors
@log_time
def select(table_data, where_clause=None, schema=None):
    """Возвращает подходящие записи с попощью кэша выборок"""
    validate_clauses(table_data, [where_clause], schema)

    cache_key = json.dumps(
        [table_data, where_clause, schema],
        sort_keys=True,
        ensure_ascii=False,
    )

    cached_records = cache_select(
        cache_key,
        lambda: [
            record.copy()
            for record in table_data
            if matches_where(record, where_clause)
        ],
    )

    return [record.copy() for record in cached_records]


@handle_db_errors
def update(table_data, set_clause, where_clause, schema=None):
    """Обновляет подходящие записи после проверки всех условий."""
    if not set_clause:
        raise ValueError(EMPTY_SET_MESSAGE)

    if not where_clause:
        raise ValueError(EMPTY_WHERE_MESSAGE)

    if ID_COLUMN_NAME in set_clause:
        raise ValueError(ID_UPDATE_MESSAGE)

    validate_clauses(table_data, [set_clause, where_clause], schema)

    for record in table_data:
        if matches_where(record, where_clause):
            record.update(set_clause)
    cache_select.clear()
    return table_data


@handle_db_errors
@confirm_action(DELETE_RECORDS_ACTION)
def delete(table_data, where_clause, schema=None):
    """Удаляет подходящие записи и сбрасывает кэш выборок."""
    if not where_clause:
        raise ValueError(EMPTY_WHERE_MESSAGE)

    validate_clauses(table_data, [where_clause], schema)

    remaining_records = [
        record for record in table_data
        if not matches_where(record, where_clause)
    ]

    cache_select.clear()
    return remaining_records
