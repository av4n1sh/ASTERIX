from tools.security_analyzer import analyze_log


result = analyze_log("security.log")

for key, value in result.items():
    print(key + ":", value)