import ollama
from memory import get_memory, add_memory
from tools.system_info import get_system_info
from tools.data_analysis import analyze_file
from tools.security_analyzer import analyze_log
from tools.router import choose_tool


SYSTEM_PROMPT = """
You are Jarvis, a highly intelligent personal AI assistant.

Speak naturally and conversationally.

Be helpful, concise, and intelligent.

Do not use emojis.

Do not use stage directions, sound effects, roleplay actions,
or phrases like *beep*, *whirring*, *chirp*, or *smile*.

Respond only with the words you want the user to hear.

You assist the user with:
- Questions
- Productivity
- Programming
- Research
- Planning
- Computer and system information
- Dataset analysis
- Defensive cybersecurity analysis

When giving instructions, explain them clearly and step by step.

When writing code, prioritize correct, practical, and beginner-friendly solutions.

Do not make up information.
"""


def ask_jarvis(text):
    memory = get_memory()

    lower_text = text.lower()

    # SYSTEM INFORMATION

    if (
        "ram" in lower_text
        or "cpu" in lower_text
        or "processor" in lower_text
        or "operating system" in lower_text
        or "computer" in lower_text
    ):
        info = get_system_info()

        system_info = "\n".join(
            key + ": " + str(value)
            for key, value in info.items()
        )

        prompt = f"""
The user asked:

{text}

Here is the actual information from the user's computer:

{system_info}

Answer the user's question using this information.

Do not make up computer specifications.
"""

        response = ollama.chat(
            model="qwen3",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    # CSV OR JSON DATASET

    elif (
        ".csv" in lower_text
        or ".json" in lower_text
        or "dataset" in lower_text
        or "data set" in lower_text
    ):
        filename = None

        words = text.replace(",", " ").split()

        for word in words:
            cleaned_word = word.strip("\"'.,!?")

            if (
                cleaned_word.lower().endswith(".csv")
                or cleaned_word.lower().endswith(".json")
            ):
                filename = cleaned_word
                break

        if filename is None:
            return "Please provide the name of the CSV or JSON file."

        result = analyze_file(filename)

        prompt = f"""
The user asked:

{text}

The file analyzed was:

{filename}

The Python dataset analysis tool returned:

{result}

Explain these results clearly to the user.

Include:
- Number of rows
- Number of columns
- Column names
- Missing values
- Duplicate rows
- Important data-quality findings

Only use information contained in the tool results.

Do not invent information.
"""

        response = ollama.chat(
            model="qwen3",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Jarvis, a data-analysis assistant.

Explain dataset analysis results clearly.

Do not use emojis.

Do not use stage directions, sound effects, or roleplay actions.

Do not invent information.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    # SECURITY LOG

    elif (
        ".log" in lower_text
        or "security log" in lower_text
        or "login attempts" in lower_text
        or "failed logins" in lower_text
    ):
        filename = None

        words = text.replace(",", " ").split()

        for word in words:
            cleaned_word = word.strip("\"'.,!?")

            if cleaned_word.lower().endswith(".log"):
                filename = cleaned_word
                break

        if filename is None:
            filename = "security.log"

        result = analyze_log(filename)

        prompt = f"""
The user asked:

{text}

The security log analyzed was:

{filename}

The Python cybersecurity analysis tool returned:

{result}

Explain the security findings clearly.

Include:
- Total events
- Failed login attempts
- Successful login attempts
- Unique IP addresses
- Suspicious IP addresses
- Security warnings

Explain whether the activity appears unusual based only on the results.

This is defensive cybersecurity analysis.

Do not provide instructions for attacking systems.

Do not invent information.
"""

        response = ollama.chat(
            model="qwen3",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Jarvis, a defensive cybersecurity assistant.

Analyze security information and explain potential security issues.

Do not use emojis.

Do not use stage directions, sound effects, or roleplay actions.

Only provide defensive and authorized cybersecurity assistance.

Do not invent information.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    # NORMAL JARVIS CONVERSATION

    else:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        for conversation in memory:
            messages.append({
                "role": "user",
                "content": conversation["user"]
            })

            messages.append({
                "role": "assistant",
                "content": conversation["jarvis"]
            })

        messages.append({
            "role": "user",
            "content": text
        })

        response = ollama.chat(
            model="qwen3",
            messages=messages
        )

    answer = response["message"]["content"]

    add_memory(text, answer)

    return answer
