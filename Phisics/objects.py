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

class Weld(PhysicsObject):
    """Фиксированная линия (статическая, невесомая, абсолютно упругая)"""

    def __init__(self, x, y):
        size = 100  # длина линии
        super().__init__(x, y, "gray", "line", size)

    def create(self, space, elasticity=1.0):
        # Статическое тело — неподвижное, невесомое
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = self.position

        # Создаём сегмент (линию) от (-size/2, 0) до (size/2, 0)
        # Третий параметр — толщина линии
        self.shape = pymunk.Segment(self.body, (-self.size/2, 0), (self.size/2, 0), 2)
        self.shape.elasticity = elasticity  # абсолютно упругая
        self.shape.friction = 0.0

        space.add(self.body, self.shape)

    def is_clicked(self, click_x, click_y):
        """Проверка клика по линии"""
        x, y = self.body.position
        half_size = self.size / 2
        thickness = 10  # допуск по толщине клика
        return (x - half_size <= click_x <= x + half_size and
                y - thickness <= click_y <= y + thickness)


class Spring(PhysicsObject):
    """Пружина - соединяет два объекта"""

    def __init__(self, obj_a, obj_b, stiffness=15.0, damping=1.0):
        super().__init__(0, 0, "gray", "spring", 50)
        self.obj_a = obj_a  # Первый объект
        self.obj_b = obj_b  # Второй объект
        self.stiffness = stiffness  # Жёсткость
        self.damping = damping  # Затухание
        self.constraint = None

    def create(self, space):
        """Создаёт пружину между двумя телами"""
        # Пружина крепится к центрам объектов
        self.constraint = pymunk.DampedSpring(
            self.obj_a.body, self.obj_b.body,
            (0, 0), (0, 0),  # Точки крепления (центр тел)
            rest_length=100,  # Длина покоя (расстояние без нагрузки)
            stiffness=self.stiffness,  # Жёсткость
            damping=self.damping  # Затухание
        )
        space.add(self.constraint)

    def is_clicked(self, click_x, click_y):
        """Проверяем клик по линии пружины (упрощённо)"""
        ax, ay = self.obj_a.body.position
        bx, by = self.obj_b.body.position

        # Расстояние от точки до линии
        import math
        dx = bx - ax
        dy = by - ay
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return False

        t = max(0, min(1, ((click_x - ax) * dx + (click_y - ay) * dy) / (length * length)))
        proj_x = ax + t * dx
        proj_y = ay + t * dy
        dist = math.sqrt((click_x - proj_x) ** 2 + (click_y - proj_y) ** 2)

        return dist < 15  # Допуск 15 пикселей


def create_object(obj_type, x, y, space, elasticity=0.8):
    """Фабрика объектов"""
    if obj_type == "circle":
        obj = Ball(x, y)
    elif obj_type == "square":
        obj = Box(x, y)
    elif obj_type == "triangle":
        obj = Triangle(x, y)
    elif obj_type == "line":
        obj = Weld(x, y)
    elif obj_type == "spring":
        return Spring(x, y, space)
    else:
        return None

    obj.create(space, elasticity)
    return obj