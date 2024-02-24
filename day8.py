import math
import time
from vstd import *


def get_input():
    maps = {}
    starts = []

    with open('day8.txt', 'r') as file:
        right_left = file.readline().rstrip()
        file.readline()

        for _ in range(10000):
            line = file.readline()

            if line == '':
                break

            line = line.translate({ord(i): None for i in '=(),'})
            line = line.split()
            
            if line[0][2] == 'A':
                starts.append(line[0])

            maps[line[0]] = (line[1], line[2])

    return starts, right_left, maps


def get_steps(input):
    starts: list[str]
    instruct: str
    maps: dict[str, tuple[str, str]]

    starts, instruct, maps = input
    instruct_len = len(instruct)

    instruct_to_index = {'L': 0, 'R': 1}

    for steps in range(10000000):
        end = True
        for i in range(len(starts)):
            if starts[i][2] != 'Z':
                end = False
                break
        
        if end:
            return steps
        
        curr_instruct = instruct_to_index[instruct[steps%instruct_len]]
        for i in range(len(starts)):
            starts[i] = maps[starts[i]][curr_instruct]

    return 'No path found in 10.000.000 steps'


def get_cycles(input: list[list[str] | str | dict[str, tuple[str, str]]]):
    starts: list[str]
    instruct: str
    maps: dict[str, tuple[str, str]]
    starts, instruct, maps = input
    
    instruct_len = len(instruct)

    instruct_to_index = {'L': 0, 'R': 1}

    cycles: list[int] = []

    for start in starts:
        for step in range(100000):
            current_instruct_index = step % instruct_len
            # if it reaches goal:
            if start[2] == 'Z':
                cycles.append(step)
                break

            start = maps[start][instruct_to_index[instruct[current_instruct_index]]]

    return cycles


def get_prime_numbers():
    primes = []

    for i in range(2, 1000):
        is_prime = True

        for prime in primes:
            if i % prime == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(i)

    return primes

def get_lcm(cycles: list[int]):
    primes = get_prime_numbers()
    answer = 1

    for prime in primes:
        active_cycles = [i for i in cycles]

        for _ in range(100):
            for i in range(len(active_cycles)-1, -1, -1):
                if active_cycles[i] % prime == 0:
                    active_cycles[i] /= prime
                else:
                    active_cycles.pop(i)
            
            if active_cycles:
                answer *= prime
                print(prime)
            else:
                break

    return answer
        


def main():
    input = get_input()
    #steps = get_steps(input)
    cycles = get_cycles(input)
    answer = get_lcm(cycles)

    return answer


print(main())