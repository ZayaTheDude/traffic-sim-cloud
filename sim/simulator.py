import pygame
import sys
from car import Car
from intersection import Intersection

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Sim")
cars = []

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60

# Create a car instance
car = Car(x=0, y=300, speed=5, direction="right")
cars.append(car)

# Define intersection box
intersection = Intersection(x=350, y=250)

running = True
while running:
    clock.tick(FPS)
    WIN.fill(WHITE)
    intersection.draw(WIN)  # Draw the intersection each frame


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for car in cars:
        car.move()
        car.draw(WIN)
        print(car.get_state())  # Print car state for debugging

    cars = [car for car in cars if car.x < WIDTH and car.y < HEIGHT]  # Filter cars within bounds

    pygame.display.update()

pygame.quit()
sys.exit()
