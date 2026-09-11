from tools.system_info import get_system_info

info = get_system_info()

for key, value in info.items():
    print(key + ":", value)