import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def add_memory(user_message, jarvis_response):
    memory = load_memory()

    memory.append({
        "user": user_message,
        "jarvis": jarvis_response
    })

    save_memory(memory)


def get_memory():
    return load_memory()