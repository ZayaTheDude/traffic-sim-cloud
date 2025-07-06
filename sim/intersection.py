
# intersection.py
# ---------------
# Defines the Intersection class for the traffic simulation.
# Handles intersection logic, traffic light phases, movement permissions, and drawing the intersection and lights.

import pygame


class Intersection:
    """
    Represents a traffic intersection with traffic light phases.
    Controls which directions/cars are allowed to move based on the current phase.
    Handles updating the phase and drawing the intersection and its lights.
    """
    def __init__(self, x, y, width=60, height=60, phase_duration=180):
        """
        Initialize an Intersection object.
        Args:
            x (int): X position of the intersection.
            y (int): Y position of the intersection.
            width (int): Width of the intersection box.
            height (int): Height of the intersection box.
            phase_duration (int): Number of ticks each phase lasts.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.phases = [
            "NS_STRAIGHT_RIGHT",  # North-South straight and right turns
            "NS_LEFT",            # North-South left turns
            "EW_STRAIGHT_RIGHT", # East-West straight and right turns
            "EW_LEFT"             # East-West left turns
        ]
        self.current_phase = 0
        self.phase_duration = phase_duration
        self.tick_count = 0


    def update(self):
        """
        Advance the phase timer and switch to the next phase if needed.
        """
        self.tick_count += 1
        if self.tick_count >= self.phase_duration:
            self.current_phase = (self.current_phase + 1) % len(self.phases)
            self.tick_count = 0


    def is_movement_allowed(self, direction, turn_direction):
        """
        Determine if a car is allowed to move through the intersection based on the current phase.
        Args:
            direction (str): The car's direction ("up", "down", "left", "right").
            turn_direction (str): The car's turn direction ("left", "right", or None).
        Returns:
            bool: True if movement is allowed, False otherwise.
        """
        phase = self.phases[self.current_phase]
        if phase == "NS_STRAIGHT_RIGHT":
            return direction in ("up", "down") and (turn_direction is None or turn_direction == "right")
        elif phase == "NS_LEFT":
            return direction in ("up", "down") and turn_direction == "left"
        elif phase == "EW_STRAIGHT_RIGHT":
            return direction in ("left", "right") and (turn_direction is None or turn_direction == "right")
        elif phase == "EW_LEFT":
            return direction in ("left", "right") and turn_direction == "left"
        return False


    def draw(self, surface):
        """
        Draw the intersection box and traffic lights on the given surface.
        Args:
            surface: The Pygame surface to draw on.
        """
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        # Color coding for each phase: (NS color, EW color)
        phase_colors = {
            "NS_STRAIGHT_RIGHT": ((0, 255, 0), (255, 0, 0)),  # NS green, EW red
            "NS_LEFT": ((0, 255, 0), (255, 0, 0)),
            "EW_STRAIGHT_RIGHT": ((255, 0, 0), (0, 255, 0)),  # NS red, EW green
            "EW_LEFT": ((255, 0, 0), (0, 255, 0)),
        }

        ns_color, ew_color = phase_colors[self.phases[self.current_phase]]
        padding = 5
        radius = 8

        # Draw North-South traffic lights (top and bottom of intersection)
        pygame.draw.circle(surface, ns_color, (self.rect.centerx, self.rect.top - padding), radius)
        pygame.draw.circle(surface, ns_color, (self.rect.centerx, self.rect.bottom + padding), radius)

        # Draw East-West traffic lights (left and right of intersection)
        pygame.draw.circle(surface, ew_color, (self.rect.left - padding, self.rect.centery), radius)
        pygame.draw.circle(surface, ew_color, (self.rect.right + padding, self.rect.centery), radius)
