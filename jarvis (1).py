import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import smtplib
import os
import subprocess
from email.message import EmailMessage
import getpass
import pyowm
import string 
import random
import string 
import matplotlib 
import matplotlib.pyplot as plt

# dependencies 
# pip install pyowm
# pip install SpeechRecognition
# pip install wikipedia
# pip install pyttsx3
# pip install --user pywin 
# pywin install pyaudio 

username = getpass.getuser()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<16:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Jarvis. Please tell me, how may I help you?")  
    print('''Here is a list of things I can do:
    1. Open websites like google, netflix, whatsapp etc.
    2. Open apps in your computer
    3. Tell jokes
    4. Play Music
    5. Give the weather forecast in any desired city
    6. Get information from wikipedia
    7. Generate a random password 
    8. Play rock paper scissors

    ''')     

def Commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:    
        print("Say that again please...")  
        return "None"
    return query

def chrome(chrome_path, url):
    webbrowser.get(using = chrome_path).open(url)
    
def default(url):
    webbrowser.open(url)

if __name__ == "__main__":
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    end = ("quit", "close", "leave","bye")
    greet()
    done= False
    while not done:
        url = ""
        query = Commands().lower()
        for val in end:
            if val == query:
                speak("Have a good day.")
                done = True  

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'youtube' in query:
            url = "youtube.com"

        elif 'google' in query:
            url = "google.com"

        elif 'netflix' in query:
            url = "netflix.com" 

        elif 'who are you' in query:
            speak("I am a virtual assistant developed and programmed by the Cornerstone team")



        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"The time is {strTime}")
        
        # elif 'plot' or 'graph' in query:
        #     speak("I can only plot linear regression graphs. Please enter the x axis values below")
        #     x=list(map(int,input("X Values").split(","))) 
        #     speak("Please enter the y axis values below")
        #     y=list(map(int,input("Y Values").split(","))) 
        #     if len(x)!= len(y):
        #         while len(x)!= len(y):
        #             if len(x)> len(y):
        #                 x.pop()
        #             else: 
        #                 y.pop()
        #     plt.plot(x, y)
        #     speak("Please enter the names of x and y labels below")
        #     xlab= input("X label: ")
        #     ylab= input("Y label: ")
        #     plt.xlabel(xlab)
        #     plt.ylabel(ylab)
        #     speak("Enter the name of your graph")
        #     title= input("Name: ")
        #     plt.title(title)
        #     plt.show()
        elif 'calculator' in query:
            subprocess.Popen('C:\\Windows\\System32\\calc.exe')

        elif 'open teams' in query: 
            try:
                subprocess.Popen(f'C:/Users/{username}/AppData/Local/Microsoft/Teams/Update.exe --processStart "Teams.exe"')
            except:
                try:
                    subprocess.Popen(f'C:/Users/{username}/Downloads/Teams_windows_x64.exe')
                except:
                    try:
                        subprocess.Popen(f'C:/Users/{username.replace(" ", "")}/AppData/Local/Microsoft/Teams/Update.exe --processStart "Teams.exe"')
                    except:
                        subprocess.Popen(f'C:/Users/{username.replace(" ", "")}/Downloads/Teams_windows_x64.exe')

        elif 'udemy' in query:
            url = "udemy.com" 
        
        if url:
            try:
                chrome(chrome_path, url)
            except:
                default(url)
        elif 'weather' in query:
            owm = pyowm.OWM('bec01343c8004631bd4c57dd2ea78a8b')
            speak("Please enter the name of the city you want the weather for:")
            city= input("City Name:")
            loc = owm.weather_manager().weather_at_place(city)
            weather = loc.weather
            # temperature
            temp = weather.temperature(unit='celsius')
            tem=(temp['temp'])
            speak(f"The temperature in {city} is {tem} degree celsius")
        elif 'password' in query:
            lowlet=string.ascii_lowercase
            letters= string.ascii_letters
            uplet= string.ascii_uppercase
            punc= string.punctuation
            lst= []
            lst.extend(list(lowlet))
            lst.extend(list(letters))
            lst.extend(list(uplet))
            lst.extend(list(punc))
            random.shuffle(lst)
            speak("Please enter the required password length below")
            length= int(input("Enter the required password length: \n"))
            password= lst[0:length]
            speak("Your new password has been generated")
            print(f'Password: {"".join(lst[0:length])}')
            
        
        # ideas --> spotify, Jarvis? Might need our own name yk, directly query google, jokes/easter eggs if long pause or something 

        
        


        
