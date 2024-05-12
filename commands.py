import main

dict_commands = {
        "intents":
        {
            "имя": ('марвин'),
            "перевод":
            {
                "responses": main.send
            },
            "баланс":
            {
             "responses": main.balance
            },
            "депозит":
            {
                "responses": main.create_deposit
            },
            "пополнить":
            {
            "responses": main.pay_service
            },
        }
}

