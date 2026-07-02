"""Физическая песочница v2.5 - ТОЧКА ВХОДА"""
import customtkinter as ctk
import tkinter as tk
import pymunk
from Phisics.objects import create_object
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

        # Поиск объекта
        for obj in reversed(self.objects):
            if obj.is_clicked(event.x, event.y):
                self.selected_object = obj
                self.ui.update_object_properties(obj)
                return

        # Создание объекта
        obj_type = self.ui.current_object.get()
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
            new_size = self.ui.right_panel.obj_size_var.get()
            new_mass = self.ui.right_panel.obj_mass_var.get()
            new_elasticity = self.ui.right_panel.obj_elasticity_var.get()
            new_color = self.ui.right_panel.obj_color_var.get()

            pos = obj.body.position
            vel = obj.body.velocity

            self.physics.space.remove(obj.shape)

            if obj.obj_type == "circle":
                obj.shape = pymunk.Circle(obj.body, new_size)
                obj.body.moment = pymunk.moment_for_circle(new_mass, 0, new_size)
            elif obj.obj_type == "square":
                obj.shape = pymunk.Poly.create_box(obj.body, (new_size, new_size))
                obj.body.moment = pymunk.moment_for_box(new_mass, (new_size, new_size))

            obj.shape.elasticity = new_elasticity
            obj.size = new_size
            obj.body.mass = new_mass
            obj.color = new_color

            self.physics.space.add(obj.shape)
            obj.body.position = pos
            obj.body.velocity = vel

    def deselect_object(self):
        self.selected_object = None

    def on_world_gravity_change(self, gx, gy):
        self.physics.set_gravity(gx, gy)

    def toggle_pause(self):
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