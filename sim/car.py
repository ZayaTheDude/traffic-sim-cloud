import pygame

class Car:
    WIDTH, HEIGHT = 60, 30
    COLOR = (255, 0, 0)

    def __init__(self, x, y, speed=5, direction="right", car_id=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # "right", "left", "up", "down"
        self.id = car_id or id(self)

    def move(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(surface, self.COLOR, rect)

    def get_state(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction
        }
