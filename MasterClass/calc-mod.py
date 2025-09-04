try:
    first_number = int(float(input("Enter a number: ")))
    second_number = int(float(input("Enter a number: ")))
    op = input("Operation (+, -, *, /, %, **): ")
    if op == "+":
        print("Result: ", first_number + second_number)
    elif op == "-":
        print("Result: ", first_number - second_number)
    elif op == "*":
        print("Result: ", first_number * second_number)
    elif op == "/":
        if second_number != 0:
            print("Result: ", first_number / second_number)
        else:
            print("Error: Cannot divide by zero!")
    elif op == "%":
        print("Result: ", first_number % second_number)
    elif op == "**":
        print("Result: ", first_number ** second_number)
    elif op == "q":
        exit()
    else:
        print("Unknown operation")
except ValueError:
    print("Error: please enter whole numbers")
