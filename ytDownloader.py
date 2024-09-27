#Welcome to the Youtube HD Video Downloader Tool code!
#Before using this code please remember to install:
#*pip install yt-dlp
#*ffmpeg

#This video downloader tool will use GUI as user interface.
#This tool downloads mp4 video and mp3 audio from Youtube.

import yt_dlp
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import time
import subprocess
import json

# Function to load user settings
def load_settings():
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        return {}

# Function to save user settings
def save_settings():
    settings = {
        'last_path': entry_path.get(),
        'download_type': download_type_var.get(),
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def download_video():
    link = entry_link.get()
    path = entry_path.get()
    download_type = download_type_var.get()

    if not link:
        messagebox.showerror("Input Error", "Please enter a YouTube video link.")
        return

    if not path:
        messagebox.showerror("Input Error", "Please select a download path.")
        return

    # Generate a timestamp to append to the filename to avoid overwriting
    timestamp = time.strftime('%Y%m%d-%H%M%S')

    # Set up download options for yt-dlp
    ydl_opts = {
        'ffmpeg_location': r'C:\ffmpeg',  # Specify the path to ffmpeg if necessary
        'outtmpl': os.path.join(path, f'%(title)s-{timestamp}.%(ext)s'),  # Output file template
        'noplaylist': True,  # Prevent downloading entire playlists
    }

    if download_type == "Video":
        ydl_opts['format'] = 'bestvideo+bestaudio/best'  # Download the best video and audio available
        ydl_opts['merge_output_format'] = 'mp4'  # Merge into mp4 format if necessary
    elif download_type == "Audio":
        ydl_opts['format'] = 'bestaudio/best'  # Download the best audio available
        ydl_opts['postprocessors'] = [{  # Convert to mp3 format
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        # Open the folder where the video was downloaded
        open_folder(path)

        messagebox.showinfo("Success", f"{download_type} download completed and folder opened!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_path.delete(0, tk.END)  # Clear previous entry
        entry_path.insert(0, folder_selected)  # Insert the new folder path

def open_folder(path):
    """Opens the folder containing the downloaded file."""
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS and Linux
        subprocess.run(['open', path] if os.uname().sysname == 'Darwin' else ['xdg-open', path])

def load_last_used_settings():
    """Load the last used settings for download path and type."""
    settings = load_settings()
    if 'last_path' in settings:
        entry_path.insert(0, settings['last_path'])
    if 'download_type' in settings:
        download_type_var.set(settings['download_type'])

def on_closing():
    """Handle the window closing event."""
    save_settings()  # Save settings before closing
    root.destroy()   # Close the window

# GUI Setup
root = tk.Tk()
root.title("YouTube Video Downloader")

# Labels and Entry Fields
tk.Label(root, text="YouTube Video Link:").pack()
entry_link = tk.Entry(root, width=50)
entry_link.pack()

tk.Label(root, text="Download Path:").pack()
entry_path = tk.Entry(root, width=50)
entry_path.pack()

# Browse button
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.pack()

# Download Type Selection
tk.Label(root, text="Select Download Type:").pack()
download_type_var = tk.StringVar(value='Video')  # Default to 'Video'
download_type_menu = tk.OptionMenu(root, download_type_var, 'Video', 'Audio')
download_type_menu.pack()

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack()

# Load last used settings
load_last_used_settings()

# Set up window close handling
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()