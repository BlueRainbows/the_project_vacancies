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

