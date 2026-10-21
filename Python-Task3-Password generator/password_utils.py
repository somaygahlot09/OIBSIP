# Password generation utilities (OIBSIP Task 3 - Random Password Generator).
# Uses the `secrets` module (cryptographically secure) together with `string`.

import secrets
import string

MIN_LENGTH = 8
MAX_LENGTH = 64

# Menu of selectable character types: key -> (label, characters)
CHARACTER_TYPES = {
    "1": ("Uppercase letters", string.ascii_uppercase),
    "2": ("Lowercase letters", string.ascii_lowercase),
    "3": ("Numbers", string.digits),
    "4": ("Symbols", string.punctuation),
}


def ask_length():
    """Ask for a password length; re-prompt until it is valid."""
    while True:
        raw = input(f"Enter password length (min {MIN_LENGTH}, max {MAX_LENGTH}): ").strip()

        try:
            length = int(raw)
        except ValueError:
            print("Invalid input: please enter a whole number.")
            continue

        if length < MIN_LENGTH:
            print(f"Password must be at least {MIN_LENGTH} characters.")
            continue

        if length > MAX_LENGTH:
            print(f"Password cannot be longer than {MAX_LENGTH} characters.")
            continue

        return length


def ask_character_types():
    """Ask which character types to include; at least 2 must be chosen."""
    while True:
        print("\nChoose character types to include:")
        for key, (label, _) in CHARACTER_TYPES.items():
            print(f"  {key}. {label}")

        answer = input("Enter numbers separated by commas (e.g. 1,2,3): ")
        keys = {part.strip() for part in answer.split(",") if part.strip()}

        if not keys:
            print("No character types selected.")
            continue

        invalid = keys - set(CHARACTER_TYPES)
        if invalid:
            print("Invalid option(s):", ", ".join(sorted(invalid)), "- choose from 1-4.")
            continue

        if len(keys) < 2:
            print("Please select at least 2 character types.")
            continue

        return [CHARACTER_TYPES[k][1] for k in sorted(keys)]


def build_password(length, pools):
    """Build a password of `length` containing at least one char from every pool."""
    # 1. Guarantee one character from each selected type
    chars = [secrets.choice(pool) for pool in pools]

    # 2. Fill the remaining positions from the combined pool
    combined = "".join(pools)
    chars += [secrets.choice(combined) for _ in range(length - len(chars))]

    # 3. Shuffle so guaranteed characters are not always at the start
    secrets.SystemRandom().shuffle(chars)

    return "".join(chars)


def generate_password():
    """Interactive generator: prompts, validates, displays and returns the password."""
    length = ask_length()
    pools = ask_character_types()

    password = build_password(length, pools)
    print("\nGenerated Password:", password)

    return password
