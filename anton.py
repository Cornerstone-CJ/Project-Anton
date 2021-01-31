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
import sqlite3
import re 
import pathlib
import sys 
from termcolor import colored
from pygame.locals import * 
import pygame
from sys import exit
from random import randrange
from typing import Dict, List, Set, Optional, Match

username = getpass.getuser()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# prep for jokes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "jokes_db.db")
joke_phrases = ["Alright this is one of my favorites", "Okay", "Try to not laugh at this one", "Here comes a funny one",
                "Alright"]
conn = sqlite3.connect(db_path)
cur = conn.cursor()

def anton_help():
    print('''Here is a list of things I can do:
    1. Open websites like google, netflix, whatsapp etc.
    2. Open apps in your computer like PyCharm and Calculator
    3. Tell jokes
    4. Play Music
    5. Give the weather forecast in any desired city
    6. Get information from wikipedia
    7. Generate a random password 
    8. Play rock paper scissors

    ''')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 16:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Anton. Please tell me, how may I help you? Just say help to see my features again.")
    anton_help()


def Commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(colored("Listening...", color="white"))
        r.pause_threshold = 1

        audio = r.listen(source)

    try:
        print(colored("Recognizing...", color="green"))    
        query = r.recognize_google(audio, language='en-in')
        print(colored(f"User said: {query}\n", color="cyan"))

    except:    
        print(colored("Please say that again...", color="red"))  
        return ""
    return query

# Rock Parer Scissors

def format_str(string: str) -> str:
    '''Uses bit operations to convert the first letter to uppercase'''
    chars: List[str] = list(string)
    chars[0] = chr(ord(chars[0]) & ~32)

    return "".join(chars) 


def play_human(values: set) -> Optional[str]:
    move = Commands().lower()
    if move == "quit":
        return None
    while move not in values:
        speak("Sorry can you say that again")
        move = Commands().lower()
        if move == "quit":
            return None
    return move 


def random_ai(values: list) -> str:
    index: int = randrange(3)

    return values[index]


def display(scores: List[int], val1: str, val2: str) -> None:
    print()
    print(f"Player 1 played {format_str(val1)}")
    print(f"Player 2 played {format_str(val2)}")
    print()
    print(colored(f"Player 1 -->  {scores[0]}     {scores[1]}  <-- Player 2", color="magenta"))


def display_gui(scores: List[int], val1: str, val2: str) -> None:
    pass 

def game(limit: int) -> None:

    speak('''To play the game say either rock, paper or scissors each round. 
    The winner is the first to reach the limit''')

    speak("You may begin")

    moves: Dict[str, str] = {
        "rock" : "scissors",
        "scissors" : "paper",
        "paper" : "rock"
    }

    moves_set: Set[str] = {v for v in moves}
    moves_list: List[str] = [v for v in moves]
  
    over: bool = False
    scores: list = [0,0]

    while not over:
        print()

        # player 1 
        val1: Optional[str] = play_human(moves_set) 
        if val1 is None:
            break  

        # player 2 
        val2: str = random_ai(moves_list)

        if moves[val1] == val2:
            scores[0] += 1
        elif moves[val2] == val1:
            scores[1] += 1

        # display scores 
        display(scores, val1, val2)
        display_gui(scores, val1, val2)

        # check if game over 
        if max(scores) == limit:
            over = True 

    print()

    if scores[0] > scores[1]:
        print(colored("Winner is player 1", color = "green"))
        speak("Game over. The winner is player 1") 
    elif scores[1] > scores[0]:
        print(colored("Winner is player 2", color = "green"))
        speak("Game over. The winner is player 2")
    else:
        print(colored("Draw!", color = "green"))
        speak("Game over. It is a draw")
    

def chrome(chrome_path, url):
    webbrowser.get(using=chrome_path).open(url)


def default(url):
    webbrowser.open(url)


