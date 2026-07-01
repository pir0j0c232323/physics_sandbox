# physics_engine.py
import pymunk


class PhysicsEngine:
    """Управляет физическим миром"""

    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 500)
        self.boundaries = []

    def set_gravity(self, value):
        """Устанавливает гравитацию"""
        self.space.gravity = (0, value)

    def create_boundaries(self, width, height):
        """Создаёт границы мира"""
        # Удаляем старые
        for b in self.boundaries:
            self.space.remove(b)
        self.boundaries = []

        # Пол (сдвинут к краю)
        floor = pymunk.Segment(self.space.static_body, (0, height - 2), (width, height - 2), 2)
        floor.elasticity = 0.8
        self.space.add(floor)
        self.boundaries.append(floor)

        # Левая стена
        wall_left = pymunk.Segment(self.space.static_body, (2, 0), (2, height - 2), 2)
        wall_left.elasticity = 0.8
        self.space.add(wall_left)
        self.boundaries.append(wall_left)

        # Правая стена
        wall_right = pymunk.Segment(self.space.static_body, (width - 2, 0), (width - 2, height - 2), 2)
        wall_right.elasticity = 0.8
        self.space.add(wall_right)
        self.boundaries.append(wall_right)

        # Потолок
        ceiling = pymunk.Segment(self.space.static_body, (2, 2), (width - 2, 2), 2)
        ceiling.elasticity = 0.8
        self.space.add(ceiling)
        self.boundaries.append(ceiling)

    def step(self):
        """Обновляет физику на 1 кадр"""
        self.space.step(1 / 60)

    def remove_object(self, body, shape):
        """Удаляет объект из мира"""
        self.space.remove(body, shape)

    def set_gravity(self, x, y):
        """Устанавливает гравитацию (X, Y)"""
        self.space.gravity = (x, y)