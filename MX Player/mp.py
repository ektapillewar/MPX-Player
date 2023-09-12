import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pygame
import os
from ttkthemes import ThemedStyle

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")

        style = ThemedStyle(root)
        style.set_theme("aquativo")

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=20)

        self.play_icon = tk.PhotoImage(file="play_icon.png")
        self.pause_icon = tk.PhotoImage(file="pause_icon.png")

        self.play_icon = self.play_icon.subsample(14, 15)
        self.pause_icon = self.pause_icon.subsample(14, 15)
        self.select_button = ttk.Button(button_frame, text="Select Media File", command=self.open_file)
        self.select_button.pack()

        self.play_button = ttk.Button(button_frame, text="Play    ", image=self.play_icon, compound=tk.LEFT, state=tk.DISABLED, command=self.play_media)
        self.play_button.pack()

        self.pause_button = ttk.Button(button_frame, text="Pause  ", image=self.pause_icon, compound=tk.LEFT, state=tk.DISABLED, command=self.pause_media)
        self.pause_button.pack()

        bold_font = (style.lookup("TButton", "font"), "-weight", "bold")
        style.configure("Bold.TButton", font=bold_font)

        self.current_time_label = ttk.Label(button_frame, text="00:00")
        self.current_time_label.pack()
        pygame.mixer.init()

        self.audio_file = None
        self.playing = False

        self.update_current_time()

    def open_file(self):
        initial_dir = "Media Files"
        filedialog_options = {
            "initialdir": initial_dir,
            "filetypes": [("Media Files", "*.mp3")]
        }

        file_path = filedialog.askopenfilename(**filedialog_options)

        if file_path:
            self.audio_file = file_path
            self.play_button["state"] = tk.NORMAL

    def play_media(self):
        if self.audio_file:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            self.play_button["state"] = tk.DISABLED
            self.pause_button["state"] = tk.NORMAL
            self.playing = True

    def pause_media(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button["state"] = tk.NORMAL
            self.pause_button["state"] = tk.DISABLED
            self.playing = False

    def update_current_time(self):
        if self.playing:
            current_time_ms = pygame.mixer.music.get_pos()
            current_time_s = current_time_ms // 1000
            minutes = current_time_s // 60
            seconds = current_time_s % 60
            time_str = f"{minutes:02}:{seconds:02}"
            self.current_time_label.config(text=time_str)
        self.root.after(1000, self.update_current_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()
