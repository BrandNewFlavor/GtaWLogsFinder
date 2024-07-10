import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import json
import sys


folder_path = None
CONFIG_FILE_NAME = 'config.json'

# Function to get the path to the config file
def get_config_path():
    if hasattr(sys, '_MEIPASS'):
        # If running from PyInstaller bundle, use the bundle directory
        return os.path.join(os.path.dirname(sys.executable), CONFIG_FILE_NAME)
    else:
        # If running from script, use the script directory
        return os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)

def load_config():
    config_path = get_config_path()
    print(f"Loading config from: {config_path}")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
                print(f"Config loaded: {config}")
                return config
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            return {}
    else:
        print("Config file does not exist.")
    return {}

def save_config(config):
    config_path = get_config_path()
    print(f"Saving config to: {config_path}")
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)
    print(f"Config saved: {config}")

def find_lines_with_keyword(directory, keyword):
    lines_with_keyword = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):  # Check if the file is a text file
                filepath = os.path.join(root, filename)
                
                # Open the file and search for the keyword
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        if keyword in line:
                            lines_with_keyword.append((filepath, line.strip()))
    return lines_with_keyword

def open_file():
    global folder_path
    folder_path = filedialog.askdirectory(title="Select a folder")
    if folder_path:
        fileLabel.config(text=f"{folder_path}")
        save_config({'folder_path': folder_path})
        print(f"Selected folder: {folder_path}")

def open_results_window(results):
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")
    results_window.geometry("400x300")
    
    results_label = ttk.Label(results_window, text="Search Results:", style="TLabel")
    results_label.pack(pady=10)
    
    results_text = tk.Text(results_window, wrap="word")
    results_text.pack(expand=True, fill="both")
    
    for filename, line in results:
        results_text.insert("end", f'File: {filename}\nLine: {line}\n\n')

def search():
    if folder_path:
        keyword = keywordEntry.get()
        if keyword:
            matching_lines = find_lines_with_keyword(folder_path, keyword)
            if matching_lines:
                open_results_window(matching_lines)
            else:
                print("No matching lines found.")
        else:
            print("Keyword entry is empty")
    else:
        print("No folder selected")



# Create the main window
root = tk.Tk()
root.title("GTAW Logs Finder")
root.geometry("400x200")

# Apply styles
style = ttk.Style()
style.theme_use("clam")

# Define Bootstrap-like styles
style.configure("TLabel", foreground="#495057", font=("Helvetica", 10))
style.configure("TEntry", foreground="#495057", font=("Helvetica", 10))
style.configure("TButton", background="#007bff", foreground="#ffffff", font=("Helvetica", 10, "bold"), padding=6)
style.map("TButton",
          background=[("active", "#0056b3")])

# Main frame to hold all widgets
main_frame = ttk.Frame(root, padding="20", style="TFrame")
main_frame.pack(expand=True, fill="both")

# Set the background color of the main window
root.configure(background="#f8f9fa")

# Keyword Label
keywordLabel = ttk.Label(main_frame, text="Keyword:", style="TLabel")
keywordLabel.pack()

# Keyword Entry
keywordEntry = ttk.Entry(main_frame, width=30, style="TEntry")
keywordEntry.pack()

# Open Folder Button
folderButton = ttk.Button(main_frame, text="Open Folder", command=open_file, style="TButton")
folderButton.pack(pady=(10, 0))

# File Label
fileLabel = ttk.Label(main_frame, text="No folder selected", style="TLabel")
fileLabel.pack()

# Search Button
searchButton = ttk.Button(main_frame, text="Search", command=search, style="TButton")
searchButton.pack(pady=(10, 0))

# Load config file
config = load_config()
folder_path = config.get("folder_path", None)
if folder_path:
    fileLabel.config(text=f"{folder_path}")
    print(f"Loaded folder path: {folder_path}")

# Run the application
root.mainloop()
