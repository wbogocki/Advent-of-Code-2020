file = open("day 1/input.txt")

expenses = [int(line) for line in file.readlines()]


def search(expenses):
    for first_num in expenses:
        for second_num in expenses:
            if first_num != second_num and first_num + second_num == 2020:
                return first_num, second_num
    return None, None


first_num, second_num = search(expenses)

print(f"First number: {first_num}")
print(f"Second number: {second_num}")

solution = first_num * second_num

print(f"Solution: {solution}")