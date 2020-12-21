from dataclasses import dataclass
import itertools
from pprint import pprint


@dataclass
class Dish:
    ingredients: set[str]
    allergens: set[str]


# load dishes

dishes = []
ingredients = set()  # all ingredients
allergens = set()  # all allergens

for dish in open("day 21/input.txt").readlines():
    dish_ingredients, dish_allergens = dish.split("(")

    dish_allergens = dish_allergens.rstrip()  # remove final new line if present

    dish_allergens = dish_allergens[8:]  # remove contains
    dish_allergens = dish_allergens[:-1]  # remove final parenthesis

    dish_ingredients = dish_ingredients.split()
    dish_allergens = [it.lstrip() for it in dish_allergens.split(",")]

    dishes.append(Dish(set(dish_ingredients), set(dish_allergens)))

    ingredients.update(dish_ingredients)
    allergens.update(dish_allergens)

# pprint(dishes)


# find allergens that could be in each ingredients (but don't check for if they are right yet)

possible_allergens_for_ingredients = dict()

for dish in dishes:
    for ingredient in dish.ingredients:
        if ingredient not in possible_allergens_for_ingredients:
            possible_allergens_for_ingredients[ingredient] = set()

        possible_allergens_for_ingredients[ingredient].update(dish.allergens)

# pprint(possible_allergens_for_ingredients)


# eliminate ingredients in the list that don't work

# TODO: This solution will sometimes hang if it matches the ingredients in a bad order; in thoses just re-run it a few times

associated_allergens = set()
while len(associated_allergens) != len(allergens):
    for ingredient, allergen in itertools.product(ingredients, allergens):
        # skip already associate allergens
        if allergen in associated_allergens:
            continue

        # check if the dishes list makes sense after this ingredient is associated with this allergen

        if allergen not in possible_allergens_for_ingredients[ingredient]:
            continue

        successful_association_for_all_dishes = True

        for dish in dishes:
            required_allergens_after_association = set()

            # include all dish allergens and this allergen if dish has this igredient
            required_allergens_after_association.update(dish.allergens)
            if ingredient in dish.ingredients:
                required_allergens_after_association.add(allergen)

            possible_allergens_after_association = set()

            for dish_ingredient in dish.ingredients:
                possible_allergens = possible_allergens_for_ingredients[dish_ingredient]

                for possible_allergen in possible_allergens:
                    # this ingredient is only possible for this allergen
                    if (
                        possible_allergen != allergen and dish_ingredient != ingredient
                    ) or (
                        possible_allergen == allergen and dish_ingredient == ingredient
                    ):
                        possible_allergens_after_association.add(possible_allergen)

            if not required_allergens_after_association.issubset(
                possible_allergens_after_association
            ):
                successful_association_for_all_dishes = False
                break

        if successful_association_for_all_dishes:
            # association successful, update possible_allergens_for_ingredients
            print(f"associate {ingredient} with {allergen}")

            associated_allergens.add(allergen)

            # remove this allergen from the list of possibilities
            for (
                possible_ingredient,
                possible_allergens,
            ) in possible_allergens_for_ingredients.items():
                if possible_ingredient != ingredient and allergen in possible_allergens:
                    possible_allergens.remove(allergen)
        else:
            # print(f"failed to associate {ingredient} with {allergen}")
            pass

pprint(possible_allergens_for_ingredients)


# get ingredients that can't contain allergens

ingredients_that_cant_contain_allergens = set()

for ingredient, allergens in possible_allergens_for_ingredients.items():
    if not allergens:
        ingredients_that_cant_contain_allergens.add(ingredient)

pprint(ingredients_that_cant_contain_allergens)


# count how many ingredients without allergens occur

count = 0

for dish in dishes:
    for ingredient in ingredients_that_cant_contain_allergens:
        if ingredient in dish.ingredients:
            count += 1

print(f"Ingredients that can't contain allergens appear {count} times.")