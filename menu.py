# menu.py
import customtkinter as ctk
import tkinter as tk

class ContextMenu:
    """Контекстное меню для объектов"""

    def __init__(self, root, delete_func, params_func, duplicate_func):
        self.menu = tk.Menu(root, tearoff=0, font=("Arial", 11))
        self.menu.add_command(label="🗑️ Удалить", command=delete_func)
        self.menu.add_command(label="⚙️ Параметры", command=params_func)
        self.menu.add_separator()
        self.menu.add_command(label="📋 Дублировать", command=duplicate_func)

    def show(self, x, y):
        """Показывает меню в точке (x, y)"""
        self.menu.post(x, y)