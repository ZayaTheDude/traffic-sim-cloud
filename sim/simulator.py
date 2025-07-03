import pygame
import sys
import random
from car import Car
from intersection import Intersection
from logger import Logger

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

clock = pygame.time.Clock()
FPS = 60

# Define intersection box
intersection = Intersection(x=350, y=250)

tick_count = 0
next_spawn = random.randint(90, 150)  # Random initial spawn time for the first car

running = True
while running:
    clock.tick(FPS)
    WIN.fill(WHITE)
    intersection.draw(WIN)  # Draw the intersection each frame


    if tick_count % next_spawn == 0:
        new_car = Car(x=0, y=300, speed=5, direction="right")
        cars.append(new_car)
        next_spawn = tick_count +random.randint(50, 150)  # Reset spawn timer


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for car in cars:
        car.move()
        car.draw(WIN)
        print(car.get_state())  # Print car state for debugging

    cars = [car for car in cars if car.x < WIDTH and car.y < HEIGHT]  # Filter cars within bounds

    # Log car states
    car_states = [car.get_state() for car in cars]
    logger.log(tick_count, car_states)

    pygame.display.update()
    tick_count += 1

logger.write_to_file()
pygame.quit()
sys.exit()