if __name__ == "__main__":
    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    end = ("quit", "close", "leave", "bye")
    greet()
    done = False
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
            speak("I am Anton, a virtual assistant developed and programmed by the Cornerstone team")

        elif 'open pycharm' in query:
            try:
                codePath = "/Applications/PyCharm CE.app"
                os.startfile(codePath)
            except:
                try:
                    jetBrainDir = "C:/Program Files/JetBrains/"
                    jetbrainApps = os.listdir(jetBrainDir)
                    for f in jetbrainApps:
                        if "PyCharm" in f:
                            pycharmDir = os.path.join(jetBrainDir, f)
                            break
                    binDir = os.path.join(pycharmDir, "bin")
                    binFiles = os.listdir(binDir)
                    pycharmExecutablePattern = (r'pycharm[0-9]{2}.exe')
                    for f in binFiles:
                        if re.match(pycharmExecutablePattern, f):
                            absolutePyCharmDir = os.path.join(binDir, f)
                            break

                    os.startfile(absolutePyCharmDir)
                except:
                    print("Could not find path for PyCharm")
                    speak("Could not find path for PyCharm")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'graph' in query:
            speak('''I can only plot linear graphs.
            Seperate entries with a comma, 
            the first x should correspond to the first y and so on
            ''')
            speak("Please enter the x axis values below.")
            x = list(map(int, input("X Values: ").split(",")))
            speak("Please enter the y axis values below")
            y = list(map(int, input("Y Values: ").split(",")))
            if len(x) != len(y):
                while len(x) != len(y):
                    if len(x) > len(y):
                        x.pop()
                    else:
                        y.pop()

            plt.plot(x, y)
            speak("Please enter the names of x and y labels below")
            xlab = input("X label: ")
            ylab = input("Y label: ")
            plt.xlabel(xlab)
            plt.ylabel(ylab)
            speak("Enter the name of your graph")
            title = input("Name: ")
            plt.title(title)
            plt.show()

        elif 'calculator' in query:
            subprocess.Popen('C:\\Windows\\System32\\calc.exe')

        elif 'open teams' in query:
            try:
                subprocess.Popen(
                    f'C:/Users/{username}/AppData/Local/Microsoft/Teams/Update.exe --processStart "Teams.exe"')
            except:
                try:
                    subprocess.Popen(f'C:/Users/{username}/Downloads/Teams_windows_x64.exe')
                except:
                    try:
                        subprocess.Popen(
                            f'C:/Users/{username.replace(" ", "")}/AppData/Local/Microsoft/Teams/Update.exe --processStart "Teams.exe"')
                    except:
                        try:
                            subprocess.Popen(f'C:/Users/{username.replace(" ", "")}/Downloads/Teams_windows_x64.exe')
                        except:
                            print("could not find path")
                            speak("could not find path")

        elif "discord" in query:
            try:
                subprocess.Popen(f'C:/Users/{username}/AppData/Local/Discord/Update.exe --processStart Discord.exe')
            except:
                try:
                    subprocess.Popen(f'C:/Users/{username.replace(" ", "")}/AppData/Local/Discord/Update.exe --processStart Discord.exe')
                except:
                    print("could not find path for Discord")
                    speak("could not find path")

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
            city = input("City Name:")
            loc = owm.weather_manager().weather_at_place(city)
            weather = loc.weather
            # temperature
            temp = weather.temperature(unit='celsius')
            tem = (temp['temp'])
            speak(f"The temperature in {city} is {tem} degree celsius")

            # Password Generator

        elif 'password' in query:
            lowlet = string.ascii_lowercase
            letters = string.ascii_letters
            uplet = string.ascii_uppercase
            punc = string.punctuation
            lst = []
            lst.extend(list(lowlet))
            lst.extend(list(letters))
            lst.extend(list(uplet))
            lst.extend(list(punc))
            random.shuffle(lst)
            speak("Please enter the required password length below")
            length = int(input("Enter the required password length: \n"))
            password = lst[0:length]
            speak("Your new password has been generated")
            print(f'Password: {"".join(lst[0:length])}')

            # Play Music

        elif 'music' in query or 'play song' in query:
            curr_dir = os.path.dirname(os.path.abspath(__file__)) 
            music_dir = os.path.join(curr_dir, "songs/")
            # screen = pygame.display.set_mode((500, 500))
            
            x = os.listdir(music_dir)
            random.shuffle(x)
            a = music_dir + str(x[0])
            pygame.mixer.init()
            
            print(f"Now playing {x[0]}")
            pygame.mixer.music.load(a)
            pygame.mixer.music.play()
            
            
            running = True
            
            while True: 
                inp = input("Press 's' to stop, 'p' to pause 'u' to unpause and 'r' to rewind: \n")
                if inp=="s": 
                    pygame.mixer.music.stop()  
                    break
                elif inp=="p":
                    pygame.mixer.music.pause()
                elif inp=="u":
                    pygame.mixer.music.unpause()
                elif inp=="r":
                    pygame.mixer.music.rewind()

        # jokes
        elif "tell me a joke" in query or "jokes" in query or "joke" in query:
            speak(random.choice(joke_phrases))
            # INSERT INTO "main"."Jokes"("Id","Joke") VALUES (NULL,"Insert joke here");
            cur.execute('SELECT Joke From Jokes ORDER BY RANDOM() LIMIT 1')
            row = cur.fetchone()
            for r in row:
                speak(r)
                break


        # Rock Paper Scissors 

        elif "rock paper scissors" in query:
            speak("welcome, you can quit the game anytime by saying the command 'quit'")
            pattern = (r'([0-9]+){1}')
            speak("How many rounds would you like?")
            val = Commands()
            if val == "quit":
                continue
            match = re.match(pattern, val)
            while not match or match.group(0) == '0':
                speak("Please say a valid number of rounds")
                val = Commands()
                match = re.match(pattern, val)

            limit = int(match.group(0))

            game(limit)

            print()
        
        elif "help" in query: 
            anton_help()
            
        # stop listening (ignores when you say things that should be commands)

        elif "stop listening" in query:
            listening = False
            while not listening:
                new_query = Commands().lower()
                if "continue listening" in new_query or "resume listening" in new_query:
                    break 

    sys.exit()
    
        
