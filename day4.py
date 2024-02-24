import math


def get_input() -> list[list[list[str]]]:
    with open("day4.txt", "r") as input:
        inputM = [] # input matrix

        for _ in range(200):
            line = input.readline().split()
            
            if line == []:
                break
                    
            cards = [[], []]
            
            cards_index = 0
            for sign in line[2:]:
                if sign == "|":
                    cards_index = 1

                else:
                    cards[cards_index].append(sign)

            inputM.append(cards)

        return inputM
    

def get_matches(input: list[list[list[str]]]) -> list[int]:
    answer = []

    for line in input:
        correctL, my_cardsL = line[0], line[1]
        matches = 0

        for my_card in my_cardsL:
            guess_correct = False

            for correct in correctL:
                if my_card == correct:
                    guess_correct = True
                    break

            if guess_correct:
                matches += 1

        answer.append(matches)

    return answer


def get_answer(amountL: list[int]) -> int:
    answer = 0

    for amount in amountL:
        if amount:
            score = 1
            amount -= 1

            while amount:
                score *= 2
                amount -= 1

            answer += score

    return answer


def get_answer_2(matchesL: list[int]) -> int:
    answer = 0
    cards: list[int] = []
    
    for _ in range(len(matchesL)):
        cards.append(1)

    for i in range(len(cards)):
        amount = cards[i]

        for j in range(1, matchesL[i] + 1):
            cards[i+j] += amount

        answer += amount

    return answer


def main():
    input = get_input()
    matches = get_matches(input)
  # part 1:
    answer = get_answer(matches)
  # part 2:
    answer = get_answer_2(matches)
    return answer

print(main())