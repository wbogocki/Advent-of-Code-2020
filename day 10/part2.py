joltages = [int(j) for j in open("day 10/input.txt").readlines()]

joltages.append(0)  # socket
joltages.append(max(joltages) + 3)  # device

joltages.sort()

differences = []

for j1, j2 in zip(joltages, joltages[1:]):
    differences.append(j2 - j1)

combinations = 1


def combine(seq_len):
    # can't change anything
    if seq_len == 0:
        return 1
    if seq_len == 1:
        return 1

    # 1 1 => 2
    if seq_len == 2:
        return 2

    # 1 1 1 => 1 2 | 2 1 | 3
    if seq_len == 3:
        return 4

    # 1 1 1 1 => 1 1 2 | 1 2 1 | 2 1 1 | 2 2 | 3 1 | 1 3
    if seq_len == 4:
        return 7

    raise Exception("Unimplemented seq_len")


seq_len = 0
for d in differences:
    if d == 1:
        seq_len += 1
    else:
        combinations *= combine(seq_len)
        seq_len = 0

print(f"Number of combinations: {combinations}")
