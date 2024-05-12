"""Base logic for Voice Assistance"""
import json
import re
import time

import requests
import speech_recognition
import pyttsx3
from ru_word2number import w2n
from CustomRecognizer import CustomRecognizer
import Levenshtein
import commands


def start():
    """
    Function for entering point in voice assistance
    in the case of the phrase "привет марвин",
    the program tells the text about all possible user actions
    :return if user's request is a existing command program redirects on the command,
    in the case of the phrase "привет марвин",
    the program tells the text about all possible user actions
    else ask to repeat
    """
    global default_user
    if "привет марвин" in recognizer.background_listener_text:
        tell_function(textDescriptionFunction)
    elif commands.dict_commands['intents']["имя"] in recognizer.background_listener_text:
        cmd = recognize_cmd(recognizer.background_listener_text, commands.dict_commands['intents'].keys())
        if cmd['cmd'] == "":
            tell_function('Повторите команду')
            start()
        else:
            try:
                if default_user is not None:
                    commands.dict_commands['intents'][cmd['cmd']]["responses"]()
                else:
                    default_user = commands.dict_commands['intents']['login']["responses"]()
                    start()
            except TypeError:
                tell_function('Команда не найдена, попробуйте еще раз')
                start()


def login():
    '''
    Function for logging in
    program asks about user's phone to enter,
    :return if it is real user it remembers the user's login and gives access to data,
    otherwise tells about mistake and ask repeat
    '''
    global BASE_URL
    global default_user
    user_authorized = False
    first = False
    while not user_authorized:
        if not first:
            first = True
            tell_function("Команды доступны только для авторизированных пользователей."
                          " Скажите номер телефона чтобы войти в профиль")
        phone = convert_telephone_number(check_length(""))
        if phone == "":
            continue
        response = requests.get(BASE_URL + "login?userphone=" + str(phone))
        if response.status_code == 200:
            user_authorized = True
            default_user = json.loads(response.text)["username"]
            tell_function(f"Здравствуйте {default_user}, Вы вошли в свой профиль")
            return default_user
        else:
            tell_function("Пользователь с таким номером телефона не обнаружен, попробуйте ещё раз")


def balance():
    """
    Function for checking balance
    asks which card user wants to check
    :return information about balance of user's card,
    in case of error tells about it
    """
    global default_user
    global BASE_URL
    card = choose_card()
    if card is not None:
        response = requests.get(BASE_URL + "balance?username=" + default_user + "&card=" + card)
        if response.status_code == 200:
            amount = json.loads(response.text)["balance"]
            tell_function(f"Баланс вашей карты {card} составляет {amount}")
        else:
            tell_function("Карта не обнаружена")
            balance()


def rename_deposite():
    """
    Function for renaming existed deposit
    asks user about current name and new name
    :return result of operation: success(change title),
    or "No contribution found" and repeat function
    """
    response = requests.get(
        BASE_URL + "alldeposits?username=" + default_user)
    if response.status_code == 200:
        deposit_name = json.loads(response.text)["deposit_name"]
        reci = check_length("Скажите название какого вклада вы хотите изменить ." + deposit_name)
        topic = recognize_cmd(reci, deposit_name)['cmd']
        new_name = check_length("Скажите новое название ")
        conf_bool = conf("Поменять название вклада" + topic + " на " + new_name)
        if conf_bool:
            response = requests.get(
                BASE_URL + "deposit?username=" + default_user + "&olddepositname=" + topic + "&newdepositname=" + new_name)
            if response.status_code == 200:
                tell_function(f"Операция выполнена")
                start()
            else:
                tell_function("Вклад не обнаружен")
                rename_deposite()
        else:
            start()


