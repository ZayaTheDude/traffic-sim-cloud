import pygame

class Intersection:
    def __init__(self, x, y, width=60, height=60, green_duration=180, red_duration=180):
        self.rect = pygame.Rect(x, y, width, height)
        self.occupants = set()
        self.timer = 0
        self.green_duration = green_duration
        self.red_duration = red_duration

    def is_green(self):
        cycle = self.green_duration + self.red_duration
        return (self.timer % cycle) < self.green_duration

    def update(self):
        self.timer += 1

    def draw(self, surface):
        color = (0, 255, 0) if self.is_green() else (255, 0, 0)
        pygame.draw.rect(surface, color, self.rect, 2)