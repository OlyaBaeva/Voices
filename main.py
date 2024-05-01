import json
import speech_recognition
import pyttsx3
from fuzzywuzzy import fuzz
from ru_word2number import w2n

import commands


tts = pyttsx3.init()
textDescriptionFunction = """
Вас приветствует голосовой помощник Марвин. Голосовому помощнику доступны следующие команды: 
команда перевод, для перевода денег.
команда баланс, для проверки баланса.
команда пополнить для пополнения телефона.
Скажите, что вы хотите сделать?
"""

def start():
    global json_data
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    json_data=callback(recognizer, audio)

def recognize_cmd(cmd, dict):
  k = {'cmd': "", 'com': " "}
  for key in dict:
     print(key,dict)
     if key in cmd:
        print(key)
        k['cmd'] = key
        return k
  print(json_data['text'], k)
  tell_function("команда не распознана, пожалуйста повторите")


def callback(recognizer, audio):
    recognized_data = recognizer.recognize_vosk(audio, language="rus")
    json_data = json.loads(recognized_data)
    if "привет марвин" in recognized_data:
        tell_function(textDescriptionFunction)
    elif commands.dict_commands['intents']["имя"] in recognized_data:
        cmd = recognized_data
        cmd = recognize_cmd(cmd, commands.dict_commands['intents'].keys())
        commands.dict_commands['intents'][cmd['cmd']]["responses"]()
    return json_data

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
    par = ""
    while not len(par) == length:
        tell_function(tell)
        start()
        par = json_data['text']
        par = convert_to_numbers(par)
    return par

def check(tell, length):
   rec = ""
   print(tell)
   if length != 0:
       rec = check_length(length, tell)
   else:
       print("tell", tell)
       while rec =="":
         print("tell", tell, rec)
         tell_function(tell)
         start()
         rec = json_data['text']
   return rec



if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    rate = tts.getProperty('rate')
    tts.setProperty('rate', rate - 40)
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    for voice in voices:
        if voice.name == 'Vsevolod':
            tts.setProperty('voice', voice.id)
    print("Init complete. Let's talk")
    while True:
         start()



def send():
    card = choose_card()
    conf_bool = False
    while not conf_bool:
        dis = {"cmd": ["карта", "номер счёта", "номер телефона"]}
        reci = check("Выберите, через что вы хотите осуществить перевод: " + str(dis['cmd']), 0)
        topic = recognize_cmd(reci, dis['cmd'])
        print('topic', topic)
        if 'карта' in topic['cmd']:
            card_num = check("Скажите номер карты цифрами ", 16)
            card_sum = check("Скажите cумму цифрами ", 0)
            conf_bool=conf("Вы хотите перевести"+ card_sum +" на карту"+str(card_num))
        elif 'номер счёта' in topic['cmd']:
            #очень больно и много параметров
            pass
        elif 'номер телефона' in topic['cmd']:
            bank = {'name': ['мтс', 'втб', 'сбербанк']}
            rec_tel = str(check("Скажите номер телефона ", 10))
            # хорошо бы подтягивать по номеру телефона имеющиеся банки, но пока список
            rec_bank = str(check("Скажите название банка получателя ", 0))
            check_bank = recognize_cmd(rec_bank, bank['name'])
            card_sum = convert_to_numbers(check("Скажите сумму цифрами ", 0))
            conf_bool = conf("Вы хотите перевести" + card_sum + " по номеру" + str(rec_tel)+ ". банк"+check_bank['cmd'])

def balance():
    card = choose_card()
    tell_function("Баланс вашей карты "+str(card) + "составляет")

def new():
    pass
def pay():
    pass



def pay_service():
    conf_bool = False
    while not conf_bool:
        card = choose_card()
        #логика для подтягивания нужной карты
        dis = {'cmd': {'связь и интернет'}}
        reci = check("Выберите то, что хотите оплатить "+str(dis['cmd']), 0)
        topic = recognize_cmd(reci, dis['cmd'])
        rec_tel = str(check("Скажите номер телефона ", 10))
        rec_sum = convert_to_numbers(check("Скажите сумму цифрами ", 0))
        conf_bool = conf("Я правильно понял, вы хотите пополнить" + topic['cmd'] + " номер телефона"+str(rec_tel)+" на сумму"+rec_sum)

def conf(tell):
    tell_function(tell+". Скажите пожалуйста Да или Нет")
    start()
    if "да" in json_data['text']:
        tell_function("выполняю "+ tell)
        #логика выполнения команды
        return True
    elif "нет" in json_data['text']:
        tell_function("Давайте попробуем еще раз ")
        return False

'''''
def execute_cmd(cmd):
    if "баланс" in cmd:
        tell_function("Скажите "+str(commands.dict_commands["баланс"]))

    elif "пополнить" in cmd:
        tell_function(cmd)
    elif "оплатить" in cmd:
        tell_function(cmd)
    elif "перевод" in cmd:
        tell_function("Уточните, пожалуйста "+commands.dict_commands["перевод"])
    else:
        print('Команда не распознана, повторите!')
'''''









