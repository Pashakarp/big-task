import os
import sys
import pygame
import requests
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((600, 450))

def draw():
    map_request = ('https://static-maps.yandex.ru/1.x/?l=sat&ll=' + coords_1 + '%2C-' + coords_2 + '&z=' + str(m))
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))


response = None
coords_1 = '140'
coords_2 = '39'
m = 3
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                m += 1
            elif event.key == pygame.K_PAGEDOWN:
                m -= 1
    draw()
    pygame.display.update()
    pygame.display.flip()
pygame.quit()

os.remove(map_file)