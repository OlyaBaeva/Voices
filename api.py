from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/cards', methods=['GET'])
def get_cards():
    return jsonify(['1234', '5678', '9012'])


app.run()
