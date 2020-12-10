def check(code, preamble_size, index, number):
    for first_index, first_term in enumerate(code[index : index + preamble_size]):
        for second_index, second_term in enumerate(code[index : index + preamble_size]):
            if first_term + second_term == number and first_index != second_index:
                return True
    return False


def find_first_number(code, preamble_size):
    for index, number in enumerate(code[preamble_size:]):
        if not check(code, preamble_size, index, number):
            return index, number


def find_contiguous_set(code, preamble_size, first_number):
    for first_index, first_term in enumerate(code):
        terms = []
        terms_sum = 0
        for term_index, term in enumerate(code[first_index:]):
            terms.append(term)
            terms_sum += term
            if terms_sum == first_number:
                return terms


code = [int(n) for n in open("day 9/input.txt").readlines()]
preamble_size = 25

_, first_number = find_first_number(code, preamble_size)

print(first_number)

contiguous_set = find_contiguous_set(code, preamble_size, first_number)

print(contiguous_set)

encryption_weakness = min(contiguous_set) + max(contiguous_set)

print(f"Encryption weakness: {encryption_weakness}")