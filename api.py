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
        card_name = ['1234', '5678', '9012']
        if card_name is None:
                return jsonify({"error": "Missing card_name "}), 400
        from main import choose_card
        import model
        card_name = choose_card()  # Assume this function makes an API call

        return jsonify({"card_name": card_name})

    return app

