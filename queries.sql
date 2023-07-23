--получает список всех компаний и количество вакансий у каждой компании.
select company_name, count(*) from employers
inner join vacancies using(employer_id)
group by company_name


--получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
select company_name, title, salary, url
from vacancies
inner join employers using(employer_id)


--получает среднюю зарплату по вакансиям.
select round(avg(salary)::numeric, 2)
from vacancies


-- получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
select * from vacancies
where salary > (select round(avg(salary)::numeric, 2) from vacancies)
order by salary desc


--получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
select * from vacancies
where title like '%{keyword}%'
or description like '%{keyword}%'
or requirements like '%{keyword}%'