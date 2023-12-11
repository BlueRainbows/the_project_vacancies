import pytest
import requests
from src.file_class import HeadHunter, SuperJob, VacancyHH, VacancySJ


def test_HeadHunter():
    """ Тест проверяет правильность возвращения ответа АПИ,
    при возникновении ошибки в передачи url сайта функция класса возвращает None """
    hh = HeadHunter()
    assert type(hh.get_api()) == dict
    hh.url = 'api.hh.ru'
    assert hh.get_api() is None


def test_SuperJob():
    """ Тест проверяет правильность возвращения ответа АПИ,
    при возникновении ошибки в передачи url сайта функция класса возвращает None """
    sj = SuperJob()
    assert type(sj.get_api()) == dict
    sj.url = 'api.superjob.ru'
    assert sj.get_api() is None


def test_VacancyHH():
    """ Тест выполняет проверку правильности возвращаемого объекта,
    обрабатывает исключения и не предвиденные ошибки в документе """
    hh = HeadHunter()
    hh_vacancy = VacancyHH(hh.get_api())
    assert type(hh_vacancy.get_vacancy()) == list
    with pytest.raises(Exception):
        hh.url = 'api.hh.ru'
        hh_vacancy = VacancyHH(hh.get_api())
        hh_vacancy.get_vacancy()
    hh.url = 'https://api.hh.ru/vacancies'
    dels_value = hh.get_api()
    del dels_value['items'][0]['name']
    hh_vacancy = VacancyHH(dels_value)
    assert hh_vacancy.name_vacancy is None


def test_VacancySJ():
    """ Тест выполняет проверку правильности возвращаемого объекта,
    обрабатывает исключения и не предвиденные ошибки в документе """
    sj = SuperJob()
    sj_vacancy = VacancySJ(sj.get_api())
    assert type(sj_vacancy.get_vacancy()) == list
    sj.url = 'https://api.hh.ru/vacancies'
    dels_value = sj.get_api()
    del dels_value['items'][0]['name']
    sj_vacancy = VacancySJ(dels_value)
    assert sj_vacancy.name_vacancy is None
