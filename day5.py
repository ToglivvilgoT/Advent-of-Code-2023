import math
import vstd


class ValRange:
    def __init__(self, low_bound: int, high_bound: int):
        self.low_bound: int = low_bound
        self.high_bound: int = high_bound
    
    def __repr__(self):
        return "(" + str(self.low_bound) + "-" + str(self.high_bound) + ")"

    def is_overlaping(self, other: 'ValRange'):
        if self.low_bound <= other.high_bound and self.high_bound >= other.low_bound:
            return True
        else:
            return False
        
    def merge(self, other: 'ValRange'):
        low = min(self.low_bound, other.low_bound)
        high = max(self.high_bound, other.high_bound)
        return ValRange(low, high)
    
    def get_intersection(self, other: 'ValRange') -> tuple['ValRange', list['ValRange']]:
        lower = other.low_bound < self.low_bound
        higher = other.high_bound > self.high_bound

        match (lower, higher):
            case (True, True):
                new_low_1 = other.low_bound
                new_high_1 = self.low_bound-1
                new_low_2 = self.high_bound+1
                new_high_2 = other.high_bound

                return (self, [ValRange(new_low_1, new_high_1), ValRange(new_low_2, new_high_2)])
            
            case (True, False):
                new_low_1 = self.low_bound
                new_high_1 = other.high_bound
                new_low_2 = other.low_bound
                new_high_2 = self.low_bound-1

                return (ValRange(new_low_1, new_high_1), [ValRange(new_low_2, new_high_2)])
            
            case (False, True):
                new_low_1 = other.low_bound
                new_high_1 = self.high_bound
                new_low_2 = self.high_bound+1
                new_high_2 = other.high_bound

                return (ValRange(new_low_1, new_high_1), [ValRange(new_low_2, new_high_2)])
            
            case (False, False):
                return (other, [])


def get_input() -> tuple[list[int], vstd.Tensor3Int]:
    maps: vstd.Tensor3Int = [[],[],[],[],[],[],[]]

    with open("day5.txt", "r") as file:
        seeds = file.readline().split()[1:]

        for i in range(len(seeds)):
            seeds[i] = int(seeds[i])

        file.readline()
        file.readline()
        map_type = 0

        for i in range(300):
            line = file.readline()

            if line == "":
                break

            if line == "\n":
                map_type += 1
                file.readline() # disgard next line (discard the header of map)
                continue

            line = line.split()

            for i in range(len(line)):
                line[i] = int(line[i])

            maps[map_type].append(line)

    return (seeds, maps)


def get_maped_seeds(seeds: list[int], maps: list[list[list[int]]]) -> list[int]:
    maped = []

    for seed in seeds:
        prev_val = seed

        for map in maps:

            for line in map:

                # check if prev_val is in range and if so convert and break
                if line[1] <= prev_val < line[1] + line[2]:
                    prev_val = line[0] + (prev_val - line[1])
                    break

        maped.append(prev_val)
    return maped


def get_maped_seeds_2(seeds: list[int], maps: list[list[list[int]]]):
    seedsR: list[ValRange] = []
    mapsR: list[list[tuple[ValRange, int]]] = []

    for i in range(0, len(seeds), 2):
        seedsR.append(ValRange(seeds[i], seeds[i] + seeds[i+1] - 1))

    for map in maps:
        map_vals: list[tuple[ValRange, int]] = []

        for line in map:
            r = ValRange(line[1], line[1] + line[2] - 1)
            diff = line[0] - line[1]
            map_vals.append((r, diff))

        mapsR.append(map_vals)


    curr_vals = seedsR

    for map in mapsR:
        next_vals: list[ValRange] = []

        for line in map:
            remove_list = []

            for i in range(len(curr_vals)):
                if line[0].is_overlaping(curr_vals[i]):
                    intsec, leftovers = line[0].get_intersection(curr_vals[i])
                    next_vals.append(ValRange(intsec.low_bound+line[1], intsec.high_bound+line[1]))

                    for leftover in leftovers:
                        curr_vals.append(leftover)

                    remove_list.append(curr_vals[i])

            for item in remove_list:
                curr_vals.remove(item)

        curr_vals += next_vals
        next_vals = []

    return curr_vals

def main():
    seeds, maps = get_input()
  # part 1
    maped = get_maped_seeds(seeds, maps)
    maped.sort()
    lowest = maped[0]

  #part 2
    maped = get_maped_seeds_2(seeds, maps)
    maped.sort(key=lambda x: x.low_bound)
    lowest = maped[0].low_bound

    return lowest

print(main())