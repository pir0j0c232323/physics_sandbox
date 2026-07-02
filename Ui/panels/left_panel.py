"""Левая панель - иерархия объектов"""
import customtkinter as ctk
from tkinter import scrolledtext
import tkinter as tk


class LeftPanel(ctk.CTkFrame):
    def __init__(self, parent, on_hierarchy_click=None, on_show_all=None, on_hide_all=None):
        super().__init__(parent, fg_color="#f5f5f5", width=220)
        self.pack(side="left", fill="y")
        self.pack_propagate(False)

        self.on_hierarchy_click = on_hierarchy_click
        self.on_show_all = on_show_all
        self.on_hide_all = on_hide_all

        self.create_panel()

    def create_panel(self):
        """Создаёт левую панель"""
        # Заголовок
        ctk.CTkLabel(
            self, text="📋 ИЕРАРХИЯ",
            fg_color="#f5f5f5", text_color="black",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # Список объектов
        self.objects_list = scrolledtext.ScrolledText(
            self, width=22, height=25,
            font=("Arial", 9), bg="white"
        )
        self.objects_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.objects_list.config(state="disabled")
        self.objects_list.bind("<Button-3>", self._on_right_click)

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="#f5f5f5")
        btn_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(
            btn_frame, text="👁️ Все",
            command=self._show_all,
            fg_color="lightblue", text_color="black", width=80
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame, text="🙈 Скрыть",
            command=self._hide_all,
            fg_color="lightgray", text_color="black", width=80
        ).pack(side="left", padx=2)

    def _on_right_click(self, event):
        if self.on_hierarchy_click:
            index = self.objects_list.index(f"@{event.x},{event.y}")
            line_number = int(index.split('.')[0])
            self.on_hierarchy_click(line_number, event)

    def _show_all(self):
        if self.on_show_all:
            self.on_show_all()

    def _hide_all(self):
        if self.on_hide_all:
            self.on_hide_all()

    def add_object(self, text):
        """Добавляет объект в список"""
        self.objects_list.config(state="normal")
        self.objects_list.insert(tk.END, text)
        self.objects_list.see(tk.END)
        self.objects_list.config(state="disabled")

    def remove_object(self, index):
        """Удаляет объект из списка"""
        self.objects_list.config(state="normal")
        line_number = index + 1
        self.objects_list.delete(f"{line_number}.0", f"{line_number + 1}.0")
        self.objects_list.config(state="disabled")

    def clear(self):
        """Очищает список"""
        self.objects_list.config(state="normal")
        self.objects_list.delete(1.0, tk.END)
        self.objects_list.config(state="disabled")