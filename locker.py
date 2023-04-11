from AppOpener import open as open_app
from AppOpener import close as close_app
from pynput import keyboard
import json

COMBINATIONS = [{keyboard.Key.shift_r, keyboard.Key.f11}, {keyboard.Key.shift_r}, {keyboard.Key.shift_r, keyboard.Key.f12}, {keyboard.Key.shift_r, keyboard.Key.f10}]
FILE_PATH = "E:/Programming/Python/Assistant/Assistant/data/apps/locker/config.json"

current = set()

def change_perms(mode=None):
        
    with open(FILE_PATH) as f:
        config = json.load(f)

    config["lock"] = not config["lock"] if mode is None else mode
    with open(FILE_PATH, mode='w') as f:
        json.dump(config, f, indent=4)

    return config["lock"]
        

def on_press(key):
    if any([key in combo for combo in COMBINATIONS]):
        current.add(key)

        if any(all(k in current for k in combo) for combo in COMBINATIONS):
            change = change_perms()
            print(change)

            if current == COMBINATIONS[0]:
                change_perms(True)
                try:
                    close_app("discord")
                except:
                    print("Couldn't close")
            elif current == COMBINATIONS[2]:

                change_perms(False)
                try:
                    open_app("discord")
                except:
                    print("Couldn't open")

        elif current == COMBINATIONS[3]:
            exit()


                

def on_release(key):
    if any([key in combo for combo in COMBINATIONS]):
        current.remove(key)
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()