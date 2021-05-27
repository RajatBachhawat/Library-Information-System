from tkinter import *
from tkinter import ttk
from colors import *

class ScrollableFrame(Frame):
    def __init__(self, container):

        super().__init__(container)
        self.canvas = Canvas(self, bg = lightorange)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg = lightorange)

        # self.scrollable_frame.config()

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind("<Configure>", self.resize_frame)

        self._frame_id = self.canvas.create_window((0, 0), height=500, width=500, window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.place(relx = 1, relheight = 1, anchor = 'ne')

    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id, height=e.height, width=e.width)