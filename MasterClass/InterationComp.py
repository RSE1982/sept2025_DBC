#fruits = {"apple", "banana", "cherry", "fig"}
# for fruit in fruits:
#     print(fruit)

# set1 = {"a", "b", "c", "a"}

# for fruit, letter in zip(fruits, set1):
#     print(fruit, letter)

words = "this is a small comprehension exercise".split()
print(words)

# 1 Make a list of word lengths
word_lengths = [len(word) for word in words]
print(word_lengths)

# 2 Make a dictionary mapping word -> word in UPPERCASE
upper_words = {word: word.upper() for word in words}
print(upper_words)

# 3 Make a set of words longer than 3 letters
long_words = {word for word in words if len(word) > 3}
print(long_words)

contains_e = {}