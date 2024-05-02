import builtins
from typing import Type, TypeVar

float_input_error = "Неверный формат данных! Пример допустимых форматов: '1', '1.2'"
int_input_error = (
    "Неверный формат данных для целого числа! Пример допустимых форматов: '1', '324'"
)

T = TypeVar("T")


def _input(
    value_type: Type[T] = str,
    prompt: str = None,
    error_description: str = None,
) -> T:
    """
    Функция для получения значения определенного типа из консоли
    :param value_type: тип переменной
    :param prompt: описание ввода
    :param error_description: текст ошибки ввода
    :return:
    """
    if error_description is None:
        match value_type:
            case builtins.int:
                error_description = int_input_error
            case builtins.float:
                error_description = float_input_error
            case _:
                error_description = "Неправильный формат данных! Попробуйте ещё раз"

    while True:
        value = input(prompt)
        try:
            return value_type(value)
        except ValueError:
            print(error_description)
