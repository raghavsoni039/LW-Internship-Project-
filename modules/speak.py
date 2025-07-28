import pyttsx3
def speak(text):
    speaker=pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()
