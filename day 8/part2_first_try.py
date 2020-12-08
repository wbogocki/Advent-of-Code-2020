program = open("day 8/input.txt").readlines()


def find_jmp_to_skip():
    ip = 0
    acc = 0

    history = set()

    jmp_to_skip = []

    while ip < len(program):
        instr = program[ip].rstrip()

        print(f"{instr.ljust(8)} | {acc}")

        history.add(ip)

        op, arg = instr.split()
        arg = int(arg)

        if op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            if ip + arg in history:
                print(f"Ignoring jmp operation at index {ip}")
                jmp_to_skip.append(ip)
                ip += 1
            else:
                last_jmp = ip
                ip += arg
        elif op == "nop":
            ip += 1
        else:
            print(f"Invalid operation: {op}")
            exit(1)

    return jmp_to_skip


def find_nop_that_skips_jmp(jmp_ip):
    ip = 0
    acc = 0

    nop_that_skip_jmp = set()

    while ip < len(program) and ip != jmp_ip:
        instr = program[ip].rstrip()

        print(f"{instr.ljust(8)} | {acc}")

        op, arg = instr.split()
        arg = int(arg)

        if op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            last_jmp = ip
            ip += arg
        elif op == "nop":
            if ip + arg > jmp_ip:
                nop_that_skip_jmp.add(ip)
            ip += 1
        else:
            print(f"Invalid operation: {op}")
            exit(1)

    return nop_that_skip_jmp


jmp_to_skip = find_jmp_to_skip()
nop_to_skip = find_nop_that_skips_jmp(jmp_to_skip[0])

print(jmp_to_skip)
print(nop_to_skip)
