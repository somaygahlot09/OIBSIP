# BMI Calculator
# Asks for weight (kg) and height (m), calculates BMI and shows the category.


def get_positive_number(prompt, unit_hint, max_value):
    """Keep asking until the user enters a valid positive number."""
    while True:
        raw = input(prompt).strip()

        try:
            value = float(raw)
        except ValueError:
            print(f"Invalid input: please enter a number (for example {unit_hint}).")
            continue

        if value < 0:
            print("Invalid input: value cannot be negative.")
            continue

        if value == 0:
            print("Invalid input: value must be greater than zero.")
            continue

        if value > max_value:
            print(f"That value looks too large. Please check the unit (for example {unit_hint}).")
            continue

        return value


def calculate_bmi(weight, height):
    """BMI = weight (kg) / height (m) squared."""
    return weight / (height ** 2)


def classify_bmi(bmi):
    """Return the standard BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def main():
    print("========== BMI CALCULATOR ==========")

    weight = get_positive_number("Enter your weight in kg: ", "68 or 72.5", 500)
    height = get_positive_number("Enter your height in metres: ", "1.75, not 175", 3)

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print(f"\nYour BMI is: {bmi:.2f}")
    print(f"Category   : {category}")


if __name__ == "__main__":
    main()
