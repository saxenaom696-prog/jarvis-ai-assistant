import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import threading
import tkinter as tk
from tkinter import scrolledtext

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # speed
engine.setProperty('volume', 1.0)  # volume

# -------- SPEAK FUNCTION --------
def speak(text):
    """Speak and show Jarvis reply"""
    chat_box.config(state='normal')
    chat_box.insert(tk.END, f"Jarvis: {text}\n\n")
    chat_box.config(state='disabled')
    chat_box.yview(tk.END)
    engine.say(text)
    engine.runAndWait()

# -------- TAKE COMMAND FUNCTION --------
def take_command():
    """Take microphone input and return text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        chat_box.config(state='normal')
        chat_box.insert(tk.END, f"You: {query}\n")
        chat_box.config(state='disabled')
        chat_box.yview(tk.END)
    except Exception:
        speak("Sorry, I didn't catch that.")
        return "none"
    return query.lower()

# -------- BMI CALCULATOR --------
def calculate_bmi():
    """Ask for weight and height and calculate BMI"""
    speak("Sure sir, let's calculate your body mass index.")
    speak("Please tell me your weight in kilograms.")
    weight_text = take_command()

    try:
        weight = float(weight_text.split()[0])
    except:
        speak("Sorry, I couldn't understand your weight. Please say it again.")
        return

    speak("Now tell me your height in meters.")
    height_text = take_command()

    try:
        height = float(height_text.split()[0])
    except:
        speak("Sorry, I couldn't understand your height. Please say it again.")
        return

    bmi = round(weight / (height ** 2), 2)
    if bmi < 18.5:
        category = "underweight"
    elif 18.5 <= bmi < 25:
        category = "normal weight"
    elif 25 <= bmi < 30:
        category = "overweight"
    else:
        category = "obese"

    speak(f"Your body mass index is {bmi}. You are classified as {category}.")

# -------- PROCESS COMMAND --------
def process_command():
    query = take_command()

    if "time" in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {strTime}")

    elif "date" in query:
        strDate = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {strDate}")

    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open music" in query or "play music" in query:
        music_dir = "C:\\Users\\Public\\Music"  # Change if needed
        songs = os.listdir(music_dir)
        if songs:
            speak("Playing music")
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            speak("No music files found")

    elif "how are you" in query:
        speak("I'm fine, thank you. How about you?")

    elif "your name" in query:
        speak("I'm Jarvis, your personal assistant")

    elif "monday schedule" in query or "monday class" in query:
        speak("Here is your schedule for Monday.")
        speak("At 9:00 AM, you have Artifical Intelligence.")
        speak("At 9:45 AM, you have ADBMS.")
        speak("At 12:00 PM, you have Computer Science.")

    elif "calculate my bmi" in query or "bmi" in query:
        calculate_bmi()

    elif "exit" in query or "quit" in query or "stop" in query:
        speak("Goodbye! Have a nice day.")
        root.destroy()

    elif query == "none":
        pass

    else:
        speak("Sorry, I didn't understand that command.")

# -------- THREAD FOR LISTENING --------
def start_listening():
    """Start listening in a new thread (so GUI doesn’t freeze)"""
    thread = threading.Thread(target=process_command)
    thread.start()

# -------- GUI SETUP --------
root = tk.Tk()
root.title("Jarvis AI Assistant")
root.geometry("520x600")
root.config(bg="#1c1c1c")

title_label = tk.Label(root, text="🎙 Jarvis AI Assistant", font=("Arial", 18, "bold"),
                       bg="#1c1c1c", fg="#00ffcc")
title_label.pack(pady=10)

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=25, font=("Arial", 10))
chat_box.pack(padx=10, pady=10)
chat_box.config(state='disabled')

mic_button = tk.Button(root, text="🎤 Speak", font=("Arial", 14, "bold"),
                       bg="#00ffcc", fg="#1c1c1c", activebackground="#00e6b8",
                       command=start_listening)
mic_button.pack(pady=20)

# -------- STARTUP GREETING --------
speak("good morning sir ! I am Jarvis, your personal assistant. How can i help you?")
root.mainloop()
