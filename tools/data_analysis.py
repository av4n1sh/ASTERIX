import csv
import json
import os


def analyze_csv(filename):
    if not os.path.exists(filename):
        return {"Error": "File not found."}

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        reader = csv.DictReader(file)

        rows = []
        columns = reader.fieldnames

        if not columns:
            return {"Error": "The CSV file does not contain column names."}

        for row in reader:
            rows.append(row)

    result = {
        "File": filename,
        "Rows": len(rows),
        "Columns": len(columns),
        "Column Names": columns
    }

    missing_values = {}

    for column in columns:
        missing = 0

        for row in rows:
            if row[column] is None or row[column].strip() == "":
                missing += 1

        missing_values[column] = missing

    result["Missing Values"] = missing_values

    duplicate_rows = len(rows) - len(
        {tuple(row.items()) for row in rows}
    )

    result["Duplicate Rows"] = duplicate_rows

    return result


def analyze_json(filename):
    if not os.path.exists(filename):
        return {"Error": "File not found."}

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        data = json.load(file)

    result = {
        "File": filename,
        "Data Type": type(data).__name__
    }

    if isinstance(data, list):
        result["Records"] = len(data)

        if len(data) > 0 and isinstance(data[0], dict):
            result["Fields"] = list(data[0].keys())

    elif isinstance(data, dict):
        result["Keys"] = list(data.keys())

    return result


def analyze_file(filename):
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".csv":
        return analyze_csv(filename)

    elif extension == ".json":
        return analyze_json(filename)

    else:
        return {
            "Error": "Unsupported file type. Use CSV or JSON."
        }