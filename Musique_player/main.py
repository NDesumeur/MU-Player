import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import pygame
from pytubefix import YouTube

import re
from moviepy.editor import AudioFileClip
import os
import threading
import time
import random
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import json
from plyer import notification
from youtubesearchpython import VideosSearch
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
# Remote control server (optional)
try:
    from flask import Flask, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


# Système de thèmes
THEMES = {
    "Purple Dream": {
        "main_bg": "#0a0508",
        "sidebar_bg": "#0f0618",
        "gradient_top": "#2a1a4e",
        "accent": "#a370f7",
        "secondary": "#3a2a5e",
        "highlight": "#5a3ab7",
        "text": "#e0d5ff",
        "text_dim": "#7a6fa8",
        "card_bg": "#1a0f2e",
        "card_gradient": "#2a1a4e",
        "progress": "#a370f7",
        "progress_light": "#d4a5ff",
        "list_bg": "#0a0508",
        "control_bar": "#2a1a4e"
    },
    "Deep Blue": {
        "main_bg": "#0a1628",
        "sidebar_bg": "#0f1b2e",
        "gradient_top": "#1a3a5e",
        "accent": "#4da6ff",
        "secondary": "#2a4a7e",
        "highlight": "#3a7abf",
        "text": "#d5e8ff",
        "text_dim": "#6fa8d8",
        "card_bg": "#162840",
        "card_gradient": "#1a3a5e",
        "progress": "#4da6ff",
        "progress_light": "#7fc4ff",
        "list_bg": "#0a1628",
        "control_bar": "#1a3a5e"
    },
    "Sunset Vibes": {
        "main_bg": "#1a0a08",
        "sidebar_bg": "#2e1410",
        "gradient_top": "#5e2a1a",
        "accent": "#ff7043",
        "secondary": "#7e3a2a",
        "highlight": "#bf5a3a",
        "text": "#ffe0d5",
        "text_dim": "#d89a6f",
        "card_bg": "#2e1610",
        "card_gradient": "#5e2a1a",
        "progress": "#ff7043",
        "progress_light": "#ffa070",
        "list_bg": "#1a0a08",
        "control_bar": "#5e2a1a"
    },
    "Dark Matter": {
        "main_bg": "#000000",
        "sidebar_bg": "#0a0a0a",
        "gradient_top": "#1a1a1a",
        "accent": "#00ff88",
        "secondary": "#2a2a2a",
        "highlight": "#3a3a3a",
        "text": "#ffffff",
        "text_dim": "#888888",
        "card_bg": "#0f0f0f",
        "card_gradient": "#1a1a1a",
        "progress": "#00ff88",
        "progress_light": "#66ffaa",
        "list_bg": "#000000",
        "control_bar": "#1a1a1a"
    },
    "Cyberpunk": {
        "main_bg": "#0d0221",
        "sidebar_bg": "#160a2e",
        "gradient_top": "#2e1a4e",
        "accent": "#ff00ff",
        "secondary": "#3a2a5e",
        "highlight": "#7a3abf",
        "text": "#00ffff",
        "text_dim": "#aa6fff",
        "card_bg": "#1a0f3e",
        "card_gradient": "#2e1a4e",
        "progress": "#ff00ff",
        "progress_light": "#ff66ff",
        "list_bg": "#0d0221",
        "control_bar": "#2e1a4e"
    },
    "Forest Night": {
        "main_bg": "#0a1a0a",
        "sidebar_bg": "#0f2e0f",
        "gradient_top": "#1a5e1a",
        "accent": "#66ff66",
        "secondary": "#2a5e2a",
        "highlight": "#3a8f3a",
        "text": "#d5ffd5",
        "text_dim": "#6fd86f",
        "card_bg": "#162e16",
        "card_gradient": "#1a5e1a",
        "progress": "#66ff66",
        "progress_light": "#99ff99",
        "list_bg": "#0a1a0a",
        "control_bar": "#1a5e1a"
    },
    "Nord": {
        "main_bg": "#0b0e14",
        "sidebar_bg": "#11161e",
        "gradient_top": "#1c2430",
        "accent": "#88c0d0",
        "secondary": "#3b4252",
        "highlight": "#5e81ac",
        "text": "#e5e9f0",
        "text_dim": "#c0c8d6",
        "card_bg": "#1b212b",
        "card_gradient": "#2e3440",
        "progress": "#88c0d0",
        "progress_light": "#a9d4df",
        "list_bg": "#0b0e14",
        "control_bar": "#2e3440"
    },
    "Dracula": {
        "main_bg": "#0b0a10",
        "sidebar_bg": "#141221",
        "gradient_top": "#1e1b2e",
        "accent": "#bd93f9",
        "secondary": "#282a36",
        "highlight": "#6272a4",
        "text": "#f8f8f2",
        "text_dim": "#cfcfc7",
        "card_bg": "#1a1c26",
        "card_gradient": "#2a2c3a",
        "progress": "#bd93f9",
        "progress_light": "#d7bafc",
        "list_bg": "#0b0a10",
        "control_bar": "#2a2c3a"
    },
    "Tokyo Night": {
        "main_bg": "#0f1215",
        "sidebar_bg": "#131720",
        "gradient_top": "#1b2230",
        "accent": "#7aa2f7",
        "secondary": "#334155",
        "highlight": "#89b4fa",
        "text": "#cdd6f4",
        "text_dim": "#aab4c8",
        "card_bg": "#1a202e",
        "card_gradient": "#242b3a",
        "progress": "#7aa2f7",
        "progress_light": "#a6c2fb",
        "list_bg": "#0f1215",
        "control_bar": "#242b3a"
    },
    "Aurora": {
        "main_bg": "#071316",
        "sidebar_bg": "#0b1b20",
        "gradient_top": "#14313a",
        "accent": "#56d6c2",
        "secondary": "#1d4e57",
        "highlight": "#2b7a87",
        "text": "#d8f7f2",
        "text_dim": "#98cfc6",
        "card_bg": "#0f2429",
        "card_gradient": "#183a44",
        "progress": "#56d6c2",
        "progress_light": "#8be6d9",
        "list_bg": "#071316",
        "control_bar": "#183a44"
    },
    "Rose Gold": {
        "main_bg": "#1a1212",
        "sidebar_bg": "#241616",
        "gradient_top": "#4a2c2c",
        "accent": "#ffb7c5",
        "secondary": "#6e4a4a",
        "highlight": "#ff8fa3",
        "text": "#ffe9ee",
        "text_dim": "#e6c8cf",
        "card_bg": "#2a1a1a",
        "card_gradient": "#4a2c2c",
        "progress": "#ffb7c5",
        "progress_light": "#ffd1db",
        "list_bg": "#1a1212",
        "control_bar": "#4a2c2c"
    },
    "Material Ocean": {
        "main_bg": "#0a1114",
        "sidebar_bg": "#0f191d",
        "gradient_top": "#16323a",
        "accent": "#64ffda",
        "secondary": "#1f3b44",
        "highlight": "#26c6da",
        "text": "#d9f7f2",
        "text_dim": "#a8d8d0",
        "card_bg": "#13252b",
        "card_gradient": "#1c333b",
        "progress": "#64ffda",
        "progress_light": "#9dffe8",
        "list_bg": "#0a1114",
        "control_bar": "#1c333b"
    },
    "Gruvbox Dark": {
        "main_bg": "#1d2021",
        "sidebar_bg": "#282828",
        "gradient_top": "#3c3836",
        "accent": "#fabd2f",
        "secondary": "#504945",
        "highlight": "#d79921",
        "text": "#ebdbb2",
        "text_dim": "#d5c4a1",
        "card_bg": "#2c2c2c",
        "card_gradient": "#3c3836",
        "progress": "#fabd2f",
        "progress_light": "#fbd57a",
        "list_bg": "#1d2021",
        "control_bar": "#3c3836"
    },
    "Mint Fresh": {
        "main_bg": "#0b1512",
        "sidebar_bg": "#10201a",
        "gradient_top": "#1a3a2e",
        "accent": "#7cf1c8",
        "secondary": "#2a5e48",
        "highlight": "#59d7aa",
        "text": "#e5fff7",
        "text_dim": "#b7e6d6",
        "card_bg": "#153228",
        "card_gradient": "#1f4a3a",
        "progress": "#7cf1c8",
        "progress_light": "#aaf6db",
        "list_bg": "#0b1512",
        "control_bar": "#1f4a3a"
    },
    "Royal Purple": {
        "main_bg": "#0e0a14",
        "sidebar_bg": "#160f22",
        "gradient_top": "#2a1a4a",
        "accent": "#a98dfc",
        "secondary": "#3b2a6e",
        "highlight": "#8466f7",
        "text": "#ece6ff",
        "text_dim": "#cfc5f5",
        "card_bg": "#1a1330",
        "card_gradient": "#2a1a4a",
        "progress": "#a98dfc",
        "progress_light": "#c6b7ff",
        "list_bg": "#0e0a14",
        "control_bar": "#2a1a4a"
    },
    "Solarized Dark": {
        "main_bg": "#002b36",
        "sidebar_bg": "#073642",
        "gradient_top": "#0f4450",
        "accent": "#268bd2",
        "secondary": "#586e75",
        "highlight": "#2aa198",
        "text": "#eee8d5",
        "text_dim": "#93a1a1",
        "card_bg": "#083a45",
        "card_gradient": "#0f4450",
        "progress": "#268bd2",
        "progress_light": "#5fb3ee",
        "list_bg": "#002b36",
        "control_bar": "#0f4450"
    },
    "Solarized Light": {
        "main_bg": "#fdf6e3",
        "sidebar_bg": "#eee8d5",
        "gradient_top": "#d9d2c2",
        "accent": "#268bd2",
        "secondary": "#839496",
        "highlight": "#2aa198",
        "text": "#073642",
        "text_dim": "#586e75",
        "card_bg": "#efe7d6",
        "card_gradient": "#d9d2c2",
        "progress": "#268bd2",
        "progress_light": "#5fb3ee",
        "list_bg": "#fdf6e3",
        "control_bar": "#d9d2c2"
    },
    "Catppuccin Mocha": {
        "main_bg": "#1e1e2e",
        "sidebar_bg": "#181825",
        "gradient_top": "#313244",
        "accent": "#89b4fa",
        "secondary": "#45475a",
        "highlight": "#b4befe",
        "text": "#cdd6f4",
        "text_dim": "#a6adc8",
        "card_bg": "#24273a",
        "card_gradient": "#313244",
        "progress": "#89b4fa",
        "progress_light": "#a6c2fb",
        "list_bg": "#1e1e2e",
        "control_bar": "#313244"
    },
    "Catppuccin Latte": {
        "main_bg": "#eff1f5",
        "sidebar_bg": "#e6e9ef",
        "gradient_top": "#ccd0da",
        "accent": "#1e66f5",
        "secondary": "#acb0be",
        "highlight": "#7287fd",
        "text": "#4c4f69",
        "text_dim": "#6c6f85",
        "card_bg": "#dce0e8",
        "card_gradient": "#ccd0da",
        "progress": "#1e66f5",
        "progress_light": "#87a5ff",
        "list_bg": "#eff1f5",
        "control_bar": "#ccd0da"
    },
    "Monokai": {
        "main_bg": "#1b1c19",
        "sidebar_bg": "#23241f",
        "gradient_top": "#2e2f29",
        "accent": "#f92672",
        "secondary": "#75715e",
        "highlight": "#66d9ef",
        "text": "#f8f8f2",
        "text_dim": "#cfcfc7",
        "card_bg": "#24251f",
        "card_gradient": "#2e2f29",
        "progress": "#f92672",
        "progress_light": "#ff7fb0",
        "list_bg": "#1b1c19",
        "control_bar": "#2e2f29"
    },
    "One Dark": {
        "main_bg": "#0f1115",
        "sidebar_bg": "#161a20",
        "gradient_top": "#21252b",
        "accent": "#61afef",
        "secondary": "#3b4048",
        "highlight": "#98c379",
        "text": "#abb2bf",
        "text_dim": "#8b929c",
        "card_bg": "#1b2027",
        "card_gradient": "#21252b",
        "progress": "#61afef",
        "progress_light": "#9ad1ff",
        "list_bg": "#0f1115",
        "control_bar": "#21252b"
    },
    "Pastel Pop": {
        "main_bg": "#121316",
        "sidebar_bg": "#17191d",
        "gradient_top": "#2b2f36",
        "accent": "#ff9ecd",
        "secondary": "#5b6a82",
        "highlight": "#ffd580",
        "text": "#f4f7fa",
        "text_dim": "#cfd6df",
        "card_bg": "#1c1f25",
        "card_gradient": "#2b2f36",
        "progress": "#ff9ecd",
        "progress_light": "#ffc2df",
        "list_bg": "#121316",
        "control_bar": "#2b2f36"
    },
    "Neon Noir": {
        "main_bg": "#0a0a12",
        "sidebar_bg": "#121224",
        "gradient_top": "#1e1e3a",
        "accent": "#00ffd1",
        "secondary": "#3a3a5e",
        "highlight": "#ff2079",
        "text": "#e6e6ff",
        "text_dim": "#b3b3cc",
        "card_bg": "#151533",
        "card_gradient": "#1e1e3a",
        "progress": "#00ffd1",
        "progress_light": "#7fffe6",
        "list_bg": "#0a0a12",
        "control_bar": "#1e1e3a"
    },
    "Sakura Light": {
        "main_bg": "#fff7f9",
        "sidebar_bg": "#ffeef3",
        "gradient_top": "#ffdce6",
        "accent": "#ff6fae",
        "secondary": "#e3a1c2",
        "highlight": "#ffa7c9",
        "text": "#5a3144",
        "text_dim": "#8c5b74",
        "card_bg": "#ffe5ed",
        "card_gradient": "#ffdce6",
        "progress": "#ff6fae",
        "progress_light": "#ff9fc7",
        "list_bg": "#fff7f9",
        "control_bar": "#ffdce6"
    },
    "Midnight Teal": {
        "main_bg": "#071a1a",
        "sidebar_bg": "#0d2b2b",
        "gradient_top": "#154545",
        "accent": "#2dd4bf",
        "secondary": "#1f6060",
        "highlight": "#38b2ac",
        "text": "#d7fffb",
        "text_dim": "#a8e9e3",
        "card_bg": "#0f3535",
        "card_gradient": "#154545",
        "progress": "#2dd4bf",
        "progress_light": "#74e7db",
        "list_bg": "#071a1a",
        "control_bar": "#154545"
    }
}


def convert_webm_to_mp3(webm_file, mp3_file):
    audio = AudioFileClip(webm_file)
    audio.write_audiofile(mp3_file)


