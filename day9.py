import math
from vstd import *


def get_input():
    with open('day9.txt', 'r') as file:
        input = []

        for _ in range(10000):
            line = file.readline().split()

            if line == []:
                break

            for i in range(len(line)):
                line[i] = int(line[i])

            input.append(line)

        return input
    

def get_differance_list(val_list: list[int]):
    diffs = []
    
    for i in range(1, len(val_list)):
        diffs.append(val_list[i] - val_list[i-1])

    return diffs
    

def get_answer(datasets: MatrixInt):
    answer = 0

    for dataset in datasets:   # loop through all datasets
        diffs_list = [dataset]

        for _ in range(1000):   # while True:
            diff = get_differance_list(diffs_list[-1])   # get differance list
            diffs_list.append(diff)   # append differance list

            all_zero = True
            for numb in diff:   # check if all zero, break or continue
                if numb != 0: 
                    all_zero = False
                    break

            if all_zero:
                break
        

        diffs_list[-1].append(0)

        for i in range(-2, -len(diffs_list)-1, -1):   # what is next value, recursion/loop
            diffs_list[i].append(diffs_list[i][-1]+diffs_list[i+1][-1])
        
        answer += diffs_list[0][-1]   # add next value to answer

    return answer


def reverse_input(input: MatrixInt):
    for row in input:
        row.reverse()
    

def main():
    input = get_input()
    reverse_input(input) # part 2   
    answer = get_answer(input)

    return answer


print(main())