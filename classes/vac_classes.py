"""
Классы:
    1. Класс для работы с вакансией (сортировка, вывод)
    2. Класс чтения (создание экземпляров класса вакансии), записи
"""
import os
import json


class Vacancy:

    def __init__(self, name, url, salary_from, salary_to, description):
        self.name = name
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __str__(self):
        return f"""Название вакансии: {self.name}
Ссылка: {self.url}
ЗП: от {self.salary_from} до {self.salary_to}
Описание: {self.description}"""

    def __lt__(self, other):
        return self.salary_from < other.salary_from


class JSONSaver:

    """ Сохраняет словарь с вакансиями в json файл"""

    def __init__(self, filename):
        self.filename = filename
        self.data_file = os.path.abspath('../data/' + self.filename)

    def write_vacancies(self, vacancies):
        with open(self.data_file, 'w', encoding="utf-8") as f:
            json.dump(vacancies, f, indent=4, ensure_ascii=False)

    def read_vacancies(self):
        with open (self.data_file, encoding='utf-8') as file:
            vacancies = json.load(file)

        list_of_vacancies = []
        for vacancy in vacancies:
            list_of_vacancies.append(Vacancy(vacancy['name'], vacancy['url'],
                                             vacancy['salary_from'], vacancy['salary_to'],
                                             vacancy['description']))
        return list_of_vacancies
