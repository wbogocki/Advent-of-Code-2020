file = open("day 6/input.txt")
content = file.read()

answers_per_group = content.split("\n\n")

sum_of_common_answers = 0

for group in answers_per_group:
    answers_per_person = group.split("\n")

    answers_common = set(answers_per_person[0])
    for person in answers_per_person:
        answers_common.intersection_update(person)

    sum_of_common_answers += len(answers_common)

print(f"Solution: {sum_of_common_answers}")