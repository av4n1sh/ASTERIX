import sys
import json

from brain import ask_jarvis


def main():
    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        try:
            data = json.loads(line)

            user_message = data.get("message", "")

            if not user_message:
                print(json.dumps({
                    "error": "No message provided."
                }), flush=True)
                continue

            response = ask_jarvis(user_message)

            print(json.dumps({
                "response": response
            }), flush=True)

        except Exception as e:
            print(json.dumps({
                "error": str(e)
            }), flush=True)


if __name__ == "__main__":
    main()