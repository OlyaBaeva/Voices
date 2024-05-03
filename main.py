import json
import time

import speech_recognition
import pyttsx3
from ru_word2number import w2n
import commands
from CustomRecognizer import CustomRecognizer


def recognize_cmd(cmd, dict):
  k = {'cmd': "", 'percent': 0}
  for key in dict:
     if key in cmd:
        k['cmd'] = key
        return k
  return k


def command_listener(recognizer):
    global microphone
    with microphone as s:
        audio = recognizer.listen(s,5)
    recognizer_data = recognizer.recognize_vosk(audio, language="rus")
    text = json.loads(recognizer_data)["text"]
    if text != "":
        return text
    else:
        return "Empty command"


def callback(recognizer, audio):
    recognized_data = recognizer.recognize_vosk(audio, language="rus")
    print(json.loads(recognized_data)["text"])
    return json.loads(recognized_data)["text"]


def main_com():
    global recognizer
    cmd = {'cmd': "", 'com': ""}
    # com - задел на будущее если вдруг хватит сил на подтягивание не только основной команды, но и аргументов
    if "привет марвин" in recognizer.background_listener_text:
        tell_function(textDescriptionFunction)
    elif commands.dict_commands['intents']["имя"] in recognizer.background_listener_text:
        cmd = recognize_cmd(recognizer.background_listener_text, commands.dict_commands['intents'].keys())
        if cmd['cmd'] == "":
             tell_function('Повторите команду')
        else:
            stop_listener()
            commands.dict_commands['intents'][cmd['cmd']]["responses"]()


def tell_function(what):
    tts.say(what)
    tts.runAndWait()
    tts.stop()


def convert_to_numbers(rec):
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
    rec = check_length(4, "Скажите последние 4 цифры карты ")
    return rec


def check_length(length, tell):
    global recognizer
    par = ""
    while not len(par) == length:
        tell_function(tell)
        par = command_listener(recognizer)
        par = convert_to_numbers(par)
    return par


def check(tell, length):
   global recognizer
   rec = ""
   if length != 0:
       rec = check_length(length, tell, recognizer)
   else:
       while rec == "":
         tell_function(tell)
         rec = recognizer.background_listener_text
   return rec


def send():
    global recognizer
    card = choose_card()
    card_str = recognizer.background_listener_text
    conf_bool = False
    while not conf_bool:
        dis = {"cmd": ["номер карты", "реквизиты", "номер телефона"]}
        reci = check("Выберите, через что вы хотите осуществить перевод: " + str(dis['cmd']), 0)
        topic = recognize_cmd(reci, dis['cmd'])
        if 'номер карты' in topic['cmd']:
            card_num = check("Скажите номер карты цифрами ", 16)
            card_str = recognizer.background_listener_text
            card_sum = check("Скажите cумму цифрами ", 0)
            conf_bool = conf("Перевести" + card_sum +" на карту"+card_str)
        elif 'реквизиты' in topic['cmd']:
            account_num = check("Скажите номер счёта получателя цифрами ", 20)
            #инн разный для ИП и нет, надо добавить проверку 10 или 12
            nn = check("Скажите ИНН получателя цифрами ", 10)
            nn_str = recognizer.background_listener_text
            pp = check("Скажите КПП получателя цифрами ", 9)
            pp_str = recognizer.background_listener_text
            bik = check("Скажите БИК получателя цифрами ", 9)
            bik_str = recognizer.background_listener_text
            card_sum = check("Скажите cумму цифрами ", 0)
            conf_bool = conf(f"Перевести {card_sum} по реквизитам. Номер счёта"
                             f" {account_num}. ИНН{nn_str}. КПП{pp_str}. БИК{bik_str}")
        elif 'номер телефона' in topic['cmd']:
            rec_tel = check("Скажите номер телефона ", 10)
            str_tel = recognizer.background_listener_text
            card_sum = (check("Скажите сумму ", 0))
            conf_bool = conf("Перевести" + card_sum + " по номеру" + str_tel)


def balance():
    global recognizer
    card = choose_card()
    card_str = recognizer.background_listener_text
    tell_function("Баланс вашей карты "+card_str + "составляет")


def new():
    conf_bool = False
    while not conf_bool:
        reci = check("Скажите название какого вклада вы хотите изменить ", 0)
        new_name = check("Скажите новое название ", 0)
        conf_bool = conf("Поменять название вклада" + reci + " на " + new_name)


def pay_service():
    global recognizer
    conf_bool = False
    while not conf_bool:
        card = choose_card()
        card_str = recognizer.background_listener_text
        #логика для подтягивания нужной карты
        dis = {'cmd': {'связь и интернет'}}
        reci = check("Выберите то, что хотите оплатить "+str(dis['cmd']), 0)
        topic = recognize_cmd(reci, dis['cmd'])
        rec_tel = check("Скажите номер телефона ", 10)
        str_tel = recognizer.background_listener_text
        rec_sum = check("Скажите сумму ", 0)
        conf_bool = conf("Пополнить" + topic['cmd'] + " номер телефона"+str_tel+" на сумму"+rec_sum)


def conf(tell):
    tell_function(tell+". Скажите пожалуйста. Да или Нет")
    if "да" in recognizer.background_listener_text:
        tell_function("выполняю команду"+ tell)
        #логика выполнения команды
        return True
    elif "нет" in recognizer.background_listener_text:
        tell_function("Давайте попробуем еще раз ")
        return False


tts = pyttsx3.init()
recognizer = CustomRecognizer()
microphone = speech_recognition.Microphone()
if __name__ == "__main__":
    textDescriptionFunction = """
    Вас приветствует голосовой помощник Марвин. Голосовому помощнику доступны следующие команды: 
    команда перевод, для перевода денег по номеру карты, реквизитам, номеру телефона.
    команда баланс, для проверки баланса.
    команда пополнить для пополнения телефона.
    команда добавить название, для добавления названия вклада.
    Скажите,Марвин и название команды для начала работы.
    """
    tts.setProperty('rate', 220)
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    for voice in voices:
        if voice.name == 'Vsevolod':
            tts.setProperty('voice', voice.id)
    print("Init complete. Let's talk")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    stop_listener = recognizer.listen_in_background(microphone, callback, 2)
    while True:
        main_com()
