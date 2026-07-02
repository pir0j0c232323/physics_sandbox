"""Правая панель - свойства объекта"""
import customtkinter as ctk
import tkinter as tk
import pymunk


class RightPanel(ctk.CTkFrame):
    def __init__(self, parent, on_property_change=None, on_gravity_change=None,
                 on_pause=None, on_clear=None):
        super().__init__(parent, fg_color="#e0e0e0", width=300)
        self.pack(side="right", fill="y")
        self.pack_propagate(False)

        self.on_property_change = on_property_change
        self.on_gravity_change = on_gravity_change
        self.on_pause = on_pause
        self.on_clear = on_clear

        # Переменные
        self.obj_size_var = ctk.IntVar(value=20)
        self.obj_mass_var = ctk.DoubleVar(value=1.0)
        self.obj_elasticity_var = ctk.DoubleVar(value=0.8)
        self.obj_friction_var = ctk.DoubleVar(value=0.5)  # Новое: трение
        self.obj_stiffness_var = ctk.DoubleVar(value=10.0)  # Новое: жёсткость
        self.obj_color_var = ctk.StringVar(value="red")
        self.paused = ctk.BooleanVar(value=False)

        self.current_obj_type = None  # Храним тип текущего объекта

        self.create_panel()

    def create_panel(self):
        """Создаёт правую панель"""
        # Заголовок
        ctk.CTkLabel(
            self, text="⚙️ СВОЙСТВА",
            fg_color="#e0e0e0", text_color="black",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        ctk.CTkFrame(self, fg_color="gray", height=2).pack(fill="x", padx=10)

        # === ФРЕЙМ ДЛЯ ДИНАМИЧЕСКИХ ОБЪЕКТОВ ===
        self.dynamic_frame = ctk.CTkFrame(self, fg_color="#d0d0d0")
        ctk.CTkLabel(
            self.dynamic_frame, text="🎯 Свойства объекта:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        # Размер
        ctk.CTkLabel(
            self.dynamic_frame, text="Размер:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15)
        tk.Scale(
            self.dynamic_frame, from_=5, to=100,
            orient="horizontal", variable=self.obj_size_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Масса
        ctk.CTkLabel(
            self.dynamic_frame, text="Масса:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        tk.Scale(
            self.dynamic_frame, from_=0.1, to=10, resolution=0.1,
            orient="horizontal", variable=self.obj_mass_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Упругость
        ctk.CTkLabel(
            self.dynamic_frame, text="Упругость:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        tk.Scale(
            self.dynamic_frame, from_=0, to=1, resolution=0.1,
            orient="horizontal", variable=self.obj_elasticity_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Цвет
        ctk.CTkLabel(
            self.dynamic_frame, text="Цвет:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        color_frame = ctk.CTkFrame(self.dynamic_frame, fg_color="#d0d0d0")
        color_frame.pack(padx=15, pady=5)
        for color in ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]:
            btn = ctk.CTkButton(
                color_frame, fg_color=color,
                width=30, height=30,
                command=lambda c=color: self._set_color(c)
            )
            btn.pack(side="left", padx=2)
        self.dynamic_frame.pack_forget()

        # === ФРЕЙМ ДЛЯ СТАТИЧЕСКИХ ОБЪЕКТОВ ===
        self.static_frame = ctk.CTkFrame(self, fg_color="#d0d0d0")
        ctk.CTkLabel(
            self.static_frame, text=" Свойства объекта:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        # Размер
        ctk.CTkLabel(
            self.static_frame, text="Размер:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15)
        tk.Scale(
            self.static_frame, from_=5, to=200,
            orient="horizontal", variable=self.obj_size_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Трение (вместо массы и упругости)
        ctk.CTkLabel(
            self.static_frame, text="Трение:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        tk.Scale(
            self.static_frame, from_=0, to=1, resolution=0.1,
            orient="horizontal", variable=self.obj_friction_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Цвет
        ctk.CTkLabel(
            self.static_frame, text="Цвет:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        color_frame2 = ctk.CTkFrame(self.static_frame, fg_color="#d0d0d0")
        color_frame2.pack(padx=15, pady=5)
        for color in ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]:
            btn = ctk.CTkButton(
                color_frame2, fg_color=color,
                width=30, height=30,
                command=lambda c=color: self._set_color(c)
            )
            btn.pack(side="left", padx=2)
        self.static_frame.pack_forget()

        # === ФРЕЙМ ДЛЯ ПРУЖИНЫ ===
        self.spring_frame = ctk.CTkFrame(self, fg_color="#d0d0d0")
        ctk.CTkLabel(
            self.spring_frame, text="🎯 Свойства пружины:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(pady=5)

        # Длина
        ctk.CTkLabel(
            self.spring_frame, text="Длина:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15)
        tk.Scale(
            self.spring_frame, from_=10, to=200,
            orient="horizontal", variable=self.obj_size_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Жёсткость (вместо трения)
        ctk.CTkLabel(
            self.spring_frame, text="Жёсткость:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        tk.Scale(
            self.spring_frame, from_=1, to=100, resolution=1,
            orient="horizontal", variable=self.obj_stiffness_var,
            bg="#d0d0d0", command=lambda v: self._on_prop_change()
        ).pack(fill="x", padx=15)

        # Цвет
        ctk.CTkLabel(
            self.spring_frame, text="Цвет:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15, pady=(5, 0))
        color_frame3 = ctk.CTkFrame(self.spring_frame, fg_color="#d0d0d0")
        color_frame3.pack(padx=15, pady=5)
        for color in ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]:
            btn = ctk.CTkButton(
                color_frame3, fg_color=color,
                width=30, height=30,
                command=lambda c=color: self._set_color(c)
            )
            btn.pack(side="left", padx=2)
        self.spring_frame.pack_forget()

        # Параметры мира
        world_frame = ctk.CTkFrame(self, fg_color="#d0d0d0")
        world_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(
            world_frame, text="🌍 Параметры мира:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(pady=(5, 10))

        # Гравитация Y
        ctk.CTkLabel(
            world_frame, text="Гравитация Y:",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)
        self.gravity_y = tk.Scale(
            world_frame, from_=-2000, to=2000,
            orient="horizontal", bg="#d0d0d0",
            command=lambda v: self._on_gravity()
        )
        self.gravity_y.set(500)
        self.gravity_y.pack(fill="x", padx=10)

        # Гравитация X
        ctk.CTkLabel(
            world_frame, text="Ветер (гравитация X):",
            fg_color="#d0d0d0", text_color="black",
            font=("Arial", 10)
        ).pack(anchor="w", padx=10, pady=(5, 0))
        self.gravity_x = tk.Scale(
            world_frame, from_=-1000, to=1000,
            orient="horizontal", bg="#d0d0d0",
            command=lambda v: self._on_gravity()
        )
        self.gravity_x.set(0)
        self.gravity_x.pack(fill="x", padx=10)

        # Управление
        ctk.CTkLabel(
            self, text="Управление:",
            fg_color="#e0e0e0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(pady=(15, 5))
        self.btn_pause = ctk.CTkButton(
            self, text="⏸️ Пауза",
            command=self._toggle_pause,
            fg_color="yellow", text_color="black"
        )
        self.btn_pause.pack(pady=5)
        ctk.CTkButton(
            self, text="🗑️ Очистить всё",
            command=self._do_clear,
            fg_color="red", text_color="white"
        ).pack(pady=5)

        # Статистика
        ctk.CTkLabel(
            self, text="📊 Статистика:",
            fg_color="#e0e0e0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(pady=(15, 5))
        self.stats = ctk.CTkLabel(
            self, text="Создано: 0\n На экране:",
            fg_color="#e0e0e0", text_color="black",
            font=("Arial", 10), justify="left"
        )
        self.stats.pack(anchor="w", padx=20)

    def _on_prop_change(self):
        if self.on_property_change:
            self.on_property_change()

    def _set_color(self, color):
        self.obj_color_var.set(color)
        if self.on_property_change:
            self.on_property_change()

    def _on_gravity(self):
        if self.on_gravity_change:
            gx = self.gravity_x.get()
            gy = self.gravity_y.get()
            self.on_gravity_change(gx, gy)

    def _toggle_pause(self):
        self.paused.set(not self.paused.get())
        if self.paused.get():
            self.btn_pause.configure(text="▶️ Старт", fg_color="lightgreen")
        else:
            self.btn_pause.configure(text="️ Пауза", fg_color="yellow")
        if self.on_pause:
            self.on_pause()

    def _do_clear(self):
        if self.on_clear:
            self.on_clear()

    def update_properties(self, obj):
        """Обновляет UI при выборе объекта"""
        # Скрываем все фреймы свойств
        self.dynamic_frame.pack_forget()
        self.static_frame.pack_forget()
        self.spring_frame.pack_forget()

        if obj:
            # Проверяем тип объекта
            if obj.obj_type == "spring":
                # Пружина - показываем фрейм с жёсткостью
                self.obj_size_var.set(int(obj.size))
                self.obj_stiffness_var.set(obj.stiffness if hasattr(obj, 'stiffness') else 10.0)
                self.obj_color_var.set(obj.color)
                self.spring_frame.pack(fill="x", padx=10, pady=10)
            else:
                # Обычные объекты - проверяем статичность
                is_static = obj.body.body_type == pymunk.Body.STATIC

                if is_static:
                    # Статический объект - показываем фрейм с трением
                    self.obj_size_var.set(int(obj.size))
                    self.obj_friction_var.set(obj.shape.friction)
                    self.obj_color_var.set(obj.color)
                    self.static_frame.pack(fill="x", padx=10, pady=10)
                else:
                    # Динамический объект - показываем фрейм с массой и упругостью
                    self.obj_size_var.set(int(obj.size))
                    self.obj_mass_var.set(obj.body.mass)
                    self.obj_elasticity_var.set(obj.shape.elasticity)
                    self.obj_color_var.set(obj.color)
                    self.dynamic_frame.pack(fill="x", padx=10, pady=10)
        else:
            self.obj_frame.pack_forget()

    def update_stats(self, created, visible):
        """Обновляет статистику"""
        self.stats.configure(text=f"Создано: {created}\nНа экране: {visible}")