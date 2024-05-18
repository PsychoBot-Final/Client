import tkinter as tk
import customtkinter as ctk

class News:
    def __init__(self, root):
        self.root = root
        self.top_frame = ctk.CTkFrame(self.root)
        self.top_frame.pack(fill='x')

        # Set the background color to match the top_frame
        self.canvas = tk.Canvas(self.top_frame, height=30, highlightthickness=2)
        self.canvas.pack(side='left', fill='x', expand=True, padx=10, pady=(5, 5))

        self.news_text = "News: Savi is a fantastic person..."
        self.text_id = self.canvas.create_text(0, 15, anchor='w', text=self.news_text, font=('Century Gothic', 12, 'bold'), fill='black')

        self.scroll_text()

    def scroll_text(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.text_id)
        if x2 < 0:
            self.canvas.coords(self.text_id, self.canvas.winfo_width(), 15)  # Reset y-coordinate to 15
        else:
            self.canvas.move(self.text_id, -2, 0)
        self.root.after(30, self.scroll_text)