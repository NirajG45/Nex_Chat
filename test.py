import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

# Initialize recognizer and TTS engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Configure voice settings
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice (change index if needed)
engine.setProperty('rate', 170)

# -----------------------------------------------
# Function: Speak text aloud
# -----------------------------------------------
def engine_speak(text):
    print(f"Nex: {text}")
    engine.say(text)
    engine.runAndWait()

# -----------------------------------------------
# Function: Listen and recognize user command
# -----------------------------------------------
def user_commands():
    command = ""
    try:
        with sr.Microphone() as source:
            print("\nListening... Speak now.")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if 'nex' in command:
                command = command.replace('nex', '').strip()
                print(f"User Command: {command}")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
    except Exception as e:
        print(f"Error: {e}")
    return command

# -----------------------------------------------
# Function: Execute recognized commands
# -----------------------------------------------
def run_nex():
    command = user_commands()

    if 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            engine_speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        else:
            engine_speak("Please say the song name clearly.")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        engine_speak(f"The current time is {current_time}.")

    elif 'who is' in command:
        name = command.replace('who is', '').strip()
        if name:
            try:
                info = wikipedia.summary(name, 1)
                print(f"Info: {info}")
                engine_speak(info)
            except wikipedia.exceptions.DisambiguationError:
                engine_speak("There are multiple results for that name, please be specific.")
            except wikipedia.exceptions.PageError:
                engine_speak("I couldn’t find any information about that.")
        else:
            engine_speak("Please say the name you want to know about.")

    elif 'stop' in command or 'exit' in command or 'quit' in command or 'goodbye' in command:
        engine_speak("Goodbye! Have a nice day.")
        return False  # Stop loop

    elif command == "":
        engine_speak("I didn’t catch that, please try again.")

    else:
        engine_speak("I could not understand your command.")
    return True

# -----------------------------------------------
# Main loop
# -----------------------------------------------
def main():
    engine_speak("Hello, I am Nex. How can I help you?")
    running = True
    while running:
        running = run_nex()

    engine_speak("Shutting down now.")

# -----------------------------------------------
# Run program
# -----------------------------------------------
if __name__ == "__main__":
    main()
