import speech_recognition as sr
import pyttsx3
import os
import webbrowser
from utils.actions import handle_command

# Initialize the TTS engine
engine = pyttsx3.init(driverName='sapi5')  # for Windows


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable.")
        return ""

def main():
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        if 'exit' in command or 'quit' in command:
            speak("Goodbye!")
            break
        handle_command(command, speak)

if __name__ == "__main__":
    main()
