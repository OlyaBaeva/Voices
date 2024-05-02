import main

dict_commands = {
    "intents": {
    "имя": ('марвин'),
    "перевод":
        {
            "responses": main.send

         },
    "баланс":
        {
             "responses": main.balance
        },
    "добавить название":{
        "responses": main.new
    },
    "пополнить":
        {

            "responses": main.pay_service
        }

}
}

