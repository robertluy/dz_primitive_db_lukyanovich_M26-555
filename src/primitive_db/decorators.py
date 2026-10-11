import time

import prompt

from primitive_db import constants


def preserve_metadata(wrapper, function):
    """Сохраняет имя, описание и ссылку на исходную функцию."""
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    wrapper.__wrapped__ = function
    return wrapper


def handle_db_errors(function):
    """Перехватывает ошибки базы данных и выводит сообщения."""
    def wrapper(*args, **kwargs):
        """Вызывает функцию с обработкой ошибок."""
        try:
            return function(*args, **kwargs)
        except FileNotFoundError:
            print(constants.FILE_NOT_FOUND_MESSAGE)
        except KeyError as error:
            print(constants.KEY_ERROR_MESSAGE.format(name=error))
        except ValueError as error:
            print(error)
        except OSError as error:
            print(constants.FILE_ERROR_MESSAGE.format(error=error))
        except Exception as error:
            print(
                constants.UNEXPECTED_ERROR_MESSAGE.format(error=error)
            )
        return None

    return preserve_metadata(wrapper, function)


def confirm_action(action_name):
    """Создаёт декоратор подтверждения указанного действия."""
    def decorator(function):
        """Оборачивает функцию запросом подтверждения."""
        def wrapper(*args, **kwargs):
            """Выполняет действие только после подтверждения."""
            answer = prompt.string(
                constants.CONFIRM_PROMPT.format(action_name=action_name)
            )
            if answer.strip().lower() != constants.CONFIRM_YES:
                print(constants.ACTION_CANCELLED_MESSAGE)
                return None
            return function(*args, **kwargs)

        return preserve_metadata(wrapper, function)

    return decorator


def log_time(function):
    """Измеряет время выполнения функции через monotonic."""
    def wrapper(*args, **kwargs):
        """Вызывает функцию и выводит затраченное время."""
        started_at = time.monotonic()
        try:
            return function(*args, **kwargs)
        finally:
            elapsed = time.monotonic() - started_at
            print(
                constants.TIME_MESSAGE.format(
                    function_name=function.__name__,
                    elapsed=elapsed,
                )
            )

    return preserve_metadata(wrapper, function)