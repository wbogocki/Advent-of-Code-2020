lines = open("day 13/input.txt").readlines()

earliest_time = int(lines[0])
bus_ids = []
for id in lines[1].split(","):
    if id != "x":
        bus_ids.append(int(id))

bus_arrivals = []
for id in bus_ids:
    arrival_time = earliest_time - (earliest_time % id) + id
    bus_arrivals.append((id, arrival_time))

(best_bus_id, best_bus_arrival_time) = min(bus_arrivals, key=lambda b: b[1])

solution = best_bus_id * (best_bus_arrival_time - earliest_time)

print(f"Solution: {solution}")