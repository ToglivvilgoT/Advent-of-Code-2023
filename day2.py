import math

def main():
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    list_index = {
        "red": 0,
        "green": 1,
        "blue": 2,
    }
    
    with open("day2.txt", "r") as input:
        answer = 0

        for index in range(100):
            input_list = input.readline().replace(",", " ,").replace(";", " ;").split()[2:]
            biggest = [0, 0, 0]

            for i in range(0, math.ceil(len(input_list)), 3):
                amount = int(input_list[i])
                color = input_list[i+1]

                if biggest[list_index[color]] < amount:
                    biggest[list_index[color]] = amount

            power = biggest[0] * biggest[1] * biggest[2]
            answer += power

        return answer

print(main())