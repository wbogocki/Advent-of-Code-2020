file = open("day 6/input.txt")
content = file.read()

answers_per_group = content.split("\n\n")
answers_per_group = [set(a.replace("\n", "")) for a in answers_per_group]

sum_of_positive_answers = 0

for answers in answers_per_group:
    sum_of_positive_answers += len(answers)

print(f"Solution: {sum_of_positive_answers}")