import pygame

class Intersection:
    def __init__(self, x, y, width=60, height=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.occupants = set()

    def try_enter(self, car_id):
        if self.is_occupied():
            return False
        self.occupants.add(car_id)
        return True

    def leave(self, car_id):
        self.occupants.discard(car_id)

    def is_occupied(self):
        return len(self.occupants) > 0

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)
