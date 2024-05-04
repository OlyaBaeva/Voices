
def test_choose_card(server):
    response = server.get('/cards?card_name=card_name')
    assert response.status_code == 200
    data = response.get_json()
    assert data['card_name'] == '1234', f"Expected temperature: 1234, Actual temperature: {data['card_name']}"
