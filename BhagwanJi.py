import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import subprocess
import requests
import json
import threading
import time

from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException, DetectorFactory
import pyttsx3
engine = pyttsx3.init()
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[1].id)
listener=sr.Recognizer()

DetectorFactory.seed = 0
last_command_language = "en"

# API Keys - Replace with your own keys
OPENWEATHER_API_KEY = "2db87f485678655926e4592c408fff59"  # Get from https://openweathermap.org/api
NEWS_API_KEY = "725d0cb53af64c8397607ff2fdcce59d"  # Get from https://newsapi.org/

# Utility translation helper
def translate_text(text, target_lang):
    if not text:
        return text
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception:
        return text

# Function for Bhagwan Ji to say what we say
def talk(text, lang_override=None):
    global last_command_language
    target_lang = lang_override or last_command_language or "en"
    spoken_text = text
    if target_lang.startswith("hi"):
        spoken_text = translate_text(text, "hi")
    engine.say(spoken_text)
    engine.runAndWait()


def normalize_command(raw_text):
    if not raw_text:
        return "", None
    text = raw_text.strip()
    if not text:
        return "", None
    detected_lang = None
    translated_text = text
    try:
        detected_lang = detect(text)
    except LangDetectException:
        detected_lang = None
    if detected_lang and detected_lang != "en":
        translated_text = translate_text(text, "en")
    normalized = translated_text.lower()
    if normalized.startswith("bhagwan ji"):
        normalized = normalized.replace("bhagwan ji", "", 1).strip()
    return normalized, detected_lang


# Fallback when Bhagwan Ji can't hear clearly
def prompt_text_command():
    """Fallback to typed command when voice input fails."""
    try:
        typed_input = input("Bhagwan Ji couldn't hear you clearly. Type your request: ")
        normalized, lang = normalize_command(typed_input)
        if normalized:
            print(f"Typed command recognized: {normalized}")
        update_last_command_language(lang)
        return normalized
    except EOFError:
        return ""


def update_last_command_language(lang):
    global last_command_language
    if lang:
        last_command_language = lang


def calculate(expression):
    """Safely evaluate basic math expressions"""
    try:
        # Remove any potentially dangerous characters
        allowed_chars = "0123456789+-*/(). "
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"The result is {result}"
        else:
            return "Sorry, I can only handle basic math operations"
    except Exception as e:
        return "Sorry, I couldn't calculate that"


def get_weather(city):
    """Get weather information for a city"""
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + OPENWEATHER_API_KEY + "&q=" + city + "&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]

            weather_info = f"The temperature in {city} is {temperature} degrees Celsius with {description}. Humidity is {humidity} percent."
            return weather_info
        else:
            return "City not found"
    except Exception as e:
        return "Unable to get weather information"


def get_news():
    """Get top news headlines"""
    try:
        base_url = "https://newsapi.org/v2/top-headlines?"
        complete_url = base_url + "country=us&apiKey=" + NEWS_API_KEY
        response = requests.get(complete_url)
        data = response.json()

        if data["status"] == "ok":
            articles = data["articles"][:5]  # Get top 5 headlines
            headlines = []
            for i, article in enumerate(articles, 1):
                headlines.append(f"Headline {i}: {article['title']}")
            return "Here are the top news headlines: " + ". ".join(headlines)
        else:
            return "Unable to fetch news"
    except Exception as e:
        return "Unable to get news information"


def set_reminder(message, seconds):
    """Set a reminder after specified seconds"""
    def reminder():
        time.sleep(seconds)
        talk(f"Reminder: {message}")
    
    thread = threading.Thread(target=reminder)
    thread.daemon = True
    thread.start()
    talk(f"Reminder set for {seconds} seconds from now")


def bhagwanji_command():
    # Speech Recognition part
    try:
        with sr.Microphone() as source:
            print("Listening... (say 'Bhagwan Ji' followed by your command)")
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=15, phrase_time_limit=8)
            command = listener.recognize_google(voice)
            if command:
                normalized, lang = normalize_command(command)
                print(f"Command recognized: {normalized}")
                update_last_command_language(lang)
                return normalized
    except sr.WaitTimeoutError:
        print("Listening timed out")
    except sr.UnknownValueError:
        print("Could not understand audio")
        talk("Sorry, I didn't catch that. Could you repeat?")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        talk("Sorry, I'm having trouble with speech recognition")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Fallback to typed command
    fallback = prompt_text_command()
    return fallback

