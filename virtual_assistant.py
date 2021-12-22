# Importing dependencies

import pyttsx3
import datetime
import requests
import speech_recognition as SR
import smtplib
from secrets import sender, password, receiver
import wikipedia
import webbrowser as browser
import pywhatkit
import clipboard
import pyjokes
import psutil
from nltk.tokenize import word_tokenize
import wolframalpha


# Setting engine for pyttsx3
engine = pyttsx3.init()


# Function to handle speech
def speak(message):
    engine.say(message)
    engine.runAndWait()


# Greeting user
def greetUser():
    hour = int(datetime.datetime.now().hour)
    if hour >= 5 and hour <= 12:
        speak("Good morning!")
    elif hour >= 13 and hour <= 15:
        speak("Good afternoon!")
    elif hour >= 16 and hour <= 21:
        speak("Good evening!")
    else:
        speak("Hope you're having a good night!")


# Welcome message
def welcomeUser():
    username = "Alex"
    speak(f"My name is Sam,your virtual assistant")
    speak(f'How may I assist you today,{username}?')
    engine.runAndWait()


# Retrieving current time
def getTime():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f'The time is ,{time}')
    engine.runAndWait()


# Get current date
def getDate():
    day = str(datetime.datetime.now().day)
    month = str(datetime.datetime.now().month)
    year = str(datetime.datetime.now().year)
    speak("Today's date is:")
    speak(day)
    speak(month)
    speak(year)
    engine.runAndWait()


# Handling send email function
def sendEmail(content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, content)
    server.close()

# Function to handle text input
def getUserCommand():
    query = input("Is there anything you would need?")
    return query

# Function to handle audio input
def getUserAudioCommand():
    r = SR.Recognizer()
    with SR.Microphone() as source:
        print("Listening.....")
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source, 10)

    try:
        print("Recognizing.....")
        data = r.recognize_google(audio)
        print(data)
    except Exception as e:
        print(e)
        speak("Please repeat your command")
        return "None"
    return data

# Function to handle google search queries
def searchGoogle():
    speak("What do you want to search for?")
    search = getUserAudioCommand()
    browser.open('https://www.google.com/search?q=' + search)

# Function to handle search weather functionalities
def getWeather(city):
    speak(f"Finding weather for{city}")
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=40e57335af4945dff62044440e27a6dc'
    try:
        res = requests.get(url)
        data = res.json()

        weather = data['weather'][0]['main']
        temperature = data['main']['temp']
        print(temperature)
        description = data['weather'][0]['description']
        temperature_celsius = round((temperature - 32) * (5 / 9))
        print(temperature_celsius)
        speak(f"Current temperature in{city} is{format(temperature_celsius)} celsius")
        speak(f"The weather is {format(description)}")

    except Exception as e:
        print(e)

# Function to handle retrieving news headlines
def getNews():
    news_API_KEY = "df460461df4b446d87408649205b57a7"
    main_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_API_KEY}'
    res = requests.get(main_url)
    data = res.json()
    articles = data["articles"]
    results = []
    for ar in articles:
        results.append(ar["title"])
    speak("Today's trending headlines are:")
    for i in range(10):
        speak(results[i])


def readText():
    text = clipboard.paste()
    speak(text)

# Function to handle getting CPU and battery usage details
def cpu():
    usage =str(psutil.cpu_percent())
    battery = psutil.sensors_battery()
    speak(f"CPU is at: {usage}")
    speak(f"Battery is at:{battery.percent}")

if __name__ == '__main__':

    greetUser()
    welcomeUser()
    wakeword = "sam"
    while True:
            query = getUserAudioCommand().lower()
            query = word_tokenize(query)
            print(query)
        # if wakeword in query:
            if 'time' in query:
                getTime()

            elif 'date' in query:
                getDate()

            elif 'email' in query:
                speak("What do you want to send?")
                try:
                    content = getUserAudioCommand()
                    sendEmail(content)
                    speak("Email has been sent successfully")
                    engine.runAndWait()
                except Exception as e:
                    print(e)
                    speak("Error occurred,failed to send email!")

            elif 'wikipedia' in query:
                speak("What would you like to know")
                search = getUserAudioCommand()
                result = wikipedia.summary(search, sentences=2)
                print(result)
                speak(str(result))

            elif 'search' in query:
                searchGoogle()

            elif 'youtube' in query:
                speak("What do you want to look up on youtube?")
                topic = getUserAudioCommand()
                pywhatkit.playonyt(topic)

            elif 'weather' in query:
                speak("Which city do you want to find the weather for?")
                city = getUserAudioCommand()
                getWeather(city)

            elif 'news' in query:
                getNews()

            elif 'read text' in query:
                readText()

            elif 'jokes' in query:
                speak(pyjokes.get_joke())

            elif 'reminder' in query:
                speak("What do you want me to remind you?")
                data = getUserAudioCommand()
                speak("Reminder set!")
                remember = open('reminders.txt', 'w')
                remember.write(data)
                remember.close()

            elif 'remind me' in query:
                remember = open('reminders.txt', 'r')
                speak("Reminders set" + remember.read())

            elif 'cpu' in query:
                cpu()

            elif 'ask' in query:
                speak('I can answer to computational and geographical questions')
                speak('What question do you want to ask now?')
                question = getUserAudioCommand().lower()
                app_id = "Paste your unique ID here "
                client = wolframalpha.Client('TKYGUV-29TE39K3U2')
                res = client.query(question)
                answer = next(res.results).text
                speak(answer)
                print(answer)

            elif 'off' in query:
                quit()
