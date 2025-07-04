import pygame
import sys
import os
import random
from car import Car
from intersection import Intersection
from logger import Logger
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cloud.upload_logs import upload_file


# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

logger = Logger()
pygame.display.set_caption("Traffic Sim")
cars = []

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRASS_GREEN = (34, 139, 34)
ROAD_GRAY = (50, 50, 50)

clock = pygame.time.Clock()
FPS = 60

# Define intersection box
intersection = Intersection(x=350, y=250, width=100, height=100)

tick_count = 0
# next_spawn = random.randint(90, 150)  # Random initial spawn time for the first car
next_spawn = 1500  # Start with no cars, will spawn on first tick


running = True
while running:
    clock.tick(FPS)
    WIN.fill(GRASS_GREEN)

    # Draw horizontal road
    pygame.draw.rect(WIN, ROAD_GRAY, pygame.Rect(0, 250, WIDTH, 100))  # horizontal strip

    # Draw vertical road
    pygame.draw.rect(WIN, ROAD_GRAY, pygame.Rect(350, 0, 100, HEIGHT))  # vertical strip

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


    # Draw intersection
    intersection.draw(WIN)


    if tick_count % next_spawn == 0:
        new_car = Car(x=0, y=310, speed=random.randint(2, 7), direction="right", turn_direction=random.choice([None, "left", "right"]), color=RED)
        cars.append(new_car)
        new_car = Car(x=360, y=0, speed=random.randint(2, 7), direction="down", turn_direction=random.choice([None, "left", "right"]), color=GREEN)
        cars.append(new_car)
        new_car = Car(x=WIDTH, y=260, speed=random.randint(2, 7), direction="left", turn_direction=random.choice([None, "left", "right"]), color=BLUE)
        cars.append(new_car)
        new_car = Car(x=410, y=HEIGHT, speed=random.randint(2, 7), direction="up", turn_direction=random.choice([None, "left", "right"]), color=ORANGE)
        cars.append(new_car)
        next_spawn = tick_count +random.randint(50, 150)  # Reset spawn timer


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    intersection.update()  # Update intersection state

    for car in cars:
        if car.should_stop(intersection, cars):
            car.increment_wait()
        else:
            car.move()
        car.draw(WIN)
        print(car.get_state())  # Print car state for debugging

    cars = [car for car in cars if car.x < WIDTH and car.y < HEIGHT]  # Filter cars within bounds

    # Log car states
    car_states = [car.get_state() for car in cars]
    logger.log(tick_count, car_states)

    pygame.display.update()
    tick_count += 1

# timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# filename = f"sim_log_{timestamp}.json"
# logger.write_to_file(f"data/{filename}")

# upload_file(f"data/{filename}")

pygame.quit()
sys.exit()
