from db_utils.config import config
from db_utils.utils import create_database, save_data_to_database
from headhunter_api import HeadHunterApi
from db_manager import DBManager


def main():

    # Список компаний, по которым ищем вакансии

    companies = ['Skyeng', 'Яндекс', 'VK', 'Тинькофф', 'Ozon', 'Альфа-Банк',
                 'Циан', 'РОЛЬФ', 'Aviasales.ru', 'Skillbox']

    # Объект класса HeadHunterApi для поиска вакансий
    hh = HeadHunterApi(companies)

    # Словарь с вакансиями
    data = hh.get_vacancies()

    # Создаем БД и таблицы
    db_name = 'hh_psql_project'
    params = config()

    create_database(db_name, params)

    save_data_to_database(data, db_name, params)

    # Объект класса DBManager для работы с запросами к таблицам
    db_manager = DBManager(params, db_name)

    # Получаем результаты запросов
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    all_vacancies = db_manager.get_all_vacancies()
    avg_salary = db_manager.get_avg_salary()
    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    keyword = 'python'
    keyword_vacancies = db_manager.get_all_vacancies(keyword)

    # Выводим результаты запросов на экран
    print("Список всех компаний и количество вакансий:")
    for company, vacancies_count in companies_and_vacancies:
        print(f"{company}: {vacancies_count} вакансий")

    print("\nСписок всех вакансий:")
    for company, title, salary, url in all_vacancies:
        print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {url}")

    print("\n Средняя зарплата по вакансиям:", avg_salary)

    print("Вакансии с зарплатой выше средней:")
    for vacancy in higher_salary_vacancies:
        print(vacancy)

    print("Вакансии с ключевым словом 'python':")
    for vacancy in keyword_vacancies:
        print(vacancy)

    # Закрываем подключение
    db_manager.close()


if __name__ == '__main__':
    main()


