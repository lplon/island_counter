import random

x = 1000
y = 100

generated_map = []
for i in range(x):
    generated_map.append([random.choice(["0", "1"]) for columns in range(y)])

str_map = ["".join(i) for i in generated_map]
with open("resources/generated_map.txt", "w") as f:
    f.writelines(str_map)
