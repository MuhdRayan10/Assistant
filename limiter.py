import pygetwindow as gw
from datetime import date
import json
import time

STAT_FILE = "./data/apps/locker/stats.json"
APPS = {"code": "Programming", "discord": "Discord", "youtube": "YouTube", "chess": "Chess"}

def get_window():
    return gw.getActiveWindowTitle()

def update_json(data):
    with open(STAT_FILE, "w") as f:
        json.dump(data, f)

def new_day(data, day):
    data[day] = {}

    window = get_window()
    for app, category in APPS.items():
        if app in window.lower():
            data[day][category] = 1

    update_json(data)

def current_day(data, day):
    window = get_window()

    for app, category in APPS.items():
        if app in window.lower():
            data[day][category] = data[day].get(category, 0) + 1

    update_json(data)

def one_tick():
    with open(STAT_FILE) as f:
        data = json.load(f)

    today = str(date.today())
    print(today in data)
    print(data)
    if today in data:
        current_day(data, today)
    else:
        new_day(data, today)

while True:
    one_tick()
    time.sleep(1)



