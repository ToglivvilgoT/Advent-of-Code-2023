import math
import time
import queue
from vstd import *


class Connection:
    DIRS = {(1, 0), (0, -1), (-1, 0), (0, 1)}
    BACKTRACK: dict[Vector2, Vector2] = {
        (1, 0): (-1, 0),
        (0, -1): (0, 1),
        (-1, 0): (1, 0),
        (0, 1): (0, -1),
    }
    ARROWS = {
        '>',
        '^',
        '<',
        'v',
    }

    def __init__(self, origin: Vector2, direction: Vector2):
        self.origin = origin
        self.direction = direction

    def resolve(self, input: list[str], start_point: Vector2, end_point: Vector2):
        x, y = self.origin
        dx, dy = self.direction
        x += dx
        y += dy
        self.length = 1

        for _ in range(10000):

            for dir in self.DIRS:
                if dir == self.BACKTRACK[self.direction]:
                    continue

                new_x = x + dir[0]
                new_y = y + dir[1]

                if input[new_y][new_x] == '#':
                    continue

                x, y = new_x, new_y
                self.direction = dir
                self.length += 1
                break

            if input[y][x] in self.ARROWS:
                x += self.direction[0]
                y += self.direction[1]
                self.length += 1
                self.end_point = (x, y)
                break
            
            elif (x, y) == end_point or (x, y) == start_point:
                self.end_point = (x, y)
                break


class Node:
    def __init__(self, position: Vector2):
        self.position = position
        self.connections: list[tuple[int, Node]] = []


    def add_connection(self, length: int, node: 'Node'):
        self.connections.append((length, node))


def get_input():
    input: list[str] = []
    with open('day23.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline()
            
            if line == '':
                break

            input.append(line.strip())

        file.close()

    start = (1, 0)
    end = (len(input[0])-2, len(input)-1)

    return input, start, end


def generate_graph(input: list[str], start: Vector2, end: Vector2):
    DIRS = {(1, 0), (0, -1), (-1, 0), (0, 1)}

    start_node = Node(start)
    start_con = Connection(start, (0, 1))
    end_node = Node(end)
    
    unres_cons = [start_con]
    nodes = {start: start_node, end: end_node}

    while unres_cons:
        con = unres_cons.pop()
        con.resolve(input, start, end)

        if not con.end_point in nodes:
            new_node = Node(con.end_point)
            nodes[new_node.position] = new_node

            for dir in DIRS:
                x = con.end_point[0] + dir[0]
                y = con.end_point[1] + dir[1]

                if input[y][x] != '#':
                    unres_cons.append(Connection(new_node.position, dir))
 
        origin_node = nodes[con.origin]
        destin_node = nodes[con.end_point]
        origin_node.add_connection(con.length, destin_node)

    return start_node, end_node


def get_longest_path(node: Node, end_node: Node, visited_nodes: set[Node] = set()):
    if node == end_node:
        return 0
    
    longest = 0

    for connection in node.connections:
        if connection[1] in visited_nodes:
            continue
        
        new_visited = visited_nodes.copy()
        new_visited.add(node)

        length = get_longest_path(connection[1], end_node, new_visited)
        if length == 'Invalid':
            continue

        longest = max(longest, connection[0] + length)

    if longest != 0:
        return longest
    
    return 'Invalid'



def main():
    input, start, end = get_input()
    print_matrix(input)

    start_node, end_node = generate_graph(input, start, end)

    answer = get_longest_path(start_node, end_node)

    return answer


print(main())