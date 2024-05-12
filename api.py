import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Union

users = {
    "Kirill": {
        "phone": '+78005553535',
        "cards": {
            "card_1": {
                "card_number": '5487345623450234',
                "balance": "5000"
            },
            "card_2": {
                "card_number": '1234567898765678',
                "balance": "1000"
            }
        },
        "deposits": {
            "deposit_1": {
                "deposit_name": "премиум",
                "balance": "",
            }
        }
    },
    "Irina": {
        "phone": '+78005554545',
        "cards": {
            "card_1": {
                "card_number": '3456865412349012',
                "balance": "50000"},
        }
    }
}


def run_FASTAPI():
    uvicorn.run(app, host="127.0.0.1", port=8000)


app = FastAPI()


@app.get("/login")
def login(userphone: Union[str, None] = None):
    """
    FastAPI endpoint for getting username of user with given telephone number
    :param userphone: the phone number that the user sent
    :return: username with this telephone number
    """
    username = None
    for key in users:
        if (users[key]["phone"]) == userphone.replace(" ", "+"):
            username = key
            break
    if username is not None:
        return {"username": username, "phone": userphone}
    raise HTTPException(status_code=404, detail=f"User with telephone number: {userphone} not found")


@app.get("/card")
def get_cards(username: Union[str, None] = None, card: Union[str, None] = None):
    """
    FastAPI endpoint for get all cards on username
    :param card: the user's card numbers
    :param username: sender's username
    :return: JSON list cards
    """
    card_numbers = [card["card_number"] for user in users.values() for card in user["cards"].values()]
    if card in card_numbers:
        return True
    else:
        raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/balance")
def get_balance(username: Union[str, None] = None, card: Union[str, None] = None):
    """
    FastAPI endpoint for get balance from card for user
    :param username: sender's username
    :param card: last 4 number card
    :return:
    """
    if users[username] is not None:
        cards = users[username]["cards"]
        for el in cards.values():
            print(el)
            if el["card_number"][-4:] == card:
                return {"card": card, "balance": el["balance"]}
        raise HTTPException(status_code=404, detail=f"User with username: {username} haven't card {card}")
    raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/alldeposits")
def deposit(username: Union[str, None] = None):
    """
    FastAPI endpoint for get balance from card for user
    :param username: sender's username
    :return:
    """
    if users[username] is not None:
        deposits = users[username]["deposits"]
        if deposits is not None:
            for el in deposits.values():
                return {"deposit_name": el["deposit_name"]}
            return {"deposit_name": deposits['']}
        raise HTTPException(404, detail=f"User with username: {username} haven't deposits")
    raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/allcards")
def allcards(username: Union[str, None] = None):
    """
    FastAPI endpoint for getting all cards of the user
    :param username: sender's username
    :return:list of user's card numbers
    """
    if users[username] is not None:
        cards = users[username]["cards"]
        if users[username]["cards"] is not None:
            arr = list()
            for el in cards.values():
                arr.append(el["card_number"])
            return arr
        return
    else:
        raise HTTPException(status_code=404, detail=f"User with username: {username} not found")


@app.get("/deposit")
def deposit(username: Union[str, None] = None, olddepositname: Union[str, None] = None,
            newdepositname: Union[str, None] = None):
    """
    FastAPI endpoint for get balance from card for user
    :param newdepositname: new name of the deposit
    :param olddepositname: the name that needs to be changed
    :param username: sender's username
    :return: changed deposit's name
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
    :param phone: the phone number to be paid for
    :param amount: the amount to be transferred
    :param username: sender's username
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


@app.get("/send")
def send(username: Union[str, None] = None, fromcard: Union[str, None] = None, tophone: Union[str, None] = None,
         tocard: Union[str, None] = None,
         amount: Union[str, None] = None):
    """
    FastAPI endpoint for sending money from one user to another user
    :param username: sender's username
    :param fromcard: card number from which money is sent
    :param tophone: recipient's phone number
    :param tocard: recipient's card number
    :param amount: sum of money that is sent
    :return: number of sender's card, changed sender's balance
    """
    if users[username] is not None:
        card_key = None
        for key in users:
            if tocard is not None:
                for k in users[key]["cards"]:
                    if (users[key]["cards"][k]["card_number"]) == tocard:
                        card_key = k
                        to_user = key
                        break
            elif tophone is not None:
                if (users[key]["phone"]) == tophone.replace(" ", "+"):
                    card_key = "card_1"
                    to_user = key
                    break
        fromcard = next((key for key, value in users[username]['cards'].items() if value["card_number"] == fromcard),
                        None)
        if card_key is not None:
            if int(users[username]['cards'][fromcard]["balance"]) >= int(amount):
                users[username]['cards'][fromcard]["balance"] = str(
                    int(users[username]['cards'][fromcard]["balance"]) - int(amount))
                users[to_user]['cards'][card_key]["balance"] = str(
                    int(users[to_user]['cards'][card_key]["balance"]) + int(amount))
                return {"card": fromcard, "balance": users[username]['cards'][fromcard]["balance"]}
            return {"card": fromcard, "balance": users[username]['cards'][fromcard]["balance"]}
        raise HTTPException(404, detail=f"User with username: {username} haven't card {fromcard}")
    raise HTTPException(status_code=404, detail=f"User with username: {username} not found")
