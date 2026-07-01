import json
import os


class Theme:
    """Управляет темой оформления"""

    def __init__(self):
        # === ГЛАВНЫЕ ЭЛЕМЕНТЫ (toolbar, заголовки) ===
        self.primary_bg = "#2c2c2c"  # Фон верхней панели
        self.primary_fg = "white"  # Текст на верхней панели
        self.primary_btn_bg = "#3c3c3c"  # Фон кнопок разделов
        self.primary_btn_hover = "#4c4c4c"  # Hover эффект

        # === ПОДГЛАВНЫЕ ЭЛЕМЕНТЫ (панели объектов, свойства) ===
        self.secondary_bg = "#e0e0e0"  # Фон панелей
        self.secondary_fg = "black"  # Текст на панелях
        self.secondary_btn_bg = "white"  # Фон кнопок объектов
        self.secondary_btn_hover = "#f0f0f0"  # Hover эффект

        # === АКЦЕНТЫ (выделение, важные кнопки) ===
        self.accent_bg = "#4a90e2"  # Цвет выделения
        self.accent_fg = "white"  # Текст на акцентах
        self.danger_bg = "#e74c3c"  # Кнопка удаления
        self.danger_fg = "white"
        self.success_bg = "#2ecc71"  # Кнопка старта
        self.success_fg = "white"
        self.warning_bg = "#f1c40f"  # Кнопка паузы
        self.warning_fg = "black"

        # === CANVAS ===
        self.canvas_bg = "white"  # Фон canvas
        self.canvas_border = "#cccccc"  # Рамка canvas
        self.grid_major = "#e0e0e0"  # Основная сетка
        self.grid_minor = "#f0f0f0"  # Подсетка

        # === ПАНЕЛИ ===
        self.left_panel_bg = "#f5f5f5"  # Фон левой панели
        self.right_panel_bg = "#e0e0e0"  # Фон правой панели
        self.properties_bg = "#d0d0d0"  # Фон свойств объекта

        # === ШРИФТЫ ===
        self.font_family = "Segoe UI"  # Семейство шрифтов
        self.font_size_small = 9  # Маленький текст
        self.font_size_normal = 11  # Обычный текст
        self.font_size_large = 14  # Заголовки
        self.font_size_xlarge = 18  # Большие заголовки

        # === ОТСТУПЫ ===
        self.padding_small = 5
        self.padding_normal = 10
        self.padding_large = 15

        # === РАМКИ ===
        self.border_width = 1  # Толщина рамок
        self.border_radius = 3  # Скругление (если поддерживается)

    def get_font(self, size="normal", bold=False):
        """Возвращает кортеж шрифта"""
        size_map = {
            "small": self.font_size_small,
            "normal": self.font_size_normal,
            "large": self.font_size_large,
            "xlarge": self.font_size_xlarge
        }
        font_size = size_map.get(size, self.font_size_normal)

        if bold:
            return (self.font_family, font_size, "bold")
        return (self.font_family, font_size)

    def save(self, filename="theme.json"):
        """Сохраняет тему в файл"""
        theme_data = {
            "primary_bg": self.primary_bg,
            "primary_fg": self.primary_fg,
            "primary_btn_bg": self.primary_btn_bg,
            "primary_btn_hover": self.primary_btn_hover,
            "secondary_bg": self.secondary_bg,
            "secondary_fg": self.secondary_fg,
            "secondary_btn_bg": self.secondary_btn_bg,
            "secondary_btn_hover": self.secondary_btn_hover,
            "accent_bg": self.accent_bg,
            "accent_fg": self.accent_fg,
            "danger_bg": self.danger_bg,
            "danger_fg": self.danger_fg,
            "success_bg": self.success_bg,
            "success_fg": self.success_fg,
            "warning_bg": self.warning_bg,
            "warning_fg": self.warning_fg,
            "canvas_bg": self.canvas_bg,
            "canvas_border": self.canvas_border,
            "grid_major": self.grid_major,
            "grid_minor": self.grid_minor,
            "left_panel_bg": self.left_panel_bg,
            "right_panel_bg": self.right_panel_bg,
            "properties_bg": self.properties_bg,
            "font_family": self.font_family,
            "font_size_small": self.font_size_small,
            "font_size_normal": self.font_size_normal,
            "font_size_large": self.font_size_large,
            "font_size_xlarge": self.font_size_xlarge,
            "padding_small": self.padding_small,
            "padding_normal": self.padding_normal,
            "padding_large": self.padding_large,
            "border_width": self.border_width
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(theme_data, f, indent=2)

        print(f"💾 Тема сохранена в {filename}")

    def load(self, filename="theme.json"):
        """Загружает тему из файла"""
        if not os.path.exists(filename):
            print(f"⚠️ Файл темы {filename} не найден, используем тему по умолчанию")
            return

        with open(filename, 'r', encoding='utf-8') as f:
            theme_data = json.load(f)

        for key, value in theme_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        print(f"✅ Тема загружена из {filename}")


# Глобальный экземпляр темы
theme = Theme()