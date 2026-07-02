"""Панель инструментов"""
import customtkinter as ctk


class ToolPanel(ctk.CTkFrame):
    def __init__(self, parent, on_tool_select=None, on_grid_toggle=None):
        super().__init__(parent, fg_color="#e0e0e0", height=60)
        self.pack(fill="x")
        self.pack_propagate(False)

        self.on_tool_select = on_tool_select
        self.on_grid_toggle = on_grid_toggle
        self.current_tool = ctk.StringVar(value="circle")

        self.create_panel()

    def create_panel(self):
        ctk.CTkLabel(
            self, text="Объекты:",
            fg_color="#e0e0e0", text_color="black",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        self.grid_btn = ctk.CTkCheckBox(
            self, text="📐 Сетка",
            fg_color="#e0e0e0",
            command=self._on_grid
        )
        self.grid_btn.pack(side="left", padx=20)

        # Механика
        self.mech = ctk.CTkFrame(self, fg_color="#e0e0e0")
        for text, tool in [("⭕ Шар", "circle"), ("⬛ Квадрат", "square"),
                           ("🔺 Треугольник", "triangle"), ("📏 Стержень", "stick"),
                           ("↔ Пружина", "spring")]:
            ctk.CTkButton(
                self.mech, text=text,
                command=lambda t=tool: self._select(t),
                fg_color="white", text_color="black"
            ).pack(side="left", padx=5, pady=5)

        # Молекулярка
        self.mol = ctk.CTkFrame(self, fg_color="#e0e0e0")
        for text, tool in [("⚫ Атом", "atom"), ("💧 Капля", "drop"), ("💨 Газ", "gas")]:
            ctk.CTkButton(
                self.mol, text=text,
                command=lambda t=tool: self._select(t),
                fg_color="white", text_color="black"
            ).pack(side="left", padx=5, pady=5)

        # Электроника
        self.elec = ctk.CTkFrame(self, fg_color="#e0e0e0")
        for text, tool in [("🔋 Батарея", "battery"), ("💡 Лампочка", "bulb"), ("➖ Провод", "wire")]:
            ctk.CTkButton(
                self.elec, text=text,
                command=lambda t=tool: self._select(t),
                fg_color="white", text_color="black"
            ).pack(side="left", padx=5, pady=5)

        self.show_section("mechanics")

    def show_section(self, name):
        self.mech.pack_forget()
        self.mol.pack_forget()
        self.elec.pack_forget()

        if name == "mechanics":
            self.mech.pack(side="left", fill="x", expand=True)
        elif name == "molecular":
            self.mol.pack(side="left", fill="x", expand=True)
        elif name == "electronics":
            self.elec.pack(side="left", fill="x", expand=True)

    def _select(self, tool):
        self.current_tool.set(tool)
        if self.on_tool_select:
            self.on_tool_select(tool)

    def _on_grid(self):
        if self.on_grid_toggle:
            self.on_grid_toggle(self.grid_btn.get())