def is_telephone_number(number):
    """
    Function for checking for consistency with the standard for phone numbers
    :param number: telephone number was given from def convert_telephone_number
    :return If the number corresponds to the standard, it returns True, otherwise, it returns False
    """
    r = re.compile(
        r'^((\+7|\+8)[-.\s]??(9[1-79]{2}|80[0-9])[-.\s]??\d{3}[-.\s]??\d{4}|\(\+7|\+8\)\s*(9[0-79]{2}|80[0-9])['
        r'-.\s]??\d{3}[-.\s]??\d{4}|\+7[-.\s]??(9[0-79]{2}|80[0-9])[-.\s]??\d{4})$')
    if r.search(number):
        return True
    else:
        return False


def convert_telephone_number(rec):
    """
    Function for converting word presentation of telephone number in numeric presentation
    :param rec: text what was recorded from micro
    :return numeric presentation of telephone number what was recorded. If numeric not transcript or does not match
    standard of telephone numbers return empty string
    """
    rec = list(rec.split())
    converted_rec = list()

    if len(rec) > 0 and rec[0] == "плюс":
        rec.remove("плюс")

    cur_digit = -1
    prev_digit = -1

    while rec:
        try:
            tmp = w2n.word_to_num(rec.pop(0))
            if len(converted_rec) == 0 and (tmp == 7 or tmp == 8):
                converted_rec.append("+7")
            else:
                if tmp // 100 > 0:
                    cur_digit = 3
                elif tmp // 10 > 1:
                    cur_digit = 2
                elif tmp // 10 <= 1 and tmp != 0:
                    cur_digit = 1
                else:
                    cur_digit = 0
                if cur_digit < prev_digit and tmp != 0:
                    converted_rec[len(converted_rec) - 1] += tmp
                else:
                    converted_rec.append(tmp)
                if tmp // 100 > 0 and len(rec) <= 4:
                    prev_digit = 2
                else:
                    prev_digit = cur_digit
        except ValueError:
            tell_function("Цифры не были распознаны, пожалуйста, повторите")
            check_length("")

    converted_rec = "".join(str(el) for el in converted_rec)
    if is_telephone_number(converted_rec):
        return converted_rec
    else:
        tell_function("Номер телефона не существует, пожалуйста, введите другой номер телефона")
        rec = vosk_listen_recognize(5)
        if convert_telephone_number(rec):
            return convert_telephone_number(rec)


def send():
    """
    money transfer at the client's choice: by card or by phone number,
    then requests information for the transfer: card number and amount
    : return do the transfer, executes the transfer and informs the
    user on the success of the operation. In case of failure informs
    the user on the wrong input data or a mistake.
    """
    response = requests.get(
        BASE_URL + "allcards?username=" + default_user)
    if response.status_code == 200:
        cards = json.loads(response.text)
        cards_last_numbers = list(el[-4:] for el in cards)
        card_names = " или ".join(" ".join(el) for el in cards_last_numbers)
        from_card = check_length("Выберите номер карты, с которой хотите перевести " + card_names, 4)
        if from_card in cards_last_numbers:
            from_card = cards[cards_last_numbers.index(from_card)]
            dis = {"cmd": ["карта", "номер телефона"]}
            reci = check_length("Выберите, через что вы хотите осуществить перевод: " + str(dis['cmd']))
            topic = recognize_cmd(reci, dis['cmd'])
            if 'карта' in topic['cmd']:
                card_num = check_length("Скажите номер карты цифрами ", 16)
                response = requests.get(
                    BASE_URL + "card?username=" + default_user + "&card=" + card_num)
                if response.status_code == 200:
                    card_sum = check_length("Скажите cумму ", -1)
                    conf_bool = conf("Перевести" + card_sum + " на карту" + card_num)
                    if conf_bool:
                        response = requests.get(
                            BASE_URL + "send?username=" + default_user + "&fromcard=" + from_card + "&tocard=" + card_num + "&amount=" + card_sum)
                        if response.status_code == 200:
                            tell_function("Операция выполнена")
                            start()
                        else:
                            resp = check_length(
                                "Не достаточно средств на карте. Хотите попробовать с другой картой? ")
                            if "да" in resp:
                                send()
                            else:
                                tell_function("Операция отменена")
                                start()
                    else:
                        start()
                else:
                    resp = check_length("Карта с таким номером не обнаружена. Хотите попробовать еще раз? ")
                    if "нет" in resp:
                        tell_function(f"Операция отменена")
                        start()
                    else:
                        send()
            elif 'номер' in topic['cmd']:
                rec_tel = convert_telephone_number(check_length("Скажите номер телефона "))
                response = requests.get(
                    BASE_URL + "login?userphone=" + rec_tel)
                if response.status_code == 200:
                    card_sum = (check_length("Скажите сумму ", -1))
                    conf_bool = conf("Перевести" + card_sum + " по номеру" + ' '.join(list(rec_tel[1:])))
                    if conf_bool:
                        response = requests.get(
                            BASE_URL + "send?username=" + default_user + "&fromcard=" + from_card + "&tophone=" + rec_tel + "&amount=" + card_sum)
                        if response.status_code == 200:
                            tell_function("Операция выполнена")
                            start()
                        else:
                            tell_function("Операция отклонена")
                            send()
                    else:
                        start()
                else:
                    tell_function("Карта не обнаружена")
                    send()


