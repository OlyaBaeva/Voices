import json
import speech_recognition
import pyttsx3
from fuzzywuzzy import fuzz
import commands

tts = pyttsx3.init()
textDescriptionFunction = """
Вас приветствует голосовой помощник Марвин. Голосовому помощнику доступны следующие команды: 
команда перевод, для перевода денег.
команда баланс, для проверки баланса.
команда пополнить для пополнения телефона.
Скажите, что вы хотите сделать?
"""

def recog(recognizer, audio):
    recognized_data = recognizer.recognize_vosk(audio, language="rus")
    return recognized_data

def recognize_cmd(cmd, dict):
  print(*dict)
  k = {'cmd':"", 'com':" "}
  for key in dict:
     print("key", key)
     if key in cmd:
         k['cmd']= key
         return k
def callback(recognizer, audio):
    recognized_data = recog(recognizer, audio)
    json_data = json.loads(recognized_data)
    if "привет марвин" in recognized_data:
        tell_function(textDescriptionFunction)
    elif commands.dict_commands['intents']["имя"] in recognized_data:
        cmd = recognized_data
        print(cmd)
        cmd = recognize_cmd(cmd, commands.dict_commands['intents'].keys())
        print("cmd", cmd)
        commands.dict_commands['intents'][cmd['cmd']]["responses"](audio, recognizer)

def tell_function(what):
    tts.say(what)
    tts.runAndWait()
    tts.stop()

def choose_card(recognizer, audio):
    tell_function("Скажите последние 4 цифры карты ")
    rec = recog(recognizer, audio)
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
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        callback(recognizer, audio)


def send():
    pass
def balance():
    pass

def new():
    pass
def pay():
    pass
def pay_service(audio, recognizer):
    card = choose_card(recognizer, audio)
    #логика для подтягивания нужной карты
    dis = {'cmd': {'мобильная связь и Интернет'}}
    print(card)
    tell_function("Выберите то, что хотите оплатить "+str(dis['cmd']))
    reci = recog(recognizer, audio)
    print(reci)
    topic = recognize_cmd(reci, dis.keys())
    tell_function("Скажите номер телефона ")
    rec_tel = recog(recognizer, audio)
    tell_function("Скажите сумму ")
    rec_sum = recog(recognizer, audio)
    tell_function("Я правильно понял, вы хотите пополнить" + topic + " номер телефона"+rec_tel+" на сумму"+rec_sum)
    print(card, rec_tel, rec_sum)


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










