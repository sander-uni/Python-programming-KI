import matrix


dict = matrix.create_dict("lol", 123, (1,2,3), "idiot", 99, 11);

print(dict)

for key, value in dict.items():
    print(f"{key}: {value}")
