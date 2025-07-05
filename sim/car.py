import pygame

class Car:
    WIDTH, HEIGHT = 60, 30
    COLOR = (255, 0, 0)

    def __init__(self, x, y, speed=5, direction="right", car_id=None, turn_direction=None, color=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # "right", "left", "up", "down"
        self.id = car_id or id(self)
        self.wait_time = 0  # Time spent waiting at an intersection
        self.in_intersection = False  # Whether the car is currently in an intersection
        self.car_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        self.front_bumper = pygame.Rect(self.x + 40, self.y, 30, 30)  # Front bumper rectangle
        self.turning = False  # Whether the car is currently turning
        self.turn_direction = turn_direction  # Direction the car is turning ("left" or "right")
        self.color = color if color else self.COLOR

    def move(self):
        if self.direction == "right":
            if self.turn_direction == "right" and self.x >= 360 and self.turning == False:  # Turn right near intersection
                self.turning = True
                self.direction = "down"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            elif self.turn_direction == "left" and self.x >= 410 and self.turning == False:  # Turn left near intersection
                self.turning = True
                self.direction = "up"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            else:
                self.x += self.speed
        elif self.direction == "left":
            if self.turn_direction == "right" and self.x <= 410 and self.turning == False:
                self.turning = True
                self.direction = "up"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            elif self.turn_direction == "left" and self.x <= 360 and self.turning == False:
                self.turning = True
                self.direction = "down"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            else:
                self.x -= self.speed
        elif self.direction == "up":
            # Adjust shape for up direction
            self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            if self.turn_direction == "right" and self.y <= 310 and self.turning == False:
                self.turning = True
                self.direction = "right"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            elif self.turn_direction == "left" and self.y <= 260 and self.turning == False:
                self.turning = True
                self.direction = "left"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            else:
                self.y -= self.speed
        elif self.direction == "down":
            # Adjust shape for down direction
            self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            if self.turn_direction == "right" and self.y >= 260 and self.turning == False:
                self.turning = True
                self.direction = "left"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            elif self.turn_direction == "left" and self.y >= 310 and self.turning == False:
                self.turning = True
                self.direction = "right"
                # adjust car shape
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            else:
                self.y += self.speed
        
        self.car_rect.x = self.x
        self.car_rect.y = self.y
        
        self.update_bumper()  # Update front bumper position based on direction


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.car_rect)
        self.update_bumper()  # Ensure bumper is updated before drawing

    def get_state(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "wait_time": self.wait_time
        }
    
    def should_stop(self, intersection, cars):
        for other in cars:
            if other == self:
                continue
            if self.front_bumper.colliderect(other.car_rect):
                # If colliding with another car, stop
                return True
        
        if self.in_intersection:
            return False # Already in intersection, no need to stop

        if self.front_bumper.colliderect(intersection.rect):
            if intersection.is_direction_green(self.direction):
                self.in_intersection = True
                return False
            else:
                return True
        
        self.in_intersection = False # Not in intersection
        return False

    def increment_wait(self):
        self.wait_time += 1

    def update_bumper(self):
        if self.direction == "right":
            self.front_bumper.x = self.x + 40
            self.front_bumper.y = self.y
        elif self.direction == "down":
            self.front_bumper.x = self.x
            self.front_bumper.y = self.y + 40
        elif self.direction == "left":
            self.front_bumper.x = self.x - 10
            self.front_bumper.y = self.y
        elif self.direction == "up":
            self.front_bumper.x = self.x
            self.front_bumper.y = self.y - 10

