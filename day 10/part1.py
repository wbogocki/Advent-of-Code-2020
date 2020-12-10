joltages = [int(j) for j in open("day 10/input.txt").readlines()]

joltages.sort()

differences = {
    1: 0,
    2: 0,
    3: 0,
}

differences[joltages[0]] = 1  # socket to first adapter
differences[3] = 1  # last adapter to device

for j1, j2 in zip(joltages, joltages[1:]):
    diff = j2 - j1
    differences[diff] += 1

solution = differences[1] * differences[3]

print(f"Solution: {solution}")