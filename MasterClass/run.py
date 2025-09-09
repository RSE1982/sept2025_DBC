"""
    @Author: Robert Elliott
"""

# def error(error_type):
#     if error_type == "div_zero":
#         return "Error! Division by zero."


# def add(a, b):
#     return a + b


# def subtract(a, b):
#     return a - b


# def multiply(a, b):
#     return a * b


# def divide(a, b):
#     if b == 0:
#         return error("div_zero")
#     return a / b


# def is_even(n):
#     if n % 2 == 0:
#         return f"{n} is Even"
#     else:
#         return f"{n} is odd"


# def division(a, b):
#     if b == 0:
#         return error("div_zero")
#     return a // b


# def modulus(a, b):
#     if b == 0:
#         return error("div_zero")
#     return a % b


# a = int(input("Enter first number: "))
# b = int(input("Enter second number: "))

# print(f"Addition: {add(a, b)}")
# print(f"Subtraction: {subtract(a, b)}")
# print(f"Multiplication: {multiply(a, b)}")
# print(f"Division: {divide(a, b)}")
# print(f"Divided Equally is {division(a, b)} with {modulus(a, b)} Left Over")
# is_even(a)
# is_even(b)
# import numpy as np

# one_d = [4, 9, 20, 1, 5, 6, 2, 10, 11]

# two_d = [[4, 9, 20], [1, 5, 6], [2, 10, 11]]

# three_d = [[[4, 9], [9, 20]],
#            [[1, 5], [5, 6]],
#            [[2, 10], [10, 11]]]


# print(one_d)
# print(np.average(one_d))

# print(one_d[1])
# print(two_d[0][1])
# print(three_d[0][0][0])

# two_one = np.array([[3, 1],
#                     [7, 2]])

# two_two = np.array([[1],
#                     [8]])

# added = np.multiply(two_one, two_two)
# print(added)

# set_one = {1, 2, 3, 6}
# set_two = {3, 4, 5, 6}

# print(set_one.union(set_two))
# print(set_one.intersection(set_two))
# print(set_one.difference(set_two))
# print(set_one.symmetric_difference(set_two))


def age_check(age: int) -> str:
    """
        Returns the age bracket Minor/Teenager/Adult
    """
    age_bracket = "Adult"
    if age < 13:
        age_bracket = "Minor"
    if (age >= 13) and (age < 18):
        age_bracket = "Teenager"

    return age_bracket


print(age_check(12))
print(age_check(18))
print(age_check(15))
