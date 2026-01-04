import tkinter
from tkinter import ttk
from tkinter import messagebox
import requests
import sys

def login(name_entry, passw_entry, URL, app, root):
    json_data = {
        "name" : name_entry.get(),
        "password" : passw_entry.get(),
    }

    try:
        response = requests.post(URL, json=json_data)

        response.raise_for_status()

        print("Sikeres kérés")
        print(response.status_code)
        app.successfull = True
        app.name = name_entry.get()
        data = response.json()
        print("JSON válasz")
        print(data)

        if app.successfull:
            root.destroy()

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Hiba", f"Nem létezik ilyen fiók")
    except requests.exceptions.ConnectionError as e:
        messagebox.showerror("Hiba", "Nem sikerült kapcsolatba lépni a szerverrel a bejelentkezéshez!")



def loginWindow():
    class App:
        def __init__(self):
           self.successfull = False
           self.name = ""

    LOGIN_URL = "http://localhost:5233/api/User/Login"

    app = tkinter.Tk()
    openedApp = App()
    
    app.geometry("300x200")
    app.title("For The Potatoe bejelentkezése")
    app.protocol("WM_DELETE_WINDOW", sys.exit)

    username_label = ttk.Label(app, text="Felhasználónév:")
    username_label.pack(pady=2)

    username_entry = ttk.Entry(app)
    username_entry.pack(pady=5)
    username_entry.focus()

    password_label = ttk.Label(app, text="Jelszó:")
    password_label.pack(pady=2)

    password_entry = ttk.Entry(app, show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(
        app,
        text="Bejelentkezés",
        command=lambda: login(username_entry, password_entry, LOGIN_URL, openedApp, app)
    )

    login_button.pack(
        pady=5
    )
    

    app.mainloop()
    return openedApp

