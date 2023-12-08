from abc import ABC, abstractmethod
import os
import requests
import json


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
            response_hh = requests.get(url=self.url, headers={'User-Agent': 'bluereinbow@yandex.ru'})
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
            response_sj = requests.get(url=self.url, headers={'X-Api-App-Id': self.api_key})
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
        self.open = None
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
            for len_item in range(len(self.api['items'])):
                self.name_vacancy = self.api['items'][len_item]['name']
                if self.api['items'][len_item]['salary'] is None:
                    self.salary_vacancy = 'Зарплата не указана'
                elif self.api['items'][len_item]['salary']['from'] is None:
                    salary = 'До ' + str(self.api['items'][len_item]['salary']['to'])
                    self.salary_vacancy = salary
                elif self.api['items'][len_item]['salary']['from'] is not None and \
                        self.api['items'][len_item]['salary']['to'] is not None:
                    salary = 'От ' + str(self.api['items'][len_item]['salary']['from']) + \
                             ' до ' + str(self.api['items'][len_item]['salary']['to'])
                    self.salary_vacancy = salary
                else:
                    salary = 'От ' + str(self.api['items'][len_item]['salary']['from'])
                    self.salary_vacancy = salary
                if self.api['items'][len_item]['type']['name'] == 'Открытая':
                    self.open = True
                else:
                    self.open = False
                if self.api['items'][len_item]['address'] is None:
                    self.address_vacancy = 'Адрес не указан'
                else:
                    self.address_vacancy = self.api['items'][len_item]['address']['raw']
                self.url_vacancy = self.api['items'][len_item]['alternate_url']
                if self.api['items'][len_item]['snippet']['requirement'] is None:
                    self.requirement_vacancy = 'Требования к сотруднику не указаны'
                else:
                    self.requirement_vacancy = self.api['items'][len_item]['snippet']['requirement']
                self.schedule_vacancy = self.api['items'][len_item]['schedule']['name']
                self.professional_roles = self.api['items'][len_item]['professional_roles'][0]['name']
                dict_vacancy = {
                    'name_vacancy': self.name_vacancy,
                    'open': self.open,
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
            raise Exception('Ошибка в чтении документа')
        try:
            for len_item in range(len(self.api['objects'])):
                self.open = self.api['objects'][len_item]['is_closed']
                if self.api['objects'][len_item]['payment_from'] == 0:
                    salary = 'До ' + str(self.api['objects'][len_item]['payment_to'])
                    self.salary_vacancy = salary
                elif self.api['objects'][len_item]['payment_to'] == 0:
                    salary = 'От ' + str(self.api['objects'][len_item]['payment_from'])
                    self.salary_vacancy = salary
                elif self.api['objects'][len_item]['payment_from'] and \
                        self.api['objects'][len_item]['payment_from'] != 0:
                    salary = 'От ' + str(self.api['objects'][len_item]['payment_from']) + \
                             ' до ' + str(self.api['objects'][len_item]['payment_to'])
                    self.salary_vacancy = salary
                if self.api['objects'][len_item]['address'] is None:
                    self.address_vacancy = 'Адрес не указан'
                else:
                    self.address_vacancy = self.api['objects'][len_item]['address']
                self.name_vacancy = self.api['objects'][len_item]['profession']
                if self.api['objects'][len_item]['candidat'] is None:
                    self.requirement_vacancy = 'Информация для кандидата не указана'
                else:
                    raw_string = self.api['objects'][len_item]['candidat']
                    string = raw_string.replace('\n', ' ')
                    string = string.replace('\n·', ' ')
                    self.requirement_vacancy = string
                self.schedule_vacancy = self.api['objects'][len_item]['type_of_work']['title']
                self.url_vacancy = self.api['objects'][len_item]['link']
                self.professional_roles = self.api['objects'][len_item]['catalogues']
                dict_vacancy = {
                    'name_vacancy': self.name_vacancy,
                    'open': self.open,
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
    """ Класс сохраняет данные в json файл """

    def __init__(self, hh, sj):
        self.hh = hh
        self.sj = sj

    def creating_json_file(self):
        with open('./src/vacancy_file.json', 'w', encoding='utf-8') as file:
            json.dump({

                'hh_vacancy': self.hh,
                'sj_vacancy': self.sj

            }, file, ensure_ascii=False, indent=4)

    def get_data(self):
        pass

    def del_data(self):
        pass


class FilterVacancy(ABC):
    """ Абстрактный класс для классов выполняющих функции фильтрации """

    def __init__(self, search_query, top_n, filter_words):
        self.vacancy = None
        self.search_query = search_query.lower()
        self.top_n = top_n
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
    def __init__(self, search_query, top_n, filter_words):
        super().__init__(search_query, top_n, filter_words)
        self.vacancy = self.open_json()['hh_vacancy']

    def open_json(self):
        with open('./src/vacancy_file.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def filter_vacancy_name(self):
        list_string_profession = []
        for i in range(len(self.vacancy)):
            if self.search_query in self.vacancy[i]['name_vacancy'].lower():
                string_profession = self.vacancy[i]['name_vacancy'] + '\n' + \
                                    self.vacancy[i]['salary_vacancy'] + '\n' + \
                                    self.vacancy[i]['address_vacancy'] + '\n' + \
                                    self.vacancy[i]['url_vacancy'] + '\n' + \
                                    self.vacancy[i]['requirement_vacancy'] + '\n' + \
                                    self.vacancy[i]['schedule_vacancy'] + '\n' + '\n'
                list_string_profession.append(string_profession)
        return list_string_profession

    def filter_top_salary(self):
        salary_full = []
        max_salary = []
        salary_string = ''
        for i in range(len(self.vacancy)):
            if 'От' and 'до' in self.vacancy[i]['salary_vacancy']:
                splitting = self.vacancy[i]['salary_vacancy'].split(' ')
                max_salary.append(int(splitting[-1]))
            elif 'До' in self.vacancy[i]['salary_vacancy']:
                max_salary.append(int(self.vacancy[i]['salary_vacancy'][3:]))
            elif 'От' in self.vacancy[i]['salary_vacancy']:
                max_salary.append(int(self.vacancy[i]['salary_vacancy'][3:]))
        set_max_salary = set(max_salary)
        max_salary.clear()
        for sets in set_max_salary:
            max_salary.append(sets)
        max_salary.sort(reverse=True)
        for salary in max_salary:
            for i in range(len(self.vacancy)):
                if self.vacancy[i]['salary_vacancy'] == 'Зарплата не указана':
                    continue
                splitting = self.vacancy[i]['salary_vacancy'].split(' ')
                if len(splitting) != 2:
                    if str(salary) == splitting[-1]:
                        salary_string += self.vacancy[i]['name_vacancy'] + '\n' + \
                                         self.vacancy[i]['salary_vacancy'] + '\n' + \
                                         self.vacancy[i]['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
                else:
                    if str(salary) == splitting[-1]:
                        salary_string += self.vacancy[i]['name_vacancy'] + '\n' + \
                                         self.vacancy[i]['salary_vacancy'] + '\n' + \
                                         self.vacancy[i]['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
        return salary_full

    def __len__(self):
        return len(self.filter_top_salary())

    def filter_the_key_words(self):
        list_the_key_words = []
        for i in range(len(self.vacancy)):
            splitting_words = self.filter_words.split(',')
            for spl in splitting_words:
                if spl.lower() in self.vacancy[i]['professional_roles'].lower():
                    string_profession = self.vacancy[i]['name_vacancy'] + '\n' + \
                                        self.vacancy[i]['salary_vacancy'] + '\n' + \
                                        self.vacancy[i]['address_vacancy'] + '\n' + \
                                        self.vacancy[i]['url_vacancy'] + '\n' + \
                                        self.vacancy[i]['requirement_vacancy'] + '\n' + \
                                        self.vacancy[i]['schedule_vacancy'] + '\n' + '\n'
                    list_the_key_words.append(string_profession)
        return list_the_key_words


class FilterSJ(FilterVacancy, ABC):
    """ Класс выполняет функцию фильтрации для запросов сайта superjob.ru """
    def __init__(self, search_query, top_n, filter_words):
        super().__init__(search_query, top_n, filter_words)
        self.vacancy = self.open_json()['sj_vacancy']

    def open_json(self):
        with open('./src/vacancy_file.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def filter_vacancy_name(self):
        list_string_profession = []
        for i in range(len(self.vacancy)):
            if self.search_query in self.vacancy[i]['name_vacancy'].lower():
                string_profession = self.vacancy[i]['name_vacancy'] + '\n' + \
                                    self.vacancy[i]['salary_vacancy'] + '\n' + \
                                    self.vacancy[i]['address_vacancy'] + '\n' + \
                                    self.vacancy[i]['url_vacancy'] + '\n' + \
                                    self.vacancy[i]['requirement_vacancy'][:100] + '...' + '\n' + \
                                    self.vacancy[i]['schedule_vacancy'] + '\n' + '\n'
                list_string_profession.append(string_profession)
        return list_string_profession

    def filter_top_salary(self):
        salary_full = []
        max_salary = []
        salary_string = ''
        for i in range(len(self.vacancy)):
            if 'От' and 'до' in self.vacancy[i]['salary_vacancy']:
                splitting = self.vacancy[i]['salary_vacancy'].split(' ')
                max_salary.append(int(splitting[-1]))
            elif 'До' in self.vacancy[i]['salary_vacancy']:
                max_salary.append(int(self.vacancy[i]['salary_vacancy'][3:]))
            elif 'От' in self.vacancy[i]['salary_vacancy']:
                max_salary.append(int(self.vacancy[i]['salary_vacancy'][3:]))
        set_max_salary = set(max_salary)
        max_salary.clear()
        for sets in set_max_salary:
            max_salary.append(sets)
        max_salary.sort(reverse=True)
        for salary in max_salary:
            for i in range(len(self.vacancy)):
                if self.vacancy[i]['salary_vacancy'] == 'Зарплата не указана':
                    continue
                splitting = self.vacancy[i]['salary_vacancy'].split(' ')
                if len(splitting) != 2:
                    if str(salary) == splitting[-1]:
                        salary_string += self.vacancy[i]['name_vacancy'] + '\n' + \
                                         self.vacancy[i]['salary_vacancy'] + '\n' + \
                                         self.vacancy[i]['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
                else:
                    if str(salary) == splitting[-1]:
                        salary_string += self.vacancy[i]['name_vacancy'] + '\n' + \
                                         self.vacancy[i]['salary_vacancy'] + '\n' + \
                                         self.vacancy[i]['url_vacancy'] + '\n'
                        salary_full.append(salary_string)
        return salary_full

    def __len__(self):
        return len(self.filter_top_salary())

    def filter_the_key_words(self):
        list_the_key_words = []
        splitting_words = self.filter_words.split(',')
        for spl in splitting_words:
            for i in range(len(self.vacancy)):
                for professional in self.vacancy[i]['professional_roles']:
                    prof_title = professional['title'].lower()
                    if spl.lower() in prof_title:
                        string_profession = self.vacancy[i]['name_vacancy'] + '\n' + \
                                            self.vacancy[i]['salary_vacancy'] + '\n' + \
                                            self.vacancy[i]['address_vacancy'] + '\n' + \
                                            self.vacancy[i]['url_vacancy'] + '\n' + \
                                            self.vacancy[i]['requirement_vacancy'][:100] + '...' + '\n' + \
                                            self.vacancy[i]['schedule_vacancy'] + '\n' + '\n'
                        list_the_key_words.append(string_profession)
                    prof_positions = professional['positions']
                    for prof in prof_positions:
                        professional_titles = prof['title'].lower()
                        if spl.lower() in professional_titles:
                            string_profession = self.vacancy[i]['name_vacancy'] + '\n' + \
                                                self.vacancy[i]['salary_vacancy'] + '\n' + \
                                                self.vacancy[i]['address_vacancy'] + '\n' + \
                                                self.vacancy[i]['url_vacancy'] + '\n' + \
                                                self.vacancy[i]['requirement_vacancy'][:100] + '...' + '\n' + \
                                                self.vacancy[i]['schedule_vacancy'] + '\n' + '\n'
                            list_the_key_words.append(string_profession)
        return list_the_key_words
