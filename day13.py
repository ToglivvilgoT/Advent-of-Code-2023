import math
import time
from vstd import *


def get_input():
    input: list[list[str]] = []
    map: list[str] = []

    with open('day13.txt', 'r') as file:
        for _ in range(100000):
            line = file.readline()

            if line == '\n':
                input.append(map)
                map = []
                continue

            if line == '':
                break

            line = line.strip()
            map.append(line)

    if map:
        input.append(map)

    return input


def get_mirror_lines(map: list[str]):
    mirror_lines = [i for i in range(len(map[0]) - 1)]
            
    for row in map:
        mini = 0
        maxi = len(row)-1

        for ml_index in range(len(mirror_lines) - 1, -1, -1):
            left = mirror_lines[ml_index]
            right = mirror_lines[ml_index] + 1
            
            mirrored = True
            while mini <= left and right <= maxi:
                if row[left] == row[right]:
                    left -= 1
                    right += 1
                else:
                    mirrored = False
                    break

            if not mirrored:
                mirror_lines.pop(ml_index)

    return mirror_lines


def get_answer1(input: list[list[str]]):
    answer = 0

    for map in input:
        for multiply in range(1, 101, 99):
            mirror_lines = get_mirror_lines(map)
                
            if mirror_lines:
                answer += (mirror_lines[0] + 1) * multiply

            map = get_matrix_transposed(map)

    return answer


def get_answer2(input: MatrixStr):
    answer = 0
    original_mls: Tensor3Int = []

    for map in input:
        original_ml = []

        for i in range(2):
            mirror_lines = get_mirror_lines(map)
            
            if mirror_lines:
                original_ml.append(mirror_lines[0])
            else:
                original_ml.append(None)

            map = get_matrix_transposed(map)

        original_mls.append(original_ml)

    for map_index in range(len(input)):
        all_mirror_lines = [[], []]
        map = input[map_index]

        for smudge_y in range(len(map)):
            for smudge_x in range(len(map[0])):
                sign = '#' if map[smudge_y][smudge_x] == '.' else '.'
                map[smudge_y] = map[smudge_y][:smudge_x] + sign + map[smudge_y][smudge_x + 1:]

                for i in range(2):
                    mirror_lines = get_mirror_lines(map)
                    for mirror_line in mirror_lines:
                        if mirror_line not in all_mirror_lines[i]:
                            all_mirror_lines[i].append(mirror_line)
                    
                    map = get_matrix_transposed(map)

                sign = '#' if map[smudge_y][smudge_x] == '.' else '.'
                map[smudge_y] = map[smudge_y][:smudge_x] + sign + map[smudge_y][smudge_x + 1:]

        print(all_mirror_lines)

        for potential_line in all_mirror_lines[0]:
            if potential_line != original_mls[map_index][0]:
                answer += potential_line + 1

        for potential_line in all_mirror_lines[1]:
            if potential_line != original_mls[map_index][1]:
                answer += (potential_line + 1) * 100

    return answer
                


def main():
    input = get_input()
    print_tensor_3(input)

    answer = get_answer1(input)
    
    answer = get_answer2(input)

    return answer


print(main())