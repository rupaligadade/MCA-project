import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import requests
import json
import sys

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Selecting a female voice

# ✅ Text-to-speech function
def talk(text):
    engine.say(text)
    engine.runAndWait()

# ✅ Weather function now returns string instead of printing
def weather(city):
    api_key = "2f192ed601337bc46cf188b08f6e189e"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    try:
        response = requests.get(complete_url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            temperature = y["temp"]
            pressure = y["pressure"]
            humidity = y["humidity"]
            weather_description = x["weather"][0]["description"]

            # Convert temperature from Kelvin to Celsius
            celsius = temperature - 273.15
            weather_info = (
                f"The temperature is {celsius:.2f} degrees Celsius, "
                f"pressure is {pressure} hPa, "
                f"humidity is {humidity}%, "
                f"and the weather is described as {weather_description}."
            )
            return weather_info
        else:
            return "City not found!"
    except Exception as e:
        return f"Error: {e}"

# ✅ Listening to command
def alexa_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                command = command.replace("alexa", "")
                print(f"Command recognized: {command}")
    except Exception as e:
        print(f"Error recognizing voice: {e}")
    return command

# ✅ Main control flow
def run_command():
    command = alexa_command()
    print(f"Final command: {command}")
    if "play" in command:
        song = command.replace("play", "")
        talk("Playing " + song)
        pywhatkit.playonyt(song)
    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        print(time)
        talk("Current time is " + time)
    elif "superstar" in command:
        person = command.replace("superstar", "")
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
    elif "joke" in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
    elif "weather" in command:
        talk("Please tell the name of the city")
        city = alexa_command()
        weather_info = weather(city)
        print(weather_info)
        talk(weather_info)
    elif "stop" in command:
        talk("Goodbye!")
        sys.exit()
    else:
        talk("I could not hear you properly. Please try again.")

# ✅ Start assistant
run_command()
