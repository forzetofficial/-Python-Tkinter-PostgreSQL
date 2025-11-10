from tkinter import *
from gui import LoginWindow


def main():
    root = Tk()
    root.title("Библиотека")
    root.geometry("1280x720")

    login_window = LoginWindow(root)

    root.protocol("WM_DELETE_WINDOW", login_window.on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()