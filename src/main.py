"""
Взаимодействие с пользователем
"""
import json
import os
from classes.api_classes import Hh
from classes.api_classes import Sj
from classes.vac_classes import JSONSaver


def user_interaction():

    empty_data_files()

    print()
    print("Начало работы")
    print()

    while True:
        print("Выберите платформу для подбора вакансий")
        print("1 - HeadHunter")
        print("2 - SuperJob")
        print("3 - обе платформы")
        print("4 - завершить работу")
        user_selection = input("Ваш выбор ->")
        try:
            user_selection = int(user_selection)
            if user_selection not in [1, 2, 3, 4]:
                print("Введите число от 1 до 4")
            else:
                break
        except ValueError:
            print("Введите число от 1 до 4")

    if user_selection == 4:
        print("Спасибо")
        return

    while True:
        key_word = input("Введите ключевое слово для поиска вакансий ->")
        if key_word.isalpha():
            break
        print("Введите слово")

    if user_selection == 1:
        # HH
        vac_count_hh = make_data_file_hh(key_word)
        print(f"Найдено {vac_count_hh} вакансий")

    elif user_selection == 2:
        # SJ
        vac_count_sj = make_data_file_sj(key_word)
        print(f"Найдено {vac_count_sj} вакансий")

    elif user_selection == 3:
        # HH + SJ
        vac_count_hh = make_data_file_hh(key_word)
        vac_count_sj = make_data_file_sj(key_word)
        vac_count = vac_count_hh + vac_count_sj
        print(f"Найдено {vac_count} вакансий")

    load_from_json_hh = JSONSaver('vac_info_hh.json')
    load_from_json_sj = JSONSaver('vac_info_sj.json')
    list_of_vac_hh = load_from_json_hh.read_vacancies()
    list_of_vac_sj = load_from_json_sj.read_vacancies()
    list_of_vac = list_of_vac_hh + list_of_vac_sj

    while True:
        print("Выберите вариант вывода:")
        print("1 - Все вакансии")
        print("2 - Вакансии по возрастанию ЗП")
        print("3 - Вакансии по убыванию ЗП")
        print("4 - Топ 5 по ЗП")
        user_selection = input("Ваш выбор ->")
        try:
            user_selection = int(user_selection)
            if user_selection not in [1, 2, 3, 4]:
                print("Введите число от 1 до 4")
            else:
                break
        except ValueError:
            print("Введите число от 1 до 4")

    if user_selection == 1:
        print_vac_list(list_of_vac)
    if user_selection == 2:
        print_vac_list(sorted(list_of_vac))
    if user_selection == 3:
        print_vac_list(sorted(list_of_vac, reverse=True))
    if user_selection == 4:
        print_vac_list(sorted(list_of_vac, reverse=True),5)


def make_data_file_hh(key_word):
    """ Получаем вакансии с сайта НН с сохранением в файл,
    а так же возвращаем кол-во найденных вакансий"""
    hh_vac = Hh()
    hh_filtered_data = hh_vac.filter_vacancies(key_word)
    save_to_json_hh = JSONSaver('vac_info_hh.json')
    save_to_json_hh.write_vacancies(hh_filtered_data)
    return len(hh_filtered_data)


def make_data_file_sj(key_word):
    """ Получаем вакансии с сайта SJ с сохранением в файл,
    а так же возвращаем кол-во найденных вакансий"""
    sj_vac = Sj()
    sj_filtered_data = sj_vac.filter_vacancies(key_word)
    save_to_json_sj = JSONSaver('vac_info_sj.json')
    save_to_json_sj.write_vacancies(sj_filtered_data)
    return len(sj_filtered_data)

def print_vac_list(list_of_vac, print_len=100):
    """ Печатает список вакансий длинной print_len"""
    print()
    for index, value in enumerate(list_of_vac, 1):
        if index > print_len:
            return
        print(f"Вакансия № {index}")
        print("-------------")
        print(value)
        print()


def empty_data_files():
    """ Записывает пустые списки в файлы данных"""
    with open(os.path.abspath('../data/vac_info_sj.json'), 'w') as f:
        json.dump([], f)

    with open (os.path.abspath('../data/vac_info_hh.json'), 'w') as f:
        json.dump([], f)


if __name__ == "__main__":
    user_interaction()
    

