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
             #скажите последние 4 цифры номера
             "responses": main.balance
        },
    "добавить название":{
        "responses": main.new
    },
    "пополнить":
        {

            "responses": main.pay_service
        },
    "оплатить":
        {

            "responses": main.pay
        }
}
}

