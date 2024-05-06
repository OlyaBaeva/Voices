def test_choose_card(server):
    response = server.get('/cards?card_name=card_name')
    assert response.status_code == 200
    from main import choose_card
    card_name = choose_card()
    data = response.get_json()
    from main import tell_function
    return card_name if card_name in data['card_name'] else tell_function(
        f"Карта с  номером: {card_name} не найдена")


def test_number(server):
    response = server.get('/number?number=number')
    assert response.status_code == 200
    from main import check_number
    number = check_number()
    data = response.get_json()
    from main import tell_function
    return number if number in data['number'] else tell_function(f"Номер телефона: {data['number']} не найден")


def test_user(server):
    response = server.get('/user?user=user')
    assert response.status_code == 200
    data = response.get_json()
    from main import tell_function
    return tell_function(f"Пользователь: {data['user']} не найден")
