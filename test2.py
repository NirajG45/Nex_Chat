import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

# -----------------------------------------------
# Initialize Recognizer and TTS Engine
# -----------------------------------------------
listener = sr.Recognizer()
engine = pyttsx3.init()

# Voice configuration
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 170)

# -----------------------------------------------
# Text-to-speech function
# -----------------------------------------------
def engine_speak(text):
    print(f"Nex: {text}")
    engine.say(text)
    engine.runAndWait()

# -----------------------------------------------
# Function to capture voice command
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
                print(f"User Command (voice): {command}")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError:
        print("Speech recognition service unavailable.")
    except Exception as e:
        print(f"Error: {e}")
    return command

# -----------------------------------------------
# Text input fallback
# -----------------------------------------------
def text_input():
    command = input("\nType your command here: ").lower()
    if 'nex' in command:
        command = command.replace('nex', '').strip()
    print(f"User Command (text): {command}")
    return command

# -----------------------------------------------
# Core assistant logic
# -----------------------------------------------
def process_command(command):
    if 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            engine_speak(f"Playing {song} on YouTube.")
            pywhatkit.playonyt(song)
        else:
            engine_speak("Please say or type the song name clearly.")

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
                engine_speak("There are multiple results for that name. Please be more specific.")
            except wikipedia.exceptions.PageError:
                engine_speak("I couldn’t find any information about that.")
        else:
            engine_speak("Please specify the name you want to know about.")

    elif 'stop' in command or 'exit' in command or 'quit' in command or 'goodbye' in command:
        engine_speak("Goodbye! Have a nice day.")
        return False

    elif command == "":
        engine_speak("I didn’t catch that, please try again.")

    else:
        engine_speak("I could not understand your command.")
    return True

# -----------------------------------------------
# Main Program Loop
# -----------------------------------------------
def main():
    engine_speak("Hello, I am Nex. Would you like to use voice or text mode?")
    print("\nChoose input mode:")
    print("1. Voice Command")
    print("2. Text Command")

    mode = input("\nEnter 1 for voice or 2 for text: ").strip()
    if mode not in ['1', '2']:
        print("Invalid input. Defaulting to voice mode.")
        mode = '1'

    running = True
    while running:
        if mode == '1':
            command = user_commands()
        else:
            command = text_input()

        # If voice mode fails to get a command, offer text fallback
        if command == "" and mode == '1':
            print("No voice detected. Switching to text mode temporarily.")
            command = text_input()

        running = process_command(command)

    engine_speak("Shutting down now.")

# -----------------------------------------------
# Entry point
# -----------------------------------------------
if __name__ == "__main__":
    main()
