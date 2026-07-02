"""Конфигурация инструментов"""

TOOLS = {
    # ГЕОМЕТРИЯ
    "circle": {"icon": "⭕", "category": "GEOMETRY", "tooltip": "Шар"},
    "square": {"icon": "⬛", "category": "GEOMETRY", "tooltip": "Квадрат"},
    "triangle": {"icon": "🔺", "category": "GEOMETRY", "tooltip": "Треугольник"},

    # СОЕДИНЕНИЯ
    "spring": {"icon": "↔", "category": "CONNECTIONS", "tooltip": "Пружина"},

    # МОЛЕКУЛЯРКА
    "atom": {"icon": "⚫", "category": "MOLECULAR", "tooltip": "Атом"},
    "drop": {"icon": "💧", "category": "MOLECULAR", "tooltip": "Капля"},
    "gas": {"icon": "💨", "category": "MOLECULAR", "tooltip": "Газ"},

    # ЭЛЕКТРОНИКА
    "battery": {"icon": "🔋", "category": "ELECTRONICS", "tooltip": "Батарея"},
    "bulb": {"icon": "💡", "category": "ELECTRONICS", "tooltip": "Лампочка"},
    "wire": {"icon": "➖", "category": "ELECTRONICS", "tooltip": "Провод"},
}

CATEGORIES = {
    "GEOMETRY": "Геометрия",
    "CONNECTIONS": "Соединения",
    "MOLECULAR": "Молекулярка",
    "ELECTRONICS": "Электроника"
}