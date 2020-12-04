file = open("day 2/input.txt")

count = 0

for line in file.readlines():
    min_len, max_len, key, password = line.replace("-", " ").replace(":", "").split()

    min_len = int(min_len)
    max_len = int(max_len)

    key_count = password.count(key)

    if min_len <= key_count <= max_len:
        count += 1

print(f"Solution: {count}")