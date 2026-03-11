import tkinter
from tkinter import ttk

def setting_size():

    root = tkinter.Tk()
    root.title("Játék méretének kiválasztása")
    root.geometry("300x200")

    selected_option = tkinter.StringVar(value="1")


    radio1 = tkinter.Radiobutton(root, text="760X760", variable=selected_option, value="1")
    radio2 = tkinter.Radiobutton(root, text="1000X1000", variable=selected_option, value="2")

    confirm_button = ttk.Button(
        root,
        text="Elfogadás",
        command=root.destroy
    )

    radio1.pack(anchor="center")
    radio2.pack(anchor="center")
    confirm_button.pack(
        pady=5
    )

    root.mainloop()
    return selected_option.get()