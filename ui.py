import customtkinter as ctk
from tkinter import ttk, colorchooser, scrolledtext
from theme import theme
import tkinter as tk

class UserInterface:
    """Управляет интерфейсом"""

    def __init__(self, root):
        self.root = root
        self.root.title("Физическая песочница v2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c2c2c")

        self.current_object = ctk.StringVar(value="circle")
        self.current_section = ctk.StringVar(value="mechanics")
        self.gravity_var = ctk.IntVar(value=500)
        self.elasticity_var = ctk.DoubleVar(value=0.8)
        self.paused = ctk.BooleanVar(value=False)
        self.show_grid = ctk.BooleanVar(value=True)

        self.obj_size_var = ctk.IntVar(value=20)
        self.obj_mass_var = ctk.DoubleVar(value=1.0)
        self.obj_elasticity_var = ctk.DoubleVar(value=0.8)
        self.obj_pos_x_var = ctk.IntVar(value=0)
        self.obj_pos_y_var = ctk.IntVar(value=0)
        self.obj_color_var = ctk.StringVar(value="red")

        self.on_clear_callback = None
        self.on_object_property_callback = None
        self.on_gravity_callback = None

        self.create_toolbar()
        self.create_objects_toolbar()
        self.create_main_container()

    def create_toolbar(self):
        """Создаёт верхнюю панель с разделами"""
        self.toolbar = ctk.CTkFrame(
            self.root,
            fg_color="#2c2c2c",
            height=50
        )
        self.toolbar.pack(fill="x")
        self.toolbar.pack_propagate(False)

        # Кнопка настроек
        btn_settings = ctk.CTkButton(
            self.toolbar,
            text="⚙️",
            fg_color="#3c3c3c",
            text_color="white",
            width=40,
            command=self.open_settings
        )
        btn_settings.pack(side="right", padx=5, pady=8)

        # Кнопки разделов
        btn_mechanics = ctk.CTkButton(
            self.toolbar,
            text="⚙️ МЕХАНИКА",
            fg_color="#3c3c3c",
            text_color="white",
            command=self.select_mechanics
        )
        btn_mechanics.pack(side="left", padx=5, pady=8)

        btn_molecular = ctk.CTkButton(
            self.toolbar,
            text="🔬 МОЛЕКУЛЯРКА",
            fg_color="#3c3c3c",
            text_color="white",
            command=self.select_molecular
        )
        btn_molecular.pack(side="left", padx=5, pady=8)

        btn_electronics = ctk.CTkButton(
            self.toolbar,
            text="⚡ ЭЛЕКТРОНИКА",
            fg_color="#3c3c3c",
            text_color="white",
            command=self.select_electronics
        )
        btn_electronics.pack(side="left", padx=5, pady=8)

        self.section_buttons = {
            "mechanics": btn_mechanics,
            "molecular": btn_molecular,
            "electronics": btn_electronics
        }

    def create_objects_toolbar(self):
        """Создаёт панель с кнопками объектов"""
        self.objects_toolbar = ctk.CTkFrame(self.root, fg_color="#e0e0e0", height=60)
        self.objects_toolbar.pack(fill="x")
        self.objects_toolbar.pack_propagate(False)

        ctk.CTkLabel(self.objects_toolbar, text="Объекты:",
                 fg_color="#e0e0e0", text_color="black",
                 font=("Arial", 11, "bold")).pack(side="left", padx=10)

        self.grid_btn = ctk.CTkCheckBox(
            self.objects_toolbar,
            text="📐 Сетка",
            variable=self.show_grid,
            fg_color="#e0e0e0"
        )
        self.grid_btn.pack(side="left", padx=20)

        self.mechanics_objects = ctk.CTkFrame(self.objects_toolbar, fg_color="#e0e0e0")

        for text, obj_type in [("⭕ Шар", "circle"), ("⬛ Квадрат", "square"),
                               ("🔺 Треугольник", "triangle"), ("📏 Стержень", "stick"),
                               ("↔ Пружина", "spring")]:
            btn = ctk.CTkButton(
                self.mechanics_objects,
                text=text,
                command=lambda t=obj_type: self.select_object(t),
                fg_color="white",
                text_color="black"
            )
            btn.pack(side="left", padx=5, pady=5)

        self.molecular_objects = ctk.CTkFrame(self.objects_toolbar, fg_color="#e0e0e0")

        for text, obj_type in [("⚫ Атом", "atom"), ("💧 Капля", "drop"), ("💨 Газ", "gas")]:
            btn = ctk.CTkButton(
                self.molecular_objects,
                text=text,
                command=lambda t=obj_type: self.select_object(t),
                fg_color="white",
                text_color="black"
            )
            btn.pack(side="left", padx=5, pady=5)

        self.electronics_objects = ctk.CTkFrame(self.objects_toolbar, fg_color="#e0e0e0")

        for text, obj_type in [("🔋 Батарея", "battery"), ("💡 Лампочка", "bulb"), ("➖ Провод", "wire")]:
            btn = ctk.CTkButton(
                self.electronics_objects,
                text=text,
                command=lambda t=obj_type: self.select_object(t),
                fg_color="white",
                text_color="black"
            )
            btn.pack(side="left", padx=5, pady=5)

        self.show_objects_section("mechanics")

    def show_objects_section(self, section_name):
        self.mechanics_objects.pack_forget()
        self.molecular_objects.pack_forget()
        self.electronics_objects.pack_forget()

        if section_name == "mechanics":
            self.mechanics_objects.pack(side="left", fill="x", expand=True)
        elif section_name == "molecular":
            self.molecular_objects.pack(side="left", fill="x", expand=True)
        elif section_name == "electronics":
            self.electronics_objects.pack(side="left", fill="x", expand=True)

    def toggle_grid(self):
        print(f"Сетка: {'включена' if self.show_grid.get() else 'выключена'}")

    def show_section(self, section_name):
        self.show_objects_section(section_name)
        self.current_section.set(section_name)
        print(f"Выбран раздел: {section_name}")

    def select_mechanics(self):
        self.show_section("mechanics")

    def select_molecular(self):
        self.show_section("molecular")

    def select_electronics(self):
        self.show_section("electronics")

    def select_object(self, obj_type):
        self.current_object.set(obj_type)
        print(f"Выбран объект: {obj_type}")

    def create_main_container(self):
        """Создаёт основной контейнер"""
        main_container = ctk.CTkFrame(self.root, fg_color="white")
        main_container.pack(fill="both", expand=True)

        # ЛЕВАЯ ПАНЕЛЬ
        left_container = ctk.CTkFrame(main_container, fg_color="#f5f5f5", width=220)
        left_container.pack(side="left", fill="y")
        left_container.pack_propagate(False)

        ctk.CTkLabel(left_container, text="📋 ИЕРАРХИЯ",
                 fg_color="#f5f5f5", text_color="black",
                 font=("Arial", 12, "bold")).pack(pady=10)

        self.objects_list = scrolledtext.ScrolledText(
            left_container, width=22, height=25,
            font=("Arial", 9), bg="white"
        )
        self.objects_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.objects_list.config(state="disabled")
        self.objects_list.bind("<Button-3>", self.on_hierarchy_right_click)

        btn_frame = ctk.CTkFrame(left_container, fg_color="#f5f5f5")
        btn_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(btn_frame, text="👁️ Все", command=self.show_all_objects,
                  fg_color="lightblue", text_color="black", width=80).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="🙈 Скрыть", command=self.hide_all_objects,
                  fg_color="lightgray", text_color="black", width=80).pack(side="left", padx=2)

        # ПРАВАЯ ПАНЕЛЬ
        self.properties_panel = ctk.CTkFrame(main_container, fg_color="#e0e0e0", width=300)
        self.properties_panel.pack(side="right", fill="y")
        self.properties_panel.pack_propagate(False)

        ctk.CTkLabel(self.properties_panel, text="⚙️ СВОЙСТВА",
                 fg_color="#e0e0e0", text_color="black",
                 font=("Arial", 14, "bold")).pack(pady=10)

        ctk.CTkFrame(self.properties_panel, fg_color="gray", height=2).pack(fill="x", padx=10)

        # Свойства объекта
        self.obj_properties_frame = ctk.CTkFrame(self.properties_panel, fg_color="#d0d0d0")

        ctk.CTkLabel(self.obj_properties_frame, text="🎯 Свойства объекта:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 11, "bold")).pack(pady=(5, 5))

        ctk.CTkLabel(self.obj_properties_frame, text="Размер:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 10)).pack(anchor="w", padx=15)
        tk.Scale(self.obj_properties_frame, from_=5, to=100,
                 orient="horizontal", variable=self.obj_size_var,
                 bg="#d0d0d0", command=lambda v: self._on_obj_prop_change()).pack(fill="x", padx=15)

        ctk.CTkLabel(self.obj_properties_frame, text="Масса:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 10)).pack(anchor="w", padx=15, pady=(5, 0))
        tk.Scale(self.obj_properties_frame, from_=0.1, to=10, resolution=0.1,
                 orient="horizontal", variable=self.obj_mass_var,
                 bg="#d0d0d0", command=lambda v: self._on_obj_prop_change()).pack(fill="x", padx=15)

        ctk.CTkLabel(self.obj_properties_frame, text="Упругость:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 10)).pack(anchor="w", padx=15, pady=(5, 0))
        tk.Scale(self.obj_properties_frame, from_=0, to=1, resolution=0.1,
                 orient="horizontal", variable=self.obj_elasticity_var,
                 bg="#d0d0d0", command=lambda v: self._on_obj_prop_change()).pack(fill="x", padx=15)

        ctk.CTkLabel(self.obj_properties_frame, text="Цвет:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 10)).pack(anchor="w", padx=15, pady=(5, 0))

        color_frame = ctk.CTkFrame(self.obj_properties_frame, fg_color="#d0d0d0")
        color_frame.pack(padx=15, pady=5)

        for color in ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]:
            btn = ctk.CTkButton(color_frame, fg_color=color, width=30, height=30,
                            command=lambda c=color: self._set_obj_color(c))
            btn.pack(side="left", padx=2)

        self.obj_properties_frame.pack_forget()

        # Параметры мира
        world_frame = ctk.CTkFrame(self.properties_panel, fg_color="#d0d0d0")
        world_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(world_frame, text="🌍 Параметры мира:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 11, "bold")).pack(pady=(5, 10))

        ctk.CTkLabel(world_frame, text="Гравитация Y:",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 10)).pack(anchor="w", padx=10)
        self.gravity_y_scale = tk.Scale(world_frame, from_=-2000, to=2000,
                                        orient="horizontal", bg="#d0d0d0",
                                        command=lambda v: self.on_world_gravity_change())
        self.gravity_y_scale.set(500)
        self.gravity_y_scale.pack(fill="x", padx=10)

        ctk.CTkLabel(world_frame, text="Ветер (гравитация X):",
                 fg_color="#d0d0d0", text_color="black",
                 font=("Arial", 10)).pack(anchor="w", padx=10, pady=(5, 0))
        self.gravity_x_scale = tk.Scale(world_frame, from_=-1000, to=1000,
                                        orient="horizontal", bg="#d0d0d0",
                                        command=lambda v: self.on_world_gravity_change())
        self.gravity_x_scale.set(0)
        self.gravity_x_scale.pack(fill="x", padx=10)

        # Управление
        ctk.CTkLabel(self.properties_panel, text="Управление:",
                 fg_color="#e0e0e0", text_color="black",
                 font=("Arial", 11, "bold")).pack(pady=(15, 5))

        self.btn_pause = ctk.CTkButton(self.properties_panel, text="⏸️ Пауза",
                                   command=self.toggle_pause,
                                   fg_color="yellow", text_color="black")
        self.btn_pause.pack(pady=5)

        self.btn_clear = ctk.CTkButton(self.properties_panel, text="🗑️ Очистить всё",
                                   command=self._do_clear,
                                   fg_color="red", text_color="white")
        self.btn_clear.pack(pady=5)

        ctk.CTkLabel(self.properties_panel, text=" Статистика:",
                 fg_color="#e0e0e0", text_color="black",
                 font=("Arial", 11, "bold")).pack(pady=(15, 5))

        self.stats_label = ctk.CTkLabel(
            self.properties_panel,
            text="Создано: 0\nНа экране: 0",
            fg_color="#e0e0e0",
            text_color="black",
            font=("Arial", 10),
            justify="left"
        )
        self.stats_label.pack(anchor="w", padx=20)

        # CANVAS
        self.canvas = tk.Canvas(main_container, bg="white", highlightthickness=0)
        self.canvas.pack(side="right", fill="both", expand=True)

    def show_all_objects(self):
        print("Показать все объекты")

    def hide_all_objects(self):
        print("Скрыть все объекты")

    def _do_clear(self):
        if self.on_clear_callback:
            self.on_clear_callback()

    def toggle_pause(self):
        self.paused.set(not self.paused.get())
        if self.paused.get():
            self.btn_pause.configure(text="▶️ Старт", fg_color="lightgreen")
        else:
            self.btn_pause.configure(text="⏸️ Пауза", fg_color="yellow")

    def update_stats(self, created, visible):
        self.stats_label.configure(text=f"Создано: {created}\nНа экране: {visible}")

    def on_hierarchy_right_click(self, event):
        index = self.objects_list.index(f"@{event.x},{event.y}")
        line_number = int(index.split('.')[0])
        if hasattr(self, 'on_hierarchy_callback'):
            self.on_hierarchy_callback(line_number, event)

    def add_object_to_list(self, text):
        self.objects_list.config(state="normal")
        self.objects_list.insert(tk.END, text)
        self.objects_list.see(tk.END)
        self.objects_list.config(state="disabled")

    def remove_object_from_list(self, index):
        self.objects_list.config(state="normal")
        line_number = index + 1
        self.objects_list.delete(f"{line_number}.0", f"{line_number + 1}.0")
        self.objects_list.config(state="disabled")

    def _on_obj_prop_change(self):
        if self.on_object_property_callback:
            self.on_object_property_callback()

    def _set_obj_color(self, color):
        self.obj_color_var.set(color)
        if self.on_object_property_callback:
            self.on_object_property_callback()

    def update_object_properties(self, obj):
        if obj:
            self.obj_size_var.set(int(obj.size))
            self.obj_mass_var.set(obj.body.mass)
            self.obj_elasticity_var.set(obj.shape.elasticity)
            self.obj_pos_x_var.set(int(obj.body.position.x))
            self.obj_pos_y_var.set(int(obj.body.position.y))
            self.obj_color_var.set(obj.color)
            self.obj_properties_frame.pack(fill="x", padx=10, pady=10)
        else:
            self.obj_properties_frame.pack_forget()

    def on_world_gravity_change(self):
        if self.on_gravity_callback:
            gx = self.gravity_x_scale.get()
            gy = self.gravity_y_scale.get()
            self.on_gravity_callback(gx, gy)

    def open_settings(self):
        """Открывает окно настроек темы"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title("🎨 Настройки темы")
        settings_win.geometry("600x800")
        settings_win.configure(bg="#f0f0f0")

        canvas = tk.Canvas(settings_win, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(settings_win, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color="#f0f0f0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ctk.CTkLabel(
            scrollable_frame,
            text="Настройки оформления",
            fg_color="#f0f0f0",
            text_color="#2c2c2c",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        preset_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")
        preset_frame.pack(pady=10)

        ctk.CTkLabel(
            preset_frame,
            text="📦 Быстрые пресеты:",
            fg_color="#f0f0f0",
            text_color="black",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            preset_frame,
            text="🌙 Тёмная",
            fg_color="#3c3c3c",
            text_color="white",
            command=lambda: self._apply_preset("dark")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            preset_frame,
            text="☀️ Светлая",
            fg_color="#e0e0e0",
            text_color="black",
            command=lambda: self._apply_preset("light")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            preset_frame,
            text=" Игровая",
            fg_color="#8e44ad",
            text_color="white",
            command=lambda: self._apply_preset("gaming")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            preset_frame,
            text="🌊 Океан",
            fg_color="#2980b9",
            text_color="white",
            command=lambda: self._apply_preset("ocean")
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            scrollable_frame,
            text="Верхняя панель (toolbar)",
            fg_color="#f0f0f0",
            text_color="#2c2c2c",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(20, 10))

        self._add_color_setting(scrollable_frame, "Фон toolbar:", "#2c2c2c", "toolbar_bg")
        self._add_color_setting(scrollable_frame, "Кнопки разделов:", "#3c3c3c", "toolbar_btn_bg")

        ctk.CTkLabel(
            scrollable_frame,
            text="Боковые панели",
            fg_color="#f0f0f0",
            text_color="#2c2c2c",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(20, 10))

        self._add_color_setting(scrollable_frame, "Левая панель:", "#f5f5f5", "left_panel_bg")
        self._add_color_setting(scrollable_frame, "Правая панель:", "#e0e0e0", "right_panel_bg")
        self._add_color_setting(scrollable_frame, "Панель объектов:", "#e0e0e0", "objects_panel_bg")

        ctk.CTkLabel(
            scrollable_frame,
            text="Canvas и сетка",
            fg_color="#f0f0f0",
            text_color="#2c2c2c",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(20, 10))

        self._add_color_setting(scrollable_frame, "Фон canvas:", "white", "canvas_bg")
        self._add_color_setting(scrollable_frame, "Сетка (основная):", "#e0e0e0", "grid_major")
        self._add_color_setting(scrollable_frame, "Сетка (мелкая):", "#f0f0f0", "grid_minor")

        ctk.CTkLabel(
            scrollable_frame,
            text="Акценты и кнопки",
            fg_color="#f0f0f0",
            text_color="#2c2c2c",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(20, 10))

        self._add_color_setting(scrollable_frame, "Кнопка паузы:", "#f1c40f", "pause_btn_bg")
        self._add_color_setting(scrollable_frame, "Кнопка очистки:", "#e74c3c", "clear_btn_bg")
        self._add_color_setting(scrollable_frame, "Выделение:", "#4a90e2", "accent_bg")

        btn_frame = ctk.CTkFrame(scrollable_frame, fg_color="#f0f0f0")
        btn_frame.pack(pady=30)

        ctk.CTkButton(
            btn_frame,
            text="💾 Сохранить и применить",
            fg_color="#2ecc71",
            text_color="white",
            command=lambda: self._save_and_apply(settings_win)
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="❌ Отмена",
            fg_color="#e74c3c",
            text_color="white",
            command=settings_win.destroy
        ).pack(side="left", padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def _add_color_setting(self, parent, label_text, current_color, attr_name):
        """Добавляет строку с выбором цвета"""
        frame = ctk.CTkFrame(parent, fg_color="#e0e0e0")
        frame.pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(
            frame,
            text=label_text,
            fg_color="#e0e0e0",
            text_color="black",
            font=("Segoe UI", 10),
            width=150,
            anchor="w"
        ).pack(side="left")

        color_btn = ctk.CTkButton(
            frame,
            fg_color=current_color,
            width=30,
            height=30,
            command=lambda: self._pick_color(color_btn, attr_name)
        )
        color_btn.pack(side="left", padx=10)

        hex_label = ctk.CTkLabel(
            frame,
            text=current_color,
            fg_color="#e0e0e0",
            text_color="black",
            font=("Courier", 9)
        )
        hex_label.pack(side="left")

        setattr(self, f"_{attr_name}_btn", color_btn)

    def _pick_color(self, btn, attr_name):
        """Открывает выбор цвета"""
        color = colorchooser.askcolor(title="Выберите цвет")
        if color[1]:
            btn.configure(fg_color=color[1])
            setattr(self, f"_{attr_name}_color", color[1])
            print(f"🎨 {attr_name} = {color[1]}")

    def _save_and_apply(self, window):
        """Сохраняет тему и применяет"""
        if hasattr(self, '_toolbar_bg_color'):
            self.toolbar.configure(fg_color=self._toolbar_bg_color)
            for child in self.toolbar.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    if hasattr(self, '_toolbar_btn_bg_color'):
                        child.configure(fg_color=self._toolbar_btn_bg_color)

        if hasattr(self, '_canvas_bg_color'):
            self.canvas.configure(bg=self._canvas_bg_color)

        self._save_theme_to_file()
        window.destroy()
        print("✅ Тема сохранена и применена!")

    def _save_theme_to_file(self):
        """Сохраняет тему в файл"""
        import json

        theme_data = {}

        if hasattr(self, '_toolbar_bg_color'):
            theme_data['toolbar_bg'] = self._toolbar_bg_color
        if hasattr(self, '_toolbar_btn_bg_color'):
            theme_data['toolbar_btn_bg'] = self._toolbar_btn_bg_color
        if hasattr(self, '_canvas_bg_color'):
            theme_data['canvas_bg'] = self._canvas_bg_color

        with open('theme.json', 'w', encoding='utf-8') as f:
            json.dump(theme_data, f, indent=2)

        print(" Тема сохранена в theme.json")

    def _apply_preset(self, preset_name):
        """Применяет пресет темы"""
        presets = {
            "dark": {
                "toolbar_bg": "#1a1a2e",
                "toolbar_btn_bg": "#16213e",
                "left_panel_bg": "#0f3460",
                "right_panel_bg": "#16213e",
                "objects_panel_bg": "#1a1a2e",
                "canvas_bg": "#0a0a0a",
                "grid_major": "#2a2a2a",
                "grid_minor": "#1a1a1a",
                "pause_btn_bg": "#e94560",
                "clear_btn_bg": "#ff6b6b",
                "accent_bg": "#00d9ff"
            },
            "light": {
                "toolbar_bg": "#ffffff",
                "toolbar_btn_bg": "#f0f0f0",
                "left_panel_bg": "#fafafa",
                "right_panel_bg": "#f5f5f5",
                "objects_panel_bg": "#ffffff",
                "canvas_bg": "white",
                "grid_major": "#e0e0e0",
                "grid_minor": "#f0f0f0",
                "pause_btn_bg": "#ffd93d",
                "clear_btn_bg": "#ff6b6b",
                "accent_bg": "#4a90e2"
            },
            "gaming": {
                "toolbar_bg": "#2d0a31",
                "toolbar_btn_bg": "#4a148c",
                "left_panel_bg": "#311b92",
                "right_panel_bg": "#4a148c",
                "objects_panel_bg": "#5e35b1",
                "canvas_bg": "#1a0033",
                "grid_major": "#4a148c",
                "grid_minor": "#311b92",
                "pause_btn_bg": "#00e676",
                "clear_btn_bg": "#ff1744",
                "accent_bg": "#00e5ff"
            },
            "ocean": {
                "toolbar_bg": "#003049",
                "toolbar_btn_bg": "#005f73",
                "left_panel_bg": "#0a9396",
                "right_panel_bg": "#005f73",
                "objects_panel_bg": "#94d2bd",
                "canvas_bg": "#e9d8a6",
                "grid_major": "#94d2bd",
                "grid_minor": "#e9d8a6",
                "pause_btn_bg": "#ee9b00",
                "clear_btn_bg": "#d62828",
                "accent_bg": "#00b4d8"
            }
        }

        if preset_name in presets:
            preset = presets[preset_name]
            for attr_name, color in preset.items():
                btn_attr = f"_{attr_name}_btn"
                if hasattr(self, btn_attr):
                    btn = getattr(self, btn_attr)
                    btn.configure(fg_color=color)
                    setattr(self, f"_{attr_name}_color", color)

            print(f"✅ Применён пресет: {preset_name}")