import math
import time
from vstd import *


def get_input():
    input: list[str] = []

    with open('day12.txt', 'r') as file:
        for _ in range(100000):
            line = file.readline().split()
            
            if line == []:
                break

            line[1] = line[1].split(',')

            for i in range(len(line[1])):
                line[1][i] = int(line[1][i])

            input.append(line)

    return input


def is_invalid(row: str, broken: list[int]) -> bool:
    brokenI = 0
    broken_len = len(broken)
    current_broke = 0

    for sign in row:
        if sign == '?':
            return False
        elif sign == '#':
            current_broke += 1
        elif current_broke:
            if brokenI == broken_len or current_broke != broken[brokenI]:
                return True
            else:
                current_broke = 0
                brokenI += 1

    return False


def is_valid(row: str, broken: list[int]) -> bool:
    current_broke = 0
    broken_check: list[int] = []

    for sign in row:
        if sign == '#':
            current_broke += 1
        elif current_broke:
            broken_check.append(current_broke)
            current_broke = 0
    
    if current_broke:
        broken_check.append(current_broke)

    return broken_check == broken


def get_permuts(row: str, broken: list[int]):
    if is_invalid(row, broken):
        return 0
    
    if '?' not in row:
        return int(is_valid(row, broken))
    
    permuts = 0
    unknown_index = row.index('?')
    permuts += get_permuts(row[:unknown_index] + '#' + row[unknown_index+1:], broken)
    permuts += get_permuts(row[:unknown_index] + '.' + row[unknown_index+1:], broken)

    return permuts


def get_answer1(input: list[str | list[int]]):
    answer = 0

    for line in input:
        permuts = get_permuts(line[0], line[1])
        answer += permuts

    return answer


def unfold_input(input: list[str | list[int]]):
    for i in range(len(input)):
        new_str = input[i][0]

        for _ in range(4):
            new_str += '?' + input[i][0]

        input[i][0] = new_str
        input[i][1] *= 5
        
    
def main():
    input = get_input()
    print_matrix(input)

    answer = get_answer1(input)
    
    return answer


print(main())