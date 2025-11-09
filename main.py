import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import warnings


warnings.filterwarnings("ignore", message="pkg_resources is deprecated")


recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi="3b05a3c47c7946a4ba39eb87c339405c"



def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    
    elif "open ai" in c.lower():
        webbrowser.open("https://chatgpt.com")
    
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    
    elif "open spotify" in c.lower():
        webbrowser.open("https://spotify.com")
        

    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=3b05a3c47c7946a4ba39eb87c339405c")
                
        if r.status_code == 200:
              # Check if request was successful
            data = r.json() 
             # Convert response to Python dict
            articles = data.get('articles', []) 



             # Extract list of articles
            if not articles:
                speak("Sorry, I couldn't find any news right now.")
            else:
                speak("Here are the top headlines.")
                for article in articles[:5]:  # only top 5
                    speak(article['title'])

        else:
            speak(f"Could not fetch news. Status code {r.status_code}")

            print("Top Headlines:\n")
            for article in articles:
                speak(article['title'])

if __name__=="__main__":
    speak("Initializing Jarvis.... ")
    while True:

        # Listen for this wake word "jarvis" 
        # obtain audio from the microphone
        r = sr.Recognizer()
       
        print("Recognizing")
       

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)

            word=r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                # Listen for command  

                with sr.Microphone() as source:
                    print("Jarvis Activate")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)
        
        except Exception as e:
            print("Error; {0}".format(e))
            