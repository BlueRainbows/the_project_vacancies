import pytest
import requests

from src.file_class import HeadHunter, SuperJob


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
