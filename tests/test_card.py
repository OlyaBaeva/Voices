import unittest.mock
import main

def test_choose_card():
    # Создаем мок для функции check_length с возвращаемым значением "1234"
    mock_check_length = unittest.mock.MagicMock(return_value="1234")

    # Патчим функцию check_length в модуле main нашим моком
    with unittest.mock.patch('main.check_length', mock_check_length):
        # Вызываем функцию choose_card
        result = main.choose_card()

    # Проверяем, что мок функции check_length был вызван с правильными аргументами
    mock_check_length.assert_called_once_with(4, "Скажите последние 4 цифры карты ")

    # Проверяем, что функция choose_card вернула ожидаемое значение
    assert result == "1234"
