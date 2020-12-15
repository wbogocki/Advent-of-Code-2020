import itertools


def apply_mask(value, mask):
    # apply all 1-bits

    for bit in range(36):
        if mask[35 - bit] == "1":
            bit_mask = 1 << bit
            value |= bit_mask

    # apply all x-bits (generate variations)

    x_positions = []
    for index, bit in enumerate(mask):
        if bit == "X":
            x_positions.append(35 - index)

    x_variations = itertools.product([0, 1], repeat=len(x_positions))

    value_variations = []
    for x_variation in x_variations:
        value_variation = value
        for bit, bit_value in zip(x_positions, x_variation):
            if bit_value == 1:
                bit_mask = 1 << bit
                value_variation |= bit_mask
            else:
                bit_mask = (1 << bit) ^ 0b111111111111111111111111111111111111
                value_variation &= bit_mask

        value_variations.append(value_variation)

    return value_variations


program = open("day 14/input.txt").readlines()

mask = None
memory = dict()

for instruction in program:
    op, arg = [it.strip() for it in instruction.split("=")]

    # print(op, arg)

    if op == "mask":
        print(f"setting mask to {arg}")
        mask = arg

    elif op.startswith("mem"):
        arg = int(arg)
        addr = int(op[4:-1])
        for masked_addr in apply_mask(addr, mask):
            print(f"setting mem[{masked_addr}] to {arg}")
            memory[masked_addr] = arg

    else:
        print(f"Unknown operation: {op}")
        exit(1)

memory_sum = sum(memory.values())

print(f"Sum of values in memory: {memory_sum}")