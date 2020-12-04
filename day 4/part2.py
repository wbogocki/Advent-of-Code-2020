import re

file = open("day 4/input.txt")
content = file.read()

passports = [passport for passport in content.split("\n\n")]

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

valid_passport_count = 0


def validate_fields_data(fields):
    birth_year = int(fields["byr"])
    if not (1920 <= birth_year <= 2002):
        return False

    issue_year = int(fields["iyr"])
    if not (2010 <= issue_year <= 2020):
        return False

    expiration_year = int(fields["eyr"])
    if not (2020 <= expiration_year <= 2030):
        return False

    height = int(fields["hgt"][:-2])
    height_unit = fields["hgt"][-2:]

    if not (
        (height_unit == "cm" and 150 <= height <= 193)
        or (height_unit == "in" and 59 <= height <= 76)
    ):
        return False

    hair_color = fields["hcl"]
    if not re.match(r"^#[0-9a-f]{6}$", hair_color):
        return False

    eye_color = fields["ecl"]
    if eye_color not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False

    passport_id = fields["pid"]
    if not re.match(r"^[0-9]{9}$", passport_id):
        return False

    return True


for passport in passports:
    fields = dict()
    for field in passport.split():
        key, val = field.split(":")
        fields[key] = val

    if required_fields.issubset(fields.keys()) and validate_fields_data(fields):
        valid_passport_count += 1


print(f"Valid passports: {valid_passport_count}")