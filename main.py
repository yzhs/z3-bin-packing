#!/bin/python3

group_sizes = [
    3,
    4,
    2,
    2,
    1,
    5,
    5,
    1,
    3,
    5,
    5,
    4,
    4,
    4,
    4,
    4,
]

max_group_size = 5
max_per_table = 5
num_tables = 10


for x in range(len(group_sizes)):
    candidate_group_sizes = sorted(group_sizes[:x+1], reverse=True)

    groups_at_table = [[] for _ in range(num_tables)]
    open_places_at_table = [max_per_table for _ in range(num_tables)]

    for i, group_size in enumerate(candidate_group_sizes):
        found_table_for_current_group = False
        for j, open_places in enumerate(open_places_at_table):
            if open_places < group_size:
                continue

            found_table_for_current_group = True
            groups_at_table[j].append(i)
            open_places_at_table[j] -= group_size
            break

        if not found_table_for_current_group:
            print(f"There's enough room to seat the first {x-1} groups but not for the first {x}:")
            print(*group_sizes[:x+1])
            print(f"Putting group {x} of size {group_sizes[x]} on the waiting list")
            print()
            break
    else:
        print(f"Successfully seated groups 0 through {x}:")
        for i in range(num_tables):
            print("Sitting at table", i, "are groups of the following sizes:", *[candidate_group_sizes[x] for x in groups_at_table[i]])
