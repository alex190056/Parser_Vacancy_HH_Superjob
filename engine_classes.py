from abc import ABC, abstractmethod
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response

from function_hh_superj import (
    get_format_name,
    get_format_url,
    get_format_published_date,
    get_format_description,
    get_format_salary,
    get_format_city,
    get_format_employer,
    get_format_name_and_url_sj,
    get_format_published_date_sj,
    get_format_description_sj,
    get_format_salary_sj,
    get_format_city_sj,
    get_format_employer_sj
)
from jobs_classes import Vacancy


class Engine(ABC):
    """
    Абстрактный базовый класс для работы с сервисами поиска работы
    """

    @abstractmethod
    def get_request(self, url: str, params: dict):
        """
        Абстрактный метод, который отправляет запрос на сайт поиска работы.
        """
        try:
            response = requests.get(url=url, params=params)
            if response.status_code != 200:
                raise LookupError(f'статус код {response.status_code}')
            if not response:
                return []
            if not response:
                raise LookupError('Ответ пустой')
            return response
        except (requests.exceptions.RequestException, LookupError) as error:
            print(f'Не могу получить данные, {error}')
            return []

    @abstractmethod
    def get_formatted_data(self, data):
        """
        Абстрактный метод, который возвращает отформатированные данные
        для создания экземпляра класса Vacancy
        """
        pass


class HeadHunter(Engine):
    """
    Класс, описывающий сервис поиска работы HH
    """

    def __init__(self, search: str, no_experience: str):
        self.__search = search
        self.__url = 'https://api.hh.ru/vacancies/'
        self.__params = {
            'text': f'NAME:{self.__search}',
            'per_page': 100,
            'area': '113'
        }
        if no_experience == '1':
            self.__params['experience'] = 'noExperience'

    def get_request(self, url: str, params: dict):
        return super().get_request(url, params)

    def get_formatted_data(self, unformatted_data: dict):
        about_vacancy = {
            'site': 'HeadHunter',
            'name': get_format_name(unformatted_data),
            'url': get_format_url(unformatted_data),
            'published_at': get_format_published_date(unformatted_data),
            'description': get_format_description(unformatted_data),
            'salary': get_format_salary(unformatted_data),
            'city': get_format_city(unformatted_data),
            'employer': get_format_employer(unformatted_data)
        }
        return about_vacancy

    def get_vacancy_list(self) -> List[Vacancy]:
        """
        Возвращает лист вакансий по запросу.
        """
        vacancy_list = []
        page = 0
        print('Ищу вакансии на HeadHunter. Подождите.')
        while True:
            self.__params['page'] = page
            data = self.get_request(url=self.__url, params=self.__params).json()
            print('.', end='')
            for item in data.get('items'):
                vacancy_list.append(Vacancy(data=self.get_formatted_data(unformatted_data=item)))
            if data.get('pages') - page <= 1:
                print(f'Количество найденных вакансий: {len(vacancy_list)}')
                break
            else:
                page += 1
        return vacancy_list


class SuperJob(Engine):
    """
    Описывает сервис поиска работы SuperJob.
    """

    def __init__(self, search: str, no_experience: str):
        self.__search = search
        self.__url = 'https://russia.superjob.ru/vacancy/search/'
        self.__params = {'keywords': self.__search}
        if no_experience == '1':
            self.__params['without_experience'] = 1

    def get_request(self, url: str, params: dict):
        return super().get_request(url, params)

    def get_formatted_data(self, unformatted_data: Tag):
        about_vacancy = {
            'site': 'SuperJob',
            'name': get_format_name_and_url_sj(unformatted_data)[0],
            'url': get_format_name_and_url_sj(unformatted_data)[1],
            'published_at': get_format_published_date_sj(unformatted_data),
            'description': get_format_description_sj(unformatted_data),
            'salary': get_format_salary_sj(unformatted_data),
            'city': get_format_city_sj(unformatted_data),
            'employer': get_format_employer_sj(unformatted_data)
        }
        return about_vacancy

    def get_vacancy_list(self) -> List[Vacancy]:
        """
        Возвращает список вакансий по запросу.
        """
        vacancy_list = []
        page = 1
        print('Ищу вакансии на SuperJob. Подождите.')
        while True:
            for _ in range(3):
                self.__params['page'] = page
                response = self.get_request(url=self.__url, params=self.__params)
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='f-test-search-result-item')
                if items:
                    print('.', end='')
                    for item in items:
                        if get_format_name_and_url_sj(unformatted_data=item)[0] is None:
                            continue
                        vacancy_list.append(Vacancy(data=self.get_formatted_data(unformatted_data=item)))
                    page += 1
                    break
            else:
                print(f'Количество найденных вакансий: {len(vacancy_list)}')
                break
        return vacancy_list
