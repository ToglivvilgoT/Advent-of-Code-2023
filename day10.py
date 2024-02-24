import math
from vstd import *


def get_input():
    input: list[str] = []

    with open('day10.txt', 'r') as file:
        for i in range(10000):
            line = file.readline().strip()
            if line == '':
                break

            input.append(line)

            for j in range(len(line)):
                if line[j] == 'S':
                    start = [j, i]

    return input, start


def get_first_pipe(GET_PIPE_DIRECTIONS, start, pipe_map):
    for incomming_dir in GET_PIPE_DIRECTIONS['S']:   # loop through eventual starting points aka next pipe:
        cords = list_add(start, incomming_dir)
        neg_incomming_dir = negative_list(incomming_dir)
        next_pipe_dirs = GET_PIPE_DIRECTIONS[pipe_map[cords[1]][cords[0]]]

        if next_pipe_dirs != None and neg_incomming_dir in next_pipe_dirs:   # if start is connected to pipe
            return list_add(start, incomming_dir), incomming_dir


def get_path(pipe_map: list[str], start: list[int]):
    GET_PIPE_DIRECTIONS: dict[str, MatrixInt | None] = {
        'S': [[0, -1], [-1, 0], [1, 0], [0, 1]],
        'F': [[1, 0], [0, 1]],
        '7': [[-1, 0], [0, 1]],
        'J': [[0, -1], [-1, 0]],
        'L': [[0, -1], [1, 0]],
        '-': [[-1, 0], [1, 0]],
        '|': [[0, -1], [0, 1]],
        '.': None
    }

    curr_pipe_cords: list[int]
    incoming_dir: list[int]
    curr_pipe_cords, incoming_dir = get_first_pipe(GET_PIPE_DIRECTIONS, start, pipe_map)
    
    path: list[list[int]] = [start, curr_pipe_cords]

    for _ in range(2, 1000000):
        # where are we going?:
        for curr_pipe_direction in GET_PIPE_DIRECTIONS[pipe_map[curr_pipe_cords[1]][curr_pipe_cords[0]]]:
            if curr_pipe_direction != negative_list(incoming_dir):
                break
        
        # move to next tile
        curr_pipe_cords = list_add(curr_pipe_cords, curr_pipe_direction)
        incoming_dir = curr_pipe_direction

        #check if loop:
        if pipe_map[curr_pipe_cords[1]][curr_pipe_cords[0]] == 'S':
            return path
        
        path.append(curr_pipe_cords)


def replace_s(pipe_map: list[str], start: list[int]):
    connected_dirs = []
    UP_ALLOW = ['|', 'F', '7']
    LEFT_ALLOW = ['-', 'F', 'L']
    RIGHT_ALLOW = ['-', 'J', '7']
    DOWN_ALLOW = ['|', 'J', 'L']
    ALLOWS = [UP_ALLOW, LEFT_ALLOW, RIGHT_ALLOW, DOWN_ALLOW]
    OFFSETS = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    for i in range(4):
        x, y = OFFSETS[i]
        if pipe_map[start[1]+y][start[0]+x] in ALLOWS[i]:
            connected_dirs.append(True)
        else:
            connected_dirs.append(False)

    match connected_dirs:
        case [True, True, False, False]:
            sign = 'J'
        case [True, False, True, False]:
            sign = 'L'
        case [True, False, False, True]:
            sign = '|'
        case [False, True, True, False]:
            sign = '-'
        case [False, True, False, True]:
            sign = '7'
        case [False, False, True, True]:
            sign = 'F'

    pipe_map[start[1]] = pipe_map[start[1]][:start[0]] + sign + pipe_map[start[1]][start[0]+1:]


def get_area(pipe_map: list[str], path: list[list[int]]):
    answer = 0

    for i in range(len(pipe_map)):
        inside = False
        for j in range(len(pipe_map[i])):
            curr_sign = pipe_map[i][j]
            curr_cords = [j, i]

            if curr_cords in path:
                if curr_sign == '|':
                    inside = not inside
                elif curr_sign == 'L' or curr_sign == 'F':
                    entry_point = curr_sign
                elif curr_sign == '7' or curr_sign == 'J':
                    if (entry_point == 'L' and curr_sign == '7') or (entry_point == 'F' and curr_sign == 'J'):
                        inside = not inside

            elif inside:
                pipe_map[i] = pipe_map[i][:j] + 'I' + pipe_map[i][j+1:]
                answer += 1

    print_matrix(pipe_map)
    return answer

def main():
    pipe_map, start = get_input()
    print_matrix(pipe_map)
    path = get_path(pipe_map, start)
    answer1 = len(path) // 2
    replace_s(pipe_map, start)
    answer2 = get_area(pipe_map, path)

    return answer2


print(main())