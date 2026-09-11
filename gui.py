import customtkinter as ctk
from brain import ask_jarvis
import threading


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()

app.title("JARVIS")
app.geometry("1000x650")
app.minsize(800, 500)


title = ctk.CTkLabel(
    app,
    text="JARVIS",
    font=("Arial", 32, "bold")
)

title.pack(pady=20)


chat_box = ctk.CTkTextbox(
    app,
    font=("Arial", 16)
)

chat_box.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)

chat_box.insert(
    "end",
    "JARVIS: System initialized.\n\n"
)


input_box = ctk.CTkEntry(
    app,
    placeholder_text="Enter a message...",
    height=45,
    font=("Arial", 16)
)

input_box.pack(
    side="left",
    padx=(30, 10),
    pady=20,
    fill="x",
    expand=True
)


def send_message():
    user_input = input_box.get()

    if user_input.strip() == "":
        return

    input_box.delete(0, "end")

    chat_box.insert(
        "end",
        "You: " + user_input + "\n"
    )

    chat_box.insert(
        "end",
        "JARVIS: Thinking...\n\n"
    )

    def process_message():
        response = ask_jarvis(user_input)

        app.after(
            0,
            lambda: show_response(response)
        )

    threading.Thread(
        target=process_message,
        daemon=True
    ).start()


def show_response(response):
    chat_box.delete("end-3l", "end")

    chat_box.insert(
        "end",
        "JARVIS: " + response + "\n\n"
    )

    chat_box.see("end")


send_button = ctk.CTkButton(
    app,
    text="SEND",
    width=120,
    height=45,
    command=send_message
)

send_button.pack(
    side="right",
    padx=(10, 30),
    pady=20
)


input_box.bind(
    "<Return>",
    lambda event: send_message()
)


app.mainloop()