# Function for Bhagwan Ji to DO what we say
def run_bhagwanji():
    command = bhagwanji_command()
    if not command:
        return True  # Continue listening

    print(f"Processing command: {command}")

    if "play" in command:
        song = command.replace("play", "")
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        print(time)
        talk("Current Time is " + time)

    elif "who is" in command or "what is" in command or "tell me about" in command:
        try:
            topic = command.replace("who is", "").replace("what is", "").replace("tell me about", "")
            info = wikipedia.summary(topic, 2)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("I couldn't find information about that.")
        except Exception as e:
            talk("Sorry, I couldn't retrieve that information.")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif "weather" in command:
        if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY.startswith("YOUR_"):
            talk("Please set up your OpenWeather API key first")
        else:
            city = command.replace("weather", "").replace("in", "").strip()
            if not city:
                city = "your location"  # Default city
            weather_info = get_weather(city)
            print(weather_info)
            talk(weather_info)

    elif "open" in command:
        if "website" in command or "site" in command:
            website = command.replace("open", "").replace("website", "").replace("site", "").strip()
            if website:
                if not website.startswith("http"):
                    website = "https://" + website
                talk(f"Opening {website}")
                webbrowser.open(website)
            else:
                talk("Please specify a website to open")
        else:
            # Try to open applications
            app = command.replace("open", "").strip()
            try:
                if "notepad" in app or "text editor" in app:
                    subprocess.run(["notepad.exe"])
                    talk("Opening Notepad")
                elif "calculator" in app:
                    subprocess.run(["calc.exe"])
                    talk("Opening Calculator")
                elif "command prompt" in app or "cmd" in app:
                    subprocess.run(["cmd.exe"])
                    talk("Opening Command Prompt")
                elif "explorer" in app or "file explorer" in app:
                    subprocess.run(["explorer.exe"])
                    talk("Opening File Explorer")
                else:
                    talk(f"Sorry, I don't know how to open {app}")
            except Exception as e:
                talk(f"Sorry, I couldn't open {app}")

    elif "search" in command:
        query = command.replace("search", "").strip()
        if query:
            talk(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            talk("What would you like to search for?")

    elif "calculate" in command or "math" in command or "compute" in command:
        expression = command.replace("calculate", "").replace("math", "").replace("compute", "").strip()
        if expression:
            result = calculate(expression)
            print(result)
            talk(result)
        else:
            talk("What would you like me to calculate?")

    elif "news" in command or "headlines" in command:
        if not NEWS_API_KEY or NEWS_API_KEY.startswith("YOUR_"):
            talk("Please set up your News API key first")
        else:
            news_info = get_news()
            print(news_info)
            talk(news_info)

    elif "remind" in command or "reminder" in command:
        # Simple reminder parsing - expects format like "remind me to [message] in [number] seconds/minutes"
        try:
            if "in" in command:
                parts = command.split("in")
                message_part = parts[0].replace("remind", "").replace("reminder", "").replace("me to", "").strip()
                time_part = parts[1].strip()
                
                # Parse time
                if "minute" in time_part:
                    minutes = int(time_part.replace("minutes", "").replace("minute", "").strip())
                    seconds = minutes * 60
                elif "second" in time_part:
                    seconds = int(time_part.replace("seconds", "").replace("second", "").strip())
                else:
                    seconds = int(time_part.strip())
                
                set_reminder(message_part, seconds)
            else:
                talk("Please specify when you want to be reminded. For example: 'remind me to drink water in 5 minutes' ")
        except Exception as e:
            talk("Sorry, I couldn't set that reminder. Try saying something like 'remind me to drink water in 5 minutes'")

    elif "hello" in command or "hi" in command or "hey" in command:
        talk("Namaste! Bhagwan Ji here. How can I bless you today?")

    elif "how are you" in command:
        talk("I am serene and ever-present. How may I assist you?")

    elif "thank you" in command or "thanks" in command:
        talk("You are most welcome. Stay blessed!")

    elif "goodbye" in command or "bye" in command or "stop" in command:
        talk("Goodbye! May blessings be with you always!")
        return False  # Exit the loop

    else:
        talk("I did not fully grasp that. You can ask Bhagwan Ji to play music, tell time, get weather, or search for guidance.")

    return True  # Continue the loop

# Main loop to keep the assistant running
def main():
    talk("Namaste, I'm Bhagwan Ji, your spiritual assistant. How can I guide you today?")
    while True:
        if not run_bhagwanji():
            break

if __name__ == "__main__":
    main()