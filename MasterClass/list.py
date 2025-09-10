# nums = [3, 1, 4, 1, 5]
# nums.append(9)
# nums.remove(1)
# nums.insert(1, 42)

# print(min(nums))
# print(sorted(nums)[0])

# colours = ("red", "red", "blue")
# print(colours.index("red"))

# person = ("Ana", 30, "UK")

# name, age, country = person

# print(f"{name} is {age} and lives in {country}.")

# scores = {"Ana": 80, "Bob": 70}
# scores["Cara"] = 90

# print(scores.get("Ana", "Not found"))

# for name, score in scores.items():
#     print(f"Name: {name} ,Score: {score}")

raw = ["ana", "bob", "cara", "ana", "bob", "dio"]

unique = set(raw)

print(unique)
print("cara" in unique)

set_b = {"ana", "eve"}

print(unique & set_b)

unique.