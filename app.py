import tkinter as tk
from tkinter import filedialog
import json
import preferences as pref
from config import *

root = tk.Tk()
root.title(root_title)

text = tk.Text(root, wrap="word", undo=True)
text.pack(expand="yes", fill="both")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

def load_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Import Suggestions
keywords = load_file("resources/keywords.json")
snippets = load_file("resources/snippets.json")

# Suggestion windows
autocomplete_window = None
suggestion_listbox = None

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

#-------------------- Autocomplete and Snippets --------------------#

def on_key_release(event):
    if event.keysym in ["Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Tab"]:
        return  # Ignore modifier keys and Tab
    if event.keysym == "space":
        return  # Ignore space key to prevent triggering autocomplete again
    show_autocomplete()

text.bind("<KeyRelease>", on_key_release)

def show_autocomplete():
    global autocomplete_window, suggestion_listbox
    hide_autocomplete()  # Hide previous autocomplete if it exists
    cursor_position = text.index(tk.INSERT)
    line_text = text.get(f"{cursor_position} linestart", cursor_position)
    current_word = line_text.split()[-1] if line_text.split() else ""
    if not current_word:
        return
    
    suggestions = []
    
    # Add snippets if any match the current word
    if current_word in snippets:
        snippet_preview = snippets[current_word][:8] + "..."
        suggestions.append((current_word, f"{current_word}: ({snippet_preview})"))
    # Add keywords that start with the current word
    keyword_suggestions = [kw for kw in keywords if kw.startswith(current_word)]
    suggestions.extend([(kw, kw) for kw in keyword_suggestions])
    if suggestions:
        autocomplete_window = tk.Toplevel(root)
        autocomplete_window.wm_overrideredirect(True)
        autocomplete_window.lift()  # Ensure it stays on top
        autocomplete_window.configure(background="#353738")
        text.focus_set()  # Ensure it takes focus
        x, y, _, _ = text.bbox(tk.INSERT)
        x += text.winfo_rootx()
        y += text.winfo_rooty() + 25
        autocomplete_window.geometry(f"+{x}+{y}")
        
        suggestion_listbox = tk.Listbox(
            autocomplete_window,
            selectmode=tk.SINGLE,
            height=min(len(suggestions), 6),
            foreground="#edf2f4",
            background="#353738"
        )
        suggestion_listbox.pack()
        for _, display_text in suggestions:
            suggestion_listbox.insert(tk.END, display_text)
        # Bind Listbox events
        suggestion_listbox.bind("<Double-1>", lambda e: insert_autocomplete())
        suggestion_listbox.bind("<Return>", lambda e: insert_autocomplete())
        suggestion_listbox.bind("<Up>", on_arrow_key_in_listbox)
        suggestion_listbox.bind("<Down>", on_arrow_key_in_listbox)
        # Bind click outside the autocomplete window to hide it
        root.bind("<Button-1>", on_click_outside)

def insert_autocomplete():
    global suggestion_listbox
    if not suggestion_listbox:
        return
    selected_text = suggestion_listbox.get(tk.ACTIVE)
    cursor_position = text.index(tk.INSERT)
    line_text = text.get(f"{cursor_position} linestart", cursor_position)
    current_word = line_text.split()[-1] if line_text.split() else ""
    text.delete(f"{cursor_position} - {len(current_word)}c", cursor_position)
    # Determine if the selected item is a snippet or a keyword
    if ':' in selected_text:
        # Extract the original word part from the selected text
        original_word = selected_text.split(':')[0]
        if original_word in snippets:
            text.insert(tk.INSERT, snippets[original_word])
    else:
        # Insert the keyword directly
        text.insert(tk.INSERT, selected_text)
    hide_autocomplete()

def accept_autocomplete_or_snippet(event):
    global suggestion_listbox

    # Ensure there is an autocomplete window and a selection
    if autocomplete_window and suggestion_listbox.curselection():
        insert_autocomplete()  # Directly call the function to insert the selected item
        return "break"

    cursor_position = text.index(tk.INSERT)
    line_text = text.get(f"{cursor_position} linestart", cursor_position)
    current_word = line_text.split()[-1] if line_text.split() else ""

    # Check if the current word matches a snippet trigger
    if current_word in snippets:
        word_start = f"{cursor_position} - {len(current_word)}c"
        text.delete(word_start, cursor_position)
        
        # Insert the snippet, handling new lines
        snippet = snippets[current_word]
        snippet_lines = snippet.split("\n")

        # Insert the first line at the current cursor position
        text.insert(tk.INSERT, snippet_lines[0])

        # Insert the remaining lines on new lines
        for line in snippet_lines[1:]:
            text.insert(tk.INSERT, f"\n{line}")
        hide_autocomplete()
        return "break"  # Prevent default behavior
    else: 
        insert_autocomplete()
        hide_autocomplete()    
        return "break"  # Prevent default behavior
        
        


text.bind("<Tab>", accept_autocomplete_or_snippet)

def on_arrow_key(event):
    if autocomplete_window:
        if event.keysym in ("Up", "Down"):
            # Prevent default behavior of moving cursor in the text widget
            return "break"

text.bind("<Up>", on_arrow_key)
text.bind("<Down>", on_arrow_key)

def on_arrow_key_in_listbox(event):
    global suggestion_listbox
    if not suggestion_listbox:
        return
    if event.keysym not in ("Up", "Down"):
        return
    current_selection = suggestion_listbox.curselection()
    if event.keysym == "Up":
        if current_selection:
            index = current_selection[0] - 1
        else:
            index = suggestion_listbox.size() - 1
    elif event.keysym == "Down":
        if current_selection:
            index = current_selection[0] + 1
        else:
            index = 0
    index = max(0, min(suggestion_listbox.size() - 1, index))
    suggestion_listbox.selection_clear(0, tk.END)
    suggestion_listbox.selection_set(index)
    suggestion_listbox.activate(index)
    suggestion_listbox.see(index)
    # Ensure Listbox retains focus
    suggestion_listbox.focus_set()
    return "break"  # Prevent further propagation of the event

def on_click_outside(event):
    if autocomplete_window and not autocomplete_window.winfo_containing(event.x_root, event.y_root):
        hide_autocomplete()

def on_space_press(event):
    if autocomplete_window:
        hide_autocomplete()

def hide_autocomplete(event=None):
    global autocomplete_window
    if autocomplete_window:
        autocomplete_window.destroy()
        autocomplete_window = None
        root.unbind("<Button-1>")  # Unbind the click outside event

#-------------------- Autocomplete and Snippets --------------------#

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