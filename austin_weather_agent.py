import requests
import datetime
import smtplib
import os
from email.mime.text import MIMEText

print("SCRIPT STARTED")

# ======================
# CONFIG FROM GITHUB SECRETS
# ======================

API_KEY = os.environ["OPENWEATHER_API_KEY"]

EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]

CITY = "Austin,US"

# ======================
# FETCH WEATHER
# ======================

def get_forecast():
    print("Fetching forecast...")

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={CITY}&appid={API_KEY}&units=imperial"
    )

    response = requests.get(url)

    print("Weather API status:", response.status_code)

    data = response.json()

    return data["list"][:8]

# ======================
# ANALYZE WEATHER
# ======================

def analyze(data):
    print("Analyzing weather...")

    temps = [d["main"]["temp"] for d in data]

    max_temp = max(temps)
    min_temp = min(temps)

    rain = any(d.get("pop", 0) > 0.3 for d in data)

    return {
        "max_temp": max_temp,
        "min_temp": min_temp,
        "rain": rain
    }

# ======================
# GENERATE REPORT
# ======================

def generate_report(analysis):
    print("Generating report...")

    report = f"""
Austin Weather Brief

High: {analysis['max_temp']:.0f}°F
Low: {analysis['min_temp']:.0f}°F

Rain expected: {"Yes" if analysis["rain"] else "No"}

Generated:
{datetime.datetime.now()}
"""

    return report

# ======================
# SEND EMAIL
# ======================

def send_email(report):
    print("Sending email...")

    msg = MIMEText(report)

    msg["Subject"] = "Austin Weather"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)

        print("Logged into Gmail")

        server.send_message(msg)

        print("Email successfully sent")

# ======================
# MAIN
# ======================

def main():
    print("Starting weather agent")

    data = get_forecast()

    analysis = analyze(data)

    report = generate_report(analysis)

    print(report)

    send_email(report)

if __name__ == "__main__":
    main()
