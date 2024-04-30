import json
import time
import speech_recognition
import pyttsx3
from fuzzywuzzy import fuzz
import threading
import commands

textDescriptionFunction = """
Вас приветствует голосовой помощник Марвин. Голосовому помощнику доступны следующие команды: 
команда перевод, для перевода денег.
команда баланс, для проверки баланса.
команда пополнить для пополнения телефона.
Скажите, что вы хотите сделать?
"""

def callback(recognizer, audio):
    recognized_data = recognizer.recognize_vosk(audio, language="rus")
    json_data = json.loads(recognized_data)

    if "привет марвин" in json_data["text"]:
        tell_function(textDescriptionFunction)
    if commands.dict_commands["имя"] in recognized_data:
        cmd = recognized_data
        print(cmd)
        cmd = recognize_cmd(cmd)
        print("cmd", cmd)
        execute_cmd(cmd)
    if "stop" in json_data["text"]:
        flag = False
        return flag
def recognize_cmd(cmd):
  print(commands.dict_commands.keys())
  for key in commands.dict_commands.keys():
     print("key", key)
     if key in cmd:
        for com in commands.dict_commands[key]:
            if com in cmd:
               return key+" "+ com


def execute_cmd(cmd):
    if  "баланс" in cmd:
        tell_function(cmd)
    elif "пополнить" in cmd:
        tell_function(cmd)
    elif "оплатить" in cmd:
        tell_function(cmd)
    elif "перевод" in cmd:
        tell_function(cmd)
    else:
        print('Команда не распознана, повторите!')

def tell_function(what):
    tts.say(what)
    tts.runAndWait()
    tts.stop()


if __name__ == "__main__":
    flag = True
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    tts = pyttsx3.init()
    rate = tts.getProperty('rate')
    tts.setProperty('rate', rate - 40)
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    for voice in voices:
        if voice.name == 'Vsevolod':
            tts.setProperty('voice', voice.id)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    print("Init complete. Let's talk")
    stop_listen = recognizer.listen_in_background(microphone, callback, 3)


    while True:
        time.sleep(4.5)





