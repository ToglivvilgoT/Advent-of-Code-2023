import math
import time
import pygame
from palette import *
from queue import Queue
from vstd import *


input: list[Vector2] = []

DIRS = {
    'R': (1, 0),
    'U': (0, -1),
    'L': (-1, 0),
    'D': (0, 1),
}



def read_input():
    with open('day18.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline().split()

            if line == []:
                break

            dir_x, dir_y = DIRS[line[0]]
            steps = int(line[1])

            input.append(((dir_x, dir_y), steps))


def get_bounds():
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    curr_x = 0
    curr_y = 0

    for move in input:
        dx, dy = move[0]

        curr_x += dx * move[1]
        curr_y += dy * move[1]

        min_x = min(min_x, curr_x)
        max_x = max(max_x, curr_x)
        min_y = min(min_y, curr_y)
        max_y = max(max_y, curr_y)

    border_x = max_x - min_x + 1
    border_y = max_y - min_y + 1

    start_x = -min_x
    start_y = -min_y

    return (border_x, border_y), (start_x, start_y)


def draw_path(size: Vector2, start_point: Vector2):
    map: MatrixStr = []
    for y in range(size[1]):
        row = []
        for x in range(size[0]):
            row.append('.')
        map.append(row)

    curr_x, curr_y = start_point
    
    for move in input:
        dir, steps = move
        dx, dy = dir

        for _ in range(steps):
            curr_x += dx
            curr_y += dy
            map[curr_y][curr_x] = '#'

    return map


def flood_fill(path, start_point):
    OFFSETS = {(1, 0), (0, -1), (-1, 0), (0, 1)}
    queue = Queue()
    queue.put_nowait(start_point)

    while not queue.empty():
        x, y = queue.get_nowait()
        if path[y][x] == '.':
            path[y][x] = '#'
            
            for offset in OFFSETS:
                queue.put_nowait((x + offset[0], y + offset[1]))

    return path


def get_answer(path: MatrixStr):
    answer = 0

    for row in path:
        for sign in row:
            if sign == '#':
                answer += 1

    return answer


def draw(path, WIN):
    for y in range(len(path)):
        for x in range(len(path[y])):
            rect = pygame.Rect(x*2, y * 2, 2, 2)

            if path[y][x] == '.':
                color = BLUE_2
            else:
                color = MONO_2

            pygame.draw.rect(WIN, color, rect)
    
    pygame.display.update()


def main():
    read_input()

    bounds, start_point = get_bounds()

    path = draw_path(bounds, start_point)

    WIN = pygame.display.set_mode((bounds[0] * 2, bounds[1] * 2))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                run = False

        draw(path, WIN)

    start_y = 1
    start_x = 0
    while path[start_y][start_x] == '.':
        start_x += 1
    while path[start_y][start_x] == '#':
        start_x += 1

    path = flood_fill(path, (start_x, start_y))

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                run = False

        draw(path, WIN)

    answer = get_answer(path)

    return answer


print(main())