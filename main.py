# main.py
import tkinter as tk
import pymunk

from Phisics.objects import create_object
from Phisics.physics_engine import PhysicsEngine
from Ui.ui import UserInterface
from menu import ContextMenu


class PhysicsSandbox:
    def __init__(self):
        self.root = tk.Tk()

        # Создаём компоненты
        self.ui = UserInterface(self.root)
        self.physics = PhysicsEngine()

        self.ui.on_clear_callback = self.clear_all
        self.ui.on_object_property_callback = self.apply_object_properties

        # Привязываем обработчик клика по иерархии
        self.ui.on_hierarchy_callback = self.on_hierarchy_click

        self.objects = []
        self.selected_object = None
        self.total_created = 0

        self.last_mouse_x = 0
        self.last_mouse_y = 0

        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_threshold = 5  # Пикселей чтобы отличить клик от перетаскивания

        # Создаём контекстное меню
        self.context_menu = ContextMenu(
            self.root,
            delete_func=self.delete_selected,
            params_func=self.show_params,
            duplicate_func=self.duplicate_selected
        )

        # Привязываем события
        self.ui.canvas.bind("<Button-1>", self.on_left_click)
        self.ui.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.ui.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.ui.canvas.bind("<Button-3>", self.on_right_click)

        # Горячие клавиши (привязываем к root)
        self.root.bind("<Delete>", lambda e: self.delete_selected())
        self.root.bind_all("<Control-d>", lambda e: self.duplicate_selected())
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Control-z>", lambda e: self.undo())  # Пока заглушка
        self.root.bind("<g>", lambda e: self.toggle_grid())
        self.root.bind("<Escape>",lambda e: self.deselect_object())

        # Обновление гравитации
        self.ui.gravity_var.trace("w", self.on_gravity_change)
        self.ui.on_gravity_callback = self.on_world_gravity_change

        # Создаём границы
        self.root.after(200, self.create_boundaries)

        # ⭐ ОБРАБОТКА ИЗМЕНЕНИЯ РАЗМЕРА
        self.ui.canvas.bind("<Configure>", lambda e: self.on_canvas_resize(e))

        # Запускаем
        self.draw()
        self.root.mainloop()



    def on_canvas_resize(self, event):
        """Обработка изменения размера canvas"""
        if event.width > 0 and event.height > 0:
            print(f"🔄 Canvas resized: {event.width}x{event.height}")
            self.create_boundaries()

    def apply_object_properties(self):
        """Применяет изменённые свойства к объекту"""
        if self.selected_object:
            obj = self.selected_object

            new_size = self.ui.obj_size_var.get()
            new_mass = self.ui.obj_mass_var.get()
            new_elasticity = self.ui.obj_elasticity_var.get()
            new_color = self.ui.obj_color_var.get()

            # Сохраняем текущие параметры
            current_pos = obj.body.position
            current_vel = obj.body.velocity

            # Удаляем старую форму из мира
            self.physics.space.remove(obj.shape)

            # Создаём новую форму с правильным размером
            if obj.obj_type == "circle":
                obj.shape = pymunk.Circle(obj.body, new_size)
                obj.body.moment = pymunk.moment_for_circle(new_mass, 0, new_size)
            elif obj.obj_type == "square":
                obj.shape = pymunk.Poly.create_box(obj.body, (new_size, new_size))
                obj.body.moment = pymunk.moment_for_box(new_mass, (new_size, new_size))
            elif obj.obj_type == "triangle":
                points = [(0, -new_size), (-new_size, new_size), (new_size, new_size)]
                obj.shape = pymunk.Poly(obj.body, points)
                obj.body.moment = pymunk.moment_for_poly(new_mass, points)

            obj.shape.elasticity = new_elasticity
            obj.size = new_size
            obj.body.mass = new_mass
            obj.color = new_color

            # Добавляем новую форму в мир
            self.physics.space.add(obj.shape)

            # Восстанавливаем позицию и скорость
            obj.body.position = current_pos
            obj.body.velocity = current_vel

            print(f"✅ Свойства обновлены: размер={new_size}, масса={new_mass}")

    def deselect_object(self):
        """Снимает выделение с объекта"""
        if self.selected_object:
            print(f"Снято выделение: {self.selected_object.obj_type}")
            self.selected_object = None

    def create_boundaries(self):
        """Создаёт границы мира"""
        self.ui.canvas.update_idletasks()

        # Получаем РЕАЛЬНЫЙ размер canvas
        canvas_width = self.ui.canvas.winfo_width()
        canvas_height = self.ui.canvas.winfo_height()

        print(f"📐 Размер canvas: {canvas_width}x{canvas_height}")

        # Удаляем старые границы
        for b in self.physics.boundaries:
            self.physics.space.remove(b)
        self.physics.boundaries = []

        # Создаём новые границы по РЕАЛЬНОМУ размеру
        self.physics.create_boundaries(canvas_width, canvas_height)

    def add_to_hierarchy(self, obj):
        """Добавляет объект в список иерархии"""
        # Формируем текст для списка
        icon = {"circle": "⭕", "square": "⬛", "triangle": "🔺"}.get(obj.obj_type, "❓")
        text = f"{icon} {obj.obj_type} #{len(self.objects)} ({obj.color})\n"

        # Используем новый метод
        self.ui.add_object_to_list(text)

        print(f"Добавлен в иерархию: {text.strip()}")

    def on_left_click(self, event):
        """Левый клик — выделение или создание объекта"""
        # Сохраняем начальную позицию
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.is_dragging = False

        # Проверяем клик по объекту
        clicked_object = None
        for obj in reversed(self.objects):
            if obj.is_clicked(event.x, event.y):
                clicked_object = obj
                break

        if clicked_object:
            # Выделяем объект
            self.selected_object = clicked_object
            self.ui.update_object_properties(clicked_object)
            print(f"Выделен: {clicked_object.obj_type}")
        else:
            # Клик по пустому месту — создаём объект
            # ⭐ НЕ сбрасываем выделение!

            obj_type = self.ui.current_object.get()
            if obj_type == "..." or obj_type == "":
                print("Сначала выбери тип объекта!")
                return

            elasticity = self.ui.elasticity_var.get()
            obj = create_object(obj_type, event.x, event.y, self.physics.space, elasticity)
            if obj:
                self.objects.append(obj)
                self.total_created += 1
                self.add_to_hierarchy(obj)
                # ⭐ НОВОЕ: Автоматически выделяем новый объект
                self.selected_object = obj

                self.selected_object = obj
                self.ui.update_object_properties(obj)

    def on_mouse_drag(self, event):
        """Перетаскивание объекта"""
        if self.selected_object is None:
            return

        # Проверяем что мышь сдвинулась достаточно (не случайное движение)
        dx = abs(event.x - self.drag_start_x)
        dy = abs(event.y - self.drag_start_y)

        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True

            # Перемещаем объект
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y

            self.selected_object.body.position = (event.x, event.y)
            self.selected_object.body.velocity = (0, 0)  # Сбрасываем скорость
            self.selected_object.body.angular_velocity = 0  # Сбрасываем вращение

    def on_mouse_release(self, event):
        """Отпускание мыши"""
        if self.is_dragging:
            print(f"Объект перемещён на ({event.x}, {event.y})")

        self.is_dragging = False

    def on_right_click(self, event):
        """Правый клик — показать меню или снять выделение"""
        # Ищем объект под курсором
        clicked_object = None
        for obj in reversed(self.objects):
            if obj.is_clicked(event.x, event.y):
                clicked_object = obj
                break

        if clicked_object:
            # Выделяем и показываем меню
            self.selected_object = clicked_object
            self.ui.update_object_properties(clicked_object)
            self.context_menu.show(event.x_root, event.y_root)
        else:
            # Клик по пустому месту — снимаем выделение
            self.deselect_object()

    def delete_selected(self):
        """Удаляет выбранный объект"""
        if self.selected_object:
            # Находим индекс объекта в списке
            obj_index = self.objects.index(self.selected_object)

            # Удаляем из физического мира
            self.physics.remove_object(
                self.selected_object.body,
                self.selected_object.shape
            )

            # Удаляем из списка объектов
            self.objects.remove(self.selected_object)

            # ⭐ НОВОЕ: Удаляем из иерархии
            self.ui.remove_object_from_list(obj_index)

            # Снимаем выделение
            self.selected_object = None

            print(f"✅ Объект удалён! Осталось: {len(self.objects)}")

    def show_params(self):
        """Показывает параметры"""
        if self.selected_object:
            obj = self.selected_object
            print(f"\n{'=' * 30}")
            print(f"Параметры объекта:")
            print(f"{'=' * 30}")
            print(f"Тип: {obj.obj_type}")
            print(f"Цвет: {obj.color}")
            print(f"Размер: {obj.size}")
            print(f"Позиция: ({obj.body.position.x:.1f}, {obj.body.position.y:.1f})")
            print(f"Скорость: ({obj.body.velocity.x:.2f}, {obj.body.velocity.y:.2f})")
            print(f"Масса: {obj.body.mass}")
            print(f"Упругость: {obj.shape.elasticity}")
            print(f"{'=' * 30}\n")

    def duplicate_selected(self):
        """Дублирует объект с сохранением всех свойств"""
        if self.selected_object:
            obj = self.selected_object

            # Создаём новый объект того же типа
            if obj.obj_type == "circle":
                from Phisics.objects import Ball
                new_obj = Ball.__new__(Ball)  # Создаём без вызова __init__
                new_obj.body = pymunk.Body(obj.body.mass, obj.body.moment)
                new_obj.shape = pymunk.Circle(new_obj.body, obj.size)
            elif obj.obj_type == "square":
                from Phisics.objects import Box
                new_obj = Box.__new__(Box)
                new_obj.body = pymunk.Body(obj.body.mass, obj.body.moment)
                new_obj.shape = pymunk.Poly.create_box(new_obj.body, (obj.size, obj.size))
            elif obj.obj_type == "triangle":
                from Phisics.objects import Triangle
                new_obj = Triangle.__new__(Triangle)
                new_obj.body = pymunk.Body(obj.body.mass, obj.body.moment)
                points = [(0, -obj.size), (-obj.size, obj.size), (obj.size, obj.size)]
                new_obj.shape = pymunk.Poly(new_obj.body, points)
            else:
                return

            # Копируем все свойства
            new_obj.body.position = (obj.body.position.x + 30, obj.body.position.y)
            new_obj.body.velocity = obj.body.velocity
            new_obj.shape.elasticity = obj.shape.elasticity
            new_obj.size = obj.size
            new_obj.color = obj.color
            new_obj.obj_type = obj.obj_type

            # Добавляем в мир
            self.physics.space.add(new_obj.body, new_obj.shape)
            self.objects.append(new_obj)
            self.total_created += 1

            # Добавляем в иерархию
            self.add_to_hierarchy(new_obj)

            print(f"📋 Объект продублирован! Всего: {len(self.objects)}")

    def clear_all(self):
        """Очищает всё"""
        for obj in self.objects:
            self.physics.remove_object(obj.body, obj.shape)
        self.objects = []
        self.total_created = 0
        self.ui.objects_list.config(state="normal")
        self.ui.objects_list.delete(1.0, tk.END)
        self.ui.objects_list.config(state="disabled")
        self.ui.update_stats(0, 0)
        print("Всё очищено!")

    def on_gravity_change(self, *args):
        """Изменение гравитации"""
        self.physics.set_gravity(self.ui.gravity_var.get())

    def draw(self):
        """Отрисовка"""
        self.ui.canvas.delete("all")

        # Получаем размеры
        canvas_width = self.ui.canvas.winfo_width()
        canvas_height = self.ui.canvas.winfo_height()

        # Рисуем сетку если включена
        if self.ui.show_grid.get():
            self.draw_grid(canvas_width, canvas_height)

        # Рисуем границы (сдвинуты к краям)
        self.ui.canvas.create_line(0, canvas_height - 2, canvas_width, canvas_height - 2,
                                   fill="black", width=4)  # Пол (было -10, стало -2)
        self.ui.canvas.create_line(2, 0, 2, canvas_height - 2,
                                   fill="black", width=4)  # Левая стена (было 5, стало 2)
        self.ui.canvas.create_line(canvas_width - 2, 0, canvas_width - 2, canvas_height - 2,
                                   fill="black", width=4)  # Правая стена (было -5, стало -2)
        self.ui.canvas.create_line(2, 2, canvas_width - 2, 2,
                                   fill="black", width=4)  # Потолок (было 5, стало 2)

        # Рисуем объекты
        visible_count = 0
        for obj in self.objects:
            x, y = obj.body.position

            if 0 <= x <= canvas_width and 0 <= y <= canvas_height:
                visible_count += 1

            if obj == self.selected_object:
                outline_color = "black"  # Чёрный цвет
                outline_width = 2  # Тонкая линия (2 пикселя)
                outline_dash = (5, 5)  # Пунктир (5 пикселей линия, 5 пикселей пробел)
            else:
                outline_color = "black"  # Чёрный цвет
                outline_width = 1  # Очень тонкая линия (1 пиксель)
                outline_dash = ""  # Пустая строка = сплошная линия

            if obj.obj_type == "circle":
                self.ui.canvas.create_oval(
                    x - obj.size, y - obj.size, x + obj.size, y + obj.size,
                    fill=obj.color, outline=outline_color, width=outline_width,
                    dash = outline_dash
                )
            elif obj.obj_type == "square":
                angle = obj.body.angle
                points = self.get_rotated_rect_points(x, y, obj.size, angle)
                self.ui.canvas.create_polygon(points, fill=obj.color,
                                              outline=outline_color, width=outline_width,dash=outline_dash)
            elif obj.obj_type == "triangle":
                angle = obj.body.angle
                points = self.get_rotated_triangle_points(x, y, obj.size, angle)
                self.ui.canvas.create_polygon(points, fill=obj.color,
                                              outline=outline_color, width=outline_width,dash=outline_dash)
            # Рисуем линию при перетаскивании
        if self.is_dragging and self.selected_object:
            x, y = self.selected_object.body.position
            self.ui.canvas.create_line(x, y, self.drag_start_x, self.drag_start_y,
                                           fill="red", width=2, dash=(5, 5))

        # Обновляем статистику
        self.ui.update_stats(self.total_created, visible_count)

        # Обновляем физику
        if not self.ui.paused.get():
            self.physics.step()

        self.root.after(16, self.draw)

    def get_rotated_rect_points(self, x, y, size, angle):
        import math
        points = []
        for dx, dy in [(-size / 2, -size / 2), (size / 2, -size / 2), (size / 2, size / 2), (-size / 2, size / 2)]:
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            points.append((x + rx, y + ry))
        return points

    def get_rotated_triangle_points(self, x, y, size, angle):
        import math
        points = [(0, -size), (-size, size), (size, size)]
        result = []
        for dx, dy in points:
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            result.append((x + rx, y + ry))
        return result

    def on_hierarchy_click(self, line_number, event):
        """Обработка правого клика по строке иерархии"""
        # Проверяем что строка валидна (line_number начинается с 1)
        # Индекс объекта = line_number - 1

        obj_index = line_number - 1

        # Проверяем границы
        if obj_index < 0 or obj_index >= len(self.objects):
            print("Клик по пустой строке")
            return

        # Выделяем объект
        self.selected_object = self.objects[obj_index]

        self.ui.update_object_properties(self.selected_object)

        # Показываем контекстное меню
        self.context_menu.show(event.x_root, event.y_root)

        print(f"Выбран объект: {self.selected_object.obj_type} #{line_number}")

    def draw_grid(self, width, height):
        """Рисует сетку на canvas"""
        major_grid = 50  # Основная сетка
        minor_grid = 10  # Подсетка

        # Подсетка (тонкие линии)
        for x in range(0, width, minor_grid):
            if x % major_grid != 0:  # Пропускаем основные линии
                self.ui.canvas.create_line(x, 0, x, height, fill="#f0f0f0", width=1)

        for y in range(0, height, minor_grid):
            if y % major_grid != 0:
                self.ui.canvas.create_line(0, y, width, y, fill="#f0f0f0", width=1)

        # Основная сетка (более видимые линии)
        for x in range(0, width, major_grid):
            self.ui.canvas.create_line(x, 0, x, height, fill="#e0e0e0", width=1)

        for y in range(0, height, major_grid):
            self.ui.canvas.create_line(0, y, width, y, fill="#e0e0e0", width=1)

    def on_world_gravity_change(self, gx, gy):
        """Изменение гравитации мира"""
        self.physics.set_gravity(gx, gy)
        print(f"🌍 Гравитация: X={gx}, Y={gy}")

    def toggle_pause(self):
        self.ui.toggle_pause()

    def toggle_grid(self):
        self.ui.show_grid.set(not self.ui.show_grid.get())

    def undo(self):
        print("↶ Отмена (в разработке)")

if __name__ == "__main__":
    app = PhysicsSandbox()