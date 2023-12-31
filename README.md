Проект "Работа с базами данных: Получение данных о компаниях и вакансиях с hh.ru"

Описание проекта:

Проект "Работа с базами данных" представляет собой программу, которая позволяет получить
данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в 
базе данных PostgreSQL и загрузить полученные данные в созданные таблицы. 
Для работы с базой данных используется библиотека psycopg2, 
а для получения данных с сайта hh.ru - библиотека requests.


Основные шаги проекта:
1. Получение данных о работодателях и их вакансиях с сайта hh.ru через публичный API и 
библиотеку requests.
2. Выбор не менее 10 интересных компаний, от которых будут получены данные о вакансиях.
3. Проектирование таблиц в базе данных PostgreSQL для хранения информации о работодателях 
и их вакансиях.
4. Реализация кода, который заполняет созданные таблицы в базе данных данными 
о работодателях и их вакансиях.
5. Создание класса DBManager для управления данными в базе данных.

Запуск проекта:

1. Убедитесь, что у вас установлена PostgreSQL база данных и библиотека psycopg2 для работы с ней.
2. Скачайте проект из репозитория.
3. Запустите скрипт main.py, чтобы получить данные с сайта hh.ru и заполнить таблицы в базе данных, и
использовать класс DBManager для получения данных о компаниях и вакансиях.

Зависимости:
Для работы проекта необходимо установить следующие зависимости:

1. Python 3
2. Библиотека requests для работы с API hh.ru
3. Библиотека psycopg2 для работы с PostgreSQL


Важно:

Для работы с сайтом hh.ru и получения данных через API, рекомендуется соблюдать 
политику использования данных и ограничения, предоставленные сайтом hh.ru. 
При использовании API, убедитесь, что вы соблюдаете правила обращения к API 
и не превышаете ограничения на количество запросов.

