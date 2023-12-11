from src.file_class import HeadHunter, VacancyHH, VacancySJ, SuperJob, FilterHH, FilterSJ, JSONSaver

if __name__ == '__main__':

    def user_interaction():
        api_hh = HeadHunter()
        api_sj = SuperJob()

        vacancy_hh = VacancyHH(api_hh.get_api())
        hh_vacancies = vacancy_hh.get_vacancy()

        vacancy_sj = VacancySJ(api_sj.get_api())
        sj_vacancies = vacancy_sj.get_vacancy()

        saver = JSONSaver(hh_vacancies, sj_vacancies)
        saver.creating_json_file()
        while True:
            try:
                platform = int(input("Выберите, с какой платформы вы хотите получить информацию о доступных "
                                     "вакансиях: \n1 - HeadHunter \n2 - SuperJob \n0 - Для выхода \n"))
                search_query = input("Введите поисковый запрос: ")
                top_n = int(input("Введите количество вакансий для вывода в топ по зарплате: "))
                filter_words = input("Введите ключевые слова для фильтрации вакансий через запятую или пробел: ")
                print('\n')
                if platform == 1:
                    filter_vacancy_hh = FilterHH(search_query, filter_words)
                    vacancies = filter_vacancy_hh.filter_vacancy_name()
                    if not vacancies:
                        print(
                            'Вакансий по вашему запросу не найдено на данной платформе. \n'
                            'Вы можете начать поиск других вакансий или поискать вакансии на другой платформе \n'
                        )
                    else:
                        for filter_vacancy_name in vacancies:
                            print(f'Ответ по поисковому запросу: {search_query} \n {filter_vacancy_name}')
                    if len(filter_vacancy_hh) < top_n:
                        print('\nКолличество введенных вакансий для вывода топа по зарплате не может превышать '
                              'колличество имеющихся\n')
                    elif top_n <= 0:
                        print('\nКолличество введенных вакансий для вывода топа не может быть 0 или меньше нуля\n')
                    else:
                        filter_top = filter_vacancy_hh.filter_top_salary()[:top_n]
                        for filtr in filter_top:
                            string = 'Топ ' + str(top_n) + ':\n' + filtr
                        print(string)
                    if ',' in filter_words:
                        if not vacancies:
                            print('\nВакансий по заданным параметрам не обнаружено \n')
                        for filter_vacancy_the_key_words in vacancies:
                            print(f'Вакансии найденые по заданным параметрам: \n {filter_vacancy_the_key_words}')
                    elif ' ' in filter_words:
                        if not vacancies:
                            print('\nВакансий по заданным параметрам не обнаружено \n')
                        for filter_vacancy_the_key_words in vacancies:
                            print(f'Вакансии найденые по заданным параметрам: \n {filter_vacancy_the_key_words}')
                    else:
                        print('\nВведите ключевые слова для фильтрации вакансий через запятую или пробел\n')
                elif platform == 2:
                    filter_vacancy_sj = FilterSJ(search_query, filter_words)
                    vacancies = filter_vacancy_sj.filter_vacancy_name()
                    if not vacancies:
                        print(
                            'Вакансий по вашему запросу не найдено на данной платформе. \n'
                            'Вы можете начать поиск других вакансий или поискать вакансии на другой платформе \n'
                        )
                    else:
                        for filter_vacancy_name in vacancies:
                            print(f'Ответ по поисковому запросу: {search_query} \n {filter_vacancy_name}')
                            print(f'Ответ по поисковому запросу: {search_query} \n {filter_vacancy_name}')
                    if len(filter_vacancy_sj) < top_n:
                        print(
                            '\nКолличество введенных вакансий для вывода топа по зарплате не может превышать '
                            'колличество имеющихся\n')
                    elif top_n <= 0:
                        print('\nКолличество введенных вакансий для вывода топа не может быть 0 или меньше нуля\n')
                    else:
                        filter_top = filter_vacancy_sj.filter_top_salary()[:top_n]
                        for filtr in filter_top:
                            string = 'Топ ' + str(top_n) + ':\n' + filtr
                        print(string)
                    if ',' in filter_words:
                        if not vacancies:
                            print('\nВакансий по заданным параметрам не обнаружено \n')
                        for filter_vacancy_the_key_words in vacancies:
                            print(f'Вакансии найденые по заданным параметрам: \n {filter_vacancy_the_key_words}')
                    elif ' ' in filter_words:
                        if not vacancies:
                            print('\nВакансий по заданным параметрам не обнаружено \n')
                        for filter_vacancy_the_key_words in vacancies:
                            print(f'Вакансии найденые по заданным параметрам: \n {filter_vacancy_the_key_words}')
                    else:
                        print('\nВведите ключевые слова для фильтрации вакансий через запятую или пробел\n')

                elif platform == 0:
                    saver.del_data()
                    break
                else:
                    print('Платформа не определена, повторите еще раз.\n')
            except ValueError:
                print('\nВведите число')


    user_interaction()
