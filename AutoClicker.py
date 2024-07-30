import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput import keyboard

# Global variables to control the clicking
clicking = False
start_key = keyboard.Key.f1  # Default start hotkey
stop_key = keyboard.Key.f2  # Default stop hotkey
current_entry = None

# Function to start clicking
def start_clicking():
    global clicking
    if not clicking:
        clicking = True
        delay = float(delay_var.get())
        while clicking:
            pyautogui.click()
            time.sleep(delay)
        print("Clicking stopped")

# Function to stop clicking
def stop_clicking():
    global clicking
    clicking = False
    print("Stopping clicker...")

# Hotkey listener setup
def on_press(key):
    try:
        if key == start_key and not clicking:
            threading.Thread(target=start_clicking).start()
        elif key == stop_key:
            stop_clicking()
    except AttributeError:
        pass

# Function to update hotkeys
def set_hotkey(event):
    global start_key, stop_key, current_entry
    key_name = event.keysym
    if current_entry == start_key_entry:
        start_key_var.set(key_name)
        start_key = keyboard.KeyCode.from_char(key_name.lower()) if len(key_name) == 1 else getattr(keyboard.Key, key_name.lower(), None)
        print(f"Set start key to {key_name}")
        current_entry = None
        root.focus_set()  # Release focus from the text box
    elif current_entry == stop_key_entry:
        stop_key_var.set(key_name)
        stop_key = keyboard.KeyCode.from_char(key_name.lower()) if len(key_name) == 1 else getattr(keyboard.Key, key_name.lower(), None)
        print(f"Set stop key to {key_name}")
        current_entry = None
        root.focus_set()  # Release focus from the text box

# Function to focus the entry for setting hotkey
def focus_entry(entry):
    global current_entry
    current_entry = entry
    entry.focus_set()

# Function to handle Enter key press in delay entry
def handle_delay_entry(event):
    if event.keysym == 'Return':
        delay_entry.selection_range(0, tk.END)
        root.focus_set()

# GUI setup
root = tk.Tk()
root.title("Autoclicker")

# Variables for delay and hotkeys
delay_var = tk.StringVar(value="0.5")
start_key_var = tk.StringVar(value="F1")
stop_key_var = tk.StringVar(value="F2")

# GUI elements
ttk.Label(root, text="Delay between clicks (seconds):").grid(column=0, row=0, padx=10, pady=5)
delay_entry = ttk.Entry(root, textvariable=delay_var)
delay_entry.grid(column=1, row=0, padx=10, pady=5)
delay_entry.bind("<Return>", handle_delay_entry)

ttk.Label(root, text="Start Hotkey:").grid(column=0, row=1, padx=10, pady=5)
start_key_entry = ttk.Entry(root, textvariable=start_key_var)
start_key_entry.grid(column=1, row=1, padx=10, pady=5)
start_key_entry.bind("<FocusIn>", lambda event: focus_entry(start_key_entry))

ttk.Label(root, text="Stop Hotkey:").grid(column=0, row=2, padx=10, pady=5)
stop_key_entry = ttk.Entry(root, textvariable=stop_key_var)
stop_key_entry.grid(column=1, row=2, padx=10, pady=5)
stop_key_entry.bind("<FocusIn>", lambda event: focus_entry(stop_key_entry))

quit_button = ttk.Button(root, text="Quit", command=root.quit)
quit_button.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

# Bind the key press event to the root window
root.bind("<KeyPress>", lambda event: set_hotkey(event) if current_entry else None)

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run the GUI loop
root.mainloop()

# Stop the listener when the GUI is closed
listener.stop()
