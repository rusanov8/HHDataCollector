import psycopg2


class DBManager:
    # Класс для работы с данными в БД

    def __init__(self, params: dict, database_name: str):
        # При создании объекта класса сразу открываем коннект и курсор
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        self.cur.execute("""
                        select company_name, count(*) from employers
                        inner join vacancies using(employer_id)
                        group by company_name
                        """)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""

        self.cur.execute("""
                        select company_name, title, salary, url
                        from vacancies 
                        inner join employers using(employer_id)
                        """)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""

        self.cur.execute("""
                        select round(avg(salary)::numeric, 2) 
                        from vacancies
                        """)
        avg_salary = self.cur.fetchone()[0]
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий,
        у которых зарплата выше средней по вакансиям"""

        avg_salary = self.get_avg_salary()

        self.cur.execute(f"""
                        select * from vacancies
                        where salary > {avg_salary}
                        order by salary desc
                        """)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий по ключевому слову"""
        self.cur.execute(f"""
                        select * from vacancies
                        where title like '%{keyword}%'
                        or description like '%{keyword}%'
                        or requirements like '%{keyword}%'
                        """)

    def close(self):
        # Метод для коммита изменений и закрытия подключения к БД
        self.conn.commit()
        self.cur.close()
        self.conn.close()

