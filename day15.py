import math
import time
from vstd import *


class Lense:
    def __init__(self, label: str, value: int = -1):
        self.label = label
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Lense):
            return self.label == other.label
        else:
            return NotImplemented
        
    def __repr__(self) -> str:
        string = '<'
        string += self.label
        string += ' '
        string += str(self.value)
        string += '>'
        return string
        

class Box:
    def __init__(self, index):
        self.index = index
        self.lenses: list[Lense] = []

    def insert_lense(self, lense: Lense):
        if lense in self.lenses:
            index = self.lenses.index(lense)
            self.lenses[index] = lense
        else:
            self.lenses.append(lense)

    def remove_lense(self, lense: Lense):
        if lense in self.lenses:
            index = self.lenses.index(lense)
            self.lenses.pop(index)

    def get_focusing_power(self):
        foc_pwr = 0

        for i in range(len(self.lenses)):
            foc_pwr += (self.index + 1) * (i + 1) * self.lenses[i].value

        return foc_pwr

    
    def __bool__(self):
        return len(self.lenses) != 0
    
    def __repr__(self):
        string = 'Box ' + str(self.index) + ': ' + str(self.lenses)
        return string


def get_input():
    with open('day15.txt', 'r') as file:
        input = file.read().replace('\n', '').split(',')
        
    return input


def appendix1a(code: str):
    current_value = 0

    for char in code:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    
    return current_value


def get_answer1(input: list[str]):
    answer = 0

    for code in input:
        code_hashed = appendix1a(code)
        print(code_hashed)
        answer += code_hashed

    return answer


def interpret_code(code: str):
    if '=' in code:
        action = 1 # insert lense
        code = code.split('=')
    else:
        action = -1 # remove lense
        code = code.split('-')

    label = code[0]
    if code[1]:
        value = int(code[1])
    else:
        value = -1
    box_index = appendix1a(label)
    
    return label, action, value, box_index


def get_answer2(input: list[str]):
    answer = 0
    boxes = [Box(i) for i in range(256)]

    for code in input:
        label, action, value, box_index = interpret_code(code)
        
        if action == 1: # insert lense
            boxes[box_index].insert_lense(Lense(label, value))
        
        elif action == -1: # remove lense
            boxes[box_index].remove_lense(Lense(label))

    for box in boxes:
        if box:
            foc_pwr = box.get_focusing_power()
            print(foc_pwr)
            answer += foc_pwr

    return answer


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