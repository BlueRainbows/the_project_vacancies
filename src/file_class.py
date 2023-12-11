from abc import ABC, abstractmethod
import requests
import json
import os


class GetAPI(ABC):
    """ Абстрактный класс с абстрактным методом получения API """

    @abstractmethod
    def get_api(self):
        pass


class HeadHunter(GetAPI):
    """ Класс для получения API сайта HeadHunter """
    url = 'https://api.hh.ru/vacancies'

    def get_api(self):
        try:
            response_hh = requests.get(url=self.url, headers={'User-Agent': 'bluereinbow@yandex.ru'},
                                       params={'page': None, 'per_page': 100})
            if response_hh.status_code == 200:
                return response_hh.json()
        except requests.RequestException as error:
            print(f'Возникла ошибка {error}')


class SuperJob(GetAPI):
    """ Класс для получения API сайта SuperJob """
    url = 'https://api.superjob.ru/2.0/vacancies/'
    api_key = os.environ.get('SUPERJOB_API_KEY')

    def get_api(self):
        try:
            response_sj = requests.get(url=self.url, headers={'X-Api-App-Id': self.api_key},
                                       params={'page': None, 'count': 100})
            if response_sj.status_code == 200:
                return response_sj.json()
        except requests.RequestException as error:
            print(f'Возникла ошибка {error}')


class Vacancy(ABC):
    """ Абстрактный класс с абстрактным методом получения API """

    @abstractmethod
    def __init__(self, api):
        self.api = api
        self.list_vacancy = []
        self.name_vacancy = None
        self.salary_vacancy = None
        self.address_vacancy = None
        self.url_vacancy = None
        self.requirement_vacancy = None
        self.schedule_vacancy = None
        self.professional_roles = None

    @abstractmethod
    def get_vacancy(self):
        pass


class VacancyHH(Vacancy, ABC):
    """ Класс получает ответ с API сайта hh.ru, инициализирует атрибуты и преобразовывает их в словарь """

    def __init__(self, api):
        super().__init__(api)
        self.__list_vac = self.get_vacancy

    def get_vacancy(self):
        if self.api is None:
            raise Exception('Ошибка в чтении документа')
        try:
            for item in self.api['items']:
                self.name_vacancy = item['name']
                if item['salary'] is None:
                    self.salary_vacancy = 'Зарплата не указана'
                elif item['salary']['from'] is None:
                    salary = 'До ' + str(item['salary']['to'])
                    self.salary_vacancy = salary
                elif item['salary']['from'] is not None and \
                        item['salary']['to'] is not None:
                    salary = 'От ' + str(item['salary']['from']) + \
                             ' до ' + str(item['salary']['to'])
                    self.salary_vacancy = salary
                else:
                    salary = 'От ' + str(item['salary']['from'])
                    self.salary_vacancy = salary
                if item['address'] is None or 'null':
                    self.address_vacancy = 'Адрес не указан'
                else:
                    self.address_vacancy = item['address']['raw']
                self.url_vacancy = item['alternate_url']
                if item['snippet']['requirement'] is None:
                    self.requirement_vacancy = 'Требования к сотруднику не указаны'
                else:
                    self.requirement_vacancy = item['snippet']['requirement']
                self.schedule_vacancy = item['schedule']['name']
                self.professional_roles = item['professional_roles'][0]['name']
                dict_vacancy = {
                    'name_vacancy': self.name_vacancy,
                    'salary_vacancy': self.salary_vacancy,
                    'address_vacancy': self.address_vacancy,
                    'url_vacancy': self.url_vacancy,
                    'requirement_vacancy': self.requirement_vacancy,
                    'schedule_vacancy': self.schedule_vacancy,
                    'professional_roles': self.professional_roles
                }
                self.list_vacancy.append(dict_vacancy)
            return self.list_vacancy
        except TypeError:
            print('Информация в документе повреждена')
        except KeyError:
            print('В документе не полная информация')


class VacancySJ(Vacancy, ABC):
    """ Класс получает ответ с API сайта superjob.ru, инициализирует атрибуты и преобразовывает их в словарь """

    def __init__(self, api):
        super().__init__(api)

    def get_vacancy(self):
        if self.api is None:
            return []
        try:
            for objects in self.api['objects']:
                if objects['payment_from'] == 0:
                    salary = 'До ' + str(objects['payment_to'])
                    self.salary_vacancy = salary
                elif objects['payment_to'] == 0:
                    salary = 'От ' + str(objects['payment_from'])
                    self.salary_vacancy = salary
                elif objects['payment_from'] and \
                        objects['payment_from'] != 0:
                    salary = 'От ' + str(objects['payment_from']) + \
                             ' до ' + str(objects['payment_to'])
                    self.salary_vacancy = salary
                if objects['address'] is None:
                    self.address_vacancy = 'Адрес не указан'
                else:
                    self.address_vacancy = objects['address']
                self.name_vacancy = objects['profession']
                if objects['candidat'] is None:
                    self.requirement_vacancy = 'Информация для кандидата не указана'
                else:
                    raw_string = objects['candidat']
                    string = raw_string.replace('\n', ' ')
                    string = string.replace('\n·', ' ')
                    self.requirement_vacancy = string
                self.schedule_vacancy = objects['type_of_work']['title']
                self.url_vacancy = objects['link']
                self.professional_roles = objects['catalogues']
                dict_vacancy = {
                    'name_vacancy': self.name_vacancy,
                    'salary_vacancy': self.salary_vacancy,
                    'address_vacancy': self.address_vacancy,
                    'url_vacancy': self.url_vacancy,
                    'requirement_vacancy': self.requirement_vacancy,
                    'schedule_vacancy': self.schedule_vacancy,
                    'professional_roles': self.professional_roles
                }
                self.list_vacancy.append(dict_vacancy)
            return self.list_vacancy
        except TypeError:
            print('Информация в документе повреждена')
        except KeyError:
            print('В документе не полная информация')


