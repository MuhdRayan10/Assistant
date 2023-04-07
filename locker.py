from pynput import keyboard
from tkinter import messagebox
import json

COMBINATIONS = [{keyboard.Key.shift_r, keyboard.Key.f12}]
FILE_PATH = "E:/Programming/Python/Assistant/Assistant/data/apps/locker/config.json"

current = set()

def change_perms():
        
    with open(FILE_PATH) as f:
        config = json.load(f)

    config["lock"] = not config["lock"]
    with open(FILE_PATH, mode='w') as f:
        json.dump(config, f, indent=4)

    return config["lock"]
        

def on_press(key):
    if any([key in combo for combo in COMBINATIONS]):
        current.add(key)

        if any(all(k in current for k in combo) for combo in COMBINATIONS):
            change = change_perms()
            print(change)
            messagebox.showinfo("Changed Lock", f"Mode set to {'un' if change else ''}locked!")


def on_release(key):
    if any([key in combo for combo in COMBINATIONS]):
        current.remove(key)
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()