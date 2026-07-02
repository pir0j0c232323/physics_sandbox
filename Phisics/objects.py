import random
import math
import pymunk


class PhysicsObject:
    """Базовый класс для всех объектов"""

    def __init__(self, x, y, color, obj_type, size):
        self.body = None
        self.shape = None
        self.color = color
        self.obj_type = obj_type
        self.size = size
        self.position = (x, y)

    def create(self, space, elasticity=0.8):
        """Создаёт физическое тело и форму"""
        pass  # Переопределяется в наследниках

    def is_clicked(self, click_x, click_y):
        """Проверяет клик по объекту"""
        pass  # Переопределяется в наследниках


class Ball(PhysicsObject):
    """Шарик"""

    def __init__(self, x, y):
        radius = 25
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]
        color = random.choice(colors)
        super().__init__(x, y, color, "circle", radius)

    def create(self, space, elasticity=0.8):
        self.body = pymunk.Body(1.0, pymunk.moment_for_circle(1.0, 0, self.size))
        self.body.position = self.position

        self.shape = pymunk.Circle(self.body, self.size)
        self.shape.elasticity = elasticity

        space.add(self.body, self.shape)

    def is_clicked(self, click_x, click_y):
        x, y = self.body.position
        distance = math.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)
        return distance <= self.size


class Box(PhysicsObject):
    """Квадрат"""

    def __init__(self, x, y):
        size = 25
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        color = random.choice(colors)
        super().__init__(x, y, color, "square", size)

    def create(self, space, elasticity=0.8):
        self.body = pymunk.Body(1.0, pymunk.moment_for_box(1.0, (self.size, self.size)))
        self.body.position = self.position

        self.shape = pymunk.Poly.create_box(self.body, (self.size, self.size))
        self.shape.elasticity = elasticity

        space.add(self.body, self.shape)

    def is_clicked(self, click_x, click_y):
        x, y = self.body.position
        half_size = self.size / 2
        return (x - half_size <= click_x <= x + half_size and
                y - half_size <= click_y <= y + half_size)


class Triangle(PhysicsObject):
    """Треугольник"""

    def __init__(self, x, y):
        size = 25
        colors = ["red", "blue", "green", "yellow", "purple"]
        color = random.choice(colors)
        super().__init__(x, y, color, "triangle", size)

    def create(self, space, elasticity=0.8):
        points = [(0, -self.size), (-self.size, self.size), (self.size, self.size)]
        self.body = pymunk.Body(1.0, pymunk.moment_for_poly(1.0, points))
        self.body.position = self.position

        points = [(0, -self.size), (-self.size, self.size), (self.size, self.size)]
        self.shape = pymunk.Poly(self.body, points)
        self.shape.elasticity = elasticity

        space.add(self.body, self.shape)

    def is_clicked(self, click_x, click_y):
        x, y = self.body.position
        distance = math.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)
        return distance <= self.size


def create_object(obj_type, x, y, space, elasticity=0.8):
    """Фабрика объектов"""
    if obj_type == "circle":
        obj = Ball(x, y)
    elif obj_type == "square":
        obj = Box(x, y)
    elif obj_type == "triangle":
        obj = Triangle(x, y)
    else:
        return None

    obj.create(space, elasticity)
    return obj