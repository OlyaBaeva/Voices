from flask import Flask, jsonify

'''''
@app.route('/cards', methods=['GET'])
def get_cards():
        #return jsonify(['1234', '5678', '9012'])
        card_name = ['1234', '5678', '9012']
        if card_name is None:
            return jsonify({"error": "Missing card_name "}), 400
        from main import choose_card
        card_name = choose_card()  # Assume this function makes an API call
        return jsonify({"card_name": card_name})

'''''


def create_app():
    app = Flask(__name__)

    @app.route('/cards', methods=['GET'])
    def get_cards():
        user = get_user()
        card_numbers = ""
        for number, i in users.items():
            if number == user:
                card_numbers = [card["card_number"] for card in i['cards'].values()]
        if card_numbers is None:
            return jsonify({"error": "Карта не найдена "}), 400
        return jsonify({"card_name": card_numbers})

    @app.route('/number', methods=['GET'])
    def get_number():
        number = ['9301071667', '9276677524']
        if number is None:
            return jsonify({"error": "Missing number "}), 400
        return jsonify({"number": number})

    @app.route('/balance/', methods=['GET'])
    def get_balance():
        '''''
        if card_inf is None:
            return jsonify({"error": "Missing card_name "}), 400
        return jsonify({"number": card_inf})
        '''''

    return app


users = {"user_1": {
    "username": 'кирилл',
    "cards": {
        "card_1": {
            "card_number": '1234',
            "balance": "5000"},
        "card_2": {
            "card_number": '5678',
            "balance": "1000"}
    }},
    "user_2": {
        "username": 'ирина',
        "cards": {
            "card_1": {
                "card_number": '9012',
                "balance": "50000"},
        }
    }}


def get_user():
    from main import get_username
    username = get_username()
    if username is None:
        return jsonify({"error": "Нет пользователя с таким именем "}), 400
    rec = ""
    for user, i in users.items():
        if i['username'] in username:
            rec = user
    return rec
