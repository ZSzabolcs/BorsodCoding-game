import tkinter
from tkinter import ttk


def loginWindow():
    root = tkinter.Tk()
    root.geometry("300x200")
    root.title("For The Potatoe login")

    username_label = ttk.Label(root, text="Username:")
    username_label.pack(pady=2)

    username_entry = ttk.Entry(root)
    username_entry.pack(pady=5)
    username_entry.focus()

    password_label = ttk.Label(root, text="Password:")
    password_label.pack(pady=2)

    password_entry = ttk.Entry(root, show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(
        root,
        text="Login",
        command=lambda: print("Működik")
    )

    login_button.pack(
        pady=5
    )


    root.mainloop()


