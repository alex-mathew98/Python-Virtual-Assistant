import speech_recognition as SR


# Function to handle text input
def getUserCommand():
    query = input("What would you like to know?")
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
        return "None"
    return data
