import math
import time
from vstd import *


def get_input():
    input: list[str] = []

    with open('day16.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline().strip()

            if line == '':
                break

            input.append(line)

    return input


def hash_light(x: int, y: int, direction: Vector2, input: list[str]):
    DIR_TO_INT: dict[Vector2, int] = {
        (1, 0): 0,
        (0, -1): 1,
        (-1, 0): 2,
        (0, 1): 3,
    }

    width_mult = 4
    height_mult = len(input[0]) * 4

    hash_val = y * height_mult + x * width_mult + DIR_TO_INT[direction]
    return hash_val


def hash_ignore_direction(hash_val):
    hash_val //= 4
    return hash_val
    


def out_of_bounds(x: int, y: int, input: list[str]):
    x_min = 0
    y_min = 0
    x_max = len(input[0]) - 1
    y_max = len(input) - 1

    return not (x_min <= x <= x_max and y_min <= y <= y_max)


def track_light_beam(input: list[str], direction: Vector2, x: int, y: int, DIRECTIONS: dict[str, Vector2], MIRRORING: dict[tuple[Vector2, str], list[Vector2]], light_has_passed: set[int]):
    for _ in range(1000):
        hashed_light = hash_light(x, y, direction, input)

        if hashed_light in light_has_passed: # check if duplicate:
            return
        
        light_has_passed.add(hashed_light)

        x += direction[0]
        y += direction[1]

        if out_of_bounds(x, y, input):
            return

        sign = input[y][x]
        if sign != '.':
            new_dirs = MIRRORING[(direction, sign)]
            for new_dir in new_dirs:
                track_light_beam(input, new_dir, x, y, DIRECTIONS, MIRRORING, light_has_passed)
            return


def get_answer1(input: list[str], start_x = 0, start_y = 0, start_dir = (1, 0)):
    light_has_passed: set[int] = set()

    DIRECTIONS: dict[str, Vector2] = {
        'right': (1, 0),
        'up': (0, -1),
        'left': (-1, 0),
        'down': (0, 1),
    }
    D = DIRECTIONS
    
    # key = (incomming direction, mirror) and value = list of outgoing direction(s)
    MIRRORING: dict[tuple[Vector2, str], list[Vector2]] = {
        (D['right'], '/'): [D['up']],
        (D['up'], '/'): [D['right']],
        (D['left'], '/'): [D['down']],
        (D['down'], '/'): [D['left']],

        (D['right'], '\\'): [D['down']],
        (D['up'], '\\'): [D['left']],
        (D['left'], '\\'): [D['up']],
        (D['down'], '\\'): [D['right']],

        (D['right'], '-'): [D['right']],
        (D['up'], '-'): [D['left'], D['right']],
        (D['left'], '-'): [D['left']],
        (D['down'], '-'): [D['left'], D['right']],

        (D['right'], '|'): [D['up'], D['down']],
        (D['up'], '|'): [D['up']],
        (D['left'], '|'): [D['up'], D['down']],
        (D['down'], '|'): [D['down']],
    }

    sign = input[start_y][start_x]
    if sign != '.':
        new_dirs = MIRRORING[(start_dir, sign)]
        for new_dir in new_dirs:
            track_light_beam(input, new_dir, start_x, start_y, DIRECTIONS, MIRRORING, light_has_passed)
    else:
        track_light_beam(input, start_dir, start_x, start_y, DIRECTIONS, MIRRORING, light_has_passed)

    energized = set()
    
    for hash_val in light_has_passed:
        energized.add(hash_ignore_direction(hash_val))

    return len(energized)


def get_answer2(input: list[str]):
    all_energized_vals: list = []

    for start_x in range(len(input[0])):
        all_energized_vals.append(get_answer1(input, start_x, 0, (0, 1)))
        all_energized_vals.append(get_answer1(input, start_x, len(input)-1, (0, -1)))

    for start_y in range(len(input)):
        all_energized_vals.append(get_answer1(input, 0, start_y, (1, 0)))
        all_energized_vals.append(get_answer1(input, len(input[0])-1, start_y, (-1, 0)))
    
    all_energized_vals.sort(reverse=True)
    return all_energized_vals[0]


def main():
    part = 2

    input = get_input()
    print_matrix(input)

    if part == 1:
        answer = get_answer1(input)
    
    elif part == 2:
        answer = get_answer2(input)

    return answer


print(main())