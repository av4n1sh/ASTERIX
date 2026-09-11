import platform
import psutil


def get_system_info():
    info = {
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Computer": platform.node(),
        "CPU": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Available RAM": f"{round(psutil.virtual_memory().available / (1024 ** 3), 2)} GB"
    }

    return info