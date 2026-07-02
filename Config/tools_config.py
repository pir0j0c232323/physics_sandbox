"""Конфигурация инструментов для каждого раздела"""

# Инструменты для раздела МЕХАНИКА
MECHANICS_TOOLS = {
    # ОБЪЕКТЫ (Draw)
    "circle": {"icon": "⭕", "category": "objects", "tooltip": "Круг"},
    "square": {"icon": "⬛", "category": "objects", "tooltip": "Квадрат"},
    "triangle": {"icon": "🔺", "category": "objects", "tooltip": "Треугольник"},
    "line": {"icon": "━", "category": "objects", "tooltip": "Линия/Стержень"},
    "polygon": {"icon": "⬡", "category": "objects", "tooltip": "Многоугольник"},

    # СОЕДИНЕНИЯ (Connections)
    "spring": {"icon": "↔", "category": "connections", "tooltip": "Пружина"},
    "hinge": {"icon": "🔗", "category": "connections", "tooltip": "Шарнир"},
    "weld": {"icon": "⛓", "category": "connections", "tooltip": "Фиксированное"},
    "slider": {"icon": "⬌", "category": "connections", "tooltip": "Скользящее"},
    "rope": {"icon": "🔩", "category": "connections", "tooltip": "Верёвка"},

    # СИЛЫ (Forces)
    "vector_force": {"icon": "➡", "category": "forces", "tooltip": "Вектор силы"},
    "field": {"icon": "", "category": "forces", "tooltip": "Поле"},
}

# Инструменты для раздела МОЛЕКУЛЯРКА
MOLECULAR_TOOLS = {
    "atom": {"icon": "⚫", "category": "particles", "tooltip": "Атом"},
    "molecule": {"icon": "⚛", "category": "particles", "tooltip": "Молекула"},
    "bond": {"icon": "🔗", "category": "connections", "tooltip": "Связь"},
    "drop": {"icon": "💧", "category": "liquids", "tooltip": "Капля"},
    "gas": {"icon": "💨", "category": "gases", "tooltip": "Газ"},
    "particle": {"icon": "•", "category": "particles", "tooltip": "Частица"},
    "temperature": {"icon": "🌡", "category": "parameters", "tooltip": "Температура"},
    "pressure": {"icon": "📊", "category": "parameters", "tooltip": "Давление"},
}

# Инструменты для раздела ЭЛЕКТРОНИКА
ELECTRONICS_TOOLS = {
    "battery": {"icon": "🔋", "category": "sources", "tooltip": "Батарея"},
    "wire": {"icon": "➖", "category": "components", "tooltip": "Провод"},
    "resistor": {"icon": "", "category": "components", "tooltip": "Резистор"},
    "capacitor": {"icon": "⚙", "category": "components", "tooltip": "Конденсатор"},
    "bulb": {"icon": "💡", "category": "outputs", "tooltip": "Лампочка"},
    "switch": {"icon": "🔘", "category": "controls", "tooltip": "Переключатель"},
    "voltage": {"icon": "📈", "category": "parameters", "tooltip": "Напряжение"},
    "current": {"icon": "🔌", "category": "parameters", "tooltip": "Ток"},
}

# Canvas Tools (инструменты работы с видом)
CANVAS_TOOLS = {
    "select": {"icon": "➤", "tooltip": "Выделение"},
    "pan": {"icon": "", "tooltip": "Панорама"},
    "zoom": {"icon": "", "tooltip": "Масштаб"},
    "rotate": {"icon": "", "tooltip": "Вращение"},
    "transform": {"icon": "", "tooltip": "Трансформация"},
    "grid": {"icon": "▦", "tooltip": "Сетка"},
    "snap": {"icon": "", "tooltip": "Привязка"},
}

# Порядок отображения категорий
CATEGORY_ORDER = [
    "objects",
    "connections",
    "forces",
    "surfaces",
    "particles",
    "liquids",
    "gases",
    "parameters",
    "sources",
    "components",
    "outputs",
    "controls",
]

CATEGORY_NAMES = {
    "geometry": "Геометрия",
    "connections": "Соединения",
    "ramps": "Рампы",
    "forces": "Силы",
    "surfaces": "Поверхности",
    "particles": "Частицы",
    "liquids": "Жидкости",
    "gases": "Газы",
    "parameters": "Параметры",
    "sources": "Источники",
    "components": "Компоненты",
    "outputs": "Выходы",
    "controls": "Управление",
}