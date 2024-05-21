"""
database/utils.py

Модуль вспомогательных функций для базы данных
Программист: Воронин И.Д. гр.344
Проверил: Дмитриева Т.А
Дата написания: 02.05.2024
"""

import datetime
from copy import deepcopy

from prettytable import PrettyTable

from config import COLUMN_NAMES, DB_COLUMNS_TYPE


def convert_column(data: dict) -> dict:
    """
    Функция для конвертации типов данных базе данных
    :param data: данные для конвертации
    :return: конвертированные данные
    """

    for column in data:
        _type = DB_COLUMNS_TYPE.get(column)
        if _type is None:
            continue
        data[column] = _type(data[column])

    return data


def print_db(db: dict) -> None:
    """
    Функция для печати базы данных
    :param db: база данных
    :return:
    """
    if not db:
        print("База данных пуста")
        return
    db_copy = deepcopy(db)

    for key in db_copy:
        worker = db_copy[key]
        worker["hired"] = datetime.datetime.fromtimestamp(worker["hired"])
        worked_at_company = datetime.datetime.now() - worker["hired"]
        experience = worked_at_company + datetime.timedelta(
            days=worker["work_experience_in_another_company"] * 365
        )

        worker["worked_at_company"] = worked_at_company.days // 7
        worker["experience"] = round(experience.days / 365.25, 1)
        worker["hired"] = worker["hired"].strftime("%Y-%m-%d")
    data = list(db_copy.values())
    table = PrettyTable()

    table.field_names = [COLUMN_NAMES.get(c, c) for c in data[0].keys()]
    table.add_rows([d.values() for d in data])

    print(table)
