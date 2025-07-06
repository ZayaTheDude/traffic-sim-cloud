
# car.py
# --------
# Defines the Car class for the traffic simulation.
# Each Car object represents a vehicle that can move, turn, detect collisions, and interact with intersections.
# Handles car movement, drawing, state reporting, and logic for stopping at intersections or behind other cars.

import pygame


class Car:
    """
    Represents a car in the traffic simulation.
    Handles movement, turning, collision detection, and intersection logic.
    """
    WIDTH, HEIGHT = 60, 30  # Default car dimensions
    COLOR = (255, 0, 0)     # Default car color (red)

    def __init__(self, x, y, speed=5, direction="right", car_id=None, turn_direction=None, color=None):
        """
        Initialize a Car object.
        Args:
            x (int): Initial x position.
            y (int): Initial y position.
            speed (int): Speed of the car (pixels per tick).
            direction (str): Initial direction ("right", "left", "up", "down").
            car_id (any): Optional unique identifier for the car.
            turn_direction (str): Optional turn direction ("left", "right", or None).
            color (tuple): Optional RGB color for the car.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # Current direction
        self.id = car_id or id(self)
        self.wait_time = 0  # Time spent waiting at an intersection
        self.in_intersection = False  # Whether the car is currently in an intersection
        self.car_rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)  # Main car rectangle
        self.front_bumper = pygame.Rect(self.x + 40, self.y, 30, 30)  # Rectangle for collision detection at the front
        self.turning = False  # Whether the car is currently turning
        self.turn_direction = turn_direction  # Direction the car is turning ("left" or "right")
        self.color = color if color else self.COLOR


    def move(self):
        """
        Move the car forward or turn if needed.
        Handles direction changes and updates the car's rectangle and bumper.
        """
        if self.direction == "right":
            # Handle right/left turns near intersection
            if self.turn_direction == "right" and self.x >= 360 and not self.turning:
                self.turning = True
                self.direction = "down"
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            elif self.turn_direction == "left" and self.x >= 410 and not self.turning:
                self.turning = True
                self.direction = "up"
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            else:
                self.x += self.speed
        elif self.direction == "left":
            if self.turn_direction == "right" and self.x <= 410 and not self.turning:
                self.turning = True
                self.direction = "up"
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            elif self.turn_direction == "left" and self.x <= 360 and not self.turning:
                self.turning = True
                self.direction = "down"
                self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            else:
                self.x -= self.speed
        elif self.direction == "up":
            # Adjust shape for up direction
            self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            if self.turn_direction == "right" and self.y <= 310 and not self.turning:
                self.turning = True
                self.direction = "right"
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            elif self.turn_direction == "left" and self.y <= 260 and not self.turning:
                self.turning = True
                self.direction = "left"
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            else:
                self.y -= self.speed
        elif self.direction == "down":
            # Adjust shape for down direction
            self.car_rect.width, self.car_rect.height = self.HEIGHT, self.WIDTH
            if self.turn_direction == "right" and self.y >= 260 and not self.turning:
                self.turning = True
                self.direction = "left"
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            elif self.turn_direction == "left" and self.y >= 310 and not self.turning:
                self.turning = True
                self.direction = "right"
                self.car_rect.width, self.car_rect.height = self.WIDTH, self.HEIGHT
            else:
                self.y += self.speed

        # Update car rectangle position
        self.car_rect.x = self.x
        self.car_rect.y = self.y

        self.update_bumper()  # Update front bumper position based on direction



    def draw(self, surface):
        """
        Draw the car on the given surface.
        Args:
            surface: The Pygame surface to draw on.
        """
        pygame.draw.rect(surface, self.color, self.car_rect)
        self.update_bumper()  # Ensure bumper is updated before drawing


    def get_state(self):
        """
        Return the current state of the car for logging or debugging.
        Returns:
            dict: Car state including id, position, direction, and wait time.
        """
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "wait_time": self.wait_time
        }

    def should_stop(self, intersection, cars):
        """
        Determine if the car should stop (for another car or at the intersection).
        Args:
            intersection: The Intersection object.
            cars (list): List of all Car objects.
        Returns:
            bool: True if the car should stop, False otherwise.
        """
        for other in cars:
            if other == self:
                continue
            if self.front_bumper.colliderect(other.car_rect):
                # If colliding with another car, stop
                return True

        if self.in_intersection:
            return False  # Already in intersection, no need to stop

        if self.front_bumper.colliderect(intersection.rect):
            if intersection.is_movement_allowed(self.direction, self.turn_direction):
                self.in_intersection = True
                return False
            else:
                return True

        self.in_intersection = False  # Not in intersection
        return False

    def increment_wait(self):
        """
        Increment the wait time counter (called when car is stopped).
        """
        self.wait_time += 1

    def update_bumper(self):
        """
        Update the position of the front bumper rectangle based on the car's direction.
        Used for collision detection.
        """
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

