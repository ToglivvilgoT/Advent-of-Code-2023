import math
import time
from queue import PriorityQueue
from types import NoneType
from vstd import *


distances: MatrixInt


class Path:
    def __init__(self, x: int, y: int, direction: Vector2, straight_moves: int, visited_cords: set[Vector2], heat_loss: int):
        self.x = x
        self.y = y
        self.direction = direction
        self.straight_moves = straight_moves
        self.visited_cords = visited_cords
        self.heat_loss = heat_loss

    def out_of_bounds(self, x, y):
        x_min = 0
        x_max = len(input[0])
        y_min = 0
        y_max = len(input)
        
        return not (x_min <= x < x_max and y_min <= y < y_max)

    def move_forward(self):
        x = self.x + self.direction[0]
        y = self.y + self.direction[1]

        if self.out_of_bounds(x, y):
            return None
        
        if (x, y) in self.visited_cords:
            return None
        
        direction = self.direction
        straight_moves = self.straight_moves + 1
        visited_cords = self.visited_cords.copy()
        visited_cords.add((x, y))
        heat_loss = self.heat_loss + int(input[y][x])

        return Path(x, y, direction, straight_moves, visited_cords, heat_loss)

    
    def compare(self, other, opperation: str):
        if isinstance(other, Path):
            self_compare_val = self.heat_loss + distances[self.y][self.x]
            other_compare_val = other.heat_loss + distances[other.y][other.x]

            match opperation:
                case '==':
                    return self_compare_val == other_compare_val
                case '!=':
                    return self_compare_val != other_compare_val
                case '<':
                    return self_compare_val < other_compare_val
                case '<=':
                    return self_compare_val <= other_compare_val
                case '>=':
                    return self_compare_val >= other_compare_val
                case '>':
                    return self_compare_val > other_compare_val
        else:
            return NotImplemented
    
    def __eq__(self, other):
        return self.compare(other, '==')        
        
    def __ne__(self, other):
        return self.compare(other, '!=')

    def __lt__(self, other):
        return self.compare(other, '<')

    def __le__(self, other):
        return self.compare(other, '<=')

    def __ge__(self, other):
        return self.compare(other, '>=')

    def __gt__(self, other):
        return self.compare(other, '>')
    

    def __repr__(self):
        string = 'Path: '

        string += 'Position (' + str(self.x) + ',' + str(self.y) + '), '

        string += 'Direction '
        match self.direction:
            case (1, 0):
                string += 'right'
            case (0, -1):
                string += 'up'
            case (-1, 0):
                string += 'left'
            case (0, 1):
                string += 'down'
        string += ', '

        string += 'Straight Moves ' + str(self.straight_moves) + ', '

        string += 'Heat Loss ' + str(self.heat_loss) + '.'

        return string


input: list[str] = []

def read_input():
    with open('day17.txt', 'r') as file:
        for _ in range(1000):
            line = file.readline().strip()

            if line == '':
                break

            input.append(line)

    return input

def out_of_bounds(x_min, x_max, y_min, y_max, x, y):
    return not (x_min <= x < x_max and y_min <= y < y_max)


def generate_distances():
    x_min = 0
    y_min = 0
    x_max = len(input[0])
    y_max = len(input)

    global distances
    distances = [[x_max * y_max * 10 for _ in range(x_max)] for _ in range(y_max)]
    distances[y_max - 1][x_max - 1] = 0

    queue = PriorityQueue()
    queue.put((0, x_max - 1, y_max - 1)) # add endpoint to queue, distance to end for that point is 0

    OFFSETS = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    while not queue.qsize() == 0:
        distance, x, y = queue.get_nowait()

        for offset in OFFSETS:
            new_x = x + offset[0]
            new_y = y + offset[1]
            if out_of_bounds(x_min, x_max, y_min, y_max, new_x, new_y):
                continue

            new_distance = distance + int(input[new_y][new_x])
            if new_distance < distances[new_y][new_x]:
                distances[new_y][new_x] = new_distance
                queue.put((new_distance, new_x, new_y))


def get_vt_index(direction: Vector2, straight_moves: int, max_steps):
    DIR_TO_INT = {
        (1, 0): 0,
        (0, -1): 1,
        (-1, 0): 2,
        (0, 1): 3,
    }
    index = DIR_TO_INT[direction] * max_steps + straight_moves - 1
    return index


def get_answer(min_steps = 0, max_steps = 3):
    DIRS: dict[str, Vector2] = {
        'right': (1, 0),
        'up': (0, -1),
        'left': (-1, 0),
        'down': (0, 1),
    }

    TURNS: dict[Vector2, tuple[Vector2, Vector2]] = {
        DIRS['right']: (DIRS['up'], DIRS['down']),
        DIRS['up']: (DIRS['left'], DIRS['right']),
        DIRS['left']: (DIRS['up'], DIRS['down']),
        DIRS['down']: (DIRS['left'], DIRS['right']),
    }


    max_val = len(input) * len(input[0]) * 10
    visited_tiles = []
    for y in range(len(input)):
        row = []
        for x in range(len(input[y])):
            tile = []
            for index in range(max_steps * 4):
                tile.append(max_val)
            row.append(tile)
        visited_tiles.append(row)

    queue = PriorityQueue()
    
    queue.put(Path(0, 0, DIRS['right'], 0, {(0, 0)}, 0))
    queue.put(Path(0, 0, DIRS['down'], 0, {(0, 0)}, 0))

    for i in range(1000000):
        path: Path = queue.get_nowait()

        if path.x == len(input[0]) - 1 and path.y == len(input) - 1:
            if path.straight_moves >= min_steps:
                return str(path.heat_loss) + ' Path was Found in ' + str(i) + ' loops'
        
        if path.straight_moves < max_steps:
            new_path = path.move_forward()

            if new_path != None:
                index = get_vt_index(new_path.direction, new_path.straight_moves, max_steps)
                new_heat_loss = new_path.heat_loss

                if new_heat_loss < visited_tiles[new_path.y][new_path.x][index]:
                    visited_tiles[new_path.y][new_path.x][index] = new_heat_loss
                    queue.put(new_path)

        if path.straight_moves >= min_steps:
            path.straight_moves = 0
            for dir in TURNS[path.direction]:
                path.direction = dir
                new_path = path.move_forward()

                if new_path != None:
                    index = get_vt_index(new_path.direction, new_path.straight_moves, max_steps)
                    new_heat_loss = new_path.heat_loss
                    
                    if new_heat_loss < visited_tiles[new_path.y][new_path.x][index]:
                        visited_tiles[new_path.y][new_path.x][index] = new_heat_loss
                        queue.put(new_path)

    return str(path.heat_loss + distances[path.y][path.x]) + ' Path was NOT Found :( ' + str(path.heat_loss)


def main():
    read_input()
    print_matrix(input)

    generate_distances()

    answer = get_answer(4, 10)

    return answer


print(main())