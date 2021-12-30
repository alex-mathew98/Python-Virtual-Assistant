from VA.src.Functionality.HandleInput import *
from VA.src.Functionality.Features import *

engine = getEngine()
user_name = "Alex"
virtual_assistant_name = "Alfred"


# Greeting user
def greetUser():
    hour = int(datetime.datetime.now().hour)
    if 5 <= hour <= 12:
        speak("Good morning!")
    elif 13 <= hour <= 15:
        speak("Good afternoon!")
    elif 16 <= hour <= 21:
        speak("Good evening!")
    else:
        speak("Hope you're having a good night!")


# Welcome message
def welcomeUser():
    speak(f"Hello {user_name}, my name is {virtual_assistant_name} your virtual assistant")
    engine.runAndWait()


def matchQuery(query):
    if 'hello' in query:
        speak("Hey,how's it going?")

    elif 'time' in query:
        getTime()

    elif 'date' in query:
        getDate()

    elif 'Google' in query:
        speak("What do you want to search for?")
        search = getUserAudioCommand()
        searchGoogle(search)

    elif 'Youtube' in query:
        speak("What do you want to look up on youtube?")
        topic = getUserAudioCommand()
        playYoutube(topic)

    elif 'weather' in query:
        speak("Which city do you want to find the weather for?")
        city = getUserAudioCommand()
        getWeather(city)

    elif 'news' in query:
        getNews()

    elif 'jokes' in query:
        tellJokes()

    elif 'note' in query:
        speak("What do you want me to take note of?")
        data = getUserAudioCommand()
        setNote(data)

    elif 'show notes' in query:
        readNotes()

    elif 'cpu' in query:
        getCPU()

    elif 'my location' in query:
        getMyLocation()

    elif 'show map' in query:
        speak("For which location")
        location = getUserAudioCommand().lower()
        displayMap(location)

    elif 'ask' in query:
        speak('I can answer to computational and geographical questions')
        speak('What question do you want to ask now?')
        question = getUserAudioCommand().lower()
        ask(question)

    elif 'log out' in query:
        logOut()

    elif 'None' in query:
        speak("No input provided")

    else:
        speak("Sorry I am not able to perform that function")

# authenticate_google():
