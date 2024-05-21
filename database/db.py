"""
database/db.py

Модуль работы с базой данных
Программист: Воронин И.Д. гр.344
Проверил: Дмитриева Т.А
Дата написания: 02.05.2024
"""

import csv
import datetime
import uuid
from pathlib import Path

from database.utils import convert_column
from utils import _input


def save_db(db: dict, db_filename: str) -> None:
    """
    Функция для сохранения базы данных в csv файл
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

    if not Path(db_filename).exists():
        return db

    with open(db_filename, "r", encoding="UTF-8") as f:
        w = csv.DictReader(f)
        for row in w:
            db[row["id"]] = convert_column(row)

    return db


def add_note(db: dict) -> dict:
    """
    Функция для добавления записи
    :param db: база данных
    :return: добавленная запись
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