class JSONSaver:
    """ Класс для работы с json файлом """

    def __init__(self, hh, sj):
        self.hh = hh
        self.sj = sj

    def creating_json_file(self):
        """ Функция сохраняет объекты в json файл """
        paths = os.path.join('src/vacancy_file.json')
        with open(paths, 'w', encoding='utf-8') as file:
            json.dump({

                'hh_vacancy': self.hh,
                'sj_vacancy': self.sj

            }, file, ensure_ascii=False, indent=4)

    def del_data(self):
        """ Функция удаляет файл"""
        paths = os.path.join('src/vacancy_file.json')
        os.remove(paths)


class FilterVacancy(ABC):
    """ Абстрактный класс для классов выполняющих функции фильтрации """

    def __init__(self, search_query: str, filter_words):
        self.vacancy = None
        self.search_query = search_query.lower()
        self.filter_words = filter_words

    @abstractmethod
    def open_json(self):
        pass

    @abstractmethod
    def filter_vacancy_name(self):
        pass

    @abstractmethod
    def filter_top_salary(self):
        pass

    @abstractmethod
    def filter_the_key_words(self):
        pass


class FilterHH(FilterVacancy, ABC):
    """ Класс выполняет функцию фильтрации для запросов сайта hh.ru """

    def __init__(self, search_query, filter_words):
        super().__init__(search_query, filter_words)
        self.vacancy = self.open_json()['hh_vacancy']

    def open_json(self):
        """ Функция открывает json файл для работы """
        paths = os.path.join('src/vacancy_file.json')
        with open(paths, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def filter_vacancy_name(self):
        """ Функция фильтрует данные по названию вакансии """
        list_string_profession = []
        for vacancy in self.vacancy:
            if self.search_query in vacancy['name_vacancy'].lower():
                string_profession = '\n' + vacancy['name_vacancy'] + '\n' + \
                                    vacancy['salary_vacancy'] + '\n' + \
                                    vacancy['address_vacancy'] + '\n' + \
                                    vacancy['url_vacancy'] + '\n' + \
                                    vacancy['requirement_vacancy'][:100] + '...' + '\n' + \
                                    vacancy['schedule_vacancy'] + '\n' + '\n'
                list_string_profession.append(string_profession)
        return list_string_profession

    def filter_top_salary(self):
        """ Функция фильтрует данные по зарплате от самой высокой, до самой низкой """
        salary_full = []
        max_salary = []
        salary_string = ''
        for vacancy in self.vacancy:
            if 'От' and 'до' in vacancy['salary_vacancy']:
                splitting = vacancy['salary_vacancy'].split(' ')
                max_salary.append(int(splitting[-1]))
            elif 'До' in vacancy['salary_vacancy']:
                max_salary.append(int(vacancy['salary_vacancy'][3:]))
            elif 'От' in vacancy['salary_vacancy']:
                max_salary.append(int(vacancy['salary_vacancy'][3:]))
        set_max_salary = set(max_salary)
        max_salary.clear()
        for sets in set_max_salary:
            max_salary.append(sets)
        max_salary.sort(reverse=True)
        for salary in max_salary:
            for vacancy in self.vacancy:
                if vacancy['salary_vacancy'] == 'Зарплата не указана':
                    continue
                splitting = vacancy['salary_vacancy'].split(' ')
                if len(splitting) != 2:
                    if str(salary) == splitting[-1]:
                        salary_string += '\n' + vacancy['name_vacancy'] + '\n' + \
                                         vacancy['salary_vacancy'] + '\n' + \
                                         vacancy['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
                else:
                    if str(salary) == splitting[-1]:
                        salary_string += '\n' + vacancy['name_vacancy'] + '\n' + \
                                         vacancy['salary_vacancy'] + '\n' + \
                                         vacancy['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
        return salary_full

    def __len__(self):
        return len(self.filter_top_salary())

    def filter_the_key_words(self):
        """ Функция фильтрует данные по ключевым словам """
        list_the_key_words = []
        for vacancy in self.vacancy:
            if ' ' in self.filter_words:
                splitting_words = self.filter_words.split(' ')
            else:
                splitting_words = self.filter_words.split(',')
            for spl in splitting_words:
                if spl.lower() in vacancy['professional_roles'].lower():
                    string_profession = '\n' + vacancy['name_vacancy'] + '\n' + \
                                        vacancy['salary_vacancy'] + '\n' + \
                                        vacancy['address_vacancy'] + '\n' + \
                                        vacancy['url_vacancy'] + '\n' + \
                                        vacancy['requirement_vacancy'] + '\n' + \
                                        vacancy['schedule_vacancy'] + '\n' + '\n'
                    list_the_key_words.append(string_profession)
        return list_the_key_words


class FilterSJ(FilterVacancy, ABC):
    """ Класс выполняет функцию фильтрации для запросов сайта superjob.ru """

    def __init__(self, search_query, filter_words):
        super().__init__(search_query, filter_words)
        self.vacancy = self.open_json()['sj_vacancy']

    def open_json(self):
        """ Функция открывает json файл для работы """
        paths = os.path.join('src/vacancy_file.json')
        with open(paths, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def filter_vacancy_name(self):
        """ Функция фильтрует данные по названию вакансии """
        list_string_profession = []
        for vacancy in self.vacancy:
            if self.search_query in vacancy['name_vacancy'].lower():
                string_profession = '\n' + vacancy['name_vacancy'] + '\n' + \
                                    vacancy['salary_vacancy'] + '\n' + \
                                    vacancy['address_vacancy'] + '\n' + \
                                    vacancy['url_vacancy'] + '\n' + \
                                    vacancy['requirement_vacancy'][:100] + '...' + '\n' + \
                                    vacancy['schedule_vacancy'] + '\n' + '\n'
                list_string_profession.append(string_profession)
        return list_string_profession

    def filter_top_salary(self):
        """ Функция фильтрует данные по зарплате от самой высокой, до самой низкой """
        salary_full = []
        max_salary = []
        salary_string = ''
        for vacancy in self.vacancy:
            if 'От' and 'до' in vacancy['salary_vacancy']:
                splitting = vacancy['salary_vacancy'].split(' ')
                max_salary.append(int(splitting[-1]))
            elif 'До' in vacancy['salary_vacancy']:
                max_salary.append(int(vacancy['salary_vacancy'][3:]))
            elif 'От' in vacancy['salary_vacancy']:
                max_salary.append(int(vacancy['salary_vacancy'][3:]))
        set_max_salary = set(max_salary)
        max_salary.clear()
        for sets in set_max_salary:
            max_salary.append(sets)
        max_salary.sort(reverse=True)
        for salary in max_salary:
            for vacancy in self.vacancy:
                if vacancy['salary_vacancy'] == 'Зарплата не указана':
                    continue
                splitting = vacancy['salary_vacancy'].split(' ')
                if len(splitting) != 2:
                    if str(salary) == splitting[-1]:
                        salary_string += '\n' + vacancy['name_vacancy'] + '\n' + \
                                         vacancy['salary_vacancy'] + '\n' + \
                                         vacancy['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
                else:
                    if str(salary) == splitting[-1]:
                        salary_string += '\n' + vacancy['name_vacancy'] + '\n' + \
                                         vacancy['salary_vacancy'] + '\n' + \
                                         vacancy['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
        return salary_full

    def __len__(self):
        return len(self.filter_top_salary())

    def filter_the_key_words(self):
        """ Функция фильтрует данные по ключевым словам """
        list_the_key_words = []
        if ' ' in self.filter_words:
            splitting_words = self.filter_words.split(' ')
        else:
            splitting_words = self.filter_words.split(',')
        for spl in splitting_words:
            for vacancy in self.vacancy:
                for professional in vacancy['professional_roles']:
                    prof_title = professional['title'].lower()
                    if spl.lower() in prof_title:
                        string_profession = '\n' + vacancy['name_vacancy'] + '\n' + \
                                            vacancy['salary_vacancy'] + '\n' + \
                                            vacancy['address_vacancy'] + '\n' + \
                                            vacancy['url_vacancy'] + '\n' + \
                                            vacancy['requirement_vacancy'][:100] + '...' + '\n' + \
                                            vacancy['schedule_vacancy'] + '\n' + '\n'
                        list_the_key_words.append(string_profession)
                    prof_positions = professional['positions']
                    for prof in prof_positions:
                        professional_titles = prof['title'].lower()
                        if spl.lower() in professional_titles:
                            string_profession = '\n' + vacancy['name_vacancy'] + '\n' + \
                                                vacancy['salary_vacancy'] + '\n' + \
                                                vacancy['address_vacancy'] + '\n' + \
                                                vacancy['url_vacancy'] + '\n' + \
                                                vacancy['requirement_vacancy'][:100] + '...' + '\n' + \
                                                vacancy['schedule_vacancy'] + '\n' + '\n'
                            list_the_key_words.append(string_profession)
        return list_the_key_words
