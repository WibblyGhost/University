with open("cplex.log", "r") as file:
    data = file.readlines()

for line in data:
    if line.split(" ")[0] == "Elapsed":
        print(line.split(" ")[3])
        # print("HIT")
print (data)