class CustomUrlDialog(tk.Toplevel):
    def __init__(self, parent, title, label_text):
        super().__init__(parent)
        self.title(title)
        self.geometry("450x220")
        self.configure(bg="#1a1a1a")
        self.iconbitmap('logo.ico')
        self.resizable(False, False)

        # Frame principal avec padding
        main_frame = tk.Frame(self, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.label = tk.Label(main_frame, text=label_text, bg="#1a1a1a", fg="#ffffff", 
                            font=("Segoe UI", 12, "bold"))
        self.label.pack(pady=(0, 15))

        self.entry = tk.Entry(main_frame, bg="#2d2d2d", fg="#ffffff", font=("Segoe UI", 11),
                            relief=tk.FLAT, insertbackground="#ffffff", bd=0)
        self.entry.pack(pady=10, padx=10, ipady=8, fill=tk.X)

        self.button_frame = tk.Frame(main_frame, bg="#1a1a1a")
        self.button_frame.pack(pady=15)

        self.ok_button = tk.Button(self.button_frame, text="✓ OK", command=self.on_ok, 
                                   bg="#1db954", fg="white", font=("Segoe UI", 10, "bold"),
                                   relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        self.ok_button.grid(row=0, column=0, padx=8)
        self.ok_button.bind("<Enter>", lambda e: self.ok_button.config(bg="#1ed760"))
        self.ok_button.bind("<Leave>", lambda e: self.ok_button.config(bg="#1db954"))

        self.cancel_button = tk.Button(self.button_frame, text="✕ Annuler", command=self.on_cancel,
                                       bg="#535353", fg="white", font=("Segoe UI", 10, "bold"),
                                       relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        self.cancel_button.grid(row=0, column=1, padx=8)
        self.cancel_button.bind("<Enter>", lambda e: self.cancel_button.config(bg="#6a6a6a"))
        self.cancel_button.bind("<Leave>", lambda e: self.cancel_button.config(bg="#535353"))

        self.result = None
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.on_ok())

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.destroy()


class CustomYesNoDialog(tk.Toplevel):
    def __init__(self, parent, title, label_text):
        super().__init__(parent)
        self.title(title)
        self.configure(bg="#1a1a1a")
        self.iconbitmap('logo.ico')
        self.resizable(False, False)

        main_frame = tk.Frame(self, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        self.label = tk.Label(main_frame, text=label_text, bg="#1a1a1a", fg="white",
                            font=("Segoe UI", 11))
        self.label.pack(pady=(0, 20))

        self.button_frame = tk.Frame(main_frame, bg="#1a1a1a")
        self.button_frame.pack(pady=10)

        self.yes_button = tk.Button(self.button_frame, text="✓ Oui", command=self.on_yes,
                                    bg="#1db954", fg="white", font=("Segoe UI", 10, "bold"),
                                    relief=tk.FLAT, cursor="hand2", padx=25, pady=8)
        self.yes_button.grid(row=0, column=0, padx=8)
        self.yes_button.bind("<Enter>", lambda e: self.yes_button.config(bg="#1ed760"))
        self.yes_button.bind("<Leave>", lambda e: self.yes_button.config(bg="#1db954"))

        self.no_button = tk.Button(self.button_frame, text="✕ Non", command=self.on_no,
                                   bg="#535353", fg="white", font=("Segoe UI", 10, "bold"),
                                   relief=tk.FLAT, cursor="hand2", padx=25, pady=8)
        self.no_button.grid(row=0, column=1, padx=8)
        self.no_button.bind("<Enter>", lambda e: self.no_button.config(bg="#6a6a6a"))
        self.no_button.bind("<Leave>", lambda e: self.no_button.config(bg="#535353"))

        self.result = None

    def on_yes(self):
        self.result = True
        self.destroy()

    def on_no(self):
        self.result = False
        self.destroy()


def ask_custom_yesno(parent, title, label_text):
    dialog = CustomYesNoDialog(parent, title, label_text)
    parent.wait_window(dialog)
    return dialog.result


class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title, label_text):
        super().__init__(parent)
        self.title(title)
        self.configure(bg="#1a1a1a")
        self.iconbitmap('logo.ico')
        self.resizable(False, False)

        main_frame = tk.Frame(self, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.label = tk.Label(main_frame, text=label_text, bg="#1a1a1a", fg="white",
                            font=("Segoe UI", 11))
        self.label.pack(pady=(0, 15))

        self.entry = tk.Entry(main_frame, bg="#2d2d2d", fg="white", font=("Segoe UI", 11),
                            relief=tk.FLAT, insertbackground="white", bd=0)
        self.entry.pack(pady=10, ipady=8, fill=tk.X)

        self.button_frame = tk.Frame(main_frame, bg="#1a1a1a")
        self.button_frame.pack(pady=15)

        self.ok_button = tk.Button(self.button_frame, text="✓ OK", command=self.on_ok,
                                   bg="#1db954", fg="white", font=("Segoe UI", 10, "bold"),
                                   relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        self.ok_button.grid(row=0, column=0, padx=8)

        self.cancel_button = tk.Button(self.button_frame, text="✕ Annuler", command=self.on_cancel,
                                       bg="#535353", fg="white", font=("Segoe UI", 10, "bold"),
                                       relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
        self.cancel_button.grid(row=0, column=1, padx=8)

        self.result = None
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.on_ok())

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.destroy()


def ask_custom_string(parent, title, label_text):
    dialog = CustomDialog(parent, title, label_text)
    parent.wait_window(dialog)
    return dialog.result


class ProgressBar(tk.Canvas):
    def __init__(self, master, theme, **kwargs):
        super().__init__(master, **kwargs)
        self.theme = theme
        self.progress = 0.0
        self.callback = None
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Configure>", lambda e: self.draw())
        self.draw()

    def set_theme(self, theme):
        self.theme = theme
        # Mettre à jour les couleurs immédiatement
        try:
            self.configure(bg=self.theme.get("card_bg", self["bg"]))
        except Exception:
            pass
        self.draw()

    def draw(self):
        self.delete("all")
        width = self.winfo_width() or 1
        height = self.winfo_height() or 1
        y = height // 2
        
        # Glow externe
        self.create_rectangle(0, y-8, width, y+8, fill=self.theme["accent"], outline="")
        
        # Fond avec bordure
        self.create_rectangle(2, y-5, width-2, y+5, fill=self.theme["main_bg"], outline="")
        self.create_rectangle(3, y-4, width-3, y+4, fill=self.theme["control_bar"], outline="")
        
        # Progression avec effet néon
        progress_width = width * self.progress
        if progress_width > 5:
            # Glow de progression
            self.create_rectangle(3, y-6, progress_width, y+6, fill=self.theme["progress"], outline="")
            # Barre principale
            self.create_rectangle(3, y-4, progress_width, y+4, fill=self.theme["progress"], outline="")
            # Highlight brillant sur le dessus
            self.create_rectangle(3, y-4, progress_width, y-2, fill=self.theme["progress_light"], outline="")
        
        # Curseur avec glow néon
        if progress_width > 10:
            # Glow externe large
            self.create_oval(progress_width-12, y-12, progress_width+12, y+12,
                           fill=self.theme["accent"], outline="")
            # Glow interne
            self.create_oval(progress_width-10, y-10, progress_width+10, y+10,
                           fill=self.theme["accent"], outline="")
            # Curseur principal
            self.create_oval(progress_width-8, y-8, progress_width+8, y+8,
                           fill="#ffffff", outline="")
            # Point central néon
            self.create_oval(progress_width-5, y-5, progress_width+5, y+5,
                           fill=self.theme["progress"], outline="")

    def set_progress(self, value):
        self.progress = max(0.0, min(1.0, value))
        self.draw()

    def on_click(self, event):
        width = self.winfo_width()
        self.progress = event.x / width
        self.draw()
        if self.callback:
            self.callback(self.progress)

    def on_drag(self, event):
        self.on_click(event)

    def set_callback(self, callback):
        self.callback = callback


class CustomScale(tk.Canvas):
    def __init__(self, master, theme, command, **kwargs):
        super().__init__(master, **kwargs)
        self.theme = theme
        self.command = command
        self.min_val = 0.0
        self.max_val = 1.0
        self.current_val = 0.1
        self.bind("<Button-1>", self.update_val)
        self.bind("<B1-Motion>", self.update_val)
        self.bind("<Enter>", lambda e: self.config(cursor="hand2"))
        self.bind("<Leave>", lambda e: self.config(cursor=""))
        self.bind("<Configure>", lambda e: self.draw_elements())
        self.draw_elements()

    def draw_elements(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Glow de fond
        self.create_line(10, height//2, width-10, height//2, fill=self.theme["accent"], width=10)
        
        # Ligne de fond
        self.create_line(10, height//2, width-10, height//2, fill=self.theme["sidebar_bg"], width=6)
        self.create_line(10, height//2, width-10, height//2, fill=self.theme["control_bar"], width=4)
        
        # Ligne de progression avec néon
        pos_x = 10 + (self.current_val * (width-20))
        if pos_x > 10:
            # Glow de progression
            self.create_line(10, height//2, pos_x, height//2, fill=self.theme["progress"], width=8)
            # Barre principale
            self.create_line(10, height//2, pos_x, height//2, fill=self.theme["progress"], width=6)
            # Highlight
            self.create_line(10, height//2-1, pos_x, height//2-1, fill=self.theme["progress_light"], width=3)
        
        # Curseur avec glow
        if pos_x > 10:
            # Glow externe
            self.create_oval(pos_x-11, height//2-11, pos_x+11, height//2+11, 
                           fill=self.theme["accent"], outline="")
            # Glow interne
            self.create_oval(pos_x-9, height//2-9, pos_x+9, height//2+9, 
                           fill=self.theme["accent"], outline="")
            # Curseur
            self.create_oval(pos_x-7, height//2-7, pos_x+7, height//2+7, 
                           fill="#ffffff", outline="")
            # Centre néon
            self.create_oval(pos_x-4, height//2-4, pos_x+4, height//2+4, 
                           fill=self.theme["progress"], outline="")

    def update_val(self, event):
        width = self.winfo_width()
        self.current_val = min(max((event.x - 10) / (width-20), self.min_val), self.max_val)
        self.draw_elements()
        self.command(self.current_val)

    def set_value(self, val: float):
        self.current_val = min(max(val, self.min_val), self.max_val)
        self.draw_elements()


def set_volume(val):
    volume_level = float(val)
    pygame.mixer.music.set_volume(volume_level)


def ask_custom_url(parent, title, label_text):
    dialog = CustomUrlDialog(parent, title, label_text)
    parent.wait_window(dialog)
    return dialog.result


class MusicPlayer:
    def __init__(self, master):
        self.playlist_names = []
        self.playlist = []
        self.master = master
        self.master.iconbitmap('logo.ico')
        self.master.title(" Mu Player ")
        self.master.attributes('-fullscreen', True)  # True fullscreen over taskbar
        
        # Charger les paramètres
        self.settings_file = 'jsons/settings.json'
        self.load_settings()
        
        # Appliquer le dimensionnement des polices sauvegardé
        font_scale = self.settings.get("font_scale", "normal")
        
    
        self.master.config(bg=self.theme["main_bg"])
        
        self.current_song_path = None
        self.current_song_index = -1  # Track l'index courant dans self.playlist
        self.seek_offset_ms = 0
        self.ignore_end_event_until = 0  # <-- ajout
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(0.5)
        
        self.load_playlist_names()
        self.c = self.theme["card_bg"]
        self.accent_color = self.theme["accent"]
        
        # Container principal
        self.main_container = tk.Frame(self.master, bg=self.theme["main_bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Bouton de contrôle de fenêtre (top-right)
        self.window_controls = tk.Frame(self.master, bg=self.theme["main_bg"])
        self.window_controls.place(relx=1.0, x=-10, y=10, anchor="ne")
        
        def create_window_button(parent, text, command, bg=None):
            if bg is None:
                bg = self.theme["secondary"]
            btn = tk.Button(parent, text=text, command=command, bg=bg, fg=self.theme["text"],
                          font=("Segoe UI", 9, "bold"), relief=tk.FLAT, cursor="hand2",
                          padx=12, pady=6, bd=0, highlightthickness=0)
            btn.pack(side=tk.LEFT, padx=3)
            btn.bind("<Enter>", lambda e: btn.config(bg=self.theme["highlight"]))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg))
            return btn
        
        self.minimize_button = create_window_button(self.window_controls, "➖", lambda: self.master.iconify())
        
        # SIDEBAR GAUCHE avec effet gradient
        self.sidebar = tk.Frame(self.main_container, bg=self.theme["sidebar_bg"], width=300)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Gradient simulé avec Frame interne
        self.gradient_top = tk.Frame(self.sidebar, bg=self.theme["gradient_top"], height=5)
        self.gradient_top.pack(fill=tk.X)
        
        # Logo/Titre avec style premium
        self.title_frame = tk.Frame(self.sidebar, bg=self.theme["sidebar_bg"])
        self.title_frame.pack(pady=25, padx=20)
        # Icône de l'application à la place de la note
        try:
            icon_img = Image.open('logo.ico').convert('RGBA')
            icon_img = icon_img.resize((64, 64), Image.Resampling.LANCZOS)
            self.app_icon_img = ImageTk.PhotoImage(icon_img)
            tk.Label(self.title_frame, image=self.app_icon_img, bg=self.theme["sidebar_bg"]).pack()
        except Exception:
            # Fallback si l'icône n'est pas disponible
            tk.Label(self.title_frame, text="", bg=self.theme["sidebar_bg"], fg=self.theme["accent"],
                font=("Segoe UI", 1)).pack()
        tk.Label(self.title_frame, text="MU Player", bg=self.theme["sidebar_bg"], fg=self.theme["text"],
            font=("Segoe UI", 16, "bold")).pack()
        
        # Sélecteur de playlist avec style moderne
        self.playlist_frame = tk.Frame(self.sidebar, bg=self.theme["sidebar_bg"])
        self.playlist_frame.pack(pady=15, padx=20, fill=tk.X)
        
        tk.Label(self.playlist_frame, text="🎶 PLAYLISTS", bg=self.theme["sidebar_bg"], fg=self.theme["text_dim"],
                font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        self.playlist_name = tk.StringVar(self.master)
        self.playlist_name.set("Favoris")
        self.playlist_name.trace("w", self.load_new_playlist)
        
        self.playlist_menu = tk.OptionMenu(self.playlist_frame, self.playlist_name, *self.playlist_names)
        self.playlist_menu.config(bg=self.theme["card_gradient"], fg=self.theme["text"], activebackground=self.theme["secondary"],
                                 activeforeground=self.theme["text"], highlightthickness=0, relief=tk.FLAT,
                                 font=("Segoe UI", 11, "bold"), anchor=tk.W, cursor="hand2",
                                 padx=15, pady=10)
        self.playlist_menu.pack(fill=tk.X, ipady=8)
        
        menu = self.playlist_menu.nametowidget(self.playlist_menu.menuname)
        menu.config(bg=self.theme["card_bg"], fg=self.theme["text"], relief=tk.FLAT, bd=0)
        for i in range(menu.index('end') + 1):
            menu.entryconfig(i, activebackground=self.theme["secondary"], activeforeground=self.theme["text"])
        
        # Boutons sidebar avec style premium
        def create_sidebar_button(parent, text, command):
            btn = tk.Button(parent, text=text, command=command, bg=self.theme["card_gradient"], fg=self.theme["text"],
                          font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2",
                          anchor=tk.W, padx=20, pady=12, bd=0, highlightthickness=1, highlightbackground=self.theme["secondary"])
            btn.pack(fill=tk.X, pady=8, padx=12)
            btn.bind("<Enter>", lambda e: btn.config(bg=self.theme["accent"], fg=self.theme["sidebar_bg"], highlightbackground=self.theme["accent"]))
            btn.bind("<Leave>", lambda e: btn.config(bg=self.theme["card_gradient"], fg=self.theme["text"], highlightbackground=self.theme["secondary"]))
            return btn
        
        create_sidebar_button(self.sidebar, "➕ Nouvelle playlist", self.new_playlist)
        
        # Bouton Paramètres
        create_sidebar_button(self.sidebar, "⚙ Paramètres", self.open_settings)
        
        # Options de tri premium
        tk.Label(self.sidebar, text="⚙ TRIER PAR", bg=self.theme["sidebar_bg"], fg=self.theme["text_dim"],
                font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(25, 10), padx=20)
        
        self.sort_options = ["Par date d'ajout", "Par ordre alphabétique", "Par auteur", "Par date de création"]
        self.sort_var = tk.StringVar(value=self.sort_options[0])
        
        self.sort_menu = tk.OptionMenu(self.sidebar, self.sort_var, *self.sort_options, command=self.sort_playlist)
        self.sort_menu.config(bg=self.theme["card_gradient"], fg=self.theme["text"], activebackground=self.theme["accent"],
                             activeforeground=self.theme["sidebar_bg"], highlightthickness=0, relief=tk.FLAT,
                             font=("Segoe UI", 10), anchor=tk.W, cursor="hand2", padx=15, pady=8)
        self.sort_menu.pack(fill=tk.X, padx=10, ipady=5)
        
        sort_m = self.sort_menu.nametowidget(self.sort_menu.menuname)
        sort_m.config(bg=self.theme["card_bg"], fg=self.theme["text"])
        for i in range(len(self.sort_options)):
            sort_m.entryconfig(i, activebackground=self.theme["secondary"], activeforeground=self.theme["text"])
        
        # ZONE CENTRALE avec fond gradient
        self.center_frame = tk.Frame(self.main_container, bg=self.theme["main_bg"])
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Canvas de fond avec gradient doux
        self.center_bg = tk.Canvas(self.center_frame, bg=self.theme["main_bg"], highlightthickness=0, bd=0)
        self.center_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.center_frame.bind("<Configure>", lambda e: self.draw_center_gradient())
        
        # Section Now Playing avec glassmorphism
        shadow_outer = tk.Frame(self.center_frame, bg=self.theme["main_bg"])
        shadow_outer.pack(fill=tk.BOTH, expand=True, padx=30, pady=(30, 15))
        
        shadow_frame = tk.Frame(shadow_outer, bg=self.theme["sidebar_bg"])
        shadow_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Gradient de fond
        self.gradient_bg = tk.Frame(shadow_frame, bg=self.theme["card_gradient"])
        self.gradient_bg.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        self.now_playing_frame = tk.Frame(self.gradient_bg, bg=self.theme["card_bg"], highlightthickness=2, highlightbackground=self.theme["accent"])
        self.now_playing_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Frame pour pochette + infos avec fond gradient
        info_container = tk.Frame(self.now_playing_frame, bg=self.theme["card_bg"])
        info_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Pochette avec glow effect
        self.album_frame = tk.Frame(info_container, bg=self.theme["card_bg"])
        self.album_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        # Glow externe
        self.glow_outer = tk.Frame(self.album_frame, bg=self.theme["accent"], padx=8, pady=8)
        self.glow_outer.pack()
        
        # Glow interne
        self.glow_inner = tk.Frame(self.glow_outer, bg=self.theme["highlight"], padx=5, pady=5)
        self.glow_inner.pack()
        
        # Bordure principale
        self.art_border = tk.Frame(self.glow_inner, bg=self.theme["highlight"], padx=3, pady=3)
        self.art_border.pack()
        
        self.album_art_label = tk.Label(self.art_border, bg=self.theme["sidebar_bg"], width=180, height=180)
        self.album_art_label.pack()
        self.set_default_album_art()
        
        # Infos musique
        song_info_frame = tk.Frame(info_container, bg=self.theme["card_bg"])
        song_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Titre de la chanson
        self.current_song_label = tk.Label(song_info_frame, text="Aucune musique en cours",
                                          bg=self.theme["card_bg"], fg=self.theme["text"],
                                          font=("Segoe UI", 20, "bold"), anchor=tk.W,
                                          wraplength=800)
        self.current_song_label.pack(anchor=tk.W, pady=(15, 2))
        
        # Artiste
        self.artist_label = tk.Label(song_info_frame, text="",
                                    bg=self.theme["card_bg"], fg=self.theme["text_dim"],
                                    font=("Segoe UI", 12, ""), anchor=tk.W,
                                    wraplength=800)
        self.artist_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Infos supplémentaires (album, date, etc)
        self.info_label = tk.Label(song_info_frame, text="",
                                  bg=self.theme["card_bg"], fg=self.theme["text_dim"],
                                  font=("Segoe UI", 10, ""), anchor=tk.W,
                                  wraplength=800)
        self.info_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Temps
        self.time_label = tk.Label(song_info_frame, text="0:00 / 0:00", bg=self.theme["card_bg"],
                                   fg=self.theme["accent"], font=("Consolas", 13, "bold"), anchor=tk.W)
        self.time_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Barre de progression premium
        self.progress_bar = ProgressBar(song_info_frame, self.theme, bg=self.theme["card_bg"], height=45,
                                       highlightthickness=0)
        self.progress_bar.pack(fill=tk.X, pady=(10, 12))
        self.progress_bar.set_callback(self.on_progress_click)
        
        self.recommended_url = ""
        self.current_song_length = 0
        
        # Recommandation INDÉPENDANTE - directement dans center_frame
        self.recommendation_frame = tk.Frame(
            self.center_frame,
            bg=self.theme["card_gradient"],
            highlightthickness=2,
            highlightbackground=self.theme["accent"],
            height=100
        )
        self.recommendation_frame.pack(fill=tk.X, padx=30, pady=(15, 15))
        self.recommendation_frame.pack_propagate(False)
        
        self.recommendation_label = tk.Label(
            self.recommendation_frame,
            text="",
            bg=self.theme["card_gradient"],
            fg=self.theme["text"],
            font=("Segoe UI", 14, "bold"),
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=1000
        )
        self.recommendation_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=15, side=tk.LEFT)
        
        self.recommendation_button = tk.Button(
            self.recommendation_frame,
            text="➕ AJOUTER",
            command=self.add_recommended_song,
            bg=self.theme["accent"],
            fg=self.theme["sidebar_bg"],
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            bd=0,
            highlightthickness=0
        )
        self.recommendation_button.pack(side=tk.RIGHT, anchor=tk.E, padx=15, pady=10)
        self.recommendation_button.pack_forget()  # Caché par défaut
        
        # Ajuste automatiquement la largeur du texte aux dimensions du cadre recommandation
        self.recommendation_frame.bind(
            "<Configure>",
            lambda e: self.recommendation_label.config(wraplength=max(e.width - 100, 200))
        )
        
        # Liste de lecture avec header premium
        self.list_header = tk.Frame(self.center_frame, bg=self.theme["main_bg"])
        self.list_header.pack(fill=tk.X, padx=30, pady=(20, 12))
        
        # Icone + titre
        self.title_container = tk.Frame(self.list_header, bg=self.theme["main_bg"])
        self.title_container.pack(side=tk.LEFT)


        
        # Ligne de séparation avec gradient
        self.separator_container = tk.Frame(self.center_frame, bg=self.theme["main_bg"], height=3)
        self.separator_container.pack(fill=tk.X, padx=30, pady=(0, 12))
        self.separator = tk.Frame(self.separator_container, bg=self.theme["accent"], height=2)
        self.separator.pack(fill=tk.X)
        
        # Listbox premium avec background sombre
        self.list_container = tk.Frame(self.center_frame, bg=self.theme["sidebar_bg"], highlightthickness=1, highlightbackground=self.theme["card_gradient"])
        self.list_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 15))
        
        self.playlistbox = tk.Listbox(self.list_container, selectmode=tk.BROWSE,
                                      bg=self.theme["list_bg"], fg=self.theme["text"],
                                      selectbackground=self.theme["accent"],
                                      selectforeground=self.theme["sidebar_bg"],
                                      font=("Segoe UI", 12),
                                      relief=tk.FLAT, highlightthickness=0,
                                      activestyle='none', bd=0)
        self.playlistbox.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # BARRE DE CONTRÔLE avec glassmorphism
        self.border_glow = tk.Frame(self.master, bg=self.theme["accent"], height=2)
        self.border_glow.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.border_top = tk.Frame(self.master, bg=self.theme["accent"], height=2)
        self.border_top.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.control_bar = tk.Frame(self.master, bg=self.theme["control_bar"], height=100)
        self.control_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.control_bar.pack_propagate(False)
        
        # Boutons de contrôle
        self.controls_container = tk.Frame(self.control_bar, bg=self.theme["control_bar"])
        self.controls_container.pack(expand=True)
        
        def create_control_button(parent, text, command, bg_color=None):
            if bg_color is None:
                bg_color = self.theme["secondary"]
            btn = tk.Button(parent, text=text, command=command, bg=bg_color, fg=self.theme["text"],
                          font=("Segoe UI", 14, "bold"), relief=tk.FLAT, cursor="hand2",
                          padx=18, pady=10, bd=0, highlightthickness=2, highlightbackground=self.theme["control_bar"])
            btn.pack(side=tk.LEFT, padx=8)
            if bg_color == self.theme["secondary"]:
                hover_color = self.theme["highlight"]
            else:
                hover_color = self.theme["highlight"]
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_color, highlightbackground=self.theme["accent"]))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_color, highlightbackground=self.theme["control_bar"]))
            return btn
        
        create_control_button(self.controls_container, "⏮", self.play_previous_song)
        create_control_button(self.controls_container, "▶", self.play_song, self.accent_color)
        create_control_button(self.controls_container, "⏸", self.pause_song)
        create_control_button(self.controls_container, "▶▶", self.unpause_song, self.accent_color)
        create_control_button(self.controls_container, "⏭", self.play_next_song)
        create_control_button(self.controls_container, "🔀", self.shuffle_play)
        create_control_button(self.controls_container, "❤", self.toggle_favorite, self.theme["secondary"])
        
        # Barre de volume premium - nouveau design
        self.volume_frame = tk.Frame(self.control_bar, bg=self.theme["control_bar"])
        self.volume_frame.pack(side=tk.RIGHT, padx=25, anchor=tk.CENTER)
        
        tk.Label(self.volume_frame, text="🔊", bg=self.theme["control_bar"], fg=self.theme["accent"],
                font=("Segoe UI", 14)).pack(side=tk.LEFT, padx=(0, 12), anchor=tk.CENTER)
        
        # Nouveau volume slider avec style moderne élégant
        class ModernVolumeSlider(tk.Canvas):
            def __init__(self, parent, theme, command=None, **kwargs):
                super().__init__(parent, width=150, height=24, bg=theme["control_bar"], highlightthickness=0, **kwargs)
                self.theme = theme
                self.command = command
                self.value = 0.5
                self.bind("<Button-1>", self.on_click)
                self.bind("<B1-Motion>", self.on_drag)
                self.draw()

            def set_theme(self, theme):
                self.theme = theme
                try:
                    self.configure(bg=self.theme.get("control_bar", self["bg"]))
                except Exception:
                    pass
                self.draw()
            
            def on_click(self, event):
                self.value = max(0, min(1, event.x / self.winfo_width()))
                self.draw()
                if self.command:
                    self.command(self.value)
            
            def on_drag(self, event):
                self.value = max(0, min(1, event.x / self.winfo_width()))
                self.draw()
                if self.command:
                    self.command(self.value)
            
            def draw(self):
                self.delete("all")
                width = self.winfo_width()
                height = self.winfo_height()
                
                # Barre de fond avec glow subtil
                self.create_rectangle(8, height//2-3, width-8, height//2+3, fill=self.theme["card_bg"], outline="")
                self.create_rectangle(8, height//2-3, width-8, height//2+3, outline=self.theme["highlight"], width=1)
                
                # Barre de progression remplie
                progress_x = 8 + (width - 16) * self.value
                if progress_x > 8:
                    self.create_rectangle(8, height//2-3, progress_x, height//2+3, fill=self.theme["progress"], outline="")
                    # Highlight sur la progression
                    self.create_rectangle(8, height//2-3, progress_x, height//2-1, fill=self.theme["progress_light"], outline="")
                
                # Curseur
                cursor_x = 8 + (width - 16) * self.value
                self.create_oval(cursor_x-6, height//2-7, cursor_x+6, height//2+7, fill=self.theme["progress"], outline="#ffffff", width=2)
                # Centre blanc du curseur
                self.create_oval(cursor_x-3, height//2-3, cursor_x+3, height//2+3, fill="#ffffff", outline="")
            
            def set_value(self, val):
                self.value = val
                self.draw()
        
        self.volume = tk.DoubleVar(self.master)
        self.volume.set(pygame.mixer.music.get_volume())
        volume_slider = ModernVolumeSlider(self.volume_frame, self.theme, command=set_volume)
        volume_slider.set_value(self.volume.get())
        volume_slider.pack(side=tk.LEFT)
        self.volume_scale = volume_slider
        
        # Boutons d'action premium
        self.actions_frame = tk.Frame(self.control_bar, bg=self.theme["control_bar"])
        self.actions_frame.pack(side=tk.LEFT, padx=20)
        
        def create_small_button(parent, text, command, bg_color=None):
            if bg_color is None:
                bg_color = self.theme["secondary"]
            btn = tk.Button(parent, text=text, command=command, bg=bg_color, fg=self.theme["text"],
                          font=("Segoe UI", 9), relief=tk.FLAT, cursor="hand2",
                          padx=10, pady=6, bd=0, highlightthickness=0)
            btn.pack(side=tk.LEFT, padx=4)
            btn.bind("<Enter>", lambda e: btn.config(bg=self.theme["highlight"]))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
            return btn
        
        create_small_button(self.actions_frame, "📁 Fichier", self.add_songs_from_file, self.theme["secondary"])
        create_small_button(self.actions_frame, "🎬 YouTube", self.add_youtube_to_playlist, self.theme["accent"])
        create_small_button(self.actions_frame, "🔍 Chercher", self.search_music, self.theme["secondary"])
        create_small_button(self.actions_frame, "🗑 Suppr", self.delete_song, self.theme["highlight"])
        
        self.metadata_file = 'jsons/metadata.json'
        if not os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'w') as f:
                json.dump([], f)
        
        self.load_metadata()
        self.music_folder = "musics/"
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)
        
        # Dossier pour les pochettes
        self.covers_folder = "covers/"
        if not os.path.exists(self.covers_folder):
            os.makedirs(self.covers_folder)
        
        self.master.after(1000, self.check_for_pygame_events)
        self.master.after(100, self.update_time_label)
        # Gestion fermeture propre
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Raccourcis clavier
        self.master.bind("<space>", lambda e: self.toggle_play_pause())
        self.master.bind("<Right>", lambda e: self.play_next_song())
        self.master.bind("<Left>", lambda e: self.play_previous_song())
        self.master.bind("<Escape>", lambda e: self.master.attributes('-fullscreen', False))
        self.master.bind("<F11>", lambda e: self.master.attributes('-fullscreen', True))
        
        # Appliquer le dimensionnement des polices après création de tous les widgets
        self.master.after(100, lambda: self.apply_font_scale(font_scale))

        # Démarrer le serveur de télécommande web si disponible
        self.remote_port = 5000
        if FLASK_AVAILABLE:
            try:
                threading.Thread(target=self._start_remote_server, daemon=True).start()
            except Exception:
                pass

    def _schedule(self, func, *args, **kwargs):
        """Exécute une action côté UI de façon thread-safe."""
        try:
            self.master.after(0, lambda: func(*args, **kwargs))
        except Exception:
            try:
                func(*args, **kwargs)
            except Exception:
                pass

    def _start_remote_server(self):
        if not FLASK_AVAILABLE:
            return
        app = Flask(__name__)

        @app.route('/status')
        def status():
            try:
                playing = bool(pygame.mixer.music.get_busy())
                pos_ms = max(0, self.seek_offset_ms + max(0, pygame.mixer.music.get_pos())) if hasattr(self, 'seek_offset_ms') else 0
                duration_ms = int(self.current_song_length) if hasattr(self, 'current_song_length') else 0
                title = self.current_song_label.cget('text') if hasattr(self, 'current_song_label') else 'Pas de musique'
                artist = self.artist_label.cget('text') if hasattr(self, 'artist_label') else ''
                vol = float(pygame.mixer.music.get_volume())
                return jsonify({
                    'playing': playing,
                    'position_sec': round(pos_ms/1000, 2),
                    'duration_sec': round(duration_ms/1000, 2),
                    'title': title,
                    'artist': artist,
                    'volume': vol
                })
            except Exception as e:
                return jsonify({'error': str(e)})

        @app.route('/play', methods=['POST'])
        def play():
            try:
                self._schedule(self.unpause_song)
                return jsonify({'ok': True})
            except:
                return jsonify({'ok': False})

        @app.route('/pause', methods=['POST'])
        def pause():
            try:
                self._schedule(self.pause_song)
                return jsonify({'ok': True})
            except:
                return jsonify({'ok': False})

        @app.route('/next', methods=['POST'])
        def next_song():
            try:
                self._schedule(self.play_next_song)
                return jsonify({'ok': True})
            except:
                return jsonify({'ok': False})

        @app.route('/prev', methods=['POST'])
        def prev_song():
            try:
                self._schedule(self.play_previous_song)
                return jsonify({'ok': True})
            except:
                return jsonify({'ok': False})

        @app.route('/seek', methods=['POST'])
        def seek():
            try:
                pos = float(request.args.get('pos', '0'))
                if hasattr(self, 'current_song_length') and self.current_song_length > 0:
                    ratio = max(0.0, min(1.0, pos / (self.current_song_length/1000.0)))
                    self._schedule(self.on_progress_click, ratio)
                return jsonify({'ok': True})
            except:
                return jsonify({'ok': False})

        @app.route('/volume', methods=['POST'])
        def volume():
            try:
                level = float(request.args.get('level', '0.5'))
                level = max(0.0, min(1.0, level))
                self._schedule(self.set_volume, level)
                return jsonify({'ok': True})
            except:
                return jsonify({'ok': False})

        @app.route('/playlists')
        def get_playlists():
            try:
                playlists = getattr(self, 'playlist_names', [])
                current = self.playlist_name.get() if hasattr(self, 'playlist_name') else 'Favoris'
                return jsonify({'playlists': playlists, 'current': current})
            except:
                return jsonify({'playlists': [], 'current': 'Favoris'})

        @app.route('/select-playlist', methods=['POST'])
        def select_playlist():
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'ok': False}), 400
                name = data.get('name', '')
                playlists = getattr(self, 'playlist_names', [])
                if name in playlists and hasattr(self, 'playlist_name'):
                    self._schedule(lambda: self.playlist_name.set(name))
                    return jsonify({'ok': True})
                return jsonify({'ok': False}), 400
            except:
                return jsonify({'ok': False}), 400

        @app.route('/playlist')
        def get_playlist():
            try:
                if not hasattr(self, 'playlist') or not self.playlist:
                    return jsonify({'songs': [], 'current': -1})
                songs = []
                try:
                    playlist_name = self.playlist_name.get() if hasattr(self, 'playlist_name') else 'Favoris'
                    metadata_file = f'jsons/metadata_{playlist_name}.json'
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        all_metadata_list = json.load(f)
                        all_metadata = {m.get('path', ''): m for m in all_metadata_list if isinstance(m, dict)}
                except:
                    all_metadata = {}
                for i, song_path in enumerate(self.playlist):
                    meta = all_metadata.get(song_path, {})
                    songs.append({
                        'index': i,
                        'title': meta.get('display_title', meta.get('title', os.path.basename(song_path))),
                        'artist': meta.get('author', meta.get('artist', 'Inconnu')),
                        'playing': i == self.current_song_index
                    })
                return jsonify({'songs': songs, 'current': self.current_song_index})
            except:
                return jsonify({'songs': [], 'current': -1})

        @app.route('/play-song/<int:index>', methods=['POST'])
        def play_song(index):
            try:
                if hasattr(self, 'playlist') and 0 <= index < len(self.playlist):
                    self._schedule(lambda: self.play_song_at_index(index))
                    return jsonify({'ok': True})
                return jsonify({'ok': False}), 400
            except:
                return jsonify({'ok': False}), 400

        @app.route('/search')
        def search():
            try:
                if not hasattr(self, 'playlist'):
                    return jsonify({'results': []})
                q = request.args.get('q', '').lower()
                if not q:
                    return jsonify({'results': []})
                results = []
                try:
                    playlist_name = self.playlist_name.get() if hasattr(self, 'playlist_name') else 'Favoris'
                    metadata_file = f'jsons/metadata_{playlist_name}.json'
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        all_metadata_list = json.load(f)
                        all_metadata = {m.get('path', ''): m for m in all_metadata_list if isinstance(m, dict)}
                except:
                    all_metadata = {}
                for i, song_path in enumerate(self.playlist):
                    meta = all_metadata.get(song_path, {})
                    title = meta.get('display_title', meta.get('title', os.path.basename(song_path))).lower()
                    artist = meta.get('author', meta.get('artist', '')).lower()
                    if q in title or q in artist:
                        results.append({
                            'index': i,
                            'title': meta.get('display_title', meta.get('title', os.path.basename(song_path))),
                            'artist': meta.get('author', meta.get('artist', 'Inconnu'))
                        })
                return jsonify({'results': results})
            except:
                return jsonify({'results': []})

        @app.route('/')
        def index():
            return '''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="theme-color" content="#000000">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Mu Player">
<link rel="manifest" href="/manifest.json">
<link rel="apple-touch-icon" href="/logo.ico">
<title>Mu Player</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #000000 0%, #0a1028 100%);
    color: #e0e0e0;
    min-height: 100vh;
    padding: 20px 0;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 15px;
}

/* HEADER avec logo */
.header {
    text-align: center;
    margin: 30px 0 40px 0;
}

.logo-container {
    width: 100px;
    height: 100px;
    margin: 0 auto 20px;
    background: linear-gradient(135deg, #4da6ff, #5fc7ff);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 25px rgba(77, 166, 255, 0.3);
    overflow: hidden;
}

.logo-container img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.header h1 {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 8px 0;
}

.header p {
    color: #4da6ff;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Section principale avec pochette */
.now-playing {
    background: linear-gradient(135deg, #1a3a5e 0%, #0f1b2e 100%);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 25px;
    border: 1px solid rgba(77, 166, 255, 0.2);
    box-shadow: 0 10px 40px rgba(77, 166, 255, 0.1);
}

.album-art-container {
    display: flex;
    justify-content: center;
    margin-bottom: 25px;
}

.album-art {
    width: 220px;
    height: 220px;
    background: linear-gradient(135deg, #1a3a5e, #0f1b2e);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 80px;
    box-shadow: 
        0 0 30px rgba(77, 166, 255, 0.4),
        0 0 60px rgba(77, 166, 255, 0.2);
    border: 2px solid #4da6ff;
    overflow: hidden;
    position: relative;
}

.album-art img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
}

.album-art-placeholder {
    position: relative;
    z-index: 1;
    font-size: 12px;
    color: #6fa8d8;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.song-info {
    text-align: center;
}

.song-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 8px 0;
    word-break: break-word;
}

.song-artist {
    font-size: 14px;
    color: #6fa8d8;
    margin: 0 0 15px 0;
}

.time-display {
    font-size: 13px;
    color: #4da6ff;
    margin: 15px 0;
    font-weight: 600;
}

.slider-group {
    margin: 20px 0;
}

input[type="range"] {
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: rgba(15, 27, 46, 0.8);
    outline: none;
    -webkit-appearance: none;
    appearance: none;
}

input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 16px;
    height: 16px;
    background: #4da6ff;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(77, 166, 255, 0.5);
}

input[type="range"]::-moz-range-thumb {
    width: 16px;
    height: 16px;
    background: #4da6ff;
    border-radius: 50%;
    cursor: pointer;
    border: none;
    box-shadow: 0 0 10px rgba(77, 166, 255, 0.5);
}

.controls {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin: 25px 0;
    flex-wrap: wrap;
}

button {
    padding: 12px 24px;
    background: linear-gradient(135deg, #2a5e8e 0%, #1a3a5e 100%);
    color: #ffffff;
    border: 1px solid #4da6ff;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(77, 166, 255, 0.2);
}

button:hover {
    background: linear-gradient(135deg, #3a7abf 0%, #2a5a9e 100%);
    box-shadow: 0 6px 20px rgba(77, 166, 255, 0.4);
    transform: translateY(-2px);
}

button:active {
    transform: translateY(0);
}

button.small {
    padding: 10px 16px;
    font-size: 13px;
}

button#playBtn {
    background: linear-gradient(135deg, #4da6ff 0%, #5fc7ff 100%);
    color: #000000;
    border: none;
    font-weight: 700;
    padding: 14px 40px;
    font-size: 15px;
}

button#playBtn:hover {
    background: linear-gradient(135deg, #5fc7ff 0%, #7fd8ff 100%);
    box-shadow: 0 8px 25px rgba(77, 166, 255, 0.5);
}

.volume-container {
    display: flex;
    gap: 12px;
    align-items: center;
    padding: 15px 0;
    border-top: 1px solid rgba(77, 166, 255, 0.2);
    border-bottom: 1px solid rgba(77, 166, 255, 0.2);
}

.volume-container span {
    font-size: 18px;
    min-width: 24px;
}

.volume-container input {
    flex: 1;
}

.section {
    background: rgba(15, 27, 46, 0.5);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    border: 1px solid rgba(77, 166, 255, 0.15);
    backdrop-filter: blur(10px);
}

h2 {
    font-size: 14px;
    font-weight: 700;
    color: #4da6ff;
    margin: 0 0 15px 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.playlists-list {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.playlist-btn {
    padding: 10px 16px;
    background: rgba(42, 94, 142, 0.4);
    color: #7fc4ff;
    border: 1px solid #4da6ff;
    border-radius: 8px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.playlist-btn:hover {
    background: rgba(42, 94, 142, 0.7);
    box-shadow: 0 4px 12px rgba(77, 166, 255, 0.3);
}

.playlist-btn.active {
    background: #4da6ff;
    color: #000000;
    border-color: #5fc7ff;
    box-shadow: 0 6px 16px rgba(77, 166, 255, 0.4);
}

.search-box {
    width: 100%;
    padding: 12px 14px;
    background: rgba(15, 27, 46, 0.8);
    border: 1px solid #4da6ff;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 13px;
    transition: all 0.3s ease;
}

.search-box:focus {
    outline: none;
    border-color: #5fc7ff;
    box-shadow: 0 0 15px rgba(77, 166, 255, 0.3);
    background: rgba(15, 27, 46, 0.95);
}

.search-box::placeholder {
    color: #6fa8d8;
}

.song-list {
    max-height: 300px;
    overflow-y: auto;
    margin-top: 12px;
}

.song-item {
    padding: 12px;
    margin: 8px 0;
    background: rgba(77, 166, 255, 0.08);
    border-left: 3px solid transparent;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.song-item:hover {
    background: rgba(77, 166, 255, 0.18);
    transform: translateX(4px);
}

.song-item.playing {
    border-left-color: #4da6ff;
    background: rgba(77, 166, 255, 0.25);
}

.song-item-title {
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
}

.song-item-artist {
    font-size: 11px;
    color: #6fa8d8;
    margin-top: 3px;
}

.loading {
    text-align: center;
    color: #6fa8d8;
    font-size: 12px;
    padding: 15px;
}

/* Scrollbar custom */
.song-list::-webkit-scrollbar {
    width: 8px;
}

.song-list::-webkit-scrollbar-track {
    background: rgba(77, 166, 255, 0.05);
    border-radius: 4px;
}

.song-list::-webkit-scrollbar-thumb {
    background: #4da6ff;
    border-radius: 4px;
}

.song-list::-webkit-scrollbar-thumb:hover {
    background: #5fc7ff;
}

</style>
</head>
<body>
<div class="container">
    <!-- HEADER avec logo -->
    <div class="header">
        <div class="logo-container">
            <img src="/logo.ico" alt="Logo" onerror="this.style.display='none'">
        </div>
        <h1>Mu Player</h1>
    </div>
    
    <!-- NOW PLAYING avec pochette -->
    <div class="now-playing">
        <div class="album-art-container">
            <div class="album-art" id="albumArt">
                <span class="album-art-placeholder">Aucune image</span>
            </div>
        </div>
        
        <div class="song-info">
            <div class="song-title" id="title">Aucune musique</div>
            <div class="song-artist" id="artist">-</div>
            <div class="time-display"><span id="time">0:00 / 0:00</span></div>
        </div>
        
        <div class="slider-group">
            <input type="range" id="seek" min="0" max="100" value="0">
        </div>
        
        <div class="controls">
            <button onclick="cmd('prev')" class="small">⏮</button>
            <button onclick="togglePlay()" id="playBtn">Play</button>
            <button onclick="cmd('next')" class="small">⏭</button>
        </div>
        
        <div class="volume-container">
            <span>Volume</span>
            <input type="range" id="volume" min="0" max="100" value="50" oninput="volChange(this.value)">
        </div>
    </div>
    
    <!-- PLAYLISTS -->
    <div class="section">
        <h2>Playlists</h2>
        <div class="playlists-list" id="playlistsList"></div>
    </div>
    
    <!-- SEARCH -->
    <div class="section">
        <h2>Recherche</h2>
        <input type="text" class="search-box" id="searchBox" placeholder="Chercher une chanson...">
        <div class="song-list" id="searchResults"></div>
    </div>
    
    <!-- CURRENT PLAYLIST -->
    <div class="section">
        <h2>Playlist actuelle</h2>
        <div class="song-list" id="playlistSongs"></div>
    </div>
</div>

<script>
let isPlaying = false;

async function refresh() {
    try {
        const res = await fetch('/status');
        const data = await res.json();
        
        if (data.error) return;
        
        isPlaying = data.playing;
        document.getElementById('title').textContent = data.title || 'Aucune musique';
        document.getElementById('artist').textContent = data.artist || '-';
        
        const cur = Math.round(data.position_sec) || 0;
        const tot = Math.round(data.duration_sec) || 0;
        
        const formatTime = (s) => {
            const m = Math.floor(s / 60);
            const sec = String(s % 60).padStart(2, '0');
            return m + ':' + sec;
        };
        
        document.getElementById('time').textContent = formatTime(cur) + ' / ' + formatTime(tot);
        
        // Ne pas modifier le slider si l'utilisateur est en train de le déplacer
        if (!isDraggingSeek) {
            document.getElementById('seek').value = tot > 0 ? Math.round((cur / tot) * 100) : 0;
        }
        
        document.getElementById('volume').value = Math.round((data.volume || 0.5) * 100);
        
        const btn = document.getElementById('playBtn');
        btn.textContent = isPlaying ? 'Pause' : 'Play';
        
        // Mettre à jour l'image de la pochette
        const albumArt = document.getElementById('albumArt');
        const placeholder = albumArt.querySelector('.album-art-placeholder');
        let existingImg = albumArt.querySelector('img');
        
        if (data.title && data.title !== 'Aucune musique' && data.title !== 'Pas de musique') {
            if (!existingImg) {
                existingImg = document.createElement('img');
                existingImg.onerror = () => {
                    existingImg.style.display = 'none';
                    if (placeholder) placeholder.style.display = 'flex';
                };
                existingImg.onload = () => {
                    existingImg.style.display = 'block';
                    if (placeholder) placeholder.style.display = 'none';
                };
                albumArt.appendChild(existingImg);
            }
            existingImg.src = '/album-art?t=' + Date.now();
        } else {
            if (existingImg) {
                existingImg.remove();
            }
            if (placeholder) placeholder.style.display = 'flex';
        }
    } catch (e) {
        console.error('Error:', e);
    }
}

async function cmd(command) {
    try {
        await fetch('/' + command, {method: 'POST'});
        refresh();
    } catch (e) {
        console.error('Error:', e);
    }
}

async function togglePlay() {
    try {
        const endpoint = isPlaying ? 'pause' : 'play';
        await fetch('/' + endpoint, {method: 'POST'});
        refresh();
    } catch (e) {
        console.error('Error:', e);
    }
}

async function volChange(val) {
    try {
        const level = val / 100.0;
        await fetch('/volume?level=' + level, {method: 'POST'});
    } catch (e) {
        console.error('Error:', e);
    }
}

async function loadPlaylists() {
    try {
        const res = await fetch('/playlists');
        const data = await res.json();
        const container = document.getElementById('playlistsList');
        container.innerHTML = '';
        
        if (!data.playlists || data.playlists.length === 0) {
            container.innerHTML = '<div class="loading">Aucune playlist</div>';
            return;
        }
        
        data.playlists.forEach(name => {
            const btn = document.createElement('button');
            btn.className = 'playlist-btn' + (name === data.current ? ' active' : '');
            btn.textContent = name;
            btn.onclick = () => selectPlaylist(name);
            container.appendChild(btn);
        });
    } catch (e) {
        console.error('Error loading playlists:', e);
    }
}

async function selectPlaylist(name) {
    try {
        await fetch('/select-playlist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name })
        });
        loadPlaylists();
        loadPlaylist();
        refresh();
    } catch (e) {
        console.error('Error:', e);
    }
}

async function loadPlaylist() {
    try {
        const res = await fetch('/playlist');
        const data = await res.json();
        const container = document.getElementById('playlistSongs');
        container.innerHTML = '';
        
        if (!data.songs || data.songs.length === 0) {
            container.innerHTML = '<div class="loading">Aucune chanson</div>';
            return;
        }
        
        data.songs.forEach(song => {
            const item = document.createElement('div');
            item.className = 'song-item' + (song.playing ? ' playing' : '');
            item.innerHTML = '<div class="song-item-title">' + song.title + '</div>' +
                           '<div class="song-item-artist">' + (song.artist || '') + '</div>';
            item.onclick = () => playSong(song.index);
            container.appendChild(item);
        });
    } catch (e) {
        console.error('Error loading playlist:', e);
    }
}

async function playSong(index) {
    try {
        await fetch('/play-song/' + index, {method: 'POST'});
        loadPlaylist();
        refresh();
    } catch (e) {
        console.error('Error:', e);
    }
}

document.getElementById('searchBox').addEventListener('input', async (e) => {
    const query = e.target.value.trim();
    const container = document.getElementById('searchResults');
    
    if (!query) {
        container.innerHTML = '';
        return;
    }
    
    try {
        const res = await fetch('/search?q=' + encodeURIComponent(query));
        const data = await res.json();
        container.innerHTML = '';
        
        if (!data.results || data.results.length === 0) {
            container.innerHTML = '<div class="loading">Aucun résultat</div>';
            return;
        }
        
        data.results.forEach(song => {
            const item = document.createElement('div');
            item.className = 'song-item';
            item.innerHTML = '<div class="song-item-title">' + song.title + '</div>' +
                           '<div class="song-item-artist">' + (song.artist || '') + '</div>';
            item.onclick = () => playSong(song.index);
            container.appendChild(item);
        });
    } catch (e) {
        console.error('Error searching:', e);
    }
});

// Seek - utiliser change au lieu de input pour éviter de spammer
let isDraggingSeek = false;
const seekSlider = document.getElementById('seek');

seekSlider.addEventListener('mousedown', () => {
    isDraggingSeek = true;
});

seekSlider.addEventListener('mouseup', async (e) => {
    isDraggingSeek = false;
    try {
        const res = await fetch('/status');
        const data = await res.json();
        const tot = data.duration_sec || 0;
        const seekPos = (e.target.value / 100) * tot;
        await fetch('/seek?pos=' + seekPos, {method: 'POST'});
        setTimeout(refresh, 100);
    } catch (err) {
        console.error(err);
    }
});

seekSlider.addEventListener('touchend', async (e) => {
    isDraggingSeek = false;
    try {
        const res = await fetch('/status');
        const data = await res.json();
        const tot = data.duration_sec || 0;
        const seekPos = (e.target.value / 100) * tot;
        await fetch('/seek?pos=' + seekPos, {method: 'POST'});
        setTimeout(refresh, 100);
    } catch (err) {
        console.error(err);
    }
});

// Initialiser
refresh();
loadPlaylists();
loadPlaylist();

// Rafraîchir régulièrement
setInterval(refresh, 1000);

// Enregistrer le Service Worker pour PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').then(() => {
        console.log('Service Worker enregistré');
    }).catch((err) => {
        console.log('Erreur Service Worker:', err);
    });
}
</script>
</body>
</html>'''

        @app.route('/favicon.ico')
        def favicon():
            return '', 204
        
        @app.route('/manifest.json')
        def manifest():
            return jsonify({
                "name": "MU Player",
                "short_name": "MU Player",
                "description": "Lecteur de musique premium avec contrôle à distance",
                "start_url": "/",
                "display": "standalone",
                "background_color": "#000000",
                "theme_color": "#000000",
                "orientation": "portrait",
                "icons": [
                    {
                        "src": "/logo.ico",
                        "sizes": "192x192",
                        "type": "image/x-icon",
                        "purpose": "any maskable"
                    }
                ]
            })
        
        @app.route('/sw.js')
        def service_worker():
            return '''
self.addEventListener('install', (e) => {
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    self.clients.claim();
});

self.addEventListener('fetch', (e) => {
    e.respondWith(fetch(e.request));
});
''', 200, {'Content-Type': 'application/javascript'}
        
        @app.route('/logo.ico')
        def get_logo():
            try:
                if os.path.exists('logo.ico'):
                    with open('logo.ico', 'rb') as f:
                        return f.read(), 200, {'Content-Type': 'image/x-icon'}
                return '', 404
            except:
                return '', 404
        
        @app.route('/album-art')
        def get_album_art():
            try:
                if not hasattr(self, 'current_song_index') or not hasattr(self, 'playlist'):
                    return '', 404
                if self.current_song_index < 0 or self.current_song_index >= len(self.playlist):
                    return '', 404
                song_path = self.playlist[self.current_song_index]
                # Chercher la pochette dans le dossier covers
                cover_filename = os.path.splitext(os.path.basename(song_path))[0] + '.jpg'
                cover_path = os.path.join(self.covers_folder, cover_filename)
                if os.path.exists(cover_path):
                    with open(cover_path, 'rb') as f:
                        return f.read(), 200, {'Content-Type': 'image/jpeg'}
                # Essayer aussi avec .png
                cover_filename_png = os.path.splitext(os.path.basename(song_path))[0] + '.png'
                cover_path_png = os.path.join(self.covers_folder, cover_filename_png)
                if os.path.exists(cover_path_png):
                    with open(cover_path_png, 'rb') as f:
                        return f.read(), 200, {'Content-Type': 'image/png'}
                return '', 404
            except:
                return '', 404

        try:
            app.run(host='0.0.0.0', port=self.remote_port, debug=False, use_reloader=False)
        except Exception:
            pass

    def rounded_album_art(self, img, radius=20):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)
        img.putalpha(mask)
        return img

    def set_default_album_art(self):
        base = Image.new('RGB', (150, 150), color=self.theme["card_gradient"])
        img = self.rounded_album_art(base)
        self.current_album_art = ImageTk.PhotoImage(img)
        self.album_art_label.config(image=self.current_album_art, bg=self.theme["card_gradient"])

    def load_album_art(self, song_path, url=None):
        """Charge la pochette depuis MP3 ou YouTube, sinon défaut."""
        # 1) Métadonnées MP3 (APIC)
        try:
            audio = MP3(song_path, ID3=ID3)
            if audio.tags:
                for tag in audio.tags.values():
                    if isinstance(tag, APIC) and tag.data:
                        img = Image.open(BytesIO(tag.data)).convert("RGB")
                        img = img.resize((150, 150), Image.Resampling.LANCZOS)
                        img = self.rounded_album_art(img)
                        self.current_album_art = ImageTk.PhotoImage(img)
                        self.album_art_label.config(image=self.current_album_art)
                        return
        except Exception:
            pass

        # 2) Miniature YouTube (si URL fournie)
        if url:
            try:
                yt = YouTube(url)
                thumbnail_url = yt.thumbnail_url
                resp = requests.get(thumbnail_url, timeout=5)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                img = img.resize((180, 180), Image.Resampling.LANCZOS)
                img = self.rounded_album_art(img)
                self.current_album_art = ImageTk.PhotoImage(img)
                self.album_art_label.config(image=self.current_album_art)
                # Sauvegarde en PNG (alpha supporté)
                cover_filename = os.path.join(self.covers_folder,
                                              os.path.basename(song_path).replace('.mp3', '.png'))
                try:
                    img.save(cover_filename, format="PNG")
                except Exception:
                    pass
                return
            except Exception:
                pass

        # 3) Pochette par défaut
        self.set_default_album_art()

    def on_progress_click(self, progress):
        """Seek en cliquant sur la barre: fiable avec play(start=...)."""
        if not self.current_song_path or self.current_song_length <= 0:
            return
        # clamp et calcul
        progress = max(0.0, min(1.0, progress))
        self.seek_offset_ms = int(progress * self.current_song_length)
        new_pos_sec = self.seek_offset_ms / 1000.0

        # Ignorer l’évènement de fin pendant un court instant (évite la boucle)
        self.ignore_end_event_until = time.time() + 0.5
        try:
            # Relance directement depuis la position (pas de stop/load ici)
            pygame.mixer.music.play(loops=0, start=new_pos_sec)
        except Exception:
            # Fallback si le backend exige un reload
            pygame.mixer.music.load(self.current_song_path)
            pygame.mixer.music.play(loops=0, start=new_pos_sec)

    def update_time_label(self):
        """Met à jour le temps et la barre de progression."""
        if pygame.mixer.music.get_busy():
            current_pos = pygame.mixer.music.get_pos()
            if current_pos < 0:
                current_pos = 0
            current_time = max(0, self.seek_offset_ms + current_pos)
            mins, sec = divmod(current_time // 1000, 60)
            mins_total, sec_total = divmod(self.current_song_length // 1000, 60)
            self.time_label.config(text=f"{mins}:{sec:02d} / {mins_total}:{sec_total:02d}")
            if self.current_song_length > 0:
                self.progress_bar.set_progress(current_time / self.current_song_length)
        self.master.after(100, self.update_time_label)

    def check_for_pygame_events(self):
        """Avance à la piste suivante à la fin, en ignorant les faux ‘end’ juste après un seek."""
        now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if now < self.ignore_end_event_until:
                    # Ignore le faux signal de fin déclenché par le seek
                    continue
                self.play_next_song()
        self.master.after(500, self.check_for_pygame_events)

    def notify_song_change(self, song_title, playlist_name):
        notification.notify(
            title='[MU Player] Nouvelle chanson en cours de lecture',
            message=f'Vous écoutez {song_title} de la playlist {playlist_name}',
            app_name='MU Player',
            app_icon='logo.ico',
            timeout=50
        )

    def update_recommendation(self, recommended_title, recommended_url):
        # Affiche une suggestion même sans URL; bouton visible seulement si URL
        if recommended_title:
            self.recommendation_label.config(text=f"Suggestion: {recommended_title}")
            self.recommended_url = recommended_url or ""
            if self.recommended_url:
                self.recommendation_button.pack(side=tk.BOTTOM, anchor=tk.E, padx=30, pady=(10, 20))
            else:
                self.recommendation_button.pack_forget()
        else:
            self.recommended_url = ""
            self.recommendation_label.config(text="Aucune recommandation disponible pour ce titre.")
            self.recommendation_button.pack_forget()

    def add_recommended_song(self):
        if self.recommended_url:
            self.add_youtube_to_playlist(self.recommended_url)

    def search_music(self):
        if self.playlist_name.get() == "Favoris":
            print("Vous ne pouvez pas ajouter des musiques directement dans la playlist Favoris")
            return

        search_query = ask_custom_string(self.master, "Recherche de musique",
                                         "Entrez le nom de la musique à rechercher:")
        if search_query:
            results = videos_search_safe(search_query, 1)
            if not results:
                return
            if 'result' in results and isinstance(results['result'], list) and len(results['result']) > 0:
                first_result = results['result'][0]
                if 'link' in first_result:
                    video_url = first_result["link"]
                    self.add_youtube_to_playlist(video_url)
                else:
                    tk.messagebox.showwarning("Résultat", "Aucun lien trouvé.")
            else:
                tk.messagebox.showwarning("Résultat", "Aucune musique trouvée.")

    def remove_duplicates(self):
        metadata_list = []
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    try:
                        metadata_list = json.loads(content)
                    except json.JSONDecodeError:
                        return

            seen = {}
            duplicates_indices = []
            for i, metadata in enumerate(metadata_list):
                path = metadata['path']
                if path in seen:
                    duplicates_indices.append(i)
                else:
                    seen[path] = i

            for index in reversed(duplicates_indices):
                del metadata_list[index]

            with open(self.metadata_file, 'w') as f:
                json.dump(metadata_list, f)

    def load_new_playlist(self, *args):
        self.playlist = []
        self.playlistbox.delete(0, tk.END)
        self.load_metadata()
        self.remove_duplicates()

    def toggle_favorite(self):
        selected_index = self.playlistbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            metadata_list = []
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r') as f:
                    content = f.read()
                    if content:
                        try:
                            metadata_list = json.loads(content)
                        except json.JSONDecodeError:
                            print("")

            metadata = metadata_list[selected_index]
            if not isinstance(metadata, dict):
                return

            metadata['is_favorite'] = not metadata.get('is_favorite', False)

            with open(self.metadata_file, 'w') as f:
                json.dump(metadata_list, f)

            self.update_favorite_status_in_all_playlists(metadata['path'], metadata['is_favorite'])
            default_metadata_file = 'jsons/metadata_Favoris.json'
            default_metadata_list = []
            if os.path.exists(default_metadata_file):
                with open(default_metadata_file, 'r') as f:
                    content = f.read()
                    if content:
                        try:
                            default_metadata_list = json.loads(content)
                        except json.JSONDecodeError:
                            print("")

            if metadata['is_favorite']:
                if not any(m['path'] == metadata['path'] for m in default_metadata_list):
                    default_metadata_list.append(metadata)
            else:
                default_metadata_list = [m for m in default_metadata_list if m['path'] != metadata['path']]

            with open(default_metadata_file, 'w') as f:
                json.dump(default_metadata_list, f)

            if self.playlist_name.get() == "Favoris":
                self.load_new_playlist()

            self.update_playlist_item(selected_index)

    def update_favorite_status_in_all_playlists(self, song_path, new_favorite_status):
        for playlist_name in self.playlist_names:
            metadata_file = f'jsons/metadata_{playlist_name}.json'
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    content = f.read()
                    if content:
                        try:
                            metadata_list = json.loads(content)
                            for metadata in metadata_list:
                                if song_path == metadata['path']:
                                    metadata['is_favorite'] = new_favorite_status
                        except json.JSONDecodeError:
                            print("")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata_list, f)

    def clean_up_unused_files(self):
        all_mp3_files = set(os.listdir(self.music_folder))
        used_mp3_files = set()

        for playlist_name in self.playlist_names:
            metadata_file = f'jsons/metadata_{playlist_name}.json'
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    content = f.read()
                    if content:
                        try:
                            metadata_list = json.loads(content)
                            for metadata in metadata_list:
                                used_mp3_files.add(os.path.basename(metadata['path']))
                        except json.JSONDecodeError:
                            print("")

        unused_mp3_files = all_mp3_files - used_mp3_files

        for unused_file in unused_mp3_files:
            try:
                os.remove(os.path.join(self.music_folder, unused_file))
            except PermissionError:
                print("")

    def sort_playlist(self, event=None):
        sort_option = self.sort_var.get()
        with open(self.metadata_file, 'r') as f:
            metadata_list = json.load(f)

        if sort_option == "Par date d'ajout":
            metadata_list.sort(key=lambda x: x.get('date_added', 0), reverse=True)
        elif sort_option == "Par date de création":
            metadata_list.sort(key=lambda x: x.get('publish_date', ''), reverse=True)
        elif sort_option == "Par ordre alphabétique":
            metadata_list.sort(key=lambda x: x.get('display_title', ''))
        elif sort_option == "Par auteur":
            metadata_list.sort(key=lambda x: (x.get('author', '').lower(), x.get('display_title', '').lower()))

        self.playlist = [x['path'] for x in metadata_list]
        self.playlistbox.delete(0, tk.END)
        for metadata in metadata_list:
            audio = MP3(metadata['path'])
            duration = audio.info.length
            mins, sec = divmod(int(duration), 60)

            heart_icon = "   ❤" if metadata.get('is_favorite', False) else ""

            display_title_with_time = f"{metadata['display_title']}  [{mins}:{sec}]{heart_icon}"
            self.playlistbox.insert(tk.END, display_title_with_time)

    def update_playlist_item(self, index):
        if not os.path.exists(self.metadata_file):
            return

        with open(self.metadata_file, 'r') as f:
            content = f.read()
            if content:
                try:
                    metadata_list = json.loads(content)
                except json.JSONDecodeError:
                    return

        if index >= len(metadata_list):
            return

        metadata = metadata_list[index]
        audio = MP3(metadata['path'])
        duration = audio.info.length
        mins, sec = divmod(int(duration), 60)

        heart_icon = "   ❤" if metadata.get('is_favorite', False) else ""

        display_title_with_time = f"{metadata['display_title']}  [{mins}:{sec}]{heart_icon}"
        self.playlistbox.delete(index)
        self.playlistbox.insert(index, display_title_with_time)

    def delete_playlist(self):
        playlist_to_delete = self.playlist_name.get()
        if playlist_to_delete == "Favoris":
            tk.messagebox.showwarning("!", "Vous ne pouvez pas supprimer la playlist Favoris.")
            return

        confirm = ask_custom_yesno(self.master, "Confirmation",
                                   f"Êtes-vous sûr de vouloir supprimer la playlist {playlist_to_delete}?")
        if confirm:
            os.remove(f"jsons/metadata_{playlist_to_delete}.json")

            self.playlist_names.remove(playlist_to_delete)
            with open("jsons/playlists.json", "w") as f:
                json.dump(self.playlist_names, f)

            self.playlist_name.set("Favoris")
            self.playlist_menu['menu'].delete(playlist_to_delete)
            self.clean_up_unused_files()

    def load_metadata(self):
        self.playlist = []
        self.playlistbox.delete(0, tk.END)
        self.metadata_file = f'jsons/metadata_{self.playlist_name.get()}.json'
        favoris_metadata_file = 'jsons/metadata_Favoris.json'
        favoris_paths = []

        if os.path.exists(favoris_metadata_file):
            with open(favoris_metadata_file, 'r', encoding='utf-8') as f:
                favoris_metadata = json.load(f)
                favoris_paths = [metadata['path'] for metadata in favoris_metadata]

        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    try:
                        metadata_list = json.loads(content)
                        for metadata in metadata_list:
                            self.playlist.append(metadata['path'])

                            audio = MP3(metadata['path'])
                            duration = audio.info.length
                            mins, sec = divmod(int(duration), 60)

                            is_favorite = metadata['path'] in favoris_paths
                            metadata['is_favorite'] = is_favorite

                            heart_icon = "   ❤" if is_favorite else ""

                            display_title = f"{len(self.playlist)}.  {self.truncate_text(metadata['display_title'], 50)}  [{mins}:{sec:02d}]{heart_icon}"
                            self.playlistbox.insert(tk.END, display_title)
                    except json.JSONDecodeError:
                        print("")
                else:
                    print("")
        return metadata_list if 'metadata_list' in locals() else []

    def load_playlist_names(self):
        self.playlist_names = ["Favoris"]
        try:
            with open("jsons/playlists.json", "r") as f:
                self.playlist_names = json.load(f)
        except FileNotFoundError:
            with open("jsons/playlists.json", "w") as f:
                json.dump(self.playlist_names, f)
        except json.JSONDecodeError:
            print("")

    def new_playlist(self):
        new_name = ask_custom_string(self.master, "Nouvelle playlist", "Entrez le nom de la nouvelle playlist:")
        if new_name and new_name not in self.playlist_names:
            self.playlist_names.append(new_name)
            with open("jsons/playlists.json", "w") as f:
                json.dump(self.playlist_names, f)
            new_json_file_path = f"jsons/metadata_{new_name}.json"
            with open(new_json_file_path, 'w') as f:
                json.dump([], f)

            self.playlist_name.set(new_name)
            self.playlist_menu['menu'].add_command(label=new_name, command=tk._setit(self.playlist_name, new_name))
            self.playlist = []
            self.playlistbox.delete(0, tk.END)
            self.load_metadata()
        elif new_name in self.playlist_names:
            print("Cette playlist existe déjà.")

    def save_metadata(self, path, display_title, author, publish_date, song_length, is_favorite, url):
        metadata_list = []
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content:
                    try:
                        metadata_list = json.loads(content)
                    except json.JSONDecodeError:
                        print("")
        metadata_list.append(
            {'path': path, 'display_title': display_title, 'author': author,
             'publish_date': publish_date, 'date_added': time.time(),
             'song_length': song_length, 'is_favorite': is_favorite, 'url': url, 'listen_count': 0})
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f)
        self.update_favorite_status_in_all_playlists(path, is_favorite)

    def increment_listen_count(self, song_path):
        """Incrémente le compteur d'écoutes pour une chanson"""
        try:
            if os.path.exists(self.metadata_file):
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        metadata_list = json.loads(content)
                        for metadata in metadata_list:
                            if metadata.get('path') == song_path:
                                metadata['listen_count'] = metadata.get('listen_count', 0) + 1
                                break
                        with open(self.metadata_file, 'w', encoding='utf-8') as fw:
                            json.dump(metadata_list, fw)
        except Exception:
            pass

    def update_now_playing_display(self, song_path):
        """Met à jour l'affichage du titre, artiste et infos pour une chanson"""
        artist = ""
        album = ""
        publish_date = ""
        listen_count = 0
        
        try:
            metadata_list = self.load_metadata()
            for meta in metadata_list:
                if meta.get('path') == song_path:
                    artist = meta.get('author', '')
                    album = meta.get('album', '')
                    publish_date = meta.get('publish_date', '')
                    listen_count = meta.get('listen_count', 0)
                    break
        except Exception:
            pass
        
        # Afficher artiste et infos
        self.artist_label.config(text=artist if artist else "Artiste inconnu")
        info_text = ""
        if listen_count > 0:
            info_text += f"Écoutée {listen_count} fois"
        if album:
            if info_text:
                info_text += f" | Album: {album}"
            else:
                info_text = f"Album: {album}"
        if publish_date:
            if info_text:
                info_text += f" | {publish_date}"
            else:
                info_text = publish_date
        self.info_label.config(text=info_text)

    def shuffle_play(self):
        with open(self.metadata_file, 'r') as f:
            metadata_list = json.load(f)

        random.shuffle(metadata_list)

        self.playlist = []
        self.playlistbox.delete(0, tk.END)
        for metadata in metadata_list:
            self.playlist.append(metadata['path'])

            audio = MP3(metadata['path'])
            duration = audio.info.length
            mins, sec = divmod(int(duration), 60)

            heart_icon = "   ❤" if metadata.get('is_favorite', False) else ""

            display_title_with_time = f"{metadata['display_title']}  [{mins}:{sec}]{heart_icon}"
            self.playlistbox.insert(tk.END, display_title_with_time)

        # Sélectionner et jouer le premier titre du shuffle
        self.playlistbox.selection_clear(0, tk.END)
        self.playlistbox.selection_set(0)
        first_song = self.playlist[0]
        self.current_song_path = first_song
        self.current_song_index = 0  # Index à 0 pour le shuffle
        self.seek_offset_ms = 0
        pygame.mixer.music.load(first_song)
        pygame.mixer.music.play()
        self.update_song_length(first_song)
        first_title = self.playlistbox.get(0).split('[')[0].strip()
        self.current_song_label.config(text=self.truncate_text(first_title))
        self.notify_song_change(first_title, self.playlist_name.get())
        # Charger la pochette et les infos (trouver par chemin)
        for meta in metadata_list:
            if meta['path'] == first_song:
                url = meta.get('url', None)
                self.load_album_art(first_song, url)
                break
        
        # Afficher artiste, album, infos et écoutes
        self.update_now_playing_display(first_song)
        
        # Incrémenter le compteur d'écoutes
        self.increment_listen_count(first_song)
        
        recommended_title, recommended_url = self.recommend_next_song()
        self.update_recommendation(recommended_title, recommended_url)

    def set_volume(self, val):
        volume_level = float(val)
        pygame.mixer.music.set_volume(volume_level)

    def recommend_next_song(self):
        # Pas de recommandation si rien n'est sélectionné
        if self.current_song_index < 0 or self.current_song_index >= self.playlistbox.size():
            return "", ""

        # Titre courant affiché dans la listbox (ex: "Song - Artist  [3:12]")
        current_entry = self.playlistbox.get(self.current_song_index)
        current_song_title = current_entry.split('[')[0].strip()
        current_artist = current_song_title.split(" - ")[-1] if " - " in current_song_title else None

        # Récupérer les URLs déjà présentes dans la playlist sans réinitialiser la liste
        existing_urls = []
        try:
            metadata_path = f'jsons/metadata_{self.playlist_name.get()}.json'
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        metadata_list = json.loads(content)
                        existing_urls = [m.get('url', '') for m in metadata_list if isinstance(m, dict)]
        except Exception:
            existing_urls = []

        # 1) Priorité: même artiste (nom de chaîne YouTube)
        if current_artist:
            results = videos_search_safe(current_artist, 40)
            if results and 'result' in results and isinstance(results['result'], list):
                for video in results['result']:
                    try:
                        recommended_song_title = video.get('title')
                        recommended_artist = video.get('channel', {}).get('name')
                        recommended_url = video.get('link')
                        if recommended_url and recommended_artist == current_artist and recommended_url not in existing_urls:
                            return recommended_song_title, recommended_url
                    except Exception:
                        pass

        # 2) Fallback: rechercher par titre courant seul
        base_title = current_song_title.split(' - ')[0].strip()
        if base_title:
            results = videos_search_safe(base_title, 10)
            if results and 'result' in results and isinstance(results['result'], list):
                for video in results['result']:
                    recommended_song_title = video.get('title')
                    recommended_url = video.get('link')
                    if recommended_url and recommended_url not in existing_urls:
                        return recommended_song_title, recommended_url

        # 3) Fallback: artistes présents dans la playlist (autres que l'actuel)
        all_artists = set()
        for i in range(self.playlistbox.size()):
            song_title = self.playlistbox.get(i).split('[')[0].strip()
            artist = song_title.split(" - ")[-1] if " - " in song_title else None
            if artist:
                all_artists.add(artist)

        for artist in all_artists:
            if current_artist and artist == current_artist:
                continue
            results = videos_search_safe(artist, 20)
            if results and 'result' in results and isinstance(results['result'], list):
                for video in results['result']:
                    recommended_song_title = video.get('title')
                    recommended_url = video.get('link')
                    if recommended_url and recommended_url not in existing_urls:
                        return recommended_song_title, recommended_url

        # 4) Fallback local: proposer un autre titre de la playlist (sans URL)
        try:
            if self.playlistbox.size() > 1:
                next_index = (self.current_song_index + 1) % self.playlistbox.size()
                next_title = self.playlistbox.get(next_index).split('[')[0].strip()
                if next_title:
                    return next_title, ""
        except Exception:
            pass

        # Rien trouvé
        return "", ""

    def play_previous_song(self):
        if len(self.playlist) == 0:
            print("La playlist est vide.")
            return

        previous_song_index = (self.current_song_index - 1) % len(self.playlist)

        self.playlistbox.selection_clear(0, tk.END)
        self.playlistbox.selection_set(previous_song_index)

        previous_song = self.playlist[previous_song_index]
        self.current_song_path = previous_song
        self.current_song_index = previous_song_index  # Mise à jour de l'index courant
        self.seek_offset_ms = 0
        pygame.mixer.music.load(previous_song)
        pygame.mixer.music.play()
        self.update_song_length(previous_song)
        previous_song_title = self.playlistbox.get(previous_song_index).split('[')[0].strip()
        self.current_song_label.config(text=self.truncate_text(previous_song_title))
        self.notify_song_change(previous_song_title, self.playlist_name.get())
        
        # Charger la pochette et les infos
        metadata_list = self.load_metadata()
        url = None
        for metadata in metadata_list:
            if metadata['path'] == previous_song:
                url = metadata.get('url', None)
                break
        self.load_album_art(previous_song, url)
        
        # Afficher artiste, album, infos et écoutes
        self.update_now_playing_display(previous_song)
        
        # Incrémenter le compteur d'écoutes
        self.increment_listen_count(previous_song)
        
        recommended_title, recommended_url = self.recommend_next_song()
        self.update_recommendation(recommended_title, recommended_url)

    def play_song_at_index(self, index):
        """Play song at a specific index (used by remote control)"""
        try:
            if 0 <= index < len(self.playlist):
                selected_song = self.playlist[index]
                self.current_song_path = selected_song
                self.current_song_index = index
                self.seek_offset_ms = 0
                pygame.mixer.music.load(selected_song)
                pygame.mixer.music.play()
                self.update_song_length(selected_song)
                
                # Get title from metadata
                try:
                    with open('jsons/metadata.json', 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                        meta = metadata.get(selected_song, {})
                        current_song_title = meta.get('title', os.path.basename(selected_song))
                except:
                    current_song_title = os.path.basename(selected_song)
                
                if hasattr(self, 'current_song_label'):
                    try:
                        self.current_song_label.config(text=self.truncate_text(current_song_title))
                    except:
                        pass
                
                try:
                    self.notify_song_change(current_song_title, self.playlist_name.get())
                except:
                    pass
                
                # Update UI if playlistbox exists
                if hasattr(self, 'playlistbox'):
                    try:
                        self.playlistbox.selection_clear(0, tk.END)
                        self.playlistbox.selection_set(index)
                        self.playlistbox.see(index)
                    except:
                        pass
                
                try:
                    self.update_now_playing_display(selected_song)
                except:
                    pass
                
                try:
                    self.increment_listen_count(selected_song)
                except:
                    pass
                
                try:
                    recommended_title, recommended_url = self.recommend_next_song()
                    self.update_recommendation(recommended_title, recommended_url)
                except:
                    pass
        except Exception as e:
            print(f"play_song_at_index error: {e}")

    def play_song(self):
        cur_selection = self.playlistbox.curselection()
        if cur_selection:
            selected_index = cur_selection[0]
            selected_song = self.playlist[selected_index]
            self.current_song_path = selected_song
            self.current_song_index = selected_index  # Mise à jour de l'index courant
            self.seek_offset_ms = 0
            pygame.mixer.music.load(selected_song)
            pygame.mixer.music.play()
            self.update_song_length(selected_song)  # <-- IMPORTANT

            current_song_title_with_duration = self.playlistbox.get(selected_index)
            current_song_title = current_song_title_with_duration.split('[')[0].strip()

            self.current_song_label.config(text=self.truncate_text(current_song_title))
            self.notify_song_change(current_song_title, self.playlist_name.get())
            
            # Charger la pochette et les infos
            metadata_list = self.load_metadata()
            url = None
            for metadata in metadata_list:
                if metadata['path'] == selected_song:
                    url = metadata.get('url', None)
                    break
            self.load_album_art(selected_song, url)
            
            # Afficher artiste, album, infos et écoutes
            self.update_now_playing_display(selected_song)
            
            # Incrémenter le compteur d'écoutes
            self.increment_listen_count(selected_song)
            
            # Mettre à jour Discord Rich Presence
            self.update_discord_presence(current_song_title, metadata_list[selected_index] if selected_index < len(metadata_list) else {})
        else:
            print("Aucune musique sélectionnée.")
        recommended_title, recommended_url = self.recommend_next_song()
        self.update_recommendation(recommended_title, recommended_url)

    def play_next_song(self):
        if len(self.playlist) == 0:
            print("La playlist est vide.")
            return

        # Utiliser l'index courant pour trouver le suivant
        next_song_index = (self.current_song_index + 1) % len(self.playlist)

        self.playlistbox.selection_clear(0, tk.END)
        self.playlistbox.selection_set(next_song_index)

        next_song = self.playlist[next_song_index]
        self.current_song_path = next_song
        self.current_song_index = next_song_index  # Mise à jour de l'index courant
        self.seek_offset_ms = 0
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()
        self.update_song_length(next_song)
        next_song_title = self.playlistbox.get(next_song_index).split('[')[0].strip()
        self.current_song_label.config(text=self.truncate_text(next_song_title))
        self.notify_song_change(next_song_title, self.playlist_name.get())
        
        # Charger la pochette et les infos
        metadata_list = self.load_metadata()
        url = None
        for metadata in metadata_list:
            if metadata['path'] == next_song:
                url = metadata.get('url', None)
                break
        self.load_album_art(next_song, url)
        
        # Afficher artiste, album, infos et écoutes
        self.update_now_playing_display(next_song)
        
        # Incrémenter le compteur d'écoutes
        self.increment_listen_count(next_song)
        
        # Mettre à jour Discord Rich Presence
        next_title = self.playlistbox.get(next_song_index).split('[')[0].strip()
        self.update_discord_presence(next_title, {})
        
        recommended_title, recommended_url = self.recommend_next_song()
        self.update_recommendation(recommended_title, recommended_url)

    def check_for_pygame_events(self):
        """Avance à la piste suivante à la fin, en ignorant les faux ‘end’ juste après un seek."""
        now = time.time()
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if now < self.ignore_end_event_until:
                    # Ignore le faux signal de fin déclenché par le seek
                    continue
                # Passer à la piste suivante avec mise à jour complète (image incluse)
                if len(self.playlist) > 0:
                    next_song_index = (self.current_song_index + 1) % len(self.playlist)
                    self.playlistbox.selection_clear(0, tk.END)
                    self.playlistbox.selection_set(next_song_index)
                    next_song = self.playlist[next_song_index]
                    self.current_song_path = next_song
                    self.current_song_index = next_song_index  # Mise à jour de l'index
                    self.seek_offset_ms = 0
                    pygame.mixer.music.load(next_song)
                    pygame.mixer.music.play()
                    self.update_song_length(next_song)
                    next_song_title = self.playlistbox.get(next_song_index).split('[')[0].strip()
                    self.current_song_label.config(text=self.truncate_text(next_song_title))
                    self.notify_song_change(next_song_title, self.playlist_name.get())
                    metadata_list = self.load_metadata()
                    url = None
                    for metadata in metadata_list:
                        if metadata['path'] == next_song:
                            url = metadata.get('url', None)
                            # Mettre à jour Discord Rich Presence
                            self.update_discord_presence(next_song_title, metadata)
                            break
                    self.load_album_art(next_song, url)
                    
                    # Afficher artiste, album, infos et écoutes
                    self.update_now_playing_display(next_song)
                    
                    # Incrémenter le compteur d'écoutes
                    self.increment_listen_count(next_song)
                    
                    recommended_title, recommended_url = self.recommend_next_song()
                    self.update_recommendation(recommended_title, recommended_url)
        self.master.after(500, self.check_for_pygame_events)

    def add_song(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = filepath.split("/")[-1]
            self.playlist.append(filepath)
            self.playlistbox.insert(tk.END, filename)

    def update_song_length(self, song_path):
        audio = MP3(song_path)
        self.current_song_length = int(audio.info.length * 1000)

    def stop_song(self):
        pygame.mixer.music.stop()

    def pause_song(self):
        pygame.mixer.music.pause()
    
    def on_close(self):
        # Stop audio and quit pygame cleanly, then close window
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
        try:
            pygame.quit()
        except Exception:
            pass
        self.master.destroy()
    
    def update_discord_presence(self, title, metadata):
        """Mets à jour la présence Discord avec les infos de la chanson actuelle"""
        if not DISCORD_AVAILABLE or self.discord_client is None:
            return
        
        try:
            # Extraire les infos de la chanson
            artist = metadata.get("artist", "Artiste inconnu") if isinstance(metadata, dict) else "Artiste inconnu"
            album = metadata.get("album", "Album inconnu") if isinstance(metadata, dict) else "Album inconnu"
            duration = metadata.get("duration", 0) if isinstance(metadata, dict) else 0
            
            # Formater l'affichage
            state = f"🎵 {artist}" if artist != "Artiste inconnu" else "Lecture en cours"
            details = title[:100]  # Limiter à 100 caractères
            
            # Calculer le temps restant (approximation)
            elapsed = int((pygame.mixer.music.get_pos() / 1000)) if pygame.mixer.music.get_busy() else 0
            
            # Mettre à jour la présence
            self.discord_client.update(
                state=state[:128],  # Limité à 128 caractères par Discord
                details=details,
                large_image="music_player",  # Nom de l'image large dans l'app Discord
                large_text=album[:128],
                start=0,  # Temps de début (en secondes depuis epoch, optionnel)
                party_size=[1, 1]  # [current, max] - un seul utilisateur
            )
        except Exception as e:
            # Silencieusement ignorer les erreurs Discord
            pass
    
    def apply_font_scale(self, size):
        """Applique le dimensionnement des polices selon la taille sélectionnée"""
        # Multiplicateurs pour chaque taille
        multipliers = {
            "small": 0.85,
            "normal": 1.0,
            "large": 1.15
        }
        multiplier = multipliers.get(size, 1.0)
        
        # Définir les tailles de base
        base_sizes = {
            "header": 18,
            "section": 12,
            "label": 11,
            "text": 10,
            "small": 9
        }
        
        # Calculer les tailles ajustées
        scaled_sizes = {k: int(v * multiplier) for k, v in base_sizes.items()}
        
        try:
            # Mettre à jour les headers s'ils existent
            if hasattr(self, 'header') and self.header:
                for child in self.header.winfo_children():
                    if isinstance(child, tk.Label):
                        try:
                            child.config(font=("Segoe UI", scaled_sizes["header"], "bold"))
                        except:
                            pass
            
            # Mettre à jour la barre de titre
            if hasattr(self, 'title_frame') and self.title_frame:
                for child in self.title_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        try:
                            current_font = child.cget("font")
                            if "bold" in str(current_font):
                                child.config(font=("Segoe UI", scaled_sizes["section"], "bold"))
                            else:
                                child.config(font=("Segoe UI", scaled_sizes["section"]))
                        except:
                            pass
            
            # Mettre à jour la liste des chansons
            if hasattr(self, 'playlistbox') and self.playlistbox:
                try:
                    self.playlistbox.config(font=("Segoe UI", scaled_sizes["text"]))
                except:
                    pass
            
            # Mettre à jour les contrôles (boutons, labels)
            if hasattr(self, 'control_frame') and self.control_frame:
                for child in self.control_frame.winfo_children():
                    if isinstance(child, (tk.Label, tk.Button)):
                        try:
                            child.config(font=("Segoe UI", scaled_sizes["text"]))
                        except:
                            pass
            
            # Mettre à jour la barre de progression
            if hasattr(self, 'time_frame') and self.time_frame:
                for child in self.time_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        try:
                            child.config(font=("Segoe UI", scaled_sizes["small"]))
                        except:
                            pass
            
            # Mettre à jour d'autres labels
            for attr_name in dir(self):
                if 'label' in attr_name.lower() and not attr_name.startswith('_'):
                    try:
                        widget = getattr(self, attr_name)
                        if isinstance(widget, tk.Label):
                            current_font = widget.cget("font")
                            if "bold" in str(current_font):
                                widget.config(font=("Segoe UI", scaled_sizes["label"], "bold"))
                            else:
                                widget.config(font=("Segoe UI", scaled_sizes["label"]))
                    except:
                        pass
        except Exception as e:
            print(f"Erreur lors de l'application du scale de police: {e}")
    
    def toggle_play_pause(self):
        """Bascule entre play et pause avec la barre espace"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            self.unpause_song()

    def truncate_text(self, text: str, max_len: int = 40) -> str:
        if not isinstance(text, str):
            return str(text)
        return text if len(text) <= max_len else text[:max_len-3] + "..."
    
    def load_settings(self):
        """Charge les paramètres depuis le fichier JSON"""
        default_settings = {
            "theme": "Purple Dream",
            "volume": 0.5,
            "auto_play_next": True,
            "font_scale": "normal"
        }
        
        if not os.path.exists('jsons'):
            os.makedirs('jsons')
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                    # Fusionner avec les valeurs par défaut pour les nouvelles clés
                    for key, value in default_settings.items():
                        if key not in self.settings:
                            self.settings[key] = value
            except (json.JSONDecodeError, Exception):
                self.settings = default_settings
        else:
            self.settings = default_settings
        
        # Charger le thème
        theme_name = self.settings.get("theme", "Purple Dream")
        self.theme = THEMES.get(theme_name, THEMES["Purple Dream"])
        self.current_theme_name = theme_name
    
    def save_settings(self):
        """Sauvegarde les paramètres dans le fichier JSON"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde settings: {e}")
    
    def apply_theme(self, theme_name):
        """Applique un nouveau thème et recharge l'interface"""
        if theme_name not in THEMES:
            return
        
        self.theme = THEMES[theme_name]
        self.current_theme_name = theme_name
        # Déterminer si le thème est clair pour ajuster les contrastes
        try:
            self.is_light_theme = self._is_light_color(self.theme.get("main_bg", "#000000"))
        except Exception:
            self.is_light_theme = False
        self.settings["theme"] = theme_name
        self.save_settings()
        
        # Rafraîchir immédiatement l'interface avec le nouveau thème
        try:
            self.refresh_theme_ui()
        except Exception as e:
            print(f"Erreur refresh theme: {e}")

    def refresh_theme_ui(self):
        """Met à jour dynamiquement les couleurs de l'interface selon le thème courant."""
        t = self.theme
        # Fenêtre et conteneurs principaux
        try:
            self.master.configure(bg=t["main_bg"])
        except Exception:
            pass
        if hasattr(self, "main_container"):
            self.main_container.configure(bg=t["main_bg"]) 
        if hasattr(self, "sidebar"):
            self.sidebar.configure(bg=t["sidebar_bg"]) 
        if hasattr(self, "center_frame"):
            self.center_frame.configure(bg=t["main_bg"]) 
        # Redessiner le gradient de fond
        if hasattr(self, "center_bg"):
            try:
                self.center_bg.configure(bg=t["main_bg"]) 
                self.draw_center_gradient()
            except Exception:
                pass

        # Window controls
        if hasattr(self, "window_controls"):
            try:
                self.window_controls.configure(bg=t["main_bg"]) 
                if hasattr(self, "minimize_button"):
                    self.minimize_button.configure(bg=t["secondary"], fg=t["text"]) 
            except Exception:
                pass

        # Sidebar frames
        if hasattr(self, "gradient_top"):
            self.gradient_top.configure(bg=t["gradient_top"]) 
        if hasattr(self, "title_frame"):
            self.title_frame.configure(bg=t["sidebar_bg"]) 
            for w in self.title_frame.winfo_children():
                if isinstance(w, tk.Label):
                    # Label avec image (icône)
                    if str(w.cget("image")) != "":
                        w.configure(bg=t["sidebar_bg"]) 
                    else:
                        w.configure(bg=t["sidebar_bg"], fg=t["text"]) 
        if hasattr(self, "playlist_frame"):
            self.playlist_frame.configure(bg=t["sidebar_bg"]) 
            # Update playlist menu as well
            if hasattr(self, "playlist_menu"):
                try:
                    self.playlist_menu.configure(bg=t["card_gradient"], fg=t["text"], activebackground=t["secondary"], activeforeground=t["text"]) 
                    pm = self.playlist_menu.nametowidget(self.playlist_menu.menuname)
                    pm.configure(bg=t["card_bg"], fg=t["text"]) 
                except Exception:
                    pass

        # Now Playing
        if hasattr(self, "now_playing_frame"):
            try:
                self.now_playing_frame.configure(bg=t["card_bg"], highlightbackground=t["accent"]) 
            except Exception:
                pass
        if hasattr(self, "gradient_bg"):
            self.gradient_bg.configure(bg=t["card_gradient"]) 
        if hasattr(self, "album_frame"):
            self.album_frame.configure(bg=t["card_bg"]) 
        if hasattr(self, "glow_outer"):
            self.glow_outer.configure(bg=t["accent"]) 
        if hasattr(self, "glow_inner"):
            self.glow_inner.configure(bg=t["highlight"]) 
        if hasattr(self, "art_border"):
            self.art_border.configure(bg=t["highlight"]) 
        if hasattr(self, "album_art_label"):
            try:
                self.album_art_label.configure(bg=t["sidebar_bg"]) 
                # Recalcule la pochette par défaut avec les nouvelles couleurs
                self.set_default_album_art()
            except Exception:
                pass
        if hasattr(self, "current_song_label"):
            self.current_song_label.configure(bg=t["card_bg"], fg=t["text"]) 
        if hasattr(self, "time_label"):
            self.time_label.configure(bg=t["card_bg"], fg=t["accent"]) 
        if hasattr(self, "recommendation_frame"):
            try:
                self.recommendation_frame.configure(bg=t["card_gradient"], highlightbackground=t["accent"])
            except Exception:
                pass
        if hasattr(self, "recommendation_label"):
            self.recommendation_label.configure(bg=t["card_gradient"], fg=t["text"]) 
        if hasattr(self, "recommendation_button"):
            self.recommendation_button.configure(bg=t["accent"], fg=t["sidebar_bg"]) 

        # Barre de progression
        if hasattr(self, "progress_bar") and hasattr(self.progress_bar, "set_theme"):
            self.progress_bar.set_theme(t)

        # Listes et listbox
        if hasattr(self, "playlistbox"):
            try:
                # Ajuster le contraste de la sélection pour les thèmes clairs
                select_fg = t["sidebar_bg"] if not getattr(self, "is_light_theme", False) else t["text"]
                self.playlistbox.configure(bg=t["list_bg"], fg=t["text"],
                                           selectbackground=t["accent"], selectforeground=select_fg) 
            except Exception:
                pass
        if hasattr(self, "list_container"):
            try:
                self.list_container.configure(bg=t["sidebar_bg"], highlightbackground=t["card_gradient"]) 
            except Exception:
                pass
        if hasattr(self, "list_header"):
            self.list_header.configure(bg=t["main_bg"]) 
        if hasattr(self, "title_container"):
            self.title_container.configure(bg=t["main_bg"]) 
            for w in self.title_container.winfo_children():
                if isinstance(w, tk.Label):
                    if w.cget("text") == "🎧":
                        w.configure(bg=t["main_bg"], fg=t["accent"]) 
                    else:
                        w.configure(bg=t["main_bg"], fg=t["text"]) 
        if hasattr(self, "separator_container"):
            self.separator_container.configure(bg=t["main_bg"]) 
        if hasattr(self, "separator"):
            self.separator.configure(bg=t["accent"]) 

        # Now Playing header (removed)

        # Menu de tri
        if hasattr(self, "sort_menu"):
            try:
                self.sort_menu.configure(bg=t["card_gradient"], fg=t["text"],
                                         activebackground=t["accent"], activeforeground=t["sidebar_bg"]) 
                sort_m = self.sort_menu.nametowidget(self.sort_menu.menuname)
                sort_m.configure(bg=t["card_bg"], fg=t["text"]) 
                if hasattr(self, "sort_options"):
                    for i in range(len(self.sort_options)):
                        try:
                            sort_m.entryconfig(i, activebackground=t["secondary"], activeforeground=t["text"]) 
                        except Exception:
                            pass
            except Exception:
                pass

        # Barre de contrôle et boutons
        if hasattr(self, "control_bar"):
            try:
                self.control_bar.configure(bg=t["control_bar"]) 
            except Exception:
                pass
            if hasattr(self, "border_glow"):
                self.border_glow.configure(bg=t["accent"]) 
            if hasattr(self, "border_top"):
                self.border_top.configure(bg=t["accent"]) 
            # Mettre à jour tous les boutons dans la barre de contrôle
            try:
                for child in self.control_bar.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn in child.winfo_children():
                            if isinstance(btn, tk.Button):
                                txt = btn.cget("text")
                                if txt in ("▶", "▶▶"):
                                    btn.configure(bg=t["accent"], fg=t["text"], highlightbackground=t["accent"]) 
                                    base_bg = t["accent"]
                                else:
                                    btn.configure(bg=t["secondary"], fg=t["text"], highlightbackground=t["control_bar"]) 
                                    base_bg = t["secondary"]
                                # Rebind hovers to use new theme colors
                                try:
                                    btn.bind("<Enter>", lambda e, b=btn: b.config(bg=t["highlight"], highlightbackground=t["accent"]))
                                    btn.bind("<Leave>", lambda e, b=btn, c=base_bg: b.config(bg=c, highlightbackground=t["control_bar"]))
                                except Exception:
                                    pass
                            elif isinstance(btn, tk.Label):
                                # Icône volume
                                if btn.cget("text") == "🔊":
                                    btn.configure(bg=t["control_bar"], fg=t["accent"]) 
                # Mettre à jour les containers eux-mêmes
                if hasattr(self, "controls_container"):
                    self.controls_container.configure(bg=t["control_bar"]) 
                if hasattr(self, "actions_frame"):
                    try:
                        self.actions_frame.configure(bg=t["control_bar"]) 
                        # Mettre à jour les petits boutons d'action
                        for w in self.actions_frame.winfo_children():
                            if isinstance(w, tk.Button):
                                # Conserver l'intention de couleur basée sur le label
                                txt = w.cget("text")
                                if "YouTube" in txt:
                                    w.configure(bg=t["accent"], fg=t["text"]) 
                                    base_bg = t["accent"]
                                elif "Suppr" in txt:
                                    w.configure(bg=t["highlight"], fg=t["text"]) 
                                    base_bg = t["highlight"]
                                else:
                                    w.configure(bg=t["secondary"], fg=t["text"]) 
                                    base_bg = t["secondary"]
                                try:
                                    w.bind("<Enter>", lambda e, b=w: b.config(bg=t["highlight"]))
                                    w.bind("<Leave>", lambda e, b=w, c=base_bg: b.config(bg=c))
                                except Exception:
                                    pass
                    except Exception:
                        pass
                if hasattr(self, "volume_frame"):
                    self.volume_frame.configure(bg=t["control_bar"]) 
            except Exception:
                pass

        # Volume slider
        if hasattr(self, "volume_scale") and hasattr(self.volume_scale, "set_theme"):
            self.volume_scale.set_theme(t)

        # Settings window live refresh
        if hasattr(self, "settings_window") and self.settings_window and self.settings_window.winfo_exists():
            try:
                self.settings_window.configure(bg=t["card_bg"]) 
            except Exception:
                pass
            if hasattr(self, "settings_header"):
                try:
                    self.settings_header.configure(bg=t["gradient_top"]) 
                except Exception:
                    pass
            if hasattr(self, "settings_main_frame"):
                self.settings_main_frame.configure(bg=t["card_bg"]) 
            if hasattr(self, "theme_frame"):
                self.theme_frame.configure(bg=t["secondary"]) 
            if hasattr(self, "theme_menu"):
                try:
                    self.theme_menu.configure(bg=t["secondary"], fg=t["text"],
                                              activebackground=t["highlight"], activeforeground=t["text"]) 
                    menu_widget = self.theme_menu.nametowidget(self.theme_menu.menuname)
                    menu_widget.configure(bg=t["card_gradient"], fg=t["text"],
                                          activebackground=t["highlight"], activeforeground=t["text"]) 
                except Exception:
                    pass
            if hasattr(self, "preview_frame"):
                self.preview_frame.configure(bg=t["card_bg"]) 
            if hasattr(self, "settings_close_btn"):
                try:
                    self.settings_close_btn.configure(bg=t["accent"], fg=t["card_bg"]) 
                except Exception:
                    pass
    
    def open_settings(self):
        """Ouvre la fenêtre de paramètres"""
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("⚙ Paramètres")
        self.settings_window.geometry("500x400")
        self.settings_window.configure(bg=self.theme["card_bg"])
        self.settings_window.resizable(False, False)
        
        try:
            self.settings_window.iconbitmap('logo.ico')
        except:
            pass
        
        # Header
        self.settings_header = tk.Frame(self.settings_window, bg=self.theme["gradient_top"], height=60)
        self.settings_header.pack(fill=tk.X)
        self.settings_header.pack_propagate(False)
        
        tk.Label(self.settings_header, text="⚙ PARAMÈTRES", bg=self.theme["gradient_top"], 
                fg=self.theme["text"], font=("Segoe UI", 18, "bold")).pack(pady=15)
        
        # Container principal
        self.settings_main_frame = tk.Frame(self.settings_window, bg=self.theme["card_bg"])
        self.settings_main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Section Thème
        theme_section = tk.Frame(self.settings_main_frame, bg=self.theme["card_bg"])
        theme_section.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(theme_section, text="🎨 Thème de l'interface", bg=self.theme["card_bg"],
                fg=self.theme["text"], font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Sélecteur de thème
        self.theme_frame = tk.Frame(theme_section, bg=self.theme["secondary"], bd=0)
        self.theme_frame.pack(fill=tk.X, ipady=5, ipadx=10)
        
        theme_var = tk.StringVar(value=self.current_theme_name)
        
        self.theme_menu = tk.OptionMenu(self.theme_frame, theme_var, *THEMES.keys(),
                       command=lambda t: self.apply_theme(t))
        self.theme_menu.config(bg=self.theme["secondary"], fg=self.theme["text"],
                         activebackground=self.theme["highlight"], activeforeground=self.theme["text"],
                         highlightthickness=0, relief=tk.FLAT, font=("Segoe UI", 11),
                         cursor="hand2", padx=10, pady=8)
        self.theme_menu.pack(fill=tk.X)
        
        menu_widget = self.theme_menu.nametowidget(self.theme_menu.menuname)
        menu_widget.config(bg=self.theme["card_gradient"], fg=self.theme["text"],
                          activebackground=self.theme["highlight"], activeforeground=self.theme["text"])
        
        # Aperçu du thème
        self.preview_frame = tk.Frame(self.settings_main_frame, bg=self.theme["card_bg"])
        self.preview_frame.pack(fill=tk.X, pady=(10, 20))
        
        tk.Label(self.preview_frame, text="👁 Aperçu:", bg=self.theme["card_bg"],
                fg=self.theme["text_dim"], font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(0, 5))
        
        preview_colors = tk.Frame(self.preview_frame, bg=self.theme["card_bg"])
        preview_colors.pack(fill=tk.X)
        
        def create_color_preview(parent, color, label):
            frame = tk.Frame(parent, bg=self.theme["card_bg"])
            frame.pack(side=tk.LEFT, padx=5)
            color_box = tk.Frame(frame, bg=color, width=40, height=40, relief=tk.RAISED, bd=1)
            color_box.pack()
            tk.Label(frame, text=label, bg=self.theme["card_bg"], fg=self.theme["text_dim"],
                    font=("Segoe UI", 8)).pack()
        
        create_color_preview(preview_colors, self.theme["accent"], "Accent")
        create_color_preview(preview_colors, self.theme["main_bg"], "Fond")
        create_color_preview(preview_colors, self.theme["text"], "Texte")
        create_color_preview(preview_colors, self.theme["progress"], "Barre")
        
        # Section Audio
        audio_section = tk.Frame(self.settings_main_frame, bg=self.theme["card_bg"])
        audio_section.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(audio_section, text="🔊 Audio", bg=self.theme["card_bg"],
                fg=self.theme["text"], font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Auto-play
        auto_play_var = tk.BooleanVar(value=self.settings.get("auto_play_next", True))
        
        def toggle_auto_play():
            self.settings["auto_play_next"] = auto_play_var.get()
            self.save_settings()
        
        auto_check = tk.Checkbutton(audio_section, text="Lecture automatique suivante",
                                    variable=auto_play_var, command=toggle_auto_play,
                                    bg=self.theme["card_bg"], fg=self.theme["text"],
                                    selectcolor=self.theme["secondary"], activebackground=self.theme["card_bg"],
                                    activeforeground=self.theme["accent"], font=("Segoe UI", 10))
        auto_check.pack(anchor=tk.W)
        
        # Section Affichage
        display_section = tk.Frame(self.settings_main_frame, bg=self.theme["card_bg"])
        display_section.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(display_section, text="📝 Affichage", bg=self.theme["card_bg"],
                fg=self.theme["text"], font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Font scaling options
        font_scale_var = tk.StringVar(value=self.settings.get("font_scale", "normal"))
        
        def change_font_scale(size):
            self.settings["font_scale"] = size
            self.save_settings()
            self.apply_font_scale(size)
        
        scale_options_frame = tk.Frame(display_section, bg=self.theme["card_bg"])
        scale_options_frame.pack(anchor=tk.W, pady=(0, 10))
        
        for size, label in [("small", "Petit"), ("normal", "Normal"), ("large", "Grand")]:
            scale_radio = tk.Radiobutton(scale_options_frame, text=label, variable=font_scale_var,
                                        value=size, command=lambda s=size: change_font_scale(s),
                                        bg=self.theme["card_bg"], fg=self.theme["text"],
                                        selectcolor=self.theme["accent"], activebackground=self.theme["card_bg"],
                                        activeforeground=self.theme["accent"], font=("Segoe UI", 10))
            scale_radio.pack(side=tk.LEFT, padx=(0, 15))
        
        # Bouton Fermer
        self.settings_close_btn = tk.Button(self.settings_main_frame, text="✓ Fermer", command=self.settings_window.destroy,
                             bg=self.theme["accent"], fg=self.theme["card_bg"],
                             font=("Segoe UI", 11, "bold"), relief=tk.FLAT, cursor="hand2",
                             padx=30, pady=10)
        self.settings_close_btn.pack(pady=20)
        self.settings_close_btn.bind("<Enter>", lambda e: self.settings_close_btn.config(bg=self.theme["highlight"]))
        self.settings_close_btn.bind("<Leave>", lambda e: self.settings_close_btn.config(bg=self.theme["accent"]))


    # ---------- Helpers & Gradient Drawing ----------
    def _hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def _mix(self, c1, c2, t):
        r1, g1, b1 = self._hex_to_rgb(c1)
        r2, g2, b2 = self._hex_to_rgb(c2)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return self._rgb_to_hex((r, g, b))

    def _is_light_color(self, h):
        r, g, b = self._hex_to_rgb(h)
        # Luminance approximative
        return (0.2126*r + 0.7152*g + 0.0722*b) > 180

    def draw_center_gradient(self):
        if not hasattr(self, 'center_bg'):
            return
        self.center_bg.delete('all')
        w = self.center_bg.winfo_width() or 1
        h = self.center_bg.winfo_height() or 1
        top = self.theme.get('gradient_top', '#000000')
        mid = self.theme.get('card_gradient', top)
        bottom = self.theme.get('main_bg', mid)
        # Dessiner bandes horizontales (20 steps)
        steps = 20
        for i in range(steps):
            t1 = i / steps
            t2 = (i+1) / steps
            # blend top->mid for first half, mid->bottom for second half
            if t1 < 0.5:
                c1 = self._mix(top, mid, t1*2)
                c2 = self._mix(top, mid, t2*2)
            else:
                c1 = self._mix(mid, bottom, (t1-0.5)*2)
                c2 = self._mix(mid, bottom, (t2-0.5)*2)
            y1 = int(h * t1)
            y2 = int(h * t2)
            self.center_bg.create_rectangle(0, y1, w, y2, outline='', fill=c1)

    def unpause_song(self):
        """Continue la lecture (unpause si en pause ou relance si arrêtée)."""
        try:
            # Premier essai: unpause si on est en pause
            pygame.mixer.music.unpause()
        except Exception:
            # Si unpause échoue, on est arrêtés: relancer depuis la position
            if self.current_song_path:
                pygame.mixer.music.load(self.current_song_path)
                # Attendre un court instant que le load soit complet
                import time
                time.sleep(0.05)
                pygame.mixer.music.play(loops=0, start=self.seek_offset_ms / 1000.0)
            else:
                # Aucune musique chargée : jouer la sélection
                self.play_song()

    def add_songs_from_file(self):
        if self.playlist_name.get() != "Favoris":
            file_path = filedialog.askopenfilename()
            if file_path:
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                thread = threading.Thread(target=self.add_videos_in_background, args=(lines,))
                thread.start()
        else:
            print("Vous ne pouvez pas ajouter des musiques directement dans la playlist Favoris")

    def add_videos_in_background(self, lines):
        for line in lines:
            self.process_line(line)

    def search_and_add_song_by_title(self, title):
        video_search = VideosSearch(title, limit=1)
        results = video_search.result()
        if 'result' in results and isinstance(results['result'], list) and len(results['result']) > 0:
            first_result = results['result'][0]
            if 'link' in first_result:
                video_url = first_result["link"]
                self.add_youtube_to_playlist(video_url)
            else:
                print(f"Aucun lien trouvé pour le titre {title}.")
        else:
            print(f"Aucune musique trouvée pour le titre {title}.")

    def process_line(self, line):
        line = line.strip()
        if line.startswith("http") or line.startswith("www"):
            self.add_youtube_to_playlist(line)
        else:
            self.search_and_add_song_by_title(line)

    def add_youtube_to_playlist(self, url=None):
        if self.playlist_name.get() != "Favoris":
            if url is None:
                url = ask_custom_url(self.master, "URL", "Entrez l'URL Youtube:")
            if not url:
                return
            try:
                yt = YouTube(url)
                ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                if ys is None:
                    ys = yt.streams.get_audio_only()
                if ys is None:
                    messagebox.showerror("YouTube", "Aucun flux audio disponible pour cette vidéo.")
                    return
            except Exception as e:
                messagebox.showerror("YouTube", f"Impossible de récupérer les flux (pytube): {e}\n"
                                                f"Mettez pytube à jour ou installez pytubefix.")
                return

            channel_name = yt.author
            clean_title = re.sub(r'[\\/*?:"<>|]', "", yt.title)
            display_title = f"{clean_title} - {channel_name}  "
            mp3_filename = os.path.join(self.music_folder, f"{clean_title}.mp3")

            if not os.path.exists(mp3_filename):
                try:
                    downloaded_path = ys.download(output_path=self.music_folder, filename=clean_title)
                except Exception as e:
                    messagebox.showerror("YouTube", f"Échec du téléchargement: {e}")
                    return

                try:
                    from moviepy.editor import AudioFileClip
                    with AudioFileClip(downloaded_path) as audio:
                        audio.write_audiofile(mp3_filename, logger=None)
                finally:
                    try:
                        if os.path.exists(downloaded_path):
                            os.remove(downloaded_path)
                    except PermissionError:
                        pass

            audio = MP3(mp3_filename)
            duration = audio.info.length
            mins, sec = divmod(int(duration), 60)

            favoris_metadata_file = 'jsons/metadata_Favoris.json'
            if self.playlist_name.get() == "Favoris":
                is_favorite = True
            else:
                is_favorite = False
            if os.path.exists(favoris_metadata_file):
                with open(favoris_metadata_file, 'r', encoding='utf-8') as f:
                    favoris_metadata = json.load(f)
                    is_favorite = any(metadata['path'] == mp3_filename for metadata in favoris_metadata)

            heart_icon = "   ❤" if is_favorite else ""

            display_title_with_duration = f"{display_title}  [{mins}:{sec}]{heart_icon}"
            self.playlistbox.insert(tk.END, display_title_with_duration)

            self.playlist.append(mp3_filename)
            author = yt.author
            publish_date = str(yt.publish_date)
            self.save_metadata(mp3_filename, display_title, author, publish_date, f"{mins}:{sec}", is_favorite, url)
        else:
            print("Vous ne pouvez pas ajouter des musiques directement dans la playlist Favoris")

    def toggle_favorite_status(self, song_path, is_favorite):
        for playlist_name in self.playlist_names:
            metadata_file = f'jsons/metadata_{playlist_name}.json'
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    content = f.read()
                    if content:
                        try:
                            metadata_list = json.loads(content)
                            for metadata in metadata_list:
                                if song_path == metadata['path']:
                                    metadata['is_favorite'] = is_favorite
                        except json.JSONDecodeError:
                            print("")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata_list, f)

    def delete_song(self):
        selected_index = self.playlistbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            confirm = ask_custom_yesno(self.master, "Confirmation",
                                       "Êtes-vous sûr de vouloir supprimer cette musique ?")
            if confirm:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

                is_in_other_playlist = False
                for playlist_name in self.playlist_names:
                    metadata_file = f'jsons/metadata_{playlist_name}.json'
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            content = f.read()
                            if content:
                                try:
                                    metadata_list = json.loads(content)
                                    for metadata in metadata_list:
                                        if self.playlist[selected_index] == metadata['path']:
                                            is_in_other_playlist = True
                                            break
                                except json.JSONDecodeError:
                                    print("")
                    if is_in_other_playlist:
                        break

                if not is_in_other_playlist:
                    try:
                        os.remove(self.playlist[selected_index])
                    except PermissionError:
                        return

                for playlist_name in self.playlist_names:
                    metadata_file = f'jsons/metadata_{playlist_name}.json'
                    if os.path.exists(metadata_file):
                        with open(metadata_file, 'r') as f:
                            content = f.read()
                            if content:
                                try:
                                    metadata_list = json.loads(content)
                                    for metadata in metadata_list:
                                        if self.playlist[selected_index] == metadata['path']:
                                            metadata['is_favorite'] = False
                                except json.JSONDecodeError:
                                    print("")
                        with open(metadata_file, 'w') as f:
                            json.dump(metadata_list, f)

                self.playlistbox.delete(selected_index)
                del self.playlist[selected_index]

                metadata_list = []
                if os.path.exists(self.metadata_file):
                    with open(self.metadata_file, 'r') as f:
                        content = f.read()
                        if content:
                            try:
                                metadata_list = json.loads(content)
                            except json.JSONDecodeError:
                                print("")
                del metadata_list[selected_index]
                with open(self.metadata_file, 'w') as f:
                    json.dump(metadata_list, f)
                self.clean_up_unused_files()


def videos_search_safe(query, limit):
    try:
        return VideosSearch(query, limit=limit).result()
    except TypeError as e:
        print("1")
        return None
    except Exception as e:
        messagebox.showerror("Recherche YouTube", f"Échec de la recherche: {e}")
        return None


root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
