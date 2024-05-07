"""Base logic for Voice Assistance"""
import json
import time

import requests
import speech_recognition
import pyttsx3
from ru_word2number import w2n
from CustomRecognizer import CustomRecognizer
import Levenshtein
import commands
import api


def start():
    """Function for enter point in voice assistance"""
    print("!", recognizer.background_listener_text)
    if "привет марвин" in recognizer.background_listener_text:
        tell_function(textDescriptionFunction)
    elif commands.dict_commands['intents']["имя"] in recognizer.background_listener_text:
        cmd = recognize_cmd(recognizer.background_listener_text, commands.dict_commands['intents'].keys())
        if cmd['cmd'] == "":
            tell_function('Повторите команду')
            start()
        else:
            commands.dict_commands['intents'][cmd['cmd']]["responses"]()
            stop_listen()


def balance():
    """Function for check balance"""
    global default_user
    global BASE_URL
    card = choose_card()
    if card is not None:
        response = requests.get(BASE_URL + "balance?username="+default_user+"&card=" + card)
        if response.status_code == 200:
            amount = json.loads(response.text)["balance"]
            tell_function(f"Баланс вашей карты {card} составляет {amount}")
        else:
            tell_function("Карта не обнаружена")
            balance()


def create_deposit():
    """Function for create new deposit"""
    conf_bool = False
    while not conf_bool:
        reci = check_length("Скажите название какого вклада вы хотите изменить ")
        new_name = check_length("Скажите новое название ")
        conf_bool = conf("Поменять название вклада" + reci + " на " + new_name)


def send():
    """Input description"""
    pass
    '''conf_bool = False
    while not conf_bool:
        dis = {"cmd": ["карта", "реквизиты", "номер телефона"]}
        reci = check("Выберите, через что вы хотите осуществить перевод: " + str(dis['cmd']), 0)
        topic = recognize_cmd(reci, dis['cmd'])
        if 'карта' in topic['cmd']:
            card_num = check("Скажите номер карты цифрами ", 16)
            card_str = json_data['text']
            card_sum = check("Скажите cумму цифрами ", 0)
            conf_bool = conf("Перевести" + card_sum + " на карту" + card_str)
        elif 'реквизиты' in topic['cmd']:
            account_num = check("Скажите номер счёта получателя цифрами ", 20)
            # инн разный для ИП и нет, надо добавить проверку 10 или 12
            nn = check("Скажите ИНН получателя цифрами ", 10)
            nn_str = json_data['text']
            pp = check("Скажите КПП получателя цифрами ", 9)
            pp_str = json_data['text']
            bik = check("Скажите БИК получателя цифрами ", 9)
            bik_str = json_data['text']
            card_sum = check("Скажите cумму цифрами ", 0)
            conf_bool = conf("Перевести" + card_sum + "по реквизитам. номер счёта" + account_num +
                             ".ИНН" + nn_str + ".КПП" + pp_str + ".БИК" + bik_str)
        elif 'номер телефона' in topic['cmd']:
            rec_tel = check("Скажите номер телефона ", 10)
            str_tel = json_data['text']
            card_sum = (check("Скажите сумму ", 0))
            conf_bool = conf("Перевести" + card_sum + " по номеру" + str_tel)
    '''


def pay_service():
    pass
    '''
    conf_bool = False
    while not conf_bool:
        card = choose_card()
        # логика для подтягивания нужной карты
        dis = {'cmd': {'связь и интернет'}}
        reci = check("Выберите то, что хотите оплатить " + str(dis['cmd']), 0)
        topic = recognize_cmd(reci, dis['cmd'])
        rec_tel = check("Скажите номер телефона ", 10)
        str_tel = json_data['text']
        rec_sum = vosk_listen_recognize("Скажите сумму ", 3)
        conf_bool = conf("Пополнить" + topic['cmd'] + " номер телефона" + str_tel + " на сумму" + rec_sum)
    '''


def recognize_cmd(cmd, com):
    """
    Function for split command and query params in statement
    :param
    cmd: type
         what is it
    com: type
         what is it
    :return
    k(dict): input what we return
    """
    k = {'cmd': "", 'percent': 0}
    if 'марвин' in cmd:
        cmd = cmd.replace('марвин', '')
    cmd = cmd.replace(" ", "")
    match_list = {}
    for key in com:
        concat_name = ''.join(key.split()).lower()
        match_list[key] = Levenshtein.jaro_winkler(cmd, concat_name) / len(key.split())
    k['cmd'] = max(match_list.items(), key=lambda x: x[1])[0]
    return k


def callback(recognizer, audio):
    """
    Function callback in background listener
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
    Function for convert word presentation number in numeric presentation
    :param rec: text what was recorded from micro
    :return numeric presentation number what was recorded. If numeric not transcript return empty string
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
    """Input description"""
    rec = check_length("Скажите последние 4 цифры карты ", 4)
    return rec


def check_length(tell, length=0):
    """
    Input description
    :return
    """
    while True:
        tell_function(tell)
        par = vosk_listen_recognize(5)
        par = convert_to_numbers(par)
        if len(par) != length:
            tell_function("Не удалось распознать параметр")
        else:
            break
    return par


def check_number():
    """
    Input description
    :return:
    """
    rec = check_length("Скажите номер телефона ", 10)
    return rec


def conf(tell):
    """Describe function"""
    tell_function(tell + ". Скажите пожалуйста. Да или Нет")
    if "да" in vosk_listen_recognize(3):
        tell_function("выполняю команду" + tell)
        # логика выполнения команды
        return True
    elif "нет" in vosk_listen_recognize(3):
        tell_function("Давайте попробуем еще раз ")
        return False


def vosk_listen_recognize(time_listen):
    """
    Function for listen in main thread micro
    :param time_listen: how many seconds we must listen micro
    :return: recognize text
    :except: Exception if vosk can't recognize audio
    """
    global microphone
    global recognizer
    with microphone as source:
        audio = recognizer.listen(source, time_listen)
    try:
        recognize_text = json.loads(recognizer.recognize_vosk(audio))["text"]
        print(recognize_text)
    except speech_recognition.UnknownValueError:
        raise Exception("Vosk not understand what you say")
    return recognize_text


microphone = speech_recognition.Microphone()
recognizer = CustomRecognizer()
tts = pyttsx3.init()
default_user = "Kirill"
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
    #api.run_FASTAPI()
    print("Init complete. Let's talk")
    while True:
        start()
        time.sleep(2)
