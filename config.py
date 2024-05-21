"""
config.py

Модуль конфигурации.
Программист: Воронин И.Д. гр.344
Проверил: Дмитриева Т.А
Дата написания: 02.05.2024
"""


MENU = """1. Просмотр всех записей в базе данных
2. Добавление N записей
3. Удаление записи по ключу
4. Поиск сотрудника по фамилии
5. Сотрудники с зарплатой ниже средней по предприятию
6. Сотрудники со стажем более 10 лет
7. Завершение работы с базой данных"""

DB_FILENAME = "db.csv"

COLUMN_NAMES = {
    "id": "Индивидуальный номер",
    "surname": "Фамилия",
    "name": "Имя",
    "patronymic": "Отчество",
    "work_experience_in_another_company": "Опыт работы в других копаниях (лет)",
    "worked_at_company": "Работает в этой компании (недель)",
    "experience": "Опыт работы (лет)",
    "hired": "Нанят",
    "salary": "Зарплата (руб.)",
    "job_title": "Должность",
}

DB_COLUMNS_TYPE = dict(
    id=str,
    surname=str,
    name=str,
    patronymic=str,
    job_title=str,
    salary=int,
    hired=float,
    work_experience_in_another_company=int,
)
