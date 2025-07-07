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
    parser.add_argument("--no-gui", action="store_true", help="Run without GUI for headless cloud execution")
    parser.add_argument("--max-ticks", type=int, default=1000, help="Number of ticks to run before exiting")
    return parser.parse_args()

args = parse_args()
config = load_config(args.config)

if not args.no_gui:
    pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = None
if not args.no_gui:
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Traffic Sim")

logger = Logger()
cars = []

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRASS_GREEN = (34, 139, 34)
ROAD_GRAY = (50, 50, 50)

clock = pygame.time.Clock()
FPS = config["fps"]

intersection = Intersection(x=350, y=250, width=100, height=100, phase_duration=config["intersection_phase_duration"])
tick_count = 0
next_spawn = tick_count + random.randint(*config["car_spawn_interval_range"])

def can_spawn(new_car, cars):
    for car in cars:
        if new_car.car_rect.colliderect(car.car_rect):
            return False
    return True

#########################
# Main Simulation Loop  #
#########################

running = True
while running:
    clock.tick(FPS)

    if not args.no_gui:
        WIN.fill(GRASS_GREEN)

        # Roads
        pygame.draw.rect(WIN, ROAD_GRAY, pygame.Rect(0, 250, WIDTH, 100))
        pygame.draw.rect(WIN, ROAD_GRAY, pygame.Rect(350, 0, 100, HEIGHT))

        # Dashed Lines
        DASH_COLOR = YELLOW
        DASH_WIDTH = 5
        DASH_HEIGHT = 20
        DASH_GAP = 20
        y_center = 250 + 50 - DASH_HEIGHT // 2 + 7
        for x in range(0, 350, DASH_HEIGHT + DASH_GAP):
            pygame.draw.rect(WIN, DASH_COLOR, (x, y_center, DASH_HEIGHT, DASH_WIDTH))
        for x in range(455, WIDTH, DASH_HEIGHT + DASH_GAP):
            pygame.draw.rect(WIN, DASH_COLOR, (x, y_center, DASH_HEIGHT, DASH_WIDTH))
        x_center = 350 + 50 - DASH_WIDTH // 2
        for y in range(0, 240, DASH_HEIGHT + DASH_GAP):
            pygame.draw.rect(WIN, DASH_COLOR, (x_center, y, DASH_WIDTH, DASH_HEIGHT))
        for y in range(350, HEIGHT, DASH_HEIGHT + DASH_GAP):
            pygame.draw.rect(WIN, DASH_COLOR, (x_center, y, DASH_WIDTH, DASH_HEIGHT))

        intersection.draw(WIN)

    # Spawn cars
    if tick_count % next_spawn == 0:
        spawn_configs = [
            {"x": 0, "y": 310, "direction": "right", "color": RED},
            {"x": 360, "y": 0, "direction": "down", "color": GREEN},
            {"x": WIDTH, "y": 260, "direction": "left", "color": BLUE},
            {"x": 410, "y": HEIGHT, "direction": "up", "color": ORANGE},
        ]
        for sconfig in spawn_configs:
            new_car = Car(
                x=sconfig["x"],
                y=sconfig["y"],
                speed=random.randint(*config["car_speed_range"]),
                direction=sconfig["direction"],
                turn_direction=random.choice([None, "left", "right"]),
                color=sconfig["color"]
            )
            if can_spawn(new_car, cars):
                cars.append(new_car)
        next_spawn = tick_count + random.randint(50, 150)

    if not args.no_gui:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    intersection.update()

    for car in cars:
        if car.should_stop(intersection, cars):
            car.increment_wait()
        else:
            car.move()
        if not args.no_gui:
            car.draw(WIN)
        print(car.get_state())

    cars = [car for car in cars if car.x < WIDTH and car.y < HEIGHT]
    car_states = [car.get_state() for car in cars]
    logger.log(tick_count, car_states)

    if not args.no_gui:
        pygame.display.update()

    tick_count += 1

    # Exit condition for headless runs
    if int(args.max_ticks) > 0 and tick_count >= int(args.max_ticks):
        print(f"Reached max ticks ({args.max_ticks}). Stopping simulation.")
        running = False


# Save + upload logs
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"sim_log_{timestamp}.json"
logger.write_to_file(f"data/{filename}")
upload_file(f"data/{filename}")

if not args.no_gui:
    pygame.quit()

sys.exit()
