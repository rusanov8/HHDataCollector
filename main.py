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

    # Закрываем подключение
    db_manager.close()


if __name__ == '__main__':
    main()


