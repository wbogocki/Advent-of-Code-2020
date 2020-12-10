code = [int(n) for n in open("day 9/input.txt").readlines()]

preamble_size = 25


def check(code, preamble_size, index, number):
    for first_index, first_term in enumerate(code[index : index + preamble_size]):
        for second_index, second_term in enumerate(code[index : index + preamble_size]):
            if first_term + second_term == number and first_index != second_index:
                return True
    return False


for index, number in enumerate(code[preamble_size:]):
    valid = check(code, preamble_size, index, number)
    if not valid:
        print(f"First invalid number: {number}")
        break