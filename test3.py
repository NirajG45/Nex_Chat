import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import threading

# -----------------------------------------------
# Setup speech engine
# -----------------------------------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

listener = sr.Recognizer()

# -----------------------------------------------
# Speak Function
# -----------------------------------------------
def engine_speak(text):
    output_text.insert(tk.END, f"Nex: {text}\n")
    output_text.see(tk.END)
    engine.say(text)
    engine.runAndWait()

# -----------------------------------------------
# Voice Command Function
# -----------------------------------------------
def listen_command():
    try:
        with sr.Microphone() as source:
            engine_speak("Listening... Speak now.")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if 'nex' in command:
                command = command.replace('nex', '').strip()
                output_text.insert(tk.END, f"You (voice): {command}\n")
                process_command(command)
            else:
                engine_speak("Please say 'Nex' before your command.")
    except Exception as e:
        engine_speak("Sorry, I couldn't understand. Try again.")

# -----------------------------------------------
# Text Command Function
# -----------------------------------------------
def handle_text_command():
    command = text_input.get().lower().strip()
    text_input.delete(0, tk.END)
    if command == "":
        engine_speak("Please type a command.")
        return
    if 'nex' in command:
        command = command.replace('nex', '').strip()
    output_text.insert(tk.END, f"You (text): {command}\n")
    process_command(command)

# -----------------------------------------------
# Core Command Processing
# -----------------------------------------------
def process_command(command):
    try:
        if 'play' in command:
            song = command.replace('play', '').strip()
            if song:
                engine_speak(f"Playing {song} on YouTube.")
                pywhatkit.playonyt(song)
            else:
                engine_speak("Please specify a song name.")
        
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            engine_speak(f"The current time is {current_time}.")

        elif 'who is' in command:
            name = command.replace('who is', '').strip()
            if name:
                try:
                    info = wikipedia.summary(name, 1)
                    output_text.insert(tk.END, f"Info: {info}\n")
                    engine_speak(info)
                except wikipedia.exceptions.DisambiguationError:
                    engine_speak("There are multiple results, please be specific.")
                except wikipedia.exceptions.PageError:
                    engine_speak("I couldn’t find any information about that.")
            else:
                engine_speak("Please specify a name.")
        
        elif 'stop' in command or 'exit' in command or 'quit' in command or 'goodbye' in command:
            engine_speak("Goodbye! Have a nice day.")
            window.after(1500, window.destroy)

        else:
            engine_speak("I could not understand your command.")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}\n")
        engine_speak("Something went wrong.")

# -----------------------------------------------
# Threaded Voice Function (so GUI doesn't freeze)
# -----------------------------------------------
def start_listening_thread():
    thread = threading.Thread(target=listen_command)
    thread.start()

# -----------------------------------------------
# GUI Setup
# -----------------------------------------------
window = tk.Tk()
window.title("Nex Voice Assistant")
window.geometry("650x480")
window.resizable(False, False)
window.configure(bg="#1E1E1E")

# Title Label
title_label = tk.Label(window, text="Nex Voice Assistant", font=("Arial", 20, "bold"), bg="#1E1E1E", fg="white")
title_label.pack(pady=10)

# Output Display Box
output_text = scrolledtext.ScrolledText(window, width=70, height=18, bg="#252526", fg="white", font=("Consolas", 11))
output_text.pack(pady=10)
output_text.insert(tk.END, "Nex: Hello! I am Nex. How can I help you?\n")

# Text Input Field
text_input = tk.Entry(window, width=50, font=("Arial", 12))
text_input.pack(side=tk.LEFT, padx=20, pady=10)

# Buttons
btn_listen = tk.Button(window, text="🎙️ Listen", command=start_listening_thread, bg="#0078D7", fg="white", font=("Arial", 12), width=12)
btn_listen.pack(side=tk.LEFT, padx=5)

btn_send = tk.Button(window, text="💬 Send", command=handle_text_command, bg="#0078D7", fg="white", font=("Arial", 12), width=12)
btn_send.pack(side=tk.LEFT, padx=5)

# Run the main window loop
window.mainloop()
