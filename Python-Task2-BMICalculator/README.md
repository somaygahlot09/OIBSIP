# BMI Calculator

A command-line Python program that calculates Body Mass Index (BMI) and classifies it into a health category.

## Features
- Prompts for weight (kg) and height (m)
- Calculates BMI = weight / height²
- Shows the BMI rounded to 2 decimal places with its category:
  - Underweight (< 18.5)
  - Normal (18.5 – 24.9)
  - Overweight (25 – 29.9)
  - Obese (≥ 30)
- Input validation: rejects non-numeric, negative and zero values, and warns if height looks like it was entered in cm

## Tech Used
- Python 3 (`input()`, basic arithmetic)

## How to Run
```
python bmi_calculator.py
```

## Author
Somay Gahlot
