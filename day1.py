import math

#digit represents the amount of letters in the numbers (digits_3 = digits with 3 letters)
digits_3 = ["one", "two", "six"]
digits_4 = ["four", "five", "nine"]
digits_5 = ["three", "seven", "eight"]

str_to_int = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def get_int_list(line: str) -> list[str]:
    min = ord("1")
    max = ord("9")
    ints = []
    len = line.__len__()
    for i in range(len):
      #check if it is an integer (1, 2 or 3 etc.)
        ord_char = ord(line[i])
        if ord_char >= min and ord_char <= max:
            ints.append(line[i])

      #check if it is a string integer (one, two, three etc.)
        if i <= len-5:
            if line[i:i+5] in digits_5:
                ints.append(str_to_int[line[i:i+5]])
        if i <= len-4:
            if line[i:i+4] in digits_4:
                ints.append(str_to_int[line[i:i+4]])
        if i <= len-3:
            if line[i:i+3] in digits_3:
                ints.append(str_to_int[line[i:i+3]])

    return ints

def get_final_number(ints: list[str]) -> int:
    str_numb = ints[0] + ints.pop()
    return int(str_numb)

def main():
    numbers = []
    with open("day1.txt", "r") as input:
        for _ in range(1000):
            line = input.readline()
            if line == None:
                break

            ints = get_int_list(line)
            numb = get_final_number(ints)

            numbers.append(numb)

    sum = 0    
    for numb in numbers:
        sum += numb

    return sum

print(main())