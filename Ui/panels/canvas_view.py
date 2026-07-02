"""Canvas для отрисовки"""
import tkinter as tk


class CanvasView(tk.Canvas):
    def __init__(self, parent, on_resize=None):
        super().__init__(parent, bg="white", highlightthickness=0)
        self.pack(side="right", fill="both", expand=True)

        self.on_resize = on_resize
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        if self.on_resize:
            self.on_resize(event)

    def draw_grid(self, width, height, show=True):
        """Рисует сетку"""
        if not show:
            return

        major = 50
        minor = 10

        # Подсетка
        for x in range(0, width, minor):
            if x % major != 0:
                self.create_line(x, 0, x, height, fill="#f0f0f0", width=1)

        for y in range(0, height, minor):
            if y % major != 0:
                self.create_line(0, y, width, y, fill="#f0f0f0", width=1)

        # Основная сетка
        for x in range(0, width, major):
            self.create_line(x, 0, x, height, fill="#e0e0e0", width=1)

        for y in range(0, height, major):
            self.create_line(0, y, width, y, fill="#e0e0e0", width=1)