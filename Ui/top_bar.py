"""Верхняя панель с разделами"""
import customtkinter as ctk


class TopBar(ctk.CTkFrame):
    def __init__(self, parent, on_section_change=None, on_settings=None):
        super().__init__(parent, fg_color="#2c2c2c", corner_radius=0, height=50)
        self.pack(fill="x")
        self.pack_propagate(False)

        self.on_section_change = on_section_change
        self.on_settings = on_settings

        self.create_bar()

    def create_bar(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        # Логотип
        ctk.CTkLabel(
            self, text="PHYSX",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w", padx=15)

        # Кнопка настроек
        ctk.CTkButton(
            self, text="⚙️",
            fg_color="#3c3c3c", text_color="white",
            width=40, command=self._on_settings
        ).grid(row=0, column=2, sticky="e", padx=15)

        # Центральные кнопки
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=1)

        ctk.CTkButton(
            center, text="⚙️ МЕХАНИКА",
            fg_color="#3c3c3c", text_color="white",
            command=lambda: self._select("mechanics")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            center, text="🔬 МОЛЕКУЛЯРКА",
            fg_color="#3c3c3c", text_color="white",
            command=lambda: self._select("molecular")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            center, text="⚡ ЭЛЕКТРОНИКА",
            fg_color="#3c3c3c", text_color="white",
            command=lambda: self._select("electronics")
        ).pack(side="left", padx=10)

    def _select(self, section):
        if self.on_section_change:
            self.on_section_change(section)

    def _on_settings(self):
        if self.on_settings:
            self.on_settings()