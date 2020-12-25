def brute_force_loop_size(subject_number, public_key):
    computed_pk = 1
    loop_size = 0
    while computed_pk != public_key:
        computed_pk *= subject_number
        computed_pk %= 20201227
        loop_size += 1
    return loop_size

def transform(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value

card_pk, door_pk = [int(pk) for pk in open("day 25/input.txt").readlines()]

subject_number = 7

card_loop_size = brute_force_loop_size(subject_number, card_pk)
door_loop_size = brute_force_loop_size(subject_number, door_pk)

print(f"Card loop size: {card_loop_size}")
print(f"Door loop size: {door_loop_size}")

encryption_key_1 = transform(door_pk, card_loop_size)
encryption_key_2 = transform(door_pk, card_loop_size)

assert encryption_key_1 == encryption_key_2

print(f"Encryption key: {encryption_key_1}")