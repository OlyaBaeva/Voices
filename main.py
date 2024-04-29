import json
import time
import speech_recognition
import pyttsx3

textDescriptionFunction = """
Вас приветствует голосовой помощник Марвин. Голосовому помощнику доступны следующие команды: 
команда перевод, для перевода денег.
команда баланс, для проверки баланса.
команда пополнить для поплнения телефона.
"""

def callback(recognizer, audio):
    recognized_data = recognizer.recognize_vosk(audio, language="rus")
    json_data = json.loads(recognized_data)
    print(json_data["text"])
    return json_data["text"]


def tell_function():
    engine.say('Привет {}!'.format(username))
    engine.say(textDescriptionFunction)
    engine.runAndWait()


if __name__ == "__main__":
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    engine = pyttsx3.init()
    username = "Алексей"
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    stop_listen = recognizer.listen_in_background(microphone, callback, 3)
    print("Init complete. Let's talk")
    while True:
        time.sleep(4.5)
        print(recognizer.background_listener_text)
        if "привет марвин" in recognizer.background_listener_text:
            stop_listen()
            tell_function()
            break

# with speech_recognition.Microphone() as source:
#    print("Say something!")
#    audio = recognizer.listen(source, 4, 4)

# words = json_data["text"].split(" ")
#    for word in words:
#        if word in dict_commands.keys():
#            print(dict_commands[word])
