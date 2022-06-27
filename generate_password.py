import string
from random import choice


class InvalidLength(Exception):
    """Custom exception for invalid length"""

    def __init__(self) -> None:
        super().__init__(
            "Sum of characters, digits and special characters should not exceed the length of the password"
        )


def main():
    pass
    # try:
    #     gen = generate_password("25", "", "24", "")
    #     print(gen)
    #     print(len(gen))
    # except InvalidLength as err:
    #     print(err)


def generate_password(length: int, no_chars: int, no_digits: int, no_special_chars: int) -> str:
    """return a generated random password based on given parameters"""
    no_all_character = no_chars + no_digits + no_special_chars
    CHARS = list(string.ascii_letters)
    DIGITS = list(string.digits)
    SPECIAL_CHARS = ["!", "@", "#", "$", "%", "^", "&", "*", "&", "/", "?", "`", "~"]

    password = []

    if no_all_character > length:
        raise InvalidLength()

    fill = length - (no_chars + no_digits + no_special_chars)
    if no_special_chars == 0:
        while len(password) != fill:
            password.append(choice(choice([CHARS, DIGITS])))
    else:
        while len(password) != fill:
            password.append(choice(choice([CHARS, DIGITS, SPECIAL_CHARS])))

    for _ in range(no_chars):
        password.append(choice(CHARS))

    for _ in range(no_digits):
        password.append(choice(DIGITS))

    for _ in range(no_special_chars):
        password.append(choice(SPECIAL_CHARS))

    return "".join(password)


if __name__ == "__main__":
    main()
