# simulator.py
# -------------
# Main entry point for the traffic simulation using Pygame.
# Handles window setup, simulation loop, car spawning, intersection logic, drawing, and logging.
#
# Key components:
#   - Initializes the Pygame window and simulation parameters
#   - Spawns cars at random intervals and directions
#   - Updates and draws cars and intersection
#   - Handles traffic light phases and car movement logic
#   - Logs car states for analysis
#   - (Optional) Uploads simulation logs to the cloud

import pygame
import sys
import os
import random
import json
import argparse
from car import Car
from intersection import Intersection
from logger import Logger
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cloud.upload_logs import upload_file

###############################
# Initialization and Settings #
###############################

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/standard.json", help="Path to simulation config file")
    return parser.parse_args()

args = parse_args()

config = load_config(args.config)

pygame.init()
WIDTH, HEIGHT = 800, 600  # Window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Main Pygame window surface

logger = Logger()  # For logging car states
pygame.display.set_caption("Traffic Sim")
cars = []  # List of active cars in the simulation

# Color definitions (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRASS_GREEN = (34, 139, 34)
ROAD_GRAY = (50, 50, 50)

clock = pygame.time.Clock()
FPS = config["fps"]  # Simulation frames per second

# Create the intersection at the center
intersection = Intersection(x=350, y=250, width=100, height=100, phase_duration=config["intersection_phase_duration"])

tick_count = 0  # Simulation tick counter
# next_spawn = random.randint(90, 150)  # Random initial spawn time for the first car
next_spawn = tick_count + random.randint(*config["car_spawn_interval_range"])  # Start with no cars, will spawn on first tick

def can_spawn(new_car, cars):
    """
    Check if a new car can be spawned without colliding with existing cars.
    Args:
        new_car (Car): The car to check.
        cars (list): List of existing cars.
    Returns:
        bool: True if spawn is possible, False otherwise.
    """
    for car in cars:
        if new_car.car_rect.colliderect(car.car_rect):
            return False
    return True

#########################
# Main Simulation Loop   #
#########################

running = True
while running:
    clock.tick(FPS)
    WIN.fill(GRASS_GREEN)

    # Draw horizontal road
    pygame.draw.rect(WIN, ROAD_GRAY, pygame.Rect(0, 250, WIDTH, 100))  # horizontal strip

    # Draw vertical road
    pygame.draw.rect(WIN, ROAD_GRAY, pygame.Rect(350, 0, 100, HEIGHT))  # vertical strip

    # Draw dashed lines for road markings
    DASH_COLOR = YELLOW
    DASH_WIDTH = 5
    DASH_HEIGHT = 20
    DASH_GAP = 20

    # Horizontal dashed line (center of horizontal road)
    y_center = 250 + 50 - DASH_HEIGHT // 2 + 7
    for x in range(0, 350, DASH_HEIGHT + DASH_GAP):
        pygame.draw.rect(WIN, DASH_COLOR, (x, y_center, DASH_HEIGHT, DASH_WIDTH))
    for x in range(455, WIDTH, DASH_HEIGHT + DASH_GAP):
        pygame.draw.rect(WIN, DASH_COLOR, (x, y_center, DASH_HEIGHT, DASH_WIDTH))

    # Vertical dashed line (center of vertical road)
    x_center = 350 + 50 - DASH_WIDTH // 2
    for y in range(0, 240, DASH_HEIGHT + DASH_GAP):
        pygame.draw.rect(WIN, DASH_COLOR, (x_center, y, DASH_WIDTH, DASH_HEIGHT))
    for y in range(350, HEIGHT, DASH_HEIGHT + DASH_GAP):
        pygame.draw.rect(WIN, DASH_COLOR, (x_center, y, DASH_WIDTH, DASH_HEIGHT))

    # Draw intersection and its traffic lights
    intersection.draw(WIN)

    # Spawn new cars at intervals
    if tick_count % next_spawn == 0:
        # Define spawn points and directions for each entry
        spawn_configs = [
            {"x": 0, "y": 310, "direction": "right", "color": RED},      # From left
            {"x": 360, "y": 0, "direction": "down", "color": GREEN},     # From top
            {"x": WIDTH, "y": 260, "direction": "left", "color": BLUE},  # From right
            {"x": 410, "y": HEIGHT, "direction": "up", "color": ORANGE}, # From bottom
        ]

        for sconfig in spawn_configs:
            new_car = Car(
                x=sconfig["x"],
                y=sconfig["y"],
                speed=random.randint(*config["car_speed_range"]),  # Random speed within defined range
                direction=sconfig["direction"],
                turn_direction=random.choice([None, "left", "right"]),
                color=sconfig["color"]
            )
            if can_spawn(new_car, cars):
                cars.append(new_car)

        # Set next spawn interval
        next_spawn = tick_count + random.randint(50, 150)

    # Handle window close event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update intersection phase
    intersection.update()

    # Update and draw each car
    for car in cars:
        if car.should_stop(intersection, cars):
            car.increment_wait()  # Car is stopped (waiting)
        else:
            car.move()           # Car moves forward or turns
        car.draw(WIN)
        print(car.get_state())  # Print car state for debugging

    # Remove cars that have exited the window
    cars = [car for car in cars if car.x < WIDTH and car.y < HEIGHT]

    # Log car states for this tick
    car_states = [car.get_state() for car in cars]
    logger.log(tick_count, car_states)

    pygame.display.update()  # Refresh display
    tick_count += 1

# Uncomment below to save and upload simulation logs after run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"sim_log_{timestamp}.json"
logger.write_to_file(f"data/{filename}")
upload_file(f"data/{filename}")

pygame.quit()
sys.exit()
