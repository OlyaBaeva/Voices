import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Union

users = {
    "Kirill": {
        "phone": '+78005553535',
        "cards": {
            "card_1": {
                "card_number": '0234',
                "balance": "5000"
            },
            "card_2": {
                "card_number": '5678',
                "balance": "1000"
            }
        }
    },
    "Irina": {
        "phone": '+78005554545',
        "cards": {
            "card_1": {
                "card_number": '9012',
                "balance": "50000"},
        }
    }
}


def run_FASTAPI():
    uvicorn.run(app, host="127.0.0.1", port=8000)


app = FastAPI()


@app.get("/cards/{username}")
def get_cards(username: str):
    """
    FastAPI endpoint for get all card on username
    :param username:
    :return: JSON list cards
    """
    if users[username] is not None:
        return users[username]["cards"]
    else:
        return HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/balance")
def get_balance(username: Union[str, None] = None, card: Union[str, None] = None):
    """
    FastAPI endpoint for get balance from card for user
    :param username: username user
    :param card: last 4 number card
    :return:
    """
    if users[username] is not None:
        cards = users[username]["cards"]
        for el in cards.values():
            print(el)
            if el["card_number"] == card:
                return {"card": card, "balance": el["balance"]}
        return HTTPException(404, detail=f"User with username: {username} haven't card {card}")
    return HTTPException(status_code=404, detail=f"User with username: {username} not found")
