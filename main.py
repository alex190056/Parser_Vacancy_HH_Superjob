from engine_classes import HeadHunter, SuperJob
from utils import (
    get_sorted_vacancy_list_by_salary,
    get_filtered_vacancy_list_by_city,
    get_sorted_vacancy_list_by_date,
    save_to_file
)

def main():
    searching_input = input('Введите вакансию для поиска: ').strip()
    experience_input = input(
        'Введите - 1, если будем искать вакансии, в которых не требуется опыт.\n'
        'Введите - 2 или любой другой символ, если неважен опыт.'
    ).strip()

    # Поиск вакансий - HH - SJ
    hh = HeadHunter(search=searching_input, no_experience=experience_input)
    sj = SuperJob(search=searching_input, no_experience=experience_input)

    hh_vacancy_list = hh.get_vacancy_list()
    sj_vacancy_list = sj.get_vacancy_list()

    #Найденные вакансии
    vacancy_list = hh_vacancy_list + sj_vacancy_list

    while True:
        print('1 - выбрать топ 10 высокооплачиваемых вакансий.\n'
              'Нажмите на любую клавишу - выход')
        choice_input = input('Введите цифру: ')

        if choice_input == '1':
            result = get_sorted_vacancy_list_by_salary(vacancy_list=vacancy_list)
            save_to_file(choice=choice_input, result=result)
        else:
            print('Программа завершила работу')
            save_to_file(choice=choice_input, result=vacancy_list)
            break


if __name__ == '__main__':
    main()
