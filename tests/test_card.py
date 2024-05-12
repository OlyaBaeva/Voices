import pytest
import commands
from main import *


class TestClassIsTelephoneNumber:
    def test_isTelephoneNumber_correctNumber(self):
        tel = "+79139702345"
        assert is_telephone_number(tel)

    def test_isTelephoneNumber_wrongNumber(self):
        tel = "+59139702345"
        assert not is_telephone_number(tel)

    def test_isTelephoneNumber_smallAmountOfNumbers(self):
        tel = "+7913970"
        assert not is_telephone_number(tel)


class TestClassCountSum:
    def test_countSum_lessThanThousand(self):
        numbers = ['сто', 'двадцать', 'восемь']
        assert count_sum(numbers) == '128'

    def test_countSum_lessThanMillion(self):
        numbers = ['сто', 'пять', 'тысяч', 'двести', 'восемьдесят']
        assert count_sum(numbers) == '105280'

    def test_countSum_moreThanMillion(self):
        numbers = ['три', 'миллиона', "триста", "девяносто", "пять", "тысяч", "двести", 'восемьдесят', "пять"]
        assert count_sum(numbers) == '3395285'

    def test_countSum_withoutThousands(self):
        numbers = ['сто', 'пять', 'миллионов', 'восемьдесят']
        assert count_sum(numbers) == "105000080"


class TestClassRecognizeCmd:
    def test_recognizeCmd_simpleTest(self):
        cmd = "пополнить"
        com = ['перевод', 'пополнить', 'оплатить']
        from main import recognize_cmd
        response = recognize_cmd(cmd, com)
        assert response['cmd'] == "пополнить"

    def test_recognizeCmd_differentNames(self):
        cmd = "пополнение"
        com = ['перевод', 'пополнить', 'оплатить']
        from main import recognize_cmd
        response = recognize_cmd(cmd, com)
        assert response['cmd'] == "пополнить"

    def test_recognizeCmd_difficultResult(self):
        cmd = "я хочу пополнить телефон"
        com = ['перевод', 'пополнить', 'оплатить']
        from main import recognize_cmd
        response = recognize_cmd(cmd, com)
        assert response['cmd'] == "пополнить"
