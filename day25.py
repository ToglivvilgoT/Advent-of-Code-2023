import random
import time
from vstd import *


class Node:
    def __init__(self, name: str):
        self.name = name
        self.connections: list[Node] = []


    def add_connection(self, other: 'Node'):
        self.connections.append(other)

    
    def remove_connection(self, other: 'Node'):
        self.connections.remove(other)


    def merge_nodes(self, other: 'Node'):
        self.name += '-' + other.name

        for node in other.connections:
            node.remove_connection(other)
            if node != self:
                node.add_connection(self)
                self.add_connection(node)
        


    def __repr__(self) -> str:
        name = self.name + ': '
        for child in self.connections:
            name += child.name + ' '
        return name.strip()


def get_input():
    nodes: dict[str, Node] = dict()
    nodes_list: list[Node] = []

    with open('day25.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline()

            if line == '':
                break

            line = line.strip().split(': ')
            node_name = line[0]
            node = nodes.get(node_name)

            if node == None:
                node = Node(node_name)
                nodes_list.append(node)
                nodes[node_name] = node

            for sibling_name in line[1].split():
                sibling = nodes.get(sibling_name)

                if sibling == None:
                    sibling = Node(sibling_name)
                    nodes_list.append(sibling)
                    nodes[sibling_name] = sibling

                node.add_connection(sibling)
                sibling.add_connection(node)

        file.close()

    return nodes_list


def get_unique_list(list: list):
    unique_list = []
    for item in list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def find_groups():
    limit = 1000
    start_time = time.time()

    for i in range(limit):
        nodes: list[Node] = get_input()

        while len(nodes) > 2:
            index1 = random.randrange(0, len(nodes))
            node1 = nodes[index1]

            unique_cons = get_unique_list(node1.connections)
            index2 = random.randrange(0, len(unique_cons))
            node2 = unique_cons[index2]

            node1.merge_nodes(node2)

            nodes.remove(node2)

        if len(node1.connections) == 3:
            break

    print(time.time() - start_time)      
    if i + 1 == limit:
        print(f'Answer not found in {limit} iterations')

    return nodes


def get_answer(groups: list[Node]):
    len1 = len(groups[0].name.split('-'))
    len2 = len(groups[1].name.split('-'))

    return len1 * len2
        

def main():
    nodes = get_input()
    print_list(nodes)
    print(len(nodes))

    groups = find_groups()
    answer = get_answer(groups)

    return answer


print(main())