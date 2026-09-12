import os
import datetime
import webbrowser
import urllib.parse
import speech_recognition as sr
import pyttsx3
import pyautogui
import wikipedia

from dotenv import load_dotenv
from openai import OpenAI


# =========================
# SETTINGS
# =========================

NAME = "Atharva"

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

sleep_mode = False

recognizer = sr.Recognizer()


# =========================
# SPEAK
# =========================

def speak(text):
    print("Jarvis:", text)

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Voice error:", e)


# =========================
# LISTEN
# =========================

def listen():
    try:
        with sr.Microphone() as source:

            print("Listening...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You:", text)

        return text.lower().strip()

    except sr.WaitTimeoutError:
        return ""

    except sr.UnknownValueError:
        print("Could not understand.")
        return ""

    except sr.RequestError:
        speak("Internet connection problem.")
        return ""

    except Exception as e:
        print("Microphone error:", e)
        return ""


# =========================
# AI BRAIN
# =========================

def ask_ai(question):

    if not client:
        return (
            "My AI brain is not connected yet. "
            "Please add your OpenAI API key in the .env file."
        )

    try:

        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=(
                "You are Jarvis, Atharva's personal AI assistant. "
                "Answer naturally and helpfully. "
                "Keep normal answers concise because your answer "
                "will be spoken aloud. "
                "If Atharva asks for a detailed explanation, "
                "provide a detailed answer."
            ),
            input=question
        )

        return response.output_text

    except Exception as e:

        print("AI error:", e)

        return (
            "Sorry Atharva, I could not connect to my AI brain right now."
        )


# =========================
# SEARCH GOOGLE
# =========================

def google_search(query):

    url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

    webbrowser.open(url)


# =========================
# SEARCH YOUTUBE
# =========================

def youtube_search(query):

    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote_plus(query)
    )

    webbrowser.open(url)


# =========================
# CLEAN WAKE WORD
# =========================

def remove_wake_words(command):

    wake_words = [
        "hey jarvis",
        "hello jarvis",
        "hey jarvish",
        "hello jarvish",
        "jarvis",
        "jarvish"
    ]

    for word in wake_words:
        command = command.replace(word, "")

    return command.strip()


# =========================
# MAIN
# =========================

def main():

    global sleep_mode

    speak(
        f"Jarvis online {NAME}. "
        "I am ready and listening."
    )

    while True:

        command = listen()

        if not command:
            continue


        # =========================
        # SLEEP MODE
        # =========================

        if sleep_mode:

            if (
                "wake up jarvis" in command
                or "wake up jarvish" in command
                or "hey jarvis" in command
                or "hello jarvis" in command
            ):

                sleep_mode = False
                speak("I am awake, Atharva.")

            continue


        # Remove wake word

        command = remove_wake_words(command)

        if not command:
            speak("Yes Atharva?")
            continue


        # =========================
        # HELLO
        # =========================

        if command in ["hello", "hi", "hey"]:

            speak("Hello Atharva. How can I help you?")

            continue


        # =========================
        # WHO ARE YOU
        # =========================

        if "who are you" in command:

            speak(
                "I am Jarvis, your personal assistant, "
                "made by Atharva."
            )

            continue


        # =========================
        # TIME
        # =========================

        if "time" in command:

            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )

            speak(f"The time is {current_time}.")

            continue


        # =========================
        # DATE
        # =========================

        if "date" in command:

            current_date = datetime.datetime.now().strftime(
                "%d %B %Y"
            )

            speak(f"Today is {current_date}.")

            continue


        # =========================
        # OPEN GOOGLE
        # =========================

        if "open google" in command:

            speak("Opening Google.")

            webbrowser.open(
                "https://www.google.com"
            )

            continue


        # =========================
        # OPEN YOUTUBE
        # =========================

        if "open youtube" in command:

            speak("Opening YouTube.")

            webbrowser.open(
                "https://www.youtube.com"
            )

            continue


        # =========================
        # OPEN WHATSAPP
        # =========================

        if "open whatsapp" in command:

            speak("Opening WhatsApp.")

            webbrowser.open(
                "https://web.whatsapp.com"
            )

            continue


        # =========================
        # OPEN CHROME
        # =========================

        if "open chrome" in command:

            speak("Opening Chrome.")

            os.system("start chrome")

            continue


        # =========================
        # GOOGLE SEARCH
        # =========================

        if command.startswith("search"):

            query = command.replace(
                "search",
                "",
                1
            ).strip()

            if not query:

                speak("What should I search?")

                query = listen()

            if query:

                speak(f"Searching for {query}.")

                google_search(query)

            continue


        # =========================
        # YOUTUBE SEARCH
        # =========================

        if command.startswith("search youtube"):

            query = command.replace(
                "search youtube",
                "",
                1
            ).strip()

            if not query:

                speak("What should I search on YouTube?")

                query = listen()

            if query:

                speak(f"Searching YouTube for {query}.")

                youtube_search(query)

            continue


        # =========================
        # PLAY ON YOUTUBE
        # =========================

        if command.startswith("play"):

            query = command.replace(
                "play",
                "",
                1
            ).strip()

            if not query:

                speak("What should I play?")

                query = listen()

            if query:

                speak(f"Searching YouTube for {query}.")

                youtube_search(query)

            continue


        # =========================
        # CLOSE TAB
        # =========================

        if (
            "close tab" in command
            or "close this tab" in command
        ):

            speak("Closing the current tab.")

            pyautogui.hotkey(
                "ctrl",
                "w"
            )

            continue


        # =========================
        # CLOSE WINDOW
        # =========================

        if (
            "close window" in command
            or "close this window" in command
        ):

            speak("Closing the current window.")

            pyautogui.hotkey(
                "alt",
                "f4"
            )

            continue


        # =========================
        # SLEEP JARVIS
        # =========================

        if (
            "shutdown jarvis" in command
            or "shut down jarvis" in command
            or "shutdown jarvish" in command
            or "shut down jarvish" in command
        ):

            speak(
                "Going to sleep. "
                "Say wake up Jarvis when you want me again."
            )

            sleep_mode = True

            continue


        # =========================
        # CANCEL SHUTDOWN
        # =========================

        if (
            "cancel shutdown" in command
            or "cancel shut down" in command
        ):

            os.system("shutdown /a")

            speak("Shutdown cancelled.")

            continue


        # =========================
        # SHUTDOWN LAPTOP
        # =========================

        if (
            "shutdown laptop" in command
            or "shut down laptop" in command
        ):

            speak(
                "Shutting down your laptop."
            )

            os.system(
                "shutdown /s /t 5"
            )

            break


        # =========================
        # RESTART LAPTOP
        # =========================

        if (
            "restart laptop" in command
            or "restart computer" in command
        ):

            speak(
                "Restarting your laptop."
            )

            os.system(
                "shutdown /r /t 5"
            )

            break


        # =========================
        # WIKIPEDIA
        # =========================

        if (
            command.startswith("who is")
            or command.startswith("what is")
        ):

            try:

                speak("Let me check.")

                result = wikipedia.summary(
                    command,
                    sentences=2
                )

                speak(result)

            except:

                speak(
                    "I could not find a Wikipedia result. "
                    "Let me ask my AI brain."
                )

                answer = ask_ai(command)

                speak(answer)

            continue


        # =========================
        # AI BRAIN
        # =========================

        speak("Let me think.")

        answer = ask_ai(command)

        speak(answer)


# =========================
# START JARVIS
# =========================

if __name__ == "__main__":
    main()
