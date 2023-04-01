from datetime import date, timedelta
from bs4.element import Tag

def get_format_name(unformatted_data: dict):
    """
    Возвращает название вакансии из неотформатированных данных,
    которые получены через API HeadHunter
    """
    return unformatted_data['name']


def get_format_url(unformatted_data: dict):
    """
    Возвращает ссылку на вакансию из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['alternate_url']


def get_format_published_date(unformatted_data: dict):
    """
    Возвращает дату  публикации вакансии из неотформатированных данных,
    полученных через API HeadHunter
    """
    date_str = unformatted_data['published_at']
    date_obj = date_str.split('T')[0]
    return date.fromisoformat(date_obj)


def get_format_description(unformatted_data: dict):
    """
    Возвращает описание вакансии из неотформатированных данных,
    полученных через API HeadHunter
    """
    str_description = ''
    if unformatted_data['snippet']['requirement'] is not None:
        str_description += unformatted_data['snippet']['requirement']
    if unformatted_data['snippet']['responsibility'] is not None:
        str_description += '\n' + unformatted_data['snippet']['responsibility']
    return str_description.replace('<highlighttext>', '').replace('</highlighttext>', '')


def get_format_salary(unformatted_data: dict):
    """
    Возвращает заработную плату из неотформатированных данных,
    полученных через API HeadHunter
    """
    salary_data = unformatted_data['salary']
    if salary_data is None or salary_data['from'] is None:
        return 0
    return salary_data['from']


def get_format_city(unformatted_data: dict):
    """
    Возвращает город из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['area']['name']


def get_format_employer(unformatted_data: dict):
    """
    Возвращает название компании из неотформатированных данных,
    полученных через API HeadHunter
    """
    return unformatted_data['employer']['name']


RU_MONTH_VALUES = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12',
}


def get_format_name_and_url_sj(unformatted_data: Tag):
    name = unformatted_data.find('span', class_='_26gg2 _3oXMw _2LaRg hbKbL rIDaO oDIMq _33qju _1ZV-S')
    if name is not None:
        url = 'https://russia.superjob.ru/' + name.find('a').get('href')
        name = name.get_text(strip=True)
        return name, url
    return None, None


def get_format_published_date_sj(unformatted_data: Tag):
    published_date_row = unformatted_data.find('span', class_='_2H6gy oDIMq WlSzf _3T7lp')
    if published_date_row is not None:
        published_date = published_date_row.get_text(strip=True)
        if published_date.split(' ')[0] == 'Сегодня':
            return date.today()
        elif published_date.split(' ')[0] == 'Вчера':
            today = date.today()
            yesterday = today + timedelta(days=-1)
            return yesterday
        else:
            day = str(published_date.split(' ')[0])
            if len(day) == 1:
                day = '0' + day
            month = RU_MONTH_VALUES[f"{published_date.split(' ')[1]}"]
            year = str(date.today().year)
            return date.fromisoformat(f'{year}-{month}-{day}')
    return None


def get_format_description_sj(unformatted_data: Tag):
    description = unformatted_data.find('span', class_='_2H6gy oDIMq _33qju _3T7lp _2R-87')
    if description is not None:
        return description.get_text(strip=True)
    return None


def get_format_salary_sj(unformatted_data: Tag):
    salary_row = unformatted_data.find('span', class_='_2eYAG rIDaO oDIMq _33qju _3T7lp')
    if salary_row is not None:
        salary = salary_row.get_text(strip=True)
        if salary.strip() == 'По договорённости':
            return 0
        elif salary.startswith('от') or salary.startswith('до'):
            result = ''
            for symbol in salary:
                if symbol.isdigit():
                    result += symbol
            return int(result)
        elif '—' in salary:
            result = ''
            for symbol in salary.split('—')[0]:
                if symbol.isdigit():
                    result += symbol
            return int(result)
        elif ' ' in salary:
            result = ''
            for symbol in salary:
                if symbol.isdigit():
                    result += symbol
            return int(result)
        return 0
    return None


def get_format_city_sj(unformatted_data: Tag):
    city_div = unformatted_data.find('div', class_='WDWTW _2SOuz _3JyWQ _1CjMB -knfs')
    if city_div is not None:
        return city_div.find('div', class_='_32Fb8').get_text(strip=True)
    return None


def get_format_employer_sj(unformatted_data: Tag):
    employer_span = unformatted_data.find('span', class_='_3nMqD f-test-text-vacancy-item-company-'
                                                         'name _2LynC oDIMq _33qju _3T7lp _2R-87')
    if employer_span is not None:
        return employer_span.find('a').get_text(strip=True)
    return None
