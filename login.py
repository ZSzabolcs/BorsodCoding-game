import tkinter
from tkinter import ttk
import requests
import datetime
import sys

# --- LOGIN FÜGGVÉNY (NEM VÁLTOZOTT, a logika rendben van) ---
def login(name_entry, passw_entry, URL, app_state, root):
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
        app_state.successfull = True
        app_state.name = name_entry.get()
        data = response.json()
        print("JSON válasz")
        print(data)

        if app_state.successfull:
            # Csak akkor zárjuk be az ablakot, ha sikeres volt a bejelentkezés
            root.destroy()

    except requests.exceptions.RequestException as e:
        # 💡 Hibaüzenet megjelenítése a felhasználónak a Tkinter ablakban
        error_message = f"Hiba történt: {e}"
        print(error_message)
        # Egy gyors Tkinter ablakban megjeleníthető hibaüzenet hozzáadása itt javasolt.


# --- LOGIN ABLAK FUNKCIÓ (RESZPONZÍV JAVÍTÁS) ---
def loginWindow():
    class AppState:
        def __init__(self):
           self.successfull = False
           self.name = ""

    LOGIN_URL = "http://localhost:5233/api/UserRegistData/Login"

    root = tkinter.Tk()
    openedApp = AppState()
    root.title("For The Potatoe login")
    
    # 1. Ablak méret beállítása és középre helyezés (opcionális, de jó felhasználói élmény)
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Ablak bezárási protokoll beállítása
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    # 2. Reszponzivitás beállítása a grid-re
    # A középső oszlopok és sorok súlyozása, hogy kitöltse a rendelkezésre álló teret
    root.columnconfigure(0, weight=1) 
    root.columnconfigure(1, weight=3) # A beviteli mezők több helyet kapnak
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(3, weight=1)
    root.rowconfigure(4, weight=1) 

    # --- Widgetek létrehozása és elhelyezése GRID-del ---

    # 1. Felhasználónév label (0. oszlop)
    username_label = ttk.Label(root, text="Username:")
    username_label.grid(row=1, column=0, padx=5, pady=5, sticky="E") # Jobbra igazítás (East)

    # 2. Felhasználónév beviteli mező (1. oszlop)
    username_entry = ttk.Entry(root)
    username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="WE") # Kitölti a teret (West/East)
    username_entry.focus()

    # 3. Jelszó label (0. oszlop)
    password_label = ttk.Label(root, text="Password:")
    password_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")

    # 4. Jelszó beviteli mező (1. oszlop)
    password_entry = ttk.Entry(root, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="WE")

    # 5. Login gomb (mindkét oszlop, középen)
    login_button = ttk.Button(
        root,
        text="Login",
        command=lambda: login(username_entry, password_entry, LOGIN_URL, openedApp, root)
    )
    # 💡 A columnspan=2 és sticky="N" (felül) használata segít a középre igazításban
    login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="N") 


    root.mainloop()
    return openedApp