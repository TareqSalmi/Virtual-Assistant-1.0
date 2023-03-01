import speech_recognition as sr
import datetime
import pyttsx3
import requests
import json
import os


r = sr.Recognizer()


engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("How can I help you?")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return None


def execute_command(text):
    if "what time is it" in text:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%I:%M %p')}.")
    elif "search for" in text:
        search_query = text.replace("search for", "")
        speak(f"Searching for {search_query}...")
       
    elif "play music" in text:
        speak("What song would you like to listen to?")
        song = listen()
        speak(f"Playing {song}...")
    elif "set a reminder" in text:
        speak("What would you like me to remind you about?")
        reminder_text = listen()
        speak("When should I remind you?")
        reminder_time = listen()
        speak(f"Okay, I'll remind you to {reminder_text} at {reminder_time}.")
    elif "what's the weather like" in text:
        api_key = "your_api_key_here"
        url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric"
        response = requests.get(url)
        data = json.loads(response.text)
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The temperature in London is {temperature} degrees Celsius with {description}.")
    elif (start := text.split(' ')[0]) in {
        "open",
        "start",
        "run",
    }:
        program = text.replace(start, "")
        os.system(f"start {program}")
        speak(f"Starting {program}")

    else:
        speak("I'm sorry, I didn't understand what you said. Could you please repeat it?")
while True:
    text = listen()
    if text:
        execute_command(text.lower())
