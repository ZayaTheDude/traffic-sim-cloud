import pygame
import sys

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Sim")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60

car_x = 0
car_y = 290
car_speed = 5

# Define intersection box
intersection = pygame.Rect(370, 270, 60, 60)

running = True
while running:
    clock.tick(FPS)
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car_x += car_speed
    if car_x > WIDTH:
        car_x = -60  # loop back

    pygame.draw.rect(WIN, GREEN, intersection, 2)
    pygame.draw.rect(WIN, RED, (car_x, car_y, 60, 30))

    pygame.display.update()

pygame.quit()
sys.exit()
