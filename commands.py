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
             "название счёта":"",
             "responses": main.balance
        },
    "добавить название":{
        "responses": main.new
    },
    "пополнить":
        {
            "мобильную связь":"",
            "интернет":"",
            "responses": main.pay_service
        },
    "оплатить":
        {
            "жкх":"",
            "responses": main.pay
        }
}
}