def pay_service():
    """
    Function for making payments
    ask which object must be paid, data about recipient and sum, then is the user sure
    :return do operation, if everything is correct tell about success, else about error
    """
    response = requests.get(
        BASE_URL + "allcards?username=" + default_user)
    if response.status_code == 200:
        cards = json.loads(response.text)
        cards_last_numbers = list(el[-4:] for el in cards)
        card_names = " или ".join(" ".join(el) for el in cards_last_numbers)
        from_card = check_length("Выберите номер карты, с которой хотите перевести " + card_names, 4)
        if from_card in cards_last_numbers:
            from_card = cards[cards_last_numbers.index(from_card)]
            dis = {'cmd': {'связь и интернет'}}
            reci = check_length("Выберите то, что хотите оплатить " + str(dis['cmd']))
            topic = recognize_cmd(reci, dis['cmd'])
            phone = convert_telephone_number(check_length("Скажите номер телефона "))
            amount = check_length("Скажите сумму ", -1)
            conf_bool = conf(
                "Пополнить" + topic['cmd'] + " номер телефона" + ' '.join(list(phone[1:])) + " на сумму" + amount)
            if conf_bool:
                response = requests.get(
                    BASE_URL + "pay?username=" + default_user + "&card=" + from_card + "&phone=" + phone + "&amount=" + amount)
                if response.status_code == 200:
                    amount = json.loads(response.text)["balance"]
                    tell_function(f"Операция выполнена")
                else:
                    resp = check_length("Недостаточно средств. Хотите попробовать с пополнить с другой карты?")
                    if "да" in resp:
                        pay_service()
                    else:
                        tell_function("Операция отменена")
                        start()
            else:
                start()


def recognize_cmd(cmd, com):
    """
    Function for splitting command and query params in statement
    :param cmd: recognized phrase; com: the list of commands where we are looking for
    :return k: command which we find by user's phrase
    """
    k = {'cmd': "", 'percent': 0}
    if 'марвин' in cmd:
        cmd = cmd.replace('марвин', '')
    if cmd.count(" ") == 0:
        flag = True
    else:
        flag = False
        cmd = cmd.replace(" ", "")
    match_list = {}
    if flag:
        if com.count(" ") == 0:
            concat_name = com
            match_list[concat_name] = Levenshtein.jaro_winkler(cmd, concat_name) / len(concat_name)
        else:
            for key in com:
                concat_name = key
                match_list[concat_name] = Levenshtein.jaro_winkler(cmd, concat_name) / len(concat_name.split())
    else:
        for key in com:
            if key.count(" ") != 0:
                key = key.replace(" ", "")
            concat_name = ''.join(key.split()).lower()
            match_list[key] = Levenshtein.jaro_winkler(cmd, concat_name) / len(key.split())
    k['cmd'] = max(match_list.items(), key=lambda x: x[1])[0]
    return k


