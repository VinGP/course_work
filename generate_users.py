import datetime
import random
import uuid

from mimesis import Gender, Locale, Person
from mimesis.builtins import RussiaSpecProvider

import db as db_package
from utils import _input

person = Person(Locale.RU)
ru = RussiaSpecProvider()

jobs = [
    "Директор",
    "Администратор",
    "Технический директор",
    "Юрист",
    "Бухгалтер",
    "Системный администратор",
    "Программист",
]


def generate_db(n: int) -> dict:
    db = {}

    for _ in range(n):
        id = str(uuid.uuid4())
        note = {
            "id": id,
        }

        gender = random.choices([Gender.MALE, Gender.FEMALE], [0.5, 0.5])[0]
        name = person.name(gender=gender)
        surname = person.surname(gender=gender)
        patronymic = ru.patronymic(gender=gender)
        job_title = random.choices(jobs)[0]
        salary = random.randint(50_000, 200_000)
        hired = (
            datetime.datetime.now() - datetime.timedelta(days=random.randint(100, 1000))
        ).timestamp()
        work_experience_in_another_company = random.randint(0, 10)

        note["surname"] = surname
        note["name"] = name
        note["patronymic"] = patronymic
        note["job_title"] = job_title
        note["salary"] = salary
        note["hired"] = hired
        note["work_experience_in_another_company"] = work_experience_in_another_company
        db[id] = note

    return db


def main() -> None:
    n = _input(int, "Введите количество записей для генерации: ")

    db = generate_db(n)
    db_package.print_db(db)
    db_package.save_db(db, "db.csv")


if __name__ == "__main__":
    main()
