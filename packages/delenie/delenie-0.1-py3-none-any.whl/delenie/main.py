def divide_numbers(num1, num2):
    try:
        result = num1 / num2
        return result
    except ZeroDivisionError:
        return "Error! Delenie na 0!"

number1 = float(input("Input first number: "))
number2 = float(input("Input second number: "))

result = divide_numbers(number1, number2)
print("Result:", result)