import math

Vector2 = tuple[int, int]
Vector3 = tuple[int, int, int]

MatrixInt = list[list[int]]
MatrixStr = list[list[str]]

Tensor3Int = list[list[list[int]]]
Tensor3Str = list[list[list[str]]]


def print_list(list: list, indent = 1):
    indent_str = ' ' * indent
    first_indent_str = ' ' * (indent - 1) + '['

    print(first_indent_str, end='')

    if len(list) == 0:
        print(']')

    elif len(list) == 1:
        print(list[0], ']', sep='')
    
    else:
        print(list[0], ',', sep='')
        
        for i in range(1, len(list)-1):
            print(indent_str, list[i], ',', sep='')

        print(indent_str, list[-1], ']', sep='')


def print_matrix(matrix: list):
    if matrix:
        first = 0
        last = len(matrix)-1

        for i in range(len(matrix)):
            if i == first:
                print("[", end="")
            else:
                print(" ", end="")

            print(str(matrix[i]), end="")

            if i == last:
                print("]\n")
            else:
                print(",")

    else:
        print(" []")


def print_tensor_3(tensor: list):
    if tensor:
        firstM = 0
        lastM = len(tensor)-1

        for j in range(len(tensor)):
            matrix = tensor[j]

            if j == firstM:
                print("[", end="")
            else:
                print(" ", end="")

            if matrix:
                first = 0
                last = len(matrix)-1

                for i in range(len(matrix)):
                    if i == first:
                        print("[", end="")
                    else:
                        print("  ", end="")

                    print(str(matrix[i]), end="")

                    if i == last:
                        print("]", end="")
                    else:
                        print(",")

            else:
                print(" []")

            if j == lastM:
                print("]")
            else:
                print(",\n")

    else:
        print(" []")


def dot_prod(vec1, vec2):
    if len(vec1) == len(vec2):
        scalar = 0
        for i in range(len(vec1)):
            scalar += vec1[i] * vec2[i]
        
        return scalar
    
    raise ValueError('Vectors must have the same length')


def list_add(list1: list, list2: list):
    added_list = []

    for i in range(min(len(list1), len(list2))):
        added_list.append(list1[i] + list2[i])

    return added_list


def negative_list(list: list):
    negated_list = []

    for i in range(len(list)):
        negated_list.append(-list[i])

    return negated_list


def get_matrix_transposed(matrix: list):
    if all(isinstance(row, str) for row in matrix):
        new_matrix = ['' for _ in range(len(matrix[0]))]
        
        for row in matrix:
            for i in range(len(row)):
                new_matrix[i] += row[i]

    else:
        raise TypeError('Type Not Supported')

    return new_matrix


def get_matrix_flipped(matrix: list, flipp_axis: str = 'y'):
    if isinstance(matrix[0], str):
        _type = str
    elif isinstance(matrix[0], list):
        _type = list
    else:
        raise TypeError('Type Not Supproted')

    if flipp_axis == 'x':
        matrix = get_matrix_transposed(matrix)

    for i in range(len(matrix)):
        row = matrix[i]

        if _type == list:
            new_row = []

            for j in range(len(row) - 1, -1, -1):
                new_row.append(row[j])

        elif _type == str:
            new_row = ''

            for j in range(len(row) - 1, -1, -1):
                new_row += row[j]

        matrix[i] = new_row
    
    if flipp_axis == 'x':
        matrix = get_matrix_transposed(matrix)

    return matrix