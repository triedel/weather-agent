import requests
import datetime
import smtplib
import os
from email.mime.text import MIMEText

print("SCRIPT STARTED")

LAT = 30.202866
LON = -97.853076

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

def get_air_quality():
    print("Fetching air quality...")

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={LAT}&lon={LON}&appid={API_KEY}"
    )

    response = requests.get(url)

    print("Air API status:", response.status_code)

    data = response.json()

    return data

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
# ANALYZE AIR QUALITY
# ======================

def analyze_air_quality(aq_data):
    aqi = aq_data["list"][0]["main"]["aqi"]
    co = aq_data["list"][0]["components"]["co"]
    pm25 = aq_data["list"][0]["components"]["pm2_5"]


    return {
        "aqi": aqi, 
        "co": co, 
        "pm25": pm25        
    }


# ======================
# GENERATE REPORT
# ======================

def generate_report(weather_analysis, air_analysis):
    print("Generating report...")

    report = f"""
    Austin Weather Brief

    High: 
    {weather_analysis['max_temp']:.0f}°F
    Low: 
    {weather_analysis['min_temp']:.0f}°F

    Rain expected: 
    {"Yes" if weather_analysis["rain"] else "No"}

    Air Quality:  1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor" 
    {air_analysis['aqi']}
   
    Carbon Monoxide (µg/m³): 
    {air_analysis['co']}
    
    PM2.5 (µg/m³): 
    {air_analysis['pm25']}
                              
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

    weather_analysis = analyze(data)

    aq_data = get_air_quality()

    air_analysis = analyze_air_quality(aq_data)

    report = generate_report(weather_analysis, air_analysis)

    print(report)

    send_email(report)

if __name__ == "__main__":
    main()
