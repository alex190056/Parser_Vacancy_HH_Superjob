import os
from datetime import datetime
from typing import List
from jobs_classes import Vacancy


def get_sorted_vacancy_list_by_salary(vacancy_list: List[Vacancy]):
    """
    Возвращает топ-10 вакансий.
    """
    return sorted(vacancy_list, key=lambda x: x.salary, reverse=True)[:10]


def get_filtered_vacancy_list_by_city(vacancy_list: List[Vacancy], city: str) -> List[Vacancy]:
    """
    Возвращает список вакансий в указанном городе.
    """
    filtered_by_city = list(filter(lambda x: x.city == city, vacancy_list))
    if filtered_by_city:
        return filtered_by_city
    return []


def get_sorted_vacancy_list_by_date(vacancy_list: List[Vacancy]) -> List[Vacancy]:
    """
    Возвращает топ-10 вакансий с сортировкой по дате публикации.
    """
    return sorted(vacancy_list, key=lambda x: x.published_at, reverse=True)[:10]


def save_to_file(choice: str, result: List[Vacancy], city=None | str):
    """
    Сохраняет результаты поиска вакансий в папку.
    """
    directory_result = os.path.join('Total')
    if not os.path.exists(directory_result):
        os.makedirs(name='Total')
    if choice == '1':
        path = os.path.join('Total', 'топ высокооплачиваемых.txt')
        title = 'ТОП-10 ВЫСОКООПЛАЧИВАЕМЫХ ВАКАНСИЙ'
    else:
        path = os.path.join('Total', 'итоговый поиск.txt')
        title = 'ВСЕ НАЙДЕННЫЕ ВАКАНСИИ'
    with open(path, 'w', encoding='utf-8') as file:
        now = datetime.now()
        date_formatted = now.strftime('%d.%m.%Y %H:%M')
        file.write(f'{date_formatted}\n')
        file.write(f'{title}\n')
        if result:
            for vacancy in result:
                file.write('=' * 300 + '\n')
                file.write(f'{vacancy.name}\n')
                file.write(f'Сайт: {vacancy.site}\n')
                file.write(f'Cсылка: {vacancy.url}\n')
                file.write(f'Дата публикации: {vacancy.published_at}\n')
                file.write(f'Описание: {vacancy.description}\n')
                file.write(f'ЗП: {vacancy.salary}\n')
                file.write(f'Город: {vacancy.city}\n')
                file.write(f'Компания: {vacancy.employer}\n')
        else:
            file.write('Вакансий не обнаружено')
    print(f'Результаты записаны в файл {path}')
