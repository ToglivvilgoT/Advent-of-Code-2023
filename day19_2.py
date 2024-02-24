import math
import time
from typing import Any
from vstd import *


class Rule:
    def __init__(self, rule_string: str):
        if ':' in rule_string:
            self.type = 'if'
            self.category = rule_string[0]
            self.opperation = rule_string[1]

            rule_string = rule_string[2:]
            rule_string = rule_string.split(':')

            self.value = int(rule_string[0])
            self.divert_name = rule_string[1]
        else:
            self.type = 'else'

            self.divert_name = rule_string


    def test_part(self, part: "Part"):
        if self.type == 'else':
            return ((part, self.divert_name),)
        
        part_value_low = part.categories['low_' + self.category]
        part_value_high = part.categories['high_' + self.category]

        if self.opperation == '<':
            if part_value_high < self.value:
                return ((part, self.divert_name),)
            elif part_value_low >= self.value:
                return ((part, False),)
            else:
                new_part_1 = part.copy()
                new_part_1.categories['high_' + self.category] = self.value - 1
                new_part_2 = part.copy()
                new_part_2.categories['low_' + self.category] = self.value

                return (new_part_1, self.divert_name), (new_part_2, False)


        elif self.opperation == '>':
            if part_value_low > self.value:
                return ((part, self.divert_name),)
            elif part_value_high <= self.value:
                return ((part, False),)
            else:
                new_part_1 = part.copy()
                new_part_1.categories['high_' + self.category] = self.value
                new_part_2 = part.copy()
                new_part_2.categories['low_' + self.category] = self.value + 1

                return (new_part_1, False), (new_part_2, self.divert_name)

        


    def __repr__(self):
        name = 'Rule: '
        if self.type == 'if':
            name += 'if ' + self.category + self.opperation + str(self.value) + ': '
        else:
            name += 'else: '
        name += self.divert_name
        return name



class Workflow:
    def __init__(self, name: str, rules: list[Rule]):
        self.name = name
        self.rules = rules


    def test_part(self, part: "Part"):
        return_parts: list[tuple['Part', str]] = []

        for rule in self.rules:
            tested_parts = rule.test_part(part)
            
            for tested_part in tested_parts:
                if not tested_part[1]:
                    part = tested_part[0]
                else:
                    return_parts.append(tested_part)

        print(return_parts)
        return return_parts


    def __repr__(self):
        name = self.name + ':\n'
        for i in range(len(self.rules) - 1):
            name += '  ' + str(self.rules[i]) + '\n'
        name += '  ' + str(self.rules[-1])

        return name



class Part:
    def __init__(self, lx: int, lm: int, la: int, ls: int, hx: int, hm: int, ha: int, hs: int):
        self.categories: dict[str, int] = dict()

        self.categories['low_x'] = lx
        self.categories['low_m'] = lm
        self.categories['low_a'] = la
        self.categories['low_s'] = ls
        self.categories['high_x'] = hx
        self.categories['high_m'] = hm
        self.categories['high_a'] = ha
        self.categories['high_s'] = hs


    def copy(self):
        new_part = Part(
            self.categories['low_x'],
            self.categories['low_m'],
            self.categories['low_a'],
            self.categories['low_s'],
            self.categories['high_x'],
            self.categories['high_m'],
            self.categories['high_a'],
            self.categories['high_s'],)
        return new_part
    

    def get_value(self):
        dx = self.categories['high_x'] - self.categories['low_x'] + 1
        dm = self.categories['high_m'] - self.categories['low_m'] + 1
        da = self.categories['high_a'] - self.categories['low_a'] + 1
        ds = self.categories['high_s'] - self.categories['low_s'] + 1
        return dx * dm * da * ds


    def __repr__(self):
        name = 'Part:\n'
        name += '  x: ' + str(self.categories['low_x']) + '-' + str(self.categories['high_x']) + '\n'
        name += '  m: ' + str(self.categories['low_m']) + '-' + str(self.categories['high_m']) + '\n'
        name += '  a: ' + str(self.categories['low_a']) + '-' + str(self.categories['high_a']) + '\n'
        name += '  s: ' + str(self.categories['low_s']) + '-' + str(self.categories['high_s'])
        return name


def get_input():
    with open('day19.txt', 'r') as file:
        workflows: dict[str, Workflow] = dict()

        for _ in range(10000):
            line = file.readline()

            if line == '\n':
                break

            split_line = line.split('{')
            name = split_line[0]
            split_line[1] = split_line[1].removesuffix('}\n')
            rule_strings = split_line[1].split(',')

            rules = []
            for rule_string in rule_strings:
                rules.append(Rule(rule_string))

            workflow = Workflow(name, rules)

            workflows[name] = workflow

        return workflows
    


def get_answer(workflows: dict[str, Workflow]):
    answer = 0
    parts: list[tuple[Part, Workflow]] = []
    parts.append((Part(1, 1, 1, 1, 4000, 4000, 4000, 4000), workflows['in']))

    while parts:
        part, workflow = parts.pop()
        new_parts = workflow.test_part(part)

        for new_part in new_parts:
            if new_part[1] == 'A':
                answer += new_part[0].get_value()
            elif new_part[1] == 'R':
                pass
            else:
                parts.append((new_part[0], workflows[new_part[1]]))

    return answer



def main():
    workflows = get_input()

    answer = get_answer(workflows)

    return answer


print(main())