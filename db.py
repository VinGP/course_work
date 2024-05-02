import csv
import datetime
import uuid
from copy import deepcopy

from prettytable import PrettyTable

from config import COLUMN_NAMES, DB_COLUMNS_TYPE
from utils import _input


def save_db(db: dict, db_filename: str) -> None:
    """
    Функция для сохраниеня базы данных в csv файл
    :param db: База данных
    :param db_filename: Имя csv файла
    :return:
    """

    data = list(db.values())
    with open(db_filename, "w", encoding="UTF-8") as f:
        w = csv.DictWriter(f, data[0].keys())
        w.writeheader()
        for d in data:
            w.writerow(d)


def get_db(db_filename: str) -> dict:
    """
    Функция для получения базы данных
    :param db_filename: файл базы данных
    :return: база данных
    """

    db = {}

    with open(db_filename, "r", encoding="UTF-8") as f:
        w = csv.DictReader(f)
        for row in w:
            db[row["id"]] = convert_column(row)

    return db


def convert_column(data: dict) -> dict:
    """
    Функция для конвертации типов данных базе данных
    :param data: данные для конвертации
    :return:
    """

    for column in data:
        _type = DB_COLUMNS_TYPE.get(column)
        if _type is None:
            continue
        data[column] = _type(data[column])

    return data


def add_note(db: dict) -> dict:
    """
    Функция для добавления записи
    :param db: база данных
    :return:
    """

    note_id = str(uuid.uuid4())
    note = {
        "id": note_id,
    }
    while True:
        surname = _input(prompt="Введите фамилию: ").strip()
        for a in surname:
            if not a.isalpha():
                print("Фамилия может содержать только буквы")
                continue
        break

    while True:
        name = _input(prompt="Введите имя: ")
        for a in name:
            if not a.isalpha():
                print("Имя может содержать только буквы")
                continue
        break

    while True:
        patronymic = _input(prompt="Введите отчество: ")
        for a in patronymic:
            if not a.isalpha():
                print("Отчество может содержать только буквы")
                continue
        break

    job_title = _input(prompt="Введите название должности: ")

    while True:
        salary = _input(
            value_type=int,
            prompt="Введите зарплату: ",
        )
        if salary < 0:
            print("Зарплата не может быть отрицательной")
            continue
        break

    while True:
        work_experience_in_another_company = _input(
            int, "Введите опыт работы в дргих компаниях (лет): "
        )
        if work_experience_in_another_company < 0:
            print("Опыт работы не может быть отрицательный")
            continue
        if work_experience_in_another_company > 100:
            print("Опыт работы не может быть больше 100 лет")
            continue
        break

    hired = datetime.datetime.now().timestamp()

    note["surname"] = surname
    note["name"] = name
    note["patronymic"] = patronymic
    note["job_title"] = job_title
    note["salary"] = salary
    note["hired"] = hired
    note["work_experience_in_another_company"] = work_experience_in_another_company

    db[note_id] = note

    return note


def add_n_notes(db: dict) -> None:
    """
    Функция для добавления нескольких записей
    :param db: база данных
    :return:
    """
    n = _input(int, "Введите количество записей: ")
    for n in range(n):
        note = add_note(db)
        print("Сотрудник добавлен. Его индивидуальный номер: ", note["id"])
    print("Записи добавлены")


def delete_note_by_key(db: dict) -> None:
    """
    Функция для удаления записи
    :param db: база данных
    :return:
    """

    key = _input(str, "Введите индивидуальный номер сотрудника для удаления: ")
    if key not in db:
        print("Нет сотрудника с таким индивидуальным номером")
        return

    del db[key]

    print("Сотрудник удален")


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


def print_db(db: dict) -> None:
    """
    Функция для печати базы данных
    :param db: база данных
    :return:
    """
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
