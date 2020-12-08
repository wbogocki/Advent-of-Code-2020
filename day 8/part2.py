program = open("day 8/input.txt").readlines()


def check(bad_instr_ip=None):
    ip = 0
    acc = 0

    history = set()

    while ip < len(program):
        instr = program[ip].rstrip()

        # print(f"{instr.ljust(8)} | {acc}")

        if ip in history:
            return None

        history.add(ip)

        op, arg = instr.split()
        arg = int(arg)

        if ip == bad_instr_ip:
            if op == "jmp":
                op = "nop"
            elif op == "nop":
                op = "jmp"
            else:
                print(f"Invalid operation at bad_instr_ip: {op}")
                exit(1)

        if op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            last_jmp = ip
            ip += arg
        elif op == "nop":
            ip += 1
        else:
            print(f"Invalid operation: {op}")
            exit(1)

    return acc


for ip, instr in enumerate(program):
    op, _ = instr.split()
    if op == "jmp" or op == "nop":
        acc = check(ip)
        if acc:
            print(f"Solution: {acc}")
            break
