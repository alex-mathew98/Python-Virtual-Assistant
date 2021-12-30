from VA.src.Functionality.Utils import *


def run():
    greetUser()
    welcomeUser()
    while True:
        speak(f"What can I help you with?")
        query = getUserAudioCommand()
        matchQuery(query)


if __name__ == '__main__':
    run()
