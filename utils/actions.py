import os
import webbrowser
import requests
import datetime as dt
import pyjokes
import pywhatkit
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


def handle_command(command, speak):
    command = command.lower()

    if 'open youtube' in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")

    elif 'open google' in command:
        webbrowser.open("https://google.com")
        speak("Opening Google.")

    elif 'open spotify' in command:
        os.system("start spotify")
        speak("Launching Spotify.")

    elif 'shutdown' in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")

    elif 'time' in command:
        now = dt.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    elif 'date' in command:
        today = dt.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}.")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif 'take a note' in command or 'write a note' in command:
        speak("What should I write?")
        from assistant import listen  # import here to avoid circular import
        note = listen()
        if note:
            with open("voice_notes.txt", "a") as f:
                f.write(f"{dt.datetime.now()}: {note}\n")
            speak("Note saved.")

    elif 'search for' in command:
        search_term = command.replace("search for", "").strip()
        if search_term:
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
            speak(f"Searching Google for {search_term}")
        else:
            speak("What do you want me to search for?")
    elif 'weather' in command:
        speak("Which city?")
        from assistant import listen
        city = listen()
        if city:
            try:
                api_key = "45a7562604d0960a7932dcbdf4868762"  # replace with your key
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                if data.get("cod") != "404":
                    main = data["main"]
                    weather = data["weather"][0]["description"]
                    temp = main["temp"]
                    weather_text = f"The weather in {city} is {weather} with a temperature of {temp} degrees Celsius."
                    print("Speaking:", weather_text)
                    speak(weather_text)
                else:
                    speak("City not found.")
            except Exception as e:
                print("Weather error:", e)
                speak("Sorry, I couldn’t fetch the weather.")
    
    elif 'send whatsapp message' in command:
        speak("Tell the 10-digit phone number without country code.")
        from assistant import listen
        number = listen().replace(" ", "")
        phone = f"+91{number}"  # Assuming India. Change prefix if needed.

        speak("What message should I send?")
        message = listen()

        if phone and message:
            try:
                from datetime import datetime
                now = datetime.now()
                hour = now.hour
                minute = now.minute + 2  # Send 2 minutes from now

                speak(f"Sending your WhatsApp message to {phone} in 2 minutes.")
                pywhatkit.sendwhatmsg(phone, message, hour, minute)
            except Exception as e:
                print("WhatsApp error:", e)
                speak("Failed to send the message. Check WhatsApp Web.")

    elif 'volume up' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
        speak("Volume increased.")

    elif 'volume down' in command:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
        speak("Volume decreased.")

    elif 'increase brightness' in command:
        try:
            current = sbc.get_brightness()[0]
            sbc.set_brightness(min(current + 10, 100))
            speak("Brightness increased.")
        except Exception as e:
            print("Brightness error:", e)
            speak("Could not change brightness.")

    elif 'decrease brightness' in command:
        try:
            current = sbc.get_brightness()[0]
            sbc.set_brightness(max(current - 10, 0))
            speak("Brightness decreased.")
        except Exception as e:
            print("Brightness error:", e)
            speak("Could not change brightness.")
    else:
        speak("Sorry, I can't handle that command yet.")
    
