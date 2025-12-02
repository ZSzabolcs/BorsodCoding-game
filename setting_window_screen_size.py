import tkinter
from tkinter import ttk

def setting_size():

    root = tkinter.Tk()
    root.title("Játék méretének kiválasztása")
    root.geometry("300x200")

    selected_option = tkinter.StringVar(value="1")

    def show_selection():
        print(f"Selected: {selected_option.get()}")

    radio1 = tkinter.Radiobutton(root, text="500X500", variable=selected_option, value="1", command=show_selection)
    radio2 = tkinter.Radiobutton(root, text="1000X1000", variable=selected_option, value="2", command=show_selection)

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