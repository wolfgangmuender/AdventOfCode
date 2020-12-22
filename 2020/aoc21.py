from copy import copy

with open("input/input21.txt") as f:
    content = f.read().splitlines()


def split_and_strip(the_string, separator):
    return [part.strip() for part in the_string.split(separator)]


def string_to_list(the_string):
    the_list = []
    the_list[:0] = the_string
    return the_list


class Meal:

    def __init__(self, the_line):
        ingredients_string, allergens_string = split_and_strip(the_line[0:-1], '(contains')
        self.ingredients = split_and_strip(ingredients_string, ' ')
        self.allergens = split_and_strip(allergens_string, ',')


candidates = {}
ingredients = set()
meals = []
for line in content:
    meal = Meal(line)
    meals.append(meal)
    ingredients.update(meal.ingredients)
    for allergen in meal.allergens:
        if allergen not in candidates:
            candidates[allergen] = set(meal.ingredients)
        else:
            candidates[allergen].intersection_update(meal.ingredients)

allergen_containing = set.union(*candidates.values())

print("Solution 1: ingredients that are free of allergens appear {} times".format(
    len([ingredient for meal in meals for ingredient in meal.ingredients if ingredient not in allergen_containing])))

mapping = {}
candidates_copy = copy(candidates)
while candidates_copy:
    uniques = {k: v for k, v in candidates_copy.items() if len(v) == 1}
    for unique in uniques.keys():
        mapping[unique] = uniques[unique].pop()
        del candidates_copy[unique]
        for curr_candidates in candidates_copy.values():
            if mapping[unique] in curr_candidates:
                curr_candidates.remove(mapping[unique])

cdi_list = []
for allergen in sorted(mapping.keys()):
    cdi_list.append(mapping[allergen])

print("Solution 2: the canonical dangerous ingredient list is '{}'".format(",".join(cdi_list)))
