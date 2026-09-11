from tools.router import choose_tool, run_tool


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    tool = choose_tool(user_input)

    print("Selected tool:", tool)

    if tool == "system_info":
        result = run_tool(tool)
        print("Tool result:", result)