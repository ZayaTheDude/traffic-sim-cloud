import pygame

class Intersection:
    def __init__(self, x, y, width=60, height=60, cycle_duration=300):
        self.rect = pygame.Rect(x, y, width, height)
        self.state = "NS_GREEN"  # Other state is "EW_GREEN"
        self.tick_count = 0
        self.cycle_duration = cycle_duration  # Ticks per light change

    def update(self):
        self.tick_count += 1
        if self.tick_count >= self.cycle_duration:
            self.state = "EW_GREEN" if self.state == "NS_GREEN" else "NS_GREEN"
            self.tick_count = 0

    def is_direction_green(self, direction):
        """Return True if car with given direction has green light."""
        if direction in ("up", "down"):
            return self.state == "NS_GREEN"
        elif direction in ("left", "right"):
            return self.state == "EW_GREEN"
        return False

    def draw(self, surface):
        # Draw the box itself
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        # Draw signal lights (just simple colored circles in each corner)
        light_radius = 8
        padding = 5

        # North/South (draw top and bottom)
        ns_color = (0, 255, 0) if self.state == "NS_GREEN" else (255, 0, 0)
        pygame.draw.circle(surface, ns_color, (self.rect.centerx, self.rect.top - padding), light_radius)
        pygame.draw.circle(surface, ns_color, (self.rect.centerx, self.rect.bottom + padding), light_radius)

        # East/West (draw left and right)
        ew_color = (0, 255, 0) if self.state == "EW_GREEN" else (255, 0, 0)
        pygame.draw.circle(surface, ew_color, (self.rect.left - padding, self.rect.centery), light_radius)
        pygame.draw.circle(surface, ew_color, (self.rect.right + padding, self.rect.centery), light_radius)
