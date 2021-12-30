from VA.src.Configuration.Engine import getEngine
from VA.src.Functionality.Secrets import *

import time
import datetime
import webbrowser as browser
import psutil
import pywhatkit
import requests
import pyjokes
import wolframalpha


engine = getEngine()


# Function for providing text to speech output
def speak(message):
    engine.say(message)
    engine.runAndWait()


# Function for retrieving current time
def getTime():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f'The time is ,{time}')
    engine.runAndWait()


# Function for retrieving current date
def getDate():
    day = str(datetime.datetime.now().day)
    month = str(datetime.datetime.now().month)
    year = str(datetime.datetime.now().year)
    speak("Today's date is:")
    speak(day)
    speak(month)
    speak(year)
    engine.runAndWait()


# Function to handle google search queries
def searchGoogle(search):
    browser.open('https://www.google.com/search?q=' + search)


# Function to redirect to youtube videos based on user input provided
def playYoutube(topic):
    pywhatkit.playonyt(topic)


# Function to handle search weather functionalities
def getWeather(city):
    speak(f"Finding weather for{city}")
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_API_KEY}'
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


# Function to handle generate jokes
def tellJokes():
    speak(pyjokes.get_joke())


# Function to handle taking user notes
def setNote(data):
    note = open('notes.txt', 'w')
    note.write(data)
    note.close()
    speak("Note set!")


# Function to handle reading set user notes
def readNotes():
    notes = open('notes.txt', 'r')
    speak(notes.read())


# Function to handle getting CPU and battery usage details
def getCPU():
    usage = str(psutil.cpu_percent())
    battery = psutil.sensors_battery()
    speak(f"CPU is at: {usage}")
    speak(f"Battery is at:{battery.percent}")


# Function to handle getting user's current location
def getMyLocation():
    my_ip = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    city = geo_d['city']
    country = geo_d['country']
    speak(f"You are currently located in {city},{country}")


# Function to handle displaying map of location set by user
def displayMap(location):
    url = 'https://google.nl/maps/place/' + location + '/&amp;'
    speak(f"Displaying the map of {location}")
    browser.open(url)
    print(f"Map opened for - {location}")


# Function to handle ask question functionalities
def ask(question):
    client = wolframalpha.Client(wolframalpha_API_KEY)
    res = client.query(question)
    answer = next(res.results).text
    speak(answer)
    print('The answer found:',answer)


# Function to handle switching off for the virtual assistant
def logOut():
    speak('Logging off')
    time.sleep(5)
    quit()
