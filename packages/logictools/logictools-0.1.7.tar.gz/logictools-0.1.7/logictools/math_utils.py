#Calculates the factorial of a number.
def factorial(n):
    try:
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    except ValueError as e:
        return f"{e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"