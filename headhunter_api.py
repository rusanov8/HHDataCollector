import requests
import time

class HeadHunterApi:
    """Класс для получения вакансий с Headhunter"""

    # Объявляем в атрибуты класса переменные для подключения к api
    pages_count = 20
    base_url = 'https://api.hh.ru/vacancies'

    default_params = {
        'per_page': 0,
        'page': 0,
        'only_with_salary': True,
    }

    def __init__(self, companies=None):
        # Сохраняем список компаний, по которым будем искать вакансии
        # Если companies не передан при создании объекта, используется пустой список []
        self.companies = companies or []
        # Получаем идентификаторы компаний при инициализации объекта
        self.employers_ids = self.get_employers_id()

    def get_employers_id(self):
        """Метод возвращает словарь с id работодателей, по которым будем искать вакансии"""

        # Создаем пустой словарь для компаний и их id
        employers_ids = {}

        for company in self.companies:
            # Устанавливаем параметры для api запроса
            self.default_params['per_page'] = 1
            self.default_params['text'] = f'COMPANY_NAME:{company}'

            try:
                response = requests.get(self.base_url, params=self.default_params)
                response.raise_for_status()
                data = response.json()
                if 'items' in data and len(data['items']) > 0:
                    employer_id = data['items'][0]['employer']['id']
                    employers_ids[company] = employer_id
                    time.sleep(0.25)

            except (requests.exceptions.HTTPError,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.TooManyRedirects,
                    requests.exceptions.RequestException) as e:
                print(f'Произошла ошибка при запросе к API: {e}')

        return employers_ids

    def search_vacancies(self, employer_id):
        """Метод получает вакансии с HeadHunter по id работодателя и возвращает их в виде списка"""

        # Устанавливаем новые параметры для api запроса
        params = dict(self.default_params)
        params['per_page'] = 100
        params['employer_id'] = employer_id
        del params['text']

        # Пустой список для вакансий
        vacancies = []

        # Цикл по количеству страниц поиска
        try:
            for params['page'] in range(self.pages_count):
                response = requests.get(self.base_url, params)
                response.raise_for_status()  # рейз исключений
                data = response.json()
                if 'items' in data:
                    vacancies.extend(data['items'])

        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects,
                requests.exceptions.RequestException) as e:
            print(f'Произошла ошибка при запросе к API: {e}')

        return vacancies

    @staticmethod
    def format_salary(salary):
        """Метод для форматирования зарплаты"""
        # Если зарплата не указана, возвращаем 0
        try:
            if salary is None:
                formatted_salary = 0

            # Если отсутствуют ключи from или get, возвращаем 0
            from_salary = salary.get('from', 0)
            to_salary = salary.get('to', 0)

            # Проверяем все ключи на значения None
            if from_salary is not None and to_salary is not None and from_salary != to_salary:
                formatted_salary = int((from_salary + to_salary) / 2)
            elif from_salary == to_salary:
                formatted_salary = from_salary
            elif from_salary is None:
                formatted_salary = to_salary
            elif to_salary is None:
                formatted_salary = from_salary

            return formatted_salary

        except (TypeError, ValueError, KeyError, AttributeError) as e:
            print(f'Произошла ошибка при форматировании зарплаты: {e}')
            return 0

    @staticmethod
    def format_vacancy(vacancy):
        """Метод для форматирования вакансий"""

        # Вызываем метод форматирования зарплаты
        try:
            formatted_salary = HeadHunterApi.format_salary(vacancy.get('salary'))

            # Для каждой вакансии оставляем только нижеперечисленные данные
            formatted_vacancy = {
                'title': vacancy['name'],
                'company_name': vacancy.get('employer', {}).get('name'),
                'company_info_url': vacancy.get('employer', {}).get('alternate_url') or 'Ссылка не указана',
                'location': vacancy.get('area', {}).get('name') or 'Место работы не указано',
                'url': vacancy.get('alternate_url') or 'Ссылка не указана',
                'salary': formatted_salary,
                'requirements': vacancy.get('snippet', {}).get('requirement') or 'Требования не указаны',
                'description': vacancy.get('snippet', {}).get('responsibility') or 'Описание не указано',
                'experience': vacancy.get('experience', {}).get('name') or 'Опыт не указан'
            }

            return formatted_vacancy

        except Exception as e:
            print(f'Произошла ошибка при форматировании вакансии: {e}')
            return {}

    def get_vacancies(self):
        """Метод возвращает словарь с отформатированными вакансиями,
        где ключ - название компании, а значение - список вакансий этой компании"""

        # Получаем id компаний
        employers_ids = self.get_employers_id()

        # Словарь для упаковки компаний и их вакансий
        vacancies_data = {}
        for company_name, employer_id in employers_ids.items():

            # Получаем список вакансий для каждого работодателя
            vacancies_for_employer = self.search_vacancies(employer_id)
            time.sleep(0.5)
            # Форматируем вакансии и добавляем их в словарь
            formatted_vacancies = [self.format_vacancy(vacancy) for vacancy in vacancies_for_employer]
            vacancies_data[company_name] = formatted_vacancies

        return vacancies_data


