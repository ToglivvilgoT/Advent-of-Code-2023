import math
import time
import queue
from vstd import *


def get_input():
    input: list[str] = []

    with open('day21.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline()

            if line == '':
                break

            input.append(line.strip())

    return input


def get_start_point(input: list[str]):
    for i in range(len(input)):
        if 'S' in input[i]:
            start_x = input[i].index('S')

            return start_x, i
        

def move_step(input: list[str], reach_points: set[Vector2]):
    DIRS = {(1, 0), (0, -1), (-1, 0), (0, 1)}
    low_x = 0
    low_y = 0
    high_x = len(input[0])
    high_y = len(input)

    new_reach_points: set[Vector2] = set()

    for point in reach_points:
        x, y = point

        for dir in DIRS:
            dx, dy = dir

            new_x = x + dx
            new_y = y + dy

            if low_x <= new_x < high_x and low_y <= new_y < high_y and input[new_y][new_x] != '#':
                new_reach_points.add((new_x, new_y))

    return new_reach_points
            
        

def get_garden_plot_reach(input: list[str], start_point: Vector2, steps: int):
    reach_points = {start_point}

    for _ in range(steps):
        reach_points = move_step(input, reach_points)

    return reach_points


def print_reach_points(input: list[str], reach_points: set[Vector2]):
    for y in range(len(input)):
        for x in range(len(input[y])):
            if (x, y) in reach_points:
                print('O', end='')
            else:
                print(input[y][x], end='')
        print()



def main():
    input = get_input()
    print_matrix(input)

    start_point = get_start_point(input)

    steps = 64
    reach_points = get_garden_plot_reach(input, start_point, steps)
    print_reach_points(input, reach_points)

    return len(reach_points)



print(main())