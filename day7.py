import math
from vstd import print_matrix, print_tensor_3


def get_input():
    input: list[tuple[str, int]] = []

    with open('day7.txt', 'r') as file:
        for _ in range(10000):
            line = file.readline().split()

            if line == []:
                break

            line[1] = int(line[1])
            input.append((line[0], line[1]))

    return input


def get_amount_str(cards: str, part_two = False):
    if cards == 'JJJJJ': return '5'

    type_list: list[str] = []
    index_dict: dict[str, int] =  {}
    amount_list: list[int] = []
    jokers = 0 # used for part 2

    for card in cards:
        if part_two and card == 'J':
            jokers += 1
        elif card not in type_list:
            type_list.append(card)
            index = len(amount_list)
            index_dict[card] = index
            amount_list.append(0)
            
            amount_list[index_dict[card]] += 1
        else:
            amount_list[index_dict[card]] += 1

    amount_list.sort()

    if part_two and jokers:
        amount_list[len(amount_list)-1] += jokers

    amount_str = ""
    for amount in amount_list:
        amount_str += str(amount)

    return amount_str


def hand_to_strength(hand: tuple[str, int]):
    cards = hand[0]
    SIGN_TO_INT = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 1,
        'Q': 12,
        'K': 13,
        'A': 14,
    }
    strength = 0
    for i in range(len(cards)):
        strength *= 16
        strength += SIGN_TO_INT[cards[i]]

    return strength


def get_sorted_by_type(input: list[tuple[str, int]], part_two = False) -> list[list[tuple[str, int]]]:
    sorted = [[] for _ in range(7)] # five - four - house - three - two pair - one pair - nothing

    amount_str_to_index = {
        '5': 0,
        '14': 1,
        '23': 2,
        '113': 3,
        '122': 4,
        '1112': 5,
        '11111': 6,
    }

    for hand in input:
        amount_list = get_amount_str(hand[0], part_two)
        sorted[amount_str_to_index[amount_list]].append(hand)

    for list in sorted:
        list.sort(key=hand_to_strength, reverse=True)

    return sorted


def get_answer(sorted: list[list[tuple[str, int]]]):
    answer = 0
    combined_list = []
    for list in sorted:
        combined_list += list

    length = len(combined_list)
    for i in range(1, length + 1):
        answer += combined_list[length-i][1] * i

    return answer


def main():
    input = get_input()
    sorted = get_sorted_by_type(input, True)
    answer = get_answer(sorted)

    return answer

print(main())