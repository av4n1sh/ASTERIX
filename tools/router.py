from tools.system_info import get_system_info
from tools.data_analysis import analyze_file
from tools.security_analyzer import analyze_log


def run_tool(tool_name, filename=None):

    if tool_name == "system_info":
        return get_system_info()

    elif tool_name == "data_analysis":
        if filename is None:
            return {"Error": "No dataset filename provided."}

        return analyze_file(filename)

    elif tool_name == "security_analysis":
        if filename is None:
            filename = "security.log"

        return analyze_log(filename)

    else:
        return None


def choose_tool(user_input):
    text = user_input.lower()

    if (
        "ram" in text
        or "cpu" in text
        or "processor" in text
        or "operating system" in text
        or "computer information" in text
        or "system information" in text
    ):
        return "system_info"

    if (
        ".csv" in text
        or ".json" in text
        or "dataset" in text
        or "data set" in text
    ):
        return "data_analysis"

    if (
        ".log" in text
        or "security log" in text
        or "failed login" in text
        or "login attempts" in text
    ):
        return "security_analysis"

    return "none"