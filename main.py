from config import DB_FILENAME, MENU
from db import *


def print_menu() -> None:
    """
    Функция печати меню
    :return:
    """
    print("МЕНЮ".center(40, "*"))
    print(MENU)


def main() -> None:
    """
    Главная функция
    :return:
    """

    db = get_db(DB_FILENAME)
    while True:
        print_menu()
        choice = input("Выберите пункт меню для продолжения: ")
        match choice:  # Просмотр всех записей в базе данных
            case "1":
                print_db(db)
            case "2":  # Добавление N записей
                add_n_notes(db)
                save_db(db, DB_FILENAME)
                print("Записи добавлены!")
            case "3":  # Удаление записи по ключу
                delete_note_by_key(db)
                save_db(db, DB_FILENAME)
            case "4":  # Поиск сотрудника по фамилии
                search_by_firstname(db)
            case "5":  # Сотрудники с зарплатой ниже средней по предприятию
                employees_with_salaries_below_the_enterprise_average(db)
            case "6":  # Сотрудники со стажем более 10 лет
                employees_with_more_than_10_years_of_experience(db)
            case "7":  # Завершение работы с базой данных
                print("Работа с базой данных завершена")
                exit(0)
            case _:
                print("Такого пункта меню нет! Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
