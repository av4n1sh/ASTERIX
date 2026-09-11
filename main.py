from brain import ask_jarvis
from voice import speak
import threading

print("================================")
print("       JARVIS ONLINE")
print("================================")
print()

speak("JARVIS is online. How may I assist you?")


def speak_in_background(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.daemon = True
    thread.start()


while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "shutdown"]:
        print("JARVIS: Shutting down.")
        speak("Shutting down. Goodbye.")
        break

    response = ask_jarvis(user_input)

    print("JARVIS:", response)

    speak_in_background(response)