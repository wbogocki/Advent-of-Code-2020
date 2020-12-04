file = open("day 2/input.txt")

count = 0

for line in file.readlines():
    first_pos, second_pos, key, password = (
        line.replace("-", " ").replace(":", "").split()
    )

    first_pos = int(first_pos) - 1
    second_pos = int(second_pos) - 1

    if (password[first_pos] == key) ^ (password[second_pos] == key):
        count += 1

print(f"Solution: {count}")