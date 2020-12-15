def apply_mask(value, mask):
    for bit in range(36):
        if mask[35 - bit] == "1":
            bit_mask = 1 << bit
            value |= bit_mask
        elif mask[35 - bit] == "0":
            bit_mask = (1 << bit) ^ 0b111111111111111111111111111111111111
            value &= bit_mask

    return value


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
        masked_arg = apply_mask(arg, mask)
        print(f"setting mem[{addr}] to {masked_arg} ({bin(masked_arg)})")
        memory[addr] = masked_arg

    else:
        print(f"Unknown operation: {op}")
        exit(1)

memory_sum = sum(memory.values())

print(f"Sum of values in memory: {memory_sum}")