def callback(recognizer, audio):
    """
    Function callback in background listener
    :params recognizer: recognizer of data (CustomRecognizer()); audio: the stream that we recognize
    :return result what can recognize from background with vosk_recognizer
    """
    recognized_data = recognizer.recognize_vosk(audio, language="rus")
    return json.loads(recognized_data)["text"]


def tell_function(what):
    """
    Function for synthesis text in voice
    :param
    what (str): text what be synthesis in text
    """
    tts.say(what)
    tts.runAndWait()
    tts.stop()


def convert_to_numbers(rec):
    """
    Function for converting word presentation of number in numeric presentation
    :param rec: text that was recorded from micro
    :return numeric presentation of number that was recorded.
    If numeric presentation is not transcripted return empty string
    """
    s = list(rec.split())
    new_rec = list()
    for i in s:
        try:
            new_rec.append(w2n.word_to_num(i))
        except ValueError:
            tell_function("Цифры не были распознаны, пожалуйста повторите")
            return ""
    new_rec = "".join(str(el) for el in new_rec)
    return new_rec


def choose_card():
    """
    The function for recognizing an authorized user's card
    """
    rec = check_length("Скажите последние 4 цифры карты ", 4)
    return rec


def check_length(tell, length=0):
    """
    Function on checking length of parameters
    :param length: which must be, default 0
    :param tell:what program sayed;
    :return if is it correct - param; else tells about error
    """
    while True:
        tell_function(tell)
        par = vosk_listen_recognize(5)
        if length == -1:
            par = count_sum(par.split())
            if par != "":
                return par
        if length != 0:
            par = convert_to_numbers(par)
            if len(par) == length:
                return par

        elif len(par) != 0:
            return par


def count_sum(numbers):
    """
    Function to identify sum
    :param numbers: what we said
    :return "normal" (for program) numeric string
    """
    num = 0
    prev = None
    for i in numbers:
        try:
            tmp = w2n.word_to_num(i)
            if tmp > 999:
                num = num - num % 1000 + num % 1000 * tmp
            else:
                num += tmp
        except ValueError:
            tell_function("Цифры не были распознаны, пожалуйста повторите")
            return ""
    return str(num)


def conf(tell):
    """
    Function for checking if user confident in choice
    asks about user sure or not
    :param tell: phrase which program will say
    :return True if answer "yes" , else False
    """
    ans = check_length(tell + ". Скажите пожалуйста. Да или Нет")
    if "да" in ans:
        tell_function("выполняю команду" + tell)
        return True
    elif "нет" in ans:
        tell_function("Операция отменена")
        return False


def vosk_listen_recognize(time_listen):
    """
    Function for listening in main thread micro
    :param time_listen: how many seconds we must listen micro
    :return: recognize text
    :except: Exception if vosk can't recognize audio
    """
    global microphone
    global recognizer
    with microphone as source:
        try:
            audio = recognizer.listen(source, time_listen)
        except:
            return ""
    try:
        recognize_text = json.loads(recognizer.recognize_vosk(audio))["text"]
    except speech_recognition.UnknownValueError:
        raise Exception("Vosk not understand what you say")
    return recognize_text


microphone = speech_recognition.Microphone()
recognizer = CustomRecognizer()
tts = pyttsx3.init()
default_user = None
BASE_URL = "http://127.0.0.1:8000/"
if __name__ == "__main__":
    textDescriptionFunction = """
    Вас приветствует голосовой помощник Марвин. Голосовому помощнику доступны следующие команды: 
    команда перевод, для перевода денег по номеру карты, реквизитам, номеру телефона.
    команда баланс, для проверки баланса.
    команда пополнить для пополнения телефона.
    команда добавить название, для добавления названия вклада.
    Скажите,Марвин и название команды для начала работы.
    """
    rate = tts.getProperty('rate')
    tts.setProperty('rate', rate - 40)
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    stop_listen = recognizer.listen_in_background(source, callback, phrase_time_limit=5)
    for voice in voices:
        if voice.name == 'Vsevolod':
            tts.setProperty('voice', voice.id)
    # api.run_FASTAPI()
    print("Init complete. Let's talk")
    while True:
        start()
        time.sleep(2)
