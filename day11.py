import math
from vstd import *


def get_input():
    input: list[str] = []

    with open('day11.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline().strip()

            if line == '':
                break
            
            input.append(line)

    return input


def universe_expand(input: list[str], part_2):
    new_universe = []
    column_length = len(input)
    row_length = len(input[0])

    # for part 2:
    expanded_rows, expanded_columns = [], []
    expanded: list[list[int]] = [expanded_rows, expanded_columns]

    # Expand all rows to be twize as thicc
    for i in range(column_length):
        empty = True

        for sign in input[i]:
            if sign == '#':
                empty = False
                break

        if empty:
            if not part_2:
                new_universe.append('.' * row_length)
            else:
                expanded_rows.append(i)
        
        new_universe.append(input[i])

    
    # Expand all columns to be twize as thicc
    input = new_universe
    column_length = len(input)
    new_universe = ['' for _ in range(column_length)]

    for i in range(row_length):
        empty = True

        for j in range(column_length):
            if input[j][i] == '#':
                empty = False
                break

        if empty:
            if not part_2:
                for j in range(column_length):
                    new_universe[j] += '.'
            else:
                expanded_columns.append(i)

        for j in range(column_length):
            new_universe[j] += input[j][i]


    return new_universe, expanded


def get_stars(universe: list[str]):
    stars: list[tuple[int, int]] = []

    for y in range(len(universe)):
        for x in range(len(universe[y])):
            if universe[y][x] == '#':
                stars.append((x, y))

    return stars


def get_star_distances(stars: list[tuple[int, int]]):
    answer = 0

    for i in range(len(stars)):
        for j in range(i+1, len(stars)):
            dx = abs(stars[i][0] - stars[j][0])
            dy = abs(stars[i][1] - stars[j][1])
            distance = dx + dy
            answer += distance

    return answer


def get_star_distances_2(stars: list[tuple[int, int]], expanded: list[list[int]], times_larger: int = 1000000):
    expansion_amount = times_larger - 1
    answer = 0

    for i in range(len(stars)):
        for j in range(i+1, len(stars)):
            min_x = min(stars[i][0], stars[j][0])
            min_y = min(stars[i][1], stars[j][1])
            max_x = max(stars[i][0], stars[j][0])
            max_y = max(stars[i][1], stars[j][1])

            dx = max_x - min_x
            dy = max_y - min_y
            
            answer += dx
            answer += dy

            for expanded_row in expanded[0]:
                if min_y < expanded_row < max_y:
                    answer += expansion_amount

            for expanded_column in expanded[1]:
                if min_x < expanded_column < max_x:
                    answer += expansion_amount

    return answer


def main():
    input = get_input()
    print_matrix(input)

    expanded_universe, expanded = universe_expand(input, True)
    print_matrix(expanded_universe)

    stars = get_stars(expanded_universe)

    answer1 = get_star_distances(stars)
    answer2 = get_star_distances_2(stars, expanded)

    return answer2


print(main())