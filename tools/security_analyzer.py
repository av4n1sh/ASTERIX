import re
import os
from collections import Counter


def analyze_log(filename):
    if not os.path.exists(filename):
        return {"Error": "Log file not found."}

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    total_events = len(lines)

    failed_logins = 0
    successful_logins = 0
    ip_addresses = []

    for line in lines:
        lower_line = line.lower()

        if "failed login" in lower_line or "login failed" in lower_line:
            failed_logins += 1

        if "successful login" in lower_line or "login successful" in lower_line:
            successful_logins += 1

        ips = re.findall(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            line
        )

        ip_addresses.extend(ips)

    ip_counts = Counter(ip_addresses)

    suspicious_ips = {}

    for ip, count in ip_counts.items():
        if count >= 3:
            suspicious_ips[ip] = count

    result = {
        "Log File": filename,
        "Total Events": total_events,
        "Failed Logins": failed_logins,
        "Successful Logins": successful_logins,
        "Unique IP Addresses": len(ip_counts),
        "Suspicious IP Addresses": suspicious_ips
    }

    if failed_logins >= 5:
        result["Security Warning"] = (
            "Multiple failed login attempts detected."
        )
    else:
        result["Security Warning"] = "No major login warning detected."

    return result