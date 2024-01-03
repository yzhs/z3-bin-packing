#!/bin/python3

import z3

groups = [
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

o = z3.Optimize()

max_group_size = 5
max_per_table = 5
num_tables = 12

tables = z3.IntVector("tables", num_tables)

# Non-negative number of people per table
o.add(z3.And([0 <= t for t in tables]))

# Maximum number of people per table
o.add(z3.And([t <= max_per_table for t in tables]))

# Break symmetry by requiring that the number of people per table decreases
o.add(z3.And([t1 >= t2 for t1, t2 in zip(tables, tables[1:])]))

# Associate groups with tables
groups_tables = [
    z3.IntVector(f"table_{i+1}_includes_group", len(groups)) for i in range(num_tables)
]

# Make groups_tables boolean, i.e. 0 or 1
# 1 means the group sits at that table, 0 means it doesn't
o.add(z3.And([0 <= x for g in groups_tables for x in g]))
o.add(z3.And([x <= 1 for g in groups_tables for x in g]))

# Each group sits at no more than one table
for j in range(len(groups)):
    o.add(sum([groups_tables[i][j] for i in range(num_tables)]) <= 1)

# Ensure that sum of group sizes at a table does not exceed table size
for i in range(num_tables):
    o.add(
        sum([groups[j] * groups_tables[i][j] for j in range(len(groups))])
        <= max_per_table
    )

# Sync tables with groups_tables
for i in range(num_tables):
    o.add(
        tables[i] == sum([groups_tables[i][j] * groups[j] for j in range(len(groups))])
    )

# Ensure that each group is seated at a table
for j in range(len(groups)):
    o.add(sum([groups_tables[i][j] for i in range(num_tables)]) == 1)

table_of_group = z3.IntVector("table_of_group", len(groups))
# sync with groups_tables
for i in range(num_tables):
    for j in range(len(groups)):
        o.add(z3.Implies(groups_tables[i][j] == 1, table_of_group[j] == i + 1))

# Break symmetry: for same number of people in group, move group with smaller
# number to table with smaller number
for j in range(len(groups)):
    for k in range(j + 1, len(groups)):
        if groups[j] != groups[k]:
            continue
        o.add(table_of_group[j] < table_of_group[k])

# Place groups that need the whole table first
for j, g in enumerate(groups):
    if g == 5:
        for k in range(j + 1, len(groups)):
            o.add(table_of_group[j] < table_of_group[k])

# Minimize number of tables used
o.minimize(
    sum(
        sum([groups_tables[i][j] for j in range(len(groups))]) > 0
        for i in range(num_tables)
    )
)

if o.check() != z3.sat:
    print("Unsatisfiable")
    exit(1)

model = o.model()
print("People per table:", *[model[t] for t in tables])
for i in range(num_tables):
    groups_at_this_table = [
        j for j in range(len(groups)) if model[groups_tables[i][j]] == 1
    ]
    print(f"Groups at table {i+1}:", *groups_at_this_table)
