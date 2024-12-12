import os
from collections import defaultdict
from pprint import pprint
from typing import Literal

rules = []
updates = []
with open(os.getcwd() + "/2024/day5/data.txt") as file:
    for line in file:
        if "|" in line:
            rules.append(line.strip())
        elif "," in line:
            updates.append([int(i) for i in line.strip().split(",")])


combined_rules = defaultdict(list)
for i in rules:
    key, value = i.split("|")
    combined_rules[int(key)].append(int(value))


def fix_ordering(update: list[int], to_return: Literal["altered", "unaltered"]):
    # print(update)
    altered = False
    for idx, base in enumerate(update):
        # skip first index
        if idx == 0:
            continue
        # get previous numbers in reverse
        prev_nums = update[:idx][::-1]
        for to_check in prev_nums:
            valid = combined_rules[to_check]
            if base in valid:
                continue
            else:
                update[idx], update[idx - 1] = update[idx - 1], update[idx]
                idx = idx - 1
                altered = True
    if altered == True and to_return == "altered":
        return update
    if altered == False and to_return == "unaltered":
        return update


updates = [fix_ordering(i, "altered") for i in updates]

updates = [i for i in updates if i is not None]


num_sum = 0
for i in updates:
    to_add = i[int((len(i) - 1) / 2)]
    num_sum += to_add


print(num_sum)
