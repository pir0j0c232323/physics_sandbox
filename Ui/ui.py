"""Главный класс интерфейса"""
import customtkinter as ctk
from tkinter import colorchooser, scrolledtext
import tkinter as tk
from Ui.top_bar import TopBar
from Ui.panels.left_panel import LeftPanel
from Ui.panels.right_panel import RightPanel
from Ui.panels.canvas_view import CanvasView
from Ui.tool_panel import ToolPanel

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Физическая песочница v2.5")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c2c2c")

        # Переменные
        self.current_object = ctk.StringVar(value="circle")
        self.current_section = ctk.StringVar(value="mechanics")
        self.elasticity_var = ctk.DoubleVar(value=0.8)
        self.paused = ctk.BooleanVar(value=False)
        self.show_grid = ctk.BooleanVar(value=True)

        # Callbacks
        self.on_clear_callback = None
        self.on_object_property_callback = None
        self.on_gravity_callback = None
        self.on_hierarchy_callback = None

        # Создаём компоненты
        self.top_bar = TopBar(
            self.root,
            on_section_change=self.on_section_change,
            on_settings=self.open_settings
        )

        self.tool_panel = ToolPanel(
            self.root,
            on_tool_select=self.on_tool_select,
            on_grid_toggle=self.on_grid_toggle
        )

        # Основной контейнер
        main_container = ctk.CTkFrame(self.root, fg_color="white")
        main_container.pack(fill="both", expand=True)

        # Панели
        self.left_panel = LeftPanel(
            main_container,
            on_hierarchy_click=self._on_hierarchy_click,
            on_show_all=self.show_all_objects,
            on_hide_all=self.hide_all_objects
        )

        self.right_panel = RightPanel(
            main_container,
            on_property_change=self._on_prop_change,
            on_gravity_change=self._on_gravity_change,
            on_pause=self._on_pause,
            on_clear=self._do_clear
        )

        self.canvas_view = CanvasView(
            main_container,
            on_resize=self._on_resize
        )

        # Для совместимости
        self.canvas = self.canvas_view
        self.objects_list = self.left_panel.objects_list

    def on_section_change(self, section):
        self.tool_panel.show_section(section)
        self.current_section.set(section)

    def on_tool_select(self, tool):
        self.current_object.set(tool)

    def on_grid_toggle(self, show):
        self.show_grid.set(show)

    def _on_prop_change(self):
        if self.on_object_property_callback:
            self.on_object_property_callback()

    def _on_gravity_change(self, gx, gy):
        if self.on_gravity_callback:
            self.on_gravity_callback(gx, gy)

    def _on_pause(self):
        self.paused.set(self.right_panel.paused.get())

    def _do_clear(self):
        if self.on_clear_callback:
            self.on_clear_callback()

    def _on_resize(self, event):
        pass

    def _on_hierarchy_click(self, line, event):
        if self.on_hierarchy_callback:
            self.on_hierarchy_callback(line, event)

    def show_all_objects(self):
        print("Показать все")

    def hide_all_objects(self):
        print("Скрыть все")

    def add_object_to_list(self, text):
        self.left_panel.add_object(text)

    def remove_object_from_list(self, index):
        self.left_panel.remove_object(index)

    def update_object_properties(self, obj):
        self.right_panel.update_properties(obj)

    def update_stats(self, created, visible):
        self.right_panel.update_stats(created, visible)

    def toggle_pause(self):
        self.paused.set(not self.paused.get())
        self.right_panel._toggle_pause()

    def open_settings(self):
        """Окно настроек (упрощённо)"""
        print("Настройки")