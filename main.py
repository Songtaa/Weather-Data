# https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m
import os
import requests
from celery import Celery
from celery.schedules import crontab
from apis.github_data import check_github_json
from dotenv import load_dotenv
load_dotenv()

def weather_task(city):
 api_key = str(os.getenv('88f92b744a91792ab48203407d635f1d'))
 url = "https://api.openweathermap.org/data/2.5/forecast"
 params = {"q": city, "appid": api_key, "units": "metric"}
 response = requests.get(url, params=params)

 if response.status_code != 200:
  print(f"Error {response.status_code}: {response.text}")
  return

 data = response.json()
 summaries = []

 for entry in data["list"]:
  if "12:00:00" in entry["dt_txt"]:
   main = entry["weather"][0]["main"]
   description = entry["weather"][0]["description"]

   if "rain" in description.lower() or "rain" in main.lower() or "rain" in entry:
    date = entry["dt_txt"].split(" ")[0]
    summaries.append({
     "Date": date,
     "Weather Description": description
    })

 if summaries:
  check_github_json(summaries)
 else:
  check_github_json(None)

if __name__ == "__main__":
 weather_task("London")