import math


def get_input() -> list[list[str]]:
    with open("day3.txt", "r") as input:
        inputM = [] # input matrix

        for _ in range(140):
            lineL = [] # line list
            line = input.readline().replace("\n", "")
            
            if line == None:
                break

            for i in range(len(line)):
                lineL.append(line[i])

            inputM.append(lineL)

        return inputM


def is_digit(sign: str) -> bool:
    LOW_LIMIT = ord("0")
    HIGH_LIMIT = ord("9")

    if LOW_LIMIT <= ord(sign) <= HIGH_LIMIT:
        return True
    else:
        return False
    

def is_symbol(sign: str) -> bool:
    DOT = ord(".")

    if ord(sign) != DOT and not is_digit(sign):
        return True
    else:
        return False


def get_valid_digits(matrix: list[list[str]]) -> list[list[bool | None]]:
    validM = [] # valid matrix

    for y in range(len(matrix)):
        validRow = []
        for x in range(len(matrix[y])):

            if not is_digit(matrix[y][x]):
                validRow.append(None)
            else:
                valid = False
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        try:
                            if is_symbol(matrix[y+dy][x+dx]):
                                valid = True
                        except IndexError:
                            pass
                
                validRow.append(valid)

        validM.append(validRow)

    return validM

def get_answer(signs: list[list[str]], valid: list[list[bool]]) -> int:
    answer = 0

    for y in range(len(signs)):
        x = 0
        while x < len(signs[y]):
            
            if valid[y][x] != None: # if it is a digit
                str_number = signs[y][x] # string version of number
                numb_valid = valid[y][x] # is the number valid (has symbol next to it)

                for _ in range(100): # loop through next signs and add them to the number if they are digits, also check if valid.
                    x += 1
                    try:
                        if valid[y][x] != None:
                            str_number += signs[y][x]

                            if valid[y][x]:
                                numb_valid = True
                        else:
                            break

                    except IndexError:
                        break

                if numb_valid:
                    answer += int(str_number)

            x += 1
    
    return answer

def is_astrix(sign: str) -> bool:
    ASTRIX = ord("*")
    if ord(sign) == ASTRIX:
        return True
    else:
        return False
    
def get_number(matrix, x, y):
    str_numb = matrix[y][x]

    #check for digits to the left
    for dx in range(-1, -140, -1):
        try:
            if is_digit(matrix[y][x+dx]):
                str_numb = matrix[y][x+dx] + str_numb
            else:
                break
        except IndexError:
            break

    #check for digits to the right
    for dx in range(1, 140):
        try:
            if is_digit(matrix[y][x+dx]):
                str_numb += matrix[y][x+dx]
            else:
                break
        except IndexError:
            break

    return int(str_numb)

def get_answer_2(matrix: list[list[str]]) -> int:
    answer = 0

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if is_astrix(matrix[y][x]):
                numbers = []

                for dy in range(-1, 2):
                    dx = -1
                    while dx < 2:
                        try:
                            if is_digit(matrix[y+dy][x+dx]):
                                numbers.append(get_number(matrix, x+dx, y+dy))
                                
                                # if next sign is a digit, skip to next row (makes sure a number is detected only once even if it has multiple
                                # digits in range)
                                try:
                                    if is_digit(matrix[y+dy][x+dx+1]):
                                        break
                                except IndexError:
                                    break

                            dx += 1

                        except IndexError:
                            break
                
                if len(numbers) == 2:
                    answer += numbers[0] * numbers[1]

    return answer


def main():
    input = get_input()
  #part 1
    valid_list = get_valid_digits(input)
    answer = get_answer(input, valid_list)
  #part 2
    answer = get_answer_2(input)
    return answer

print("\n\n\n\n\n")
print(main())