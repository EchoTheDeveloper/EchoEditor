import tkinter as tk
from config import *

def run():
    root = tk.Tk()
    root.title(preferences_title)
    root.geometry("400x400")

    root.mainloop()

# FOR DEBUG PURPOSES, WON'T EVER GET RUN THIS WAY NORMALLY
if __name__ == "__main__":
    run()