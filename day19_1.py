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
            return self.divert_name
        
        part_value = part.categories[self.category]
        if self.opperation == '<':
            if part_value < self.value:
                return self.divert_name
            else:
                return False
        elif self.opperation == '>':
            if part_value > self.value:
                return self.divert_name
            else:
                return False


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


    def deligate_part(self, part: "Part"):
        for rule in self.rules:
            test_result = rule.test_part(part)
            if test_result:
                return test_result


    def __repr__(self):
        name = self.name + ':\n'
        for i in range(len(self.rules) - 1):
            name += '  ' + str(self.rules[i]) + '\n'
        name += '  ' + str(self.rules[-1])

        return name



class Part:
    ALL_CATEGORIES = ('x', 'm', 'a', 's')

    def __init__(self, part_string: str):
        categories = part_string.split(',')
        self.categories: dict[str, int] = dict()

        for category in categories:
            category = category.split('=')
            self.categories[category[0]] = int(category[1])

        
    def test(self, workflows: dict[str, Workflow]):
        current_workflow_name = 'in'

        for _ in range(10000):
            if current_workflow_name == 'A':
                return True
            elif current_workflow_name == 'R':
                return False
            
            current_workflow = workflows[current_workflow_name]
            current_workflow_name = current_workflow.deligate_part(self)


    def get_sum_rating(self):
        sum = 0
        for category in self.ALL_CATEGORIES:
            sum += self.categories[category]

        return sum


    def __repr__(self):
        name = 'Part: '

        for category in self.ALL_CATEGORIES:
            name += category + ' = ' + str(self.categories[category])
            if category != 's':
                name += ', '

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

        parts = []
        for _ in range(10000):
            line = file.readline()

            if line == '':
                break

            line = line.strip().replace('{', '').replace('}', '')

            part = Part(line)
            parts.append(part)

        return workflows, parts
    


def get_answer(workflows: dict[str, Workflow], parts: list[Part]):
    answer = 0

    for part in parts:
        if part.test(workflows):
            answer += part.get_sum_rating()

    return answer



def main():
    workflows, parts = get_input()

    answer = get_answer(workflows, parts)

    return answer


print(main())