import tkinter
from tkinter import ttk
from tkinter import messagebox
import requests
import sys

def login(username_entry, passw_entry, URL, loginState, root):
    try:
        if username_entry.get() == "" and passw_entry.get() == "":
            root.destroy()
            return

        json_data = {
        "userName" : username_entry.get(),
        "password" : passw_entry.get(),
    }
        response = requests.post(URL, json=json_data, verify=False)


        body = response.json()
        if response.status_code != 200:
            messagebox.showerror("Hiba", body["message"])

        messagebox.showinfo("A burgonyáért!", body["message"])

        loginState.token = body["token"]
        loginState.isSuccessfull = True
        loginState.username = username_entry.get()

        if loginState.isSuccessfull:
            root.destroy()

    except requests.exceptions.ConnectionError as e:
        messagebox.showerror("Hiba", f"Nem sikerült kapcsolatba lépni a szerverrel a bejelentkezéshez!", icon="error")
    except Exception as ex:
        messagebox.showerror("Hiba", f"Nem regisztált, vagy helytelen a felhasználónév vagy jelszó!", icon="error")



def loginWindow():
    class LoginState:
        def __init__(self):
           self.token = ""
           self.isSuccessfull = False
           self.username = ""

    LOGIN_URL = "https://localhost:7159/auth/login"

    app = tkinter.Tk()
    loginState = LoginState()
    
    app.geometry("450x200")
    app.title("For The Potato bejelentkezése")
    app.protocol("WM_DELETE_WINDOW", sys.exit)

    offline_mode_label = ttk.Label(app, text="Ha üresen nyomja meg a bejelentkezés gombot, akkor offline módon játszol!")
    offline_mode_label.pack(pady=2)

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
        command=lambda: login(username_entry, password_entry, LOGIN_URL, loginState, app)
    )

    login_button.pack(
        pady=5
    )
    

    app.mainloop()
    return loginState

