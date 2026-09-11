import ollama
from memory import get_memory, add_memory
from tools.system_info import get_system_info
from tools.data_analysis import analyze_file
from tools.security_analyzer import analyze_log
from tools.router import choose_tool, run_tool


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
    tool = choose_tool(text)

    if tool == "system_info":
        result = run_tool(tool)
        prompt = f"""
The user asked:

{text}

The computer information tool returned:

{result}

Answer the user's question using only this information.

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

    elif tool == "data_analysis":
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

        result = run_tool(tool, filename)
        prompt = f"""
The user asked:

{text}

The dataset analyzed was:

{filename}

The dataset analysis tool returned:

{result}

Explain the results clearly.

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
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    elif tool == "security_analysis":
        filename = None
        words = text.replace(",", " ").split()

        for word in words:
            cleaned_word = word.strip("\"'.,!?")
            if cleaned_word.lower().endswith(".log"):
                filename = cleaned_word
                break

        if filename is None:
            filename = "security.log"

        result = run_tool(tool, filename)
        prompt = f"""
The user asked:

{text}

The security log analyzed was:

{filename}

The security analysis tool returned:

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
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

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