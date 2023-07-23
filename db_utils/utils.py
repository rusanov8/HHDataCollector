import psycopg2
from config import config

params = config()


def create_database(database_name: str, params: dict) -> None:
    """Создание БД и таблиц для сохранения данных о вакансиях"""

    # Создаем БД
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.set_session(autocommit=True)  # Отключаем автоматический транзакционный режим

    cur = conn.cursor()

    cur.execute(f'drop database if exists {database_name}')
    cur.execute(f'create database {database_name}')

    cur.close()
    conn.close()

    # Создаем таблицу employers
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                    create table employers (
                        employer_id serial primary key,
                        company_name varchar(255) unique,
                        company_info_url varchar(255)
                    )
                """)

    # Создаем таблицу vacancies
    with conn.cursor() as cur:
        cur.execute("""
                     CREATE TABLE vacancies (
                         vacancy_id serial primary key,
                         employer_id int references employers(employer_id) on delete cascade,
                         title varchar(255) not null,
                         salary int,
                         location varchar(100),
                         url varchar(255),
                         requirements text,
                         description text,
                         experience text
                     )
                 """)

    conn.commit()
    conn.close()


def save_data_to_database(data: dict, database_name: str, params: dict) -> None:
    try:
        conn = psycopg2.connect(dbname=database_name, **params)

        # Заполняем таблицу данными из словаря
        with conn.cursor() as cur:
            # Цикл по ключам и значениям словаря
            for company_name, vacancies in data.items():
                # Заполняем таблицу employers
                cur.execute(""" 
                            insert into employers (company_name, company_info_url)
                            values (%s, %s)
                            on conflict (company_name) do nothing
                            returning employer_id
                            """, (company_name, vacancies[0]['company_info_url']))

                # Получаем значение employer_id из кортежа
                employer_id = cur.fetchone()[0]

                # Цикл по списку с вакансиями
                for vacancy in vacancies:
                    # Заполняем таблицу vacancies
                    cur.execute(""" 
                            insert into vacancies 
                            (employer_id, title, salary, location, url, requirements, description, experience)
                            values (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, (employer_id, vacancy['title'], vacancy['salary'], vacancy['location'], vacancy['url'],
                                  vacancy['requirements'], vacancy['description'], vacancy['experience']))

        # Коммит изменений в БД
        conn.commit()

    # Обрабатываем исключения при сохранении данных в БД
    except psycopg2.Error as e:
        print(f'Произошла ошибка при сохранении данных в БД: {e}')
    finally:
        # Закрываем соединение
        conn.close()
            
            





