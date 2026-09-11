from tools.data_analysis import analyze_file


result = analyze_file("test.csv")

for key, value in result.items():
    print(key + ":", value)