import math
import vstd


def get_input() -> list[tuple[int, int]]:
    with open('day6.txt', 'r') as file:
        time = file.readline().split()[1:]
        distance = file.readline().split()[1:]

        races = []
        for i in range(len(time)):
            races.append((int(time[i]), int(distance[i])))

        return races
    

def get_margins(races: list[tuple[int, int]]):
    margins: list[int] = []

    for race in races:
        time, distance = race

        root = ((time / 2)**2 - distance)**0.5
        lower = math.floor(time / 2 - root)+1
        higher = math.ceil(time / 2 + root)-1

        margins.append(higher - lower + 1)

    return margins


def get_answer(margins: list[int]):
    answer = 1
    for margin in margins:
        answer *= margin

    return answer


def get_input_2():
    with open('day6.txt', 'r') as file:
        time = int(file.readline()[10:].replace(' ', ''))
        distance = int(file.readline()[10:].replace(' ', ''))

        return time, distance
    

def main():
  # part 1
    races = get_input()
    margins = get_margins(races)
    answer = get_answer(margins)

  # part 2
    race = get_input_2()
    margin = get_margins([race])
    answer = get_answer(margin)
    
    return answer

print(main())