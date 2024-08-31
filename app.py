import tkinter as tk
from tkinter import filedialog
import preferences as pref
from config import *

root = tk.Tk()
root.title(root_title)

text = tk.Text(root, wrap="word", undo=True)
text.pack(expand="yes", fill="both")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

def new_file():
    text.delete("1.0", tk.END)
    root.title(root_title)

def open_file():
    file_path = filedialog.askopenfilename(defaultextension="*.*", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*"), ("Python Files", "*.py"), ("Csharp Files", "*.cs"), ("JavaScript Files", "*.js"), ("C Files", "*.c"), ("C++ Files", "*.cpp"), ("Make Files", "*.makefile"), ("Batch Scripts", "*.bat"), ("Bash Scripts", "*.sh")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text.delete("1.0", tk.END)
            text.insert(tk.END, content)
        root.title(file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension="*.*", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*"), ("Python Files", "*.py"), ("Csharp Files", "*.cs"), ("JavaScript Files", "*.js"), ("C Files", "*.c"), ("C++ Files", "*.cpp"), ("Make Files", "*.makefile"), ("Batch Scripts", "*.bat"), ("Bash Scripts", "*.sh")])
    if file_path:
        with open(file_path, "w") as file:
            content = text.get("1.0", tk.END)
            file.write(content)
        root.title(file_path)

def open_preferences():
    pref.run()

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=fm_title, menu=file_menu)
file_menu.add_command(label=fm_new, command=new_file)
file_menu.add_command(label=fm_open, command=open_file)
file_menu.add_command(label=fm_save, command=save_file)
file_menu.add_separator()
file_menu.add_command(label=fm_exit, command=root.destroy)

edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=em_title, menu=edit_menu)
edit_menu.add_command(label=em_preferences, command=open_preferences)

root.mainloop()