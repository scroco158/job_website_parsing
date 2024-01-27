"""
Классы для работы с получением данных с сайтов:
    1. Наследуются от абстрактного
    2.  Имеют 2 метода
        а) получение данных
        б) фильтрация данных
"""

from abc import ABC, abstractmethod
import requests
import json
import os


class AbstractAPI(ABC):
    @abstractmethod
    def get_vacancies(self, key_word):
        pass

    @abstractmethod
    def filter_vacancies(self, key_words):
        pass


class Hh(AbstractAPI):

    def get_vacancies(self, key_word):
        """
        Получает список вакансий по ключевому слову key_word
        и возвращает словарь с нефильтрованными вакансиями
        """

        hh_url = "https://api.hh.ru/vacancies?text="+key_word
        response = requests.get(url=hh_url).json()

        return response['items']

    def filter_vacancies(self, key_word):
        """
        Отбираем необходимые для работы поля и возвращаем словарь с
        отфильтрованной информацией по вакансиям
        """
        vacancies = self.get_vacancies(key_word)
        filtered_vacancies = []
        for vacancy in vacancies:
            s_f = 0
            s_t = 0
            if vacancy["salary"] is not None:
                if vacancy["salary"]["from"] is not None:
                    s_f = vacancy["salary"]["from"]
                if vacancy["salary"]["to"] is not None:
                    s_t = vacancy["salary"]["to"]

            filtered_vacancies.append({
                "name": vacancy["name"],
                "url": vacancy["url"],
                "salary_from": s_f,
                "salary_to": s_t,
                "description": vacancy["snippet"]["responsibility"]})

        return filtered_vacancies


class Sj(AbstractAPI):

    def get_vacancies(self, key_word):

        """
        Получает список вакансий по ключевому слову key_word
        и возвращает словарь с нефильтрованными вакансиями
        (необходимо создать переменную окружения SJ_API_KEY с
        ключом доступа к SuperJob)
        """

        sj_api_key = os.environ.get('SJ_API_KEY')
        headers = {"X-Api-App-Id": sj_api_key}
        params = {"keyword": key_word}
        response = requests.get("https://api.superjob.ru/2.0/vacancies/", params=params, headers=headers).json()
        return response['objects']

    def filter_vacancies(self, key_word):
        """
        Отбираем необходимые для работы поля и возвращаем словарь с
        отфильтрованной информацией по вакансиям
        """
        vacancies = self.get_vacancies(key_word)
        filtered_vacancies = []
        for vacancy in vacancies:
            filtered_vacancies.append({
                "name": vacancy["profession"],
                "url": vacancy["link"],
                "salary_from": vacancy["payment_from"],
                "salary_to": vacancy["payment_to"],
                "description": vacancy["work"]})

        return filtered_vacancies
