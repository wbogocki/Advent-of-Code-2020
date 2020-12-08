program = open("day 8/input.txt").readlines()

ip = 0
acc = 0

history = set()

while True:
    instr = program[ip].rstrip()

    print(f"{instr.ljust(8)} | {acc}")

    if ip in history:
        print("Instruction would run for the 2nd time")
        print(f"Solution: {acc}")
        exit(0)

    history.add(ip)

    op, arg = instr.split()
    arg = int(arg)

    if op == "acc":
        acc += arg
        ip += 1
    elif op == "jmp":
        ip += arg
    elif op == "nop":
        ip += 1
    else:
        print(f"Invalid operation: {op}")
        exit(1)
