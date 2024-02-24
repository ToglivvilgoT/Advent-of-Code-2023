import math
from vstd import *


class Hail:
    def __init__(self, x: int, y: int, z: int, xv: int, yv: int, zv: int):
        self.x = x
        self.y = y
        self.z = z
        self.xv = xv
        self.yv = yv
        self.zv = zv


    def is_parallel_xy(self, other: 'Hail'):
        if self.xv / other.xv == self.yv / other.yv:
            return True
        else:
            return False
        

    def get_intersection(self, other: 'Hail'):
        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y
        vx1, vy1 = self.xv, self.yv
        vx2, vy2 = other.xv, other.yv

        term1 = vy2 * (x1 - x2)
        term2 = vx2 * (y1 - y2)
        divisor = vy1 * vx2 - vx1 * vy2
        
        time_self = (term1 - term2) / divisor
        time_other = (y1 - y2 + vy1 * time_self) / vy2

        coll_point_x = x1 + vx1 * time_self
        coll_point_y = y1 + vy1 * time_self
        coll_point = (coll_point_x, coll_point_y)

        return coll_point, time_self, time_other


    def __repr__(self) -> str:
        name = 'Hail: '
        name += str((self.x, self.y)) + ' '
        name += str((self.xv, self.yv))
        return name


def get_input():
    hails: list[Hail] = []

    with open('day24.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline()

            if line == '':
                break
            
            line = line.strip().split(' @ ')
            pos, vel = line[0], line[1]
            pos = pos.split(', ')
            vel = vel.split(', ')

            for i in range(3):
                pos[i] = int(pos[i])
                vel[i] = int(vel[i])

            hail = Hail(*pos, *vel)
            hails.append(hail)

    return hails


def get_collisions(hails: list[Hail], low_bound = 200000000000000, high_bound = 400000000000000):
    collisions = 0

    for i in range(len(hails)):
        for j in range(i + 1, len(hails)):
            hail1, hail2 = hails[i], hails[j]

            if hail1.is_parallel_xy(hail2):
                continue

            position, time1, time2 = hail1.get_intersection(hail2)
            x, y = position

            if not (low_bound <= x <= high_bound and low_bound <= y <= high_bound):
                continue

            elif min(time1, time2) <= 0:
                continue

            else:
                collisions += 1

    return collisions


def main():
    hails = get_input()
    print_list(hails)

    collisions = get_collisions(hails)

    return collisions


print(main())