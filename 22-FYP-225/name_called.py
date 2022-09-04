import speech_recognition as sr 
from speech_recognition import UnknownValueError

rec = sr.Recognizer()

my_micro = sr.Microphone(device_index=1)

with my_micro as source:

    # print("Say Something...")
    # audio = rec.listen(source, 3)

    harvard = sr.AudioFile('audio\input\live_audio.wav')
    
    with harvard as source:
        audio = rec.record(source)
    try:
        to_text = rec.recognize_google(audio)
        print(to_text)

        if "luqman" in to_text or "Lukman" in to_text or 'lukma' in to_text:
            print("your name is called.")
            print("Vibrator is on now for 2seconds")
        else:
            print("unknown name")

    except UnknownValueError:
        print("Unable to recognize")

