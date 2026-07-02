"""Физическая песочница v2.5 - ТОЧКА ВХОДА"""
import customtkinter as ctk
import tkinter as tk
import pymunk
from Phisics.objects import create_object,Spring
from Phisics.physics_engine import PhysicsEngine
from Ui.ui import UserInterface
from menu import ContextMenu


class PhysicsSandbox:
    def __init__(self):
        self.root = tk.Tk()
        self.ui = UserInterface(self.root)
        self.physics = PhysicsEngine()

        # Callbacks
        self.ui.on_clear_callback = self.clear_all
        self.ui.on_object_property_callback = self.apply_object_properties
        self.ui.on_gravity_callback = self.on_world_gravity_change
        self.ui.on_hierarchy_callback = self.on_hierarchy_click

        # Состояние
        self.objects = []
        self.selected_object = None
        self.total_created = 0
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_threshold = 5
        self.spring_first_obj = None  # Первый объект для пружины
        self.spring_mode = False  # Режим создания пружины

        # Контекстное меню
        self.context_menu = ContextMenu(
            self.root,
            delete_func=self.delete_selected,
            params_func=self.show_params,
            duplicate_func=self.duplicate_selected
        )

        # События canvas
        self.ui.canvas.bind("<Button-1>", self.on_left_click)
        self.ui.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.ui.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.ui.canvas.bind("<Button-3>", self.on_right_click)
        self.ui.canvas.bind("<Configure>", lambda e: self.on_canvas_resize(e))

        # Горячие клавиши
        self.root.bind("<Delete>", lambda e: self.delete_selected())
        self.root.bind_all("<Control-d>", lambda e: self.duplicate_selected())
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<g>", lambda e: self.toggle_grid())
        self.root.bind("<Escape>", lambda e: self.deselect_object())

        # Границы
        self.root.after(200, self.create_boundaries)

        # Запуск
        self.draw()
        self.root.mainloop()

    def on_canvas_resize(self, event):
        if event.width > 0 and event.height > 0:
            self.create_boundaries()

    def create_boundaries(self):
        self.ui.canvas.update_idletasks()
        width = self.ui.canvas.winfo_width()
        height = self.ui.canvas.winfo_height()
        self.physics.create_boundaries(width, height)

    def on_left_click(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.is_dragging = False

        obj_type = self.ui.tool_panel.current_tool.get()

        # === РЕЖИМ СОЗДАНИЯ ПРУЖИНЫ ===
        if obj_type == "spring":
            # Ищем объект под курсором
            clicked_obj = None
            for obj in reversed(self.objects):
                if obj.obj_type != "spring" and obj.is_clicked(event.x, event.y):
                    clicked_obj = obj
                    break

            if clicked_obj:
                if self.spring_first_obj is None:
                    # Первый клик — запоминаем объект
                    self.spring_first_obj = clicked_obj
                    self.selected_object = clicked_obj
                    self.ui.update_object_properties(clicked_obj)
                    print(f"Пружина: выберите второй объект (первый: {clicked_obj.obj_type})")
                else:
                    # Второй клик — создаём пружину!
                    if clicked_obj != self.spring_first_obj:
                        spring = Spring(self.spring_first_obj, clicked_obj)
                        spring.create(self.physics.space)
                        self.objects.append(spring)
                        self.total_created += 1
                        self.ui.add_object_to_list(f"↔ spring #{len(self.objects)}\n")
                        self.selected_object = spring
                        self.ui.update_object_properties(spring)
                        print(f"Пружина создана!")
                    # Сбрасываем
                    self.spring_first_obj = None
            return

        # === ОБЫЧНОЕ ПОВЕДЕНИЕ ===
        # Сбрасываем режим пружины если выбрали другой инструмент
        self.spring_first_obj = None

        # Поиск объекта
        for obj in reversed(self.objects):
            if obj.is_clicked(event.x, event.y):
                self.selected_object = obj
                self.ui.update_object_properties(obj)
                return

        # Создание объекта
        if not obj_type:
            return
        obj = create_object(obj_type, event.x, event.y, self.physics.space,
                            self.ui.elasticity_var.get())
        if obj:
            self.objects.append(obj)
            self.total_created += 1
            icon = {"circle": "⭕", "square": "⬛", "triangle": "🔺"}.get(obj_type, "❓")
            self.ui.add_object_to_list(f"{icon} {obj_type} #{len(self.objects)} ({obj.color})\n")
            self.selected_object = obj
            self.ui.update_object_properties(obj)

    def on_mouse_drag(self, event):
        if not self.selected_object:
            return

        dx = abs(event.x - self.drag_start_x)
        dy = abs(event.y - self.drag_start_y)

        if dx > self.drag_threshold or dy > self.drag_threshold:
            self.is_dragging = True
            self.selected_object.body.position = (event.x, event.y)
            self.selected_object.body.velocity = (0, 0)

    def on_mouse_release(self, event):
        self.is_dragging = False

    def on_right_click(self, event):
        for obj in reversed(self.objects):
            if obj.is_clicked(event.x, event.y):
                self.selected_object = obj
                self.ui.update_object_properties(obj)
                self.context_menu.show(event.x_root, event.y_root)
                return
        self.deselect_object()

    def delete_selected(self):
        if self.selected_object:
            idx = self.objects.index(self.selected_object)
            self.physics.remove_object(self.selected_object.body, self.selected_object.shape)
            self.objects.remove(self.selected_object)
            self.ui.remove_object_from_list(idx)
            self.selected_object = None

    def show_params(self):
        if self.selected_object:
            obj = self.selected_object
            print(f"\n{'=' * 30}")
            print(f"Тип: {obj.obj_type}, Цвет: {obj.color}")
            print(f"Размер: {obj.size}, Масса: {obj.body.mass}")
            print(f"Позиция: ({obj.body.position.x:.1f}, {obj.body.position.y:.1f})")
            print(f"{'=' * 30}\n")

    def duplicate_selected(self):
        if self.selected_object:
            obj = self.selected_object
            # Упрощённое дублирование
            new_obj = create_object(obj.obj_type, obj.body.position.x + 30,
                                    obj.body.position.y, self.physics.space,
                                    obj.shape.elasticity)
            if new_obj:
                new_obj.color = obj.color
                new_obj.size = obj.size
                self.objects.append(new_obj)
                self.total_created += 1
                icon = {"circle": "⭕", "square": "⬛", "triangle": "🔺"}.get(obj.obj_type, "❓")
                self.ui.add_object_to_list(f"{icon} {obj.obj_type} #{len(self.objects)} ({obj.color})\n")

    def clear_all(self):
        for obj in self.objects:
            self.physics.remove_object(obj.body, obj.shape)
        self.objects = []
        self.total_created = 0
        self.ui.objects_list.config(state="normal")
        self.ui.objects_list.delete(1.0, tk.END)
        self.ui.objects_list.config(state="disabled")
        self.ui.update_stats(0, 0)

    def apply_object_properties(self):
        if self.selected_object:
            obj = self.selected_object

            # === ПРУЖИНА — отдельная обработка ===
            if obj.obj_type == "spring":
                new_stiffness = self.ui.right_panel.obj_size_var.get() / 10.0  # Размер → жёсткость
                new_color = self.ui.right_panel.obj_color_var.get()
                obj.stiffness = new_stiffness
                obj.color = new_color
                # Пересоздаём constraint с новой жёсткостью
                self.physics.space.remove(obj.constraint)
                obj.create(self.physics.space)
                return

            # Получаем новые значения из UI
            new_size = self.ui.right_panel.obj_size_var.get()
            new_color = self.ui.right_panel.obj_color_var.get()

            # Проверяем тип объекта
            is_static = obj.body.body_type == pymunk.Body.STATIC

            pos = obj.body.position
            vel = obj.body.velocity

            # Удаляем старую форму из пространства
            self.physics.space.remove(obj.shape)

            # Обрабатываем в зависимости от типа
            if obj.obj_type == "spring":
                # Пружина - меняем длину и жёсткость
                new_stiffness = self.ui.right_panel.obj_stiffness_var.get()
                obj.shape = pymunk.Segment(obj.body, (-new_size / 2, 0), (new_size / 2, 0), 2)
                obj.shape.elasticity = 1.0
                obj.shape.friction = 0.0
                obj.size = new_size
                obj.color = new_color
                obj.stiffness = new_stiffness  # Сохраняем жёсткость

            elif is_static:
                # Статический объект - меняем размер и трение
                new_friction = self.ui.right_panel.obj_friction_var.get()

                if obj.obj_type == "line":
                    obj.shape = pymunk.Segment(obj.body, (-new_size / 2, 0), (new_size / 2, 0), 2)
                elif obj.obj_type == "circle":
                    obj.shape = pymunk.Circle(obj.body, new_size)
                elif obj.obj_type == "square":
                    obj.shape = pymunk.Poly.create_box(obj.body, (new_size, new_size))
                elif obj.obj_type == "spring":
                    obj.shape = pymunk.Segment(obj.body, (-new_size / 2, 0), (new_size / 2, 0), 2,obj.stiffness)

                obj.shape.elasticity = 1.0  # Статические всегда упругие
                obj.shape.friction = new_friction
                obj.size = new_size
                obj.color = new_color

            else:
                # Динамический объект - меняем размер, массу и упругость
                new_mass = self.ui.right_panel.obj_mass_var.get()
                new_elasticity = self.ui.right_panel.obj_elasticity_var.get()

                if obj.obj_type == "circle":
                    obj.shape = pymunk.Circle(obj.body, new_size)
                    obj.body.moment = pymunk.moment_for_circle(new_mass, 0, new_size)
                elif obj.obj_type == "square":
                    obj.shape = pymunk.Poly.create_box(obj.body, (new_size, new_size))
                    obj.body.moment = pymunk.moment_for_box(new_mass, (new_size, new_size))
                elif obj.obj_type == "triangle":
                    # Для треугольника нужна своя логика
                    obj.shape = pymunk.Poly.create_box(obj.body, (new_size, new_size))
                    obj.body.moment = pymunk.moment_for_box(new_mass, (new_size, new_size))

                obj.shape.elasticity = new_elasticity
                obj.shape.friction = 0.5
                obj.size = new_size
                obj.body.mass = new_mass
                obj.color = new_color

            # Возвращаем форму в пространство и восстанавливаем позицию
            self.physics.space.add(obj.shape)
            obj.body.position = pos
            obj.body.velocity = vel

    def deselect_object(self):
        self.selected_object = None

    def on_world_gravity_change(self, gx, gy):
        self.physics.set_gravity(gx, gy)

    def toggle_pause(self):
        self.ui.paused.set(not self.ui.paused.get())
        self.ui.toggle_pause()

    def toggle_grid(self):
        self.ui.show_grid.set(not self.ui.show_grid.get())

    def on_hierarchy_click(self, line_number, event):
        idx = line_number - 1
        if 0 <= idx < len(self.objects):
            self.selected_object = self.objects[idx]
            self.ui.update_object_properties(self.selected_object)
            self.context_menu.show(event.x_root, event.y_root)

    def draw(self):
        self.ui.canvas.delete("all")

        width = self.ui.canvas.winfo_width()
        height = self.ui.canvas.winfo_height()

        # Сетка
        if self.ui.show_grid.get():
            self.ui.canvas_view.draw_grid(width, height, show=True)

        # Границы
        self.ui.canvas.create_line(0, height - 2, width, height - 2, fill="black", width=4)
        self.ui.canvas.create_line(2, 0, 2, height - 2, fill="black", width=4)
        self.ui.canvas.create_line(width - 2, 0, width - 2, height - 2, fill="black", width=4)
        self.ui.canvas.create_line(2, 2, width - 2, 2, fill="black", width=4)

        # Объекты
        visible = 0
        for obj in self.objects:
            # === ПРУЖИНА - отдельная отрисовка ===
            if obj.obj_type == "spring":
                ax, ay = obj.obj_a.body.position
                bx, by = obj.obj_b.body.position
                points = self.get_spring_points(ax, ay, bx, by)
                self.ui.canvas.create_line(
                    points, fill=obj.color, width=2
                )
                # Рисуем кружочки на концах
                self.ui.canvas.create_oval(ax - 4, ay - 4, ax + 4, ay + 4, fill="gray")
                self.ui.canvas.create_oval(bx - 4, by - 4, bx + 4, by + 4, fill="gray")
                continue
            x, y = obj.body.position
            if 0 <= x <= width and 0 <= y <= height:
                visible += 1

            if obj == self.selected_object:
                outline = "black"
                width_line = 2
                dash = (5, 5)
            else:
                outline = "black"
                width_line = 1
                dash = ""

            if obj.obj_type == "circle":
                self.ui.canvas.create_oval(
                    x - obj.size, y - obj.size, x + obj.size, y + obj.size,
                    fill=obj.color, outline=outline, width=width_line, dash=dash
                )
            elif obj.obj_type == "square":
                points = self.get_rotated_rect_points(x, y, obj.size, obj.body.angle)
                self.ui.canvas.create_polygon(points, fill=obj.color,
                                              outline=outline, width=width_line, dash=dash)
            elif obj.obj_type == "triangle":
                points = self.get_rotated_triangle_points(x, y, obj.size, obj.body.angle)
                self.ui.canvas.create_polygon(points, fill=obj.color,
                                              outline=outline, width=width_line, dash=dash)
            elif obj.obj_type == "line":
                # Получаем точки сегмента относительно центра тела
                a = obj.shape.a
                b = obj.shape.b
                angle = obj.body.angle

                # Поворачиваем точки
                import math
                ax = a[0] * math.cos(angle) - a[1] * math.sin(angle)
                ay = a[0] * math.sin(angle) + a[1] * math.cos(angle)
                bx = b[0] * math.cos(angle) - b[1] * math.sin(angle)
                by = b[0] * math.sin(angle) + b[1] * math.cos(angle)

                # Прибавляем позицию тела
                x1 = x + ax
                y1 = y + ay
                x2 = x + bx
                y2 = y + by

                # Рисуем линию
                self.ui.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=obj.color, width=3,
                    capstyle=tk.ROUND
                )
            elif obj.obj_type == "spring":
                # Пружина — рисуем зигзаг между двумя объектами
                ax, ay = obj.obj_a.body.position
                bx, by = obj.obj_b.body.position
                points = self.get_spring_points(ax, ay, bx, by)
                self.ui.canvas.create_line(
                    points, fill=obj.color, width=2
                )
                # Рисуем кружочки на концах
                self.ui.canvas.create_oval(ax-4, ay-4, ax+4, ay+4, fill="gray")
                self.ui.canvas.create_oval(bx-4, by-4, bx+4, by+4, fill="gray")

        # Статистика
        self.ui.update_stats(self.total_created, visible)

        # Физика
        if not self.ui.paused.get():
            self.physics.step()

        self.root.after(16, self.draw)

    def get_rotated_rect_points(self, x, y, size, angle):
        import math
        points = []
        for dx, dy in [(-size / 2, -size / 2), (size / 2, -size / 2),
                       (size / 2, size / 2), (-size / 2, size / 2)]:
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            points.append((x + rx, y + ry))
        return points

    def get_spring_points(self, x1, y1, x2, y2, coils=8, amplitude=10):
        """Генерирует точки зигзага для пружины"""
        import math
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return [x1, y1, x2, y2]

        # Направление и перпендикуляр
        nx = dx / length
        ny = dy / length
        px = -ny  # перпендикуляр
        py = nx

        points = []
        segments = coils * 2
        for i in range(segments + 1):
            t = i / segments
            # Базовая точка
            bx = x1 + dx * t
            by = y1 + dy * t
            # Отклонение
            if i == 0 or i == segments:
                offset = 0
            else:
                offset = amplitude * (1 if i % 2 == 1 else -1)
            points.append((bx + px * offset, by + py * offset))

        # Разворачиваем в плоский список для create_line
        flat = []
        for p in points:
            flat.extend(p)
        return flat

    def get_rotated_triangle_points(self, x, y, size, angle):
        import math
        points = [(0, -size), (-size, size), (size, size)]
        result = []
        for dx, dy in points:
            rx = dx * math.cos(angle) - dy * math.sin(angle)
            ry = dx * math.sin(angle) + dy * math.cos(angle)
            result.append((x + rx, y + ry))
        return result


if __name__ == "__main__":
    app = PhysicsSandbox()