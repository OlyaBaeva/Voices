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
        },
        "deposits": {
            "deposit_1": {
                "deposit_name": "премиум",
                "money": "",
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
        raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


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
        raise HTTPException(status_code=404, detail=f"User with username: {username} haven't card {card}")
    raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/deposit")
def deposit(username: Union[str, None] = None, olddepositname: Union[str, None] = None,
            newdepositname: Union[str, None] = None):
    """
    FastAPI endpoint for get balance from card for user
    :param newdepositname:
    :param olddepositname:
    :param username: username user
    :return:
    """
    if users[username] is not None:
        deposit_key = next(
            (key for key, value in users[username]['deposits'].items() if value["deposit_name"] == olddepositname),
            None)
        if deposit_key is not None:
            users[username]['deposits'][deposit_key]["deposit_name"] = newdepositname
            return {"deposit_name": newdepositname}
        raise HTTPException(404, detail=f"User with username: {username} haven't deposit {olddepositname}")
    raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/pay")
def pay_service(username: Union[str, None] = None, card: Union[str, None] = None, phone: Union[str, None] = None,
                amount: Union[str, None] = None):
    """
    FastAPI endpoint for get balance from card for user
    :param phone:
    :param amount:
    :param username: username user
    :param card: last 4 number card
    :return:
    """
    if users[username] is not None:
        card_key = next((key for key, value in users[username]['cards'].items() if value["card_number"] == card), None)
        if card_key is not None:
            if int(users[username]['cards'][card_key]["balance"]) >= int(amount):
                users[username]['cards'][card_key]["balance"] = str(
                    int(users[username]['cards'][card_key]["balance"]) - int(amount))
                return {"card": card, "balance": users[username]['cards'][card_key]["balance"]}
            raise HTTPException(404, detail=f"Insufficient funds")
        raise HTTPException(404, detail=f"User with username: {username} haven't card {card}")
    raise HTTPException(status_code=404, detail=f"User with username: {username} not found")
