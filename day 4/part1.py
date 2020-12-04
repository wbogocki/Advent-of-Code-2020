file = open("day 4/input.txt")
content = file.read()

passports = [passport for passport in content.split("\n\n")]

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

valid_passport_count = 0

for passport in passports:
    fields = set()
    for field in passport.split():
        key, _ = field.split(":")
        fields.add(key)

    if required_fields.issubset(fields):
        valid_passport_count += 1

print(f"Valid passports: {valid_passport_count}")