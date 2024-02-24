import math
import time
from vstd import *


def get_input():
    input = []

    with open('day14.txt', 'r') as file:
        for _ in range(1000):
            line = file.readline()

            if line == '':
                break

            line = line.strip()
            input.append(line)

    return input


def get_load(row: str) -> int:
    total_load = 0
    max_load = len(row)
    current_load = max_load

    for i in range(len(row)):
        if row[i] == 'O':
            total_load += current_load
            current_load -= 1

        elif row[i] == '#':
            current_load = max_load - i - 1

    return total_load


def get_answer1(input: list[str]) -> int:
    answer = 0

    for row in input:
        answer += get_load(row)

    return answer


def roll_stones(input: list[str]):
    for i in range(len(input)):
        row = input[i]
        new_row = ''
        current_os = 0
        current_dots = 0

        for sign in row:
            if sign == 'O':
                current_os += 1
            
            elif sign == '.':
                current_dots += 1

            elif sign == '#':
                new_row += 'O' * current_os + '.' * current_dots + '#'
                current_dots = 0
                current_os = 0

        new_row += 'O' * current_os + '.' * current_dots

        input[i] = new_row


def cycle(input: list[str]):
    for _ in range(2):
        for _ in range(2):
            input = get_matrix_transposed(input)
            roll_stones(input)
        
        input = get_matrix_flipped(input, 'x')
        input = get_matrix_flipped(input, 'y')

    return input


def get_load2(input: list[str]) -> int:
    input = get_matrix_transposed(input)
    answer = 0
    max_load = len(input[0])

    for row in input:
        for i in range(len(row)):
            if row[i] == 'O':
                answer += max_load - i

    return answer


def get_answer2(input: list[str]):
    prev_inputs: list[list[str]] = []

    for current_cycle in range(1, 1000):
        input = cycle(input)

        if input in prev_inputs:
            cycle_length = current_cycle - prev_inputs.index(input) - 1
            break
        else:
            prev_inputs.append(input)

    for power in range(8, -1, -1):
        for _ in range(10):
            step = cycle_length * 10**power

            if current_cycle + step <= 10**9:
                current_cycle += step 
            else:
                break

    rest = 10**9 - current_cycle

    for _ in range(rest):
        input = cycle(input)

    print_matrix(input)

    return get_load2(input)
        


def main():
    part = 2

    input = get_input()
    
    if part == 1:
        input = get_matrix_transposed(input)
        print_matrix(input)
        answer = get_answer1(input)

    elif part == 2:
        print_matrix(input)
        answer = get_answer2(input)

    return answer


print(main())    