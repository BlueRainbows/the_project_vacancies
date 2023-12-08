from src.file_class import HeadHunter, VacancyHH, VacancySJ, SuperJob, FilterHH, FilterSJ

if __name__ == '__main__':
    api_hh = HeadHunter()
    api_sj = SuperJob()

    vacancy_hh = VacancyHH(api_hh.get_api())
    vacancy_hh.get_vacancy()

    vacancy_sj = VacancySJ(api_sj.get_api())
    vacancy_sj.get_vacancy()

    # saver = JSONSaver(vacancy_hh.get_vacancy(), vacancy_sj.get_vacancy())
    # saver.creating_json_file()


    def user_interaction():
        platform = input(
            '''Выберите, с какой платформы вы хотите получить информацию о доступных вакансиях:

1 - HeadHunter
2 - SuperJob
3 - Из всех платформ
'''
        )
        search_query = input("Введите поисковый запрос: ")
        top_n = int(input("Введите количество вакансий для вывода в топ по зарплате: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий через запятую: ")
        filter_vacancy_hh = FilterHH(vacancy_hh.get_vacancy(), vacancy_sj.get_vacancy(), search_query, top_n, filter_words)
        filter_vacancy_sj = FilterSJ(vacancy_hh.get_vacancy(), vacancy_sj.get_vacancy(), search_query, top_n, filter_words)
        print(filter_vacancy_sj.filter_the_key_words())

    user_interaction()

