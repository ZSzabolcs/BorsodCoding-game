import tkinter
from tkinter import ttk
import requests
import datetime

def login(name_entry, passw_entry, URL, app, root):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    json_data = {
        "name" : name_entry.get(),
        "password" : passw_entry.get(),
        "date" : timestamp
    }

    try:
        response = requests.post(URL, json=json_data)

        response.raise_for_status()

        print("Sikeres kérés")
        print(response.status_code)
        app.successfull = True
        data = response.json()
        print("JSON válasz")
        print(data)

        if app.successfull:
            root.destroy()

    except requests.exceptions.RequestException as e:
        print(f"Hiba történt: {e}")



def loginWindow():
    class App:
        def __init__(self):
           self.successfull = False

    LOGIN_URL = "http://localhost:5233/api/UserRegistData/Login"

    app = tkinter.Tk()
    openedApp = App()
    app.geometry("300x200")
    app.title("For The Potatoe login")
    app.protocol("WM_DELETE_WINDOW", app.destroy)

    username_label = ttk.Label(app, text="Username:")
    username_label.pack(pady=2)

    username_entry = ttk.Entry(app)
    username_entry.pack(pady=5)
    username_entry.focus()

    password_label = ttk.Label(app, text="Password:")
    password_label.pack(pady=2)

    password_entry = ttk.Entry(app, show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(
        app,
        text="Login",
        command=lambda: login(username_entry, password_entry, LOGIN_URL, openedApp, app)
    )

    login_button.pack(
        pady=5
    )


    app.mainloop()
    return openedApp

