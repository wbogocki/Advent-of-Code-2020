import math


def lcm_of_list(numbers):
    lcm = numbers[0]
    for n in numbers[1:]:
        lcm = math.lcm(lcm, n)
    return lcm


lines = open("day 13/input.txt").readlines()

bus_ids = []
bus_positions = {}
for index, id in enumerate(lines[1].split(",")):
    if id != "x":
        id = int(id)
        bus_ids.append(id)
        bus_positions[id] = index

t = 0
period = 1
bus_count = 1  # how many bus ids repeat at this period

print(lcm_of_list(bus_ids))

while bus_count != len(bus_ids):
    t += period

    # print(f"{t} {period} {bus_count}")

    buses_at_this_t = []
    for bus_id in bus_ids:
        # check if this t is valid for this bus
        if t % bus_id == (bus_id - bus_positions[bus_id]) % bus_id:
            # print(
            #     f"bus {bus_id} reapeats at t {t} plus position {bus_positions[bus_id]}"
            # )
            buses_at_this_t.append(bus_id)

    bus_count_at_this_t = len(buses_at_this_t)
    if bus_count_at_this_t > bus_count:
        bus_count = bus_count_at_this_t
        period = lcm_of_list(buses_at_this_t)

print(f"Solution: {t}")
