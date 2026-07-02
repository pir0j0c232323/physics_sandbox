"""Панель инструментов с иконками"""
import customtkinter as ctk
import tkinter as tk
from Config.tools_config import MECHANICS_TOOLS, CATEGORY_ORDER


class ToolPanel(ctk.CTkFrame):
    def __init__(self, parent, on_tool_select=None, on_grid_toggle=None):
        super().__init__(parent, fg_color="#2c2c2c", height=60)
        self.pack(fill="x")
        self.pack_propagate(False)

        self.on_tool_select = on_tool_select
        self.on_grid_toggle = on_grid_toggle
        self.current_tool = ctk.StringVar(value="circle")
        self.show_grid = tk.BooleanVar(value=True)

        self.create_panel()

    def create_panel(self):
        """Создаёт панель инструментов"""
        # Чекбокс сетки
        self.grid_btn = ctk.CTkCheckBox(
            self,
            text="▦",
            variable=self.show_grid,
            fg_color="#2c2c2c",
            text_color="white",
            command=self._on_grid_toggle
        )
        self.grid_btn.pack(side="left", padx=10)

        # Разделитель
        ctk.CTkFrame(self, fg_color="#4c4c4c", width=2, height=40).pack(side="left", padx=10)

        # Контейнер для инструментов
        self.tools_container = ctk.CTkFrame(self, fg_color="#2c2c2c")
        self.tools_container.pack(side="left", fill="x", expand=True)

        # Показываем инструменты механики
        self.show_section("mechanics")

    def show_section(self, section_name):
        """Показывает инструменты для раздела"""
        # Очищаем контейнер
        for widget in self.tools_container.winfo_children():
            widget.destroy()

        # Получаем инструменты
        tools = MECHANICS_TOOLS if section_name == "mechanics" else {}

        # Группируем по категориям
        categories = {}
        for tool_id, tool_data in tools.items():
            category = tool_data.get("category", "other")
            if category not in categories:
                categories[category] = []
            categories[category].append((tool_id, tool_data))

        # Создаём кнопки для каждой категории
        for category in CATEGORY_ORDER:
            if category not in categories:
                continue

            # Разделитель между категориями (кроме первой)
            if category != CATEGORY_ORDER[0]:
                ctk.CTkFrame(self.tools_container, fg_color="#4c4c4c", width=2, height=40).pack(side="left", padx=10)

            for tool_id, tool_data in categories[category]:
                icon = tool_data.get("icon", "❓")
                tooltip = tool_data.get("tooltip", tool_id)

                btn = ctk.CTkButton(
                    self.tools_container,
                    text=icon,
                    width=35,
                    height=35,
                    fg_color="white",
                    text_color="black",
                    hover_color="#f0f0f0",
                    command=lambda t=tool_id: self.select_tool(t)
                )
                btn.pack(side="left", padx=3, pady=5)

    def select_tool(self, tool_name):
        """Выбор инструмента"""
        self.current_tool.set(tool_name)
        if self.on_tool_select:
            self.on_tool_select(tool_name)
        print(f"Выбран инструмент: {tool_name}")

    def _on_grid_toggle(self):
        """Обработчик переключения сетки"""
        if self.on_grid_toggle:
            self.on_grid_toggle(self.show_grid.get())
        print(f"Сетка: {'включена' if self.show_grid.get() else 'выключена'}")