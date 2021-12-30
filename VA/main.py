# Importing dependencies
import time

import datetime
import pickle
import os.path

import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder

# Setting engine for pyttsx3
engine = pyttsx3.init()

paths = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
}

user_name = "Alex"
assistant_name = "Jarvis"

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])



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
    speak(f"My name is {assistant_name},your virtual assistant")
    speak(f'How may I assist you today,{user_name}?')
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
    usage = str(psutil.cpu_percent())
    battery = psutil.sensors_battery()
    speak(f"CPU is at: {usage}")
    speak(f"Battery is at:{battery.percent}")

# To be modified
# def get_daily_events(day, service):
#     # Call the Calendar API
#     date = datetime.datetime.combine(day, datetime.datetime.min.time())
#     end = datetime.datetime.combine(day, datetime.datetime.max.time())
#     utc = pytz.UTC
#     date = date.astimezone(utc)
#     end = end.astimezone(utc)
#     events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end.isoformat(),
#                                         singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])
#
#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])

def getMyLocation():
    my_ip = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    city = geo_d['city']
    country = geo_d['country']
    speak(f"You are currently located in {city},{country}")

def calculateDistance(destination):
    dest_url = "https://www.google.com/maps/place/" + str(destination)
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(destination, addressdetails=True)
    dest_location = location.latitude, location.longitude
    location = location.raw['address']
    target = {
        'city': location.get('city', ''),
        'state': location.get('state', ''),
        'country': location.get('country', ''),
    }
    current_location = geocoder.ip('me')
    distance = str(great_circle(current_location, dest_location))
    distance = str(distance.split('', 1)[0])
    distance = round(float(distance), 2)

    speak(f"{destination} is {distance} kilometres away from your current location")

def logOut():
    speak('Logging off')
    time.sleep(10)
    quit()

service = authenticate_google()


speak('What question do you want to ask now?')
question = getUserAudioCommand().lower()
app_id = "Paste your unique ID here "
client = wolframalpha.Client('TKYGUV-29TE39K3U2')
res = client.query(question)
answer = next(res.results).text
speak(answer)
print(answer)

# if __name__ == '__main__':
#
#     greetUser()
#     welcomeUser()
#     wakeword = "sam"
#     while True:
#         query = getUserAudioCommand().lower()
#
#         # if wakeword in query:
#         if 'time' in query:
#             getTime()
#
#         elif 'date' in query:
#             getDate()
#
#         elif 'email' in query:
#             speak("What do you want to send?")
#             try:
#                 content = getUserAudioCommand()
#                 sendEmail(content)
#                 speak("Email has been sent successfully")
#                 engine.runAndWait()
#             except Exception as e:
#                 print(e)
#                 speak("Error occurred,failed to send email!")
#
#         elif 'wikipedia' in query:
#             speak("What would you like to know")
#             search = getUserAudioCommand()
#             result = wikipedia.summary(search, sentences=2)
#             print(result)
#             speak(str(result))
#
#         elif 'search' in query:
#             searchGoogle()
#
#         elif 'youtube' in query:
#             speak("What do you want to look up on youtube?")
#             topic = getUserAudioCommand()
#             pywhatkit.playonyt(topic)
#
#         elif 'weather' in query:
#             speak("Which city do you want to find the weather for?")
#             city = getUserAudioCommand()
#             getWeather(city)
#
#         elif 'news' in query:
#             getNews()
#
#         elif 'read text' in query:
#             readText()
#
#         elif 'jokes' in query:
#             speak(pyjokes.get_joke())
#
#         elif 'note' in query:
#             speak("What do you want me to take note of?")
#             data = getUserAudioCommand()
#             speak("Note set!")
#             note = open('notes.txt', 'w')
#             note.write(data)
#             note.close()
#
#         elif 'show notes' in query:
#             notes = open('notes.txt', 'r')
#             speak(notes.read())
#
#         elif 'cpu' in query:
#             cpu()
#
#         elif 'my location' in query:
#             getMyLocation()
#
#         elif 'calculate distance' in query:
#             speak("What would you like to set as the destination?")
#             destination = getUserAudioCommand().lower()
#             calculateDistance(destination)
#
#         elif 'ask' in query:
#             speak('I can answer to computational and geographical questions')
#             speak('What question do you want to ask now?')
#             question = getUserAudioCommand().lower()
#             app_id = "Paste your unique ID here "
#             client = wolframalpha.Client('TKYGUV-29TE39K3U2')
#             res = client.query(question)
#             answer = next(res.results).text
#             speak(answer)
#             print(answer)
#
#         elif 'show map' in query:
#             speak("For which location")
#             location = getUserAudioCommand().lower()
#             url = 'https://google.nl/maps/place/' + location + '/&amp;'
#             speak(f"Displaying the map of {location}")
#             browser.open(url)
#             print(f"Map opened for - {location}")
#
#         elif 'hello' in query:
#             speak("Hey,how's it going?")
#
#         elif 'events' in query:
#             get_events(2, service)
#         elif 'off' in query:
#             logOut()
