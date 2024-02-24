import math
import time
import queue
from vstd import *


class Brick:
    def __init__(self, start: Vector3, end: Vector3):
        self.start = start
        self.end = end
        self.xy_cords = self.get_xy_cords()
        self.supporting: list['Brick'] = []
        self.supported_by: list['Brick'] = []


    def get_xy_cords(self):
        xy_cords: list[Vector2] = []
        sx = self.start[0]
        sy = self.start[1]
        ex = self.end[0]
        ey = self.end[1]

        for x in range(sx, ex+1):
            for y in range(sy, ey+1):
                xy_cords.append((x, y))

        return xy_cords
    

    def get_height(self):
        return self.end[2] - self.start[2] + 1
    

    def set_z(self, new_z: int):
        z_diff = self.end[2] - new_z
        self.start = (self.start[0], self.start[1], self.start[2] - z_diff)
        self.end = (self.end[0], self.end[1], self.end[2] - z_diff)

    
    def get_min_z(self):
        return self.start[2]
    

    def get_max_z(self):
        return self.end[2]
    

    def add_supporting(self, brick: 'Brick'):
        self.supporting.append(brick)


    def add_supported_by(self, brick: 'Brick'):
        self.supported_by.append(brick)


    def set_stable(self):
        self.is_stable = len(self.supported_by) >= 2
        

    def is_removable(self):
        if len(self.supporting) == 0:
            return True
        
        removable = True
        for supported_brick in self.supporting:
            if not supported_brick.is_stable:
                removable = False
                break

        return removable

    
    def __repr__(self) -> str:
        return 'Brick: ' + str(self.start) + '-' + str(self.end)


class Pile:
    def __init__(self, low_x: int, low_y: int, high_x: int, high_y: int):
        width = high_x - low_x + 1
        height = high_y - low_y + 1

        bird_wiew: MatrixInt = []
        for _ in range(height):
            row: list[int] = [0 for _ in range(width)]
            bird_wiew.append(row)

        self.bird_wiew = bird_wiew


    def fall_brick(self, brick: Brick):
        xy_cords = brick.xy_cords
        brick_height = brick.get_height()

        landing_z = 0
        for xy_cord in xy_cords:
            x, y = xy_cord
            landing_z = max(landing_z, self.bird_wiew[y][x])

        new_z = landing_z + brick_height

        for xy_cord in xy_cords:
            x, y = xy_cord
            self.bird_wiew[y][x] = new_z

        brick.set_z(new_z)


def get_input():
    bricks: list[Brick] = []
    low_x = low_y = 999999
    high_x = high_y = 0

    with open('day22.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline()

            if line == '':
                break

            line = line.split('~')
            start = line[0].split(',')
            end = line[1].strip().split(',')

            start = tuple(int(i) for i in start)
            end = tuple(int(i) for i in end)

            brick = Brick(start, end)
            bricks.append(brick)

            low_x = min(low_x, start[0])
            low_y = min(low_y, start[1])
            high_x = max(high_x, end[0])
            high_y = max(high_y, end[1])

    pile = Pile(low_x, low_y, high_x, high_y)

    return bricks, pile


def drop_bricks(bricks: list[Brick], pile: Pile):
    for brick in bricks:
        pile.fall_brick(brick)


def get_stable_bricks(bricks: list[Brick]):
    stable_bricks = 0

    z_limit = 0
    for brick in bricks:
        z_limit = max(z_limit, brick.get_min_z())

    for i in range(len(bricks)): # brick under
        for j in range(len(bricks)): # brick over
            if bricks[i].get_max_z() + 1 == bricks[j].get_min_z():
                supported = False
                for xy_cord in bricks[i].xy_cords:
                    if xy_cord in bricks[j].xy_cords:
                        supported = True
                        break
                
                if supported:
                    bricks[i].add_supporting(bricks[j])
                    bricks[j].add_supported_by(bricks[i])

    for brick in bricks:
        brick.set_stable()

    for brick in bricks:
        if brick.is_removable():
            stable_bricks += 1

    return stable_bricks


def get_chain_reaction_fall(bricks: list[Brick]):
    bricks_supports: dict[Vector3, int] = {}
    total_fallen_bricks = 0

    for removed_brick in bricks:
        fallen_bricks = -1
        bricks_to_remove = [removed_brick]

        for brick in bricks:
            bricks_supports[brick.start] = len(brick.supported_by)

        while bricks_to_remove:
            brick_to_remove = bricks_to_remove.pop()

            for distabled_brick in brick_to_remove.supporting:
                bricks_supports[distabled_brick.start] -= 1

                if bricks_supports[distabled_brick.start] == 0:
                    bricks_to_remove.append(distabled_brick)

            fallen_bricks += 1

        total_fallen_bricks += fallen_bricks

    return total_fallen_bricks


def main():
    bricks, pile = get_input()
    bricks.sort(key=lambda x: x.start[2])

    drop_bricks(bricks, pile)

    answer = get_stable_bricks(bricks) # part 1

    answer = get_chain_reaction_fall(bricks) # part 2

    return answer


print(main())