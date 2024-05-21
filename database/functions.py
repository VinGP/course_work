"""
database/functions.py

Модуль прикладных функций для базы данных
Программист: Воронин И.Д. гр.344
Проверил: Дмитриева Т.А
Дата написания: 02.05.2024
"""

import datetime

from database.utils import print_db
from utils import _input


def employees_with_salaries_below_the_enterprise_average(db: dict) -> None:
    """
    Функция для поиска сотрудников с зарплатой ниже средней
    :param db: база данных
    :return:
    """

    if len(db) == 0:
        print("Сотрудников с зарплатой ниже средней не найдено")
        return
    sum_salaries = 0
    count_workers = 0
    for key in db:
        worker = db[key]
        sum_salaries += worker["salary"]
        count_workers += 1

    average = sum_salaries / count_workers
    res = {}
    for key in db:
        worker = db[key]
        if worker["salary"] < average:
            res[key] = worker

    if len(res) == 0:
        print("Сотрудников с зарплатой ниже средней не найдено")
        return
    print("Сотрудники с зарплатой ниже средней:")
    print_db(res)


def employees_with_more_than_10_years_of_experience(db: dict) -> None:
    """
    Функция для поиска сотрудников со стажем более 10 лет
    :param db: база данных
    :return:
    """

    res = {}
    for key in db:
        worker = db[key]

        worked_at_company = datetime.datetime.now() - datetime.datetime.fromtimestamp(
            worker["hired"]
        )
        experience = worked_at_company + datetime.timedelta(
            days=worker["work_experience_in_another_company"] * 365
        )

        experience = round(experience.days / 365.25, 1)

        if experience > 10:
            res[key] = worker

    if len(res) == 0:
        print("Сотрудников со стажем более 10 лет не найдено")
        return

    print("Сотрудники со стажем более 10 лет:")
    print_db(res)


def search_by_firstname(db: dict) -> None:
    """
    Функция для поиска сотрудника по фамилии
    :param db: база данных
    :return:
    """

    while True:
        surname = _input(prompt="Введите фамилию сотрудника: ")
        data = {key: db[key] for key in db if db[key]["surname"] == surname}
        if len(data) == 0:
            print("Ничего не найдено")
        else:
            print_db(data)

        choice = input("Продолжить поиск? (Да/Нет): ")
        if choice.lower() == "нет":
            break
