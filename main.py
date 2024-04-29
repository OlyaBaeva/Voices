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
    tts = pyttsx3.init()
    rate = tts.getProperty('rate')
    tts.setProperty('rate', rate - 40)
    voices = tts.getProperty('voices')
    print("Init complete. Let's talk")
    tts.setProperty('voice', 'ru')

    for voice in voices:
        if voice.name == 'Vsevolod':
            tts.setProperty('voice', voice.id)


    while True:
        time.sleep(4.5)
        tts.say("ЭТА ШТУКА МЕНЯ УБИЛА")
        tts.runAndWait()
        if "привет марвин" in recognizer.listen("привет марвин"):
            stop_listen()
            tell_function()
            break


