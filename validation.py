
import re


def validate_isbn(isbn):
    """
    Validate ISBN-10 or ISBN-13 format.
    """

    isbn = isbn.replace("-", "").replace(" ", "")

    # ISBN-13 validation
    if len(isbn) == 13 and isbn.isdigit():
        total = 0

        for i in range(12):
            if i % 2 == 0:
                total += int(isbn[i])
            else:
                total += int(isbn[i]) * 3

        check_digit = (10 - (total % 10)) % 10

        return check_digit == int(isbn[12])

    # ISBN-10 validation
    if len(isbn) == 10:
        if not isbn[:9].isdigit():
            return False

        if not (isbn[9].isdigit() or isbn[9] == "X"):
            return False

        total = 0

        for i in range(9):
            total += int(isbn[i]) * (10 - i)

        last_digit = 10 if isbn[9] == "X" else int(isbn[9])

        total += last_digit

        return total % 11 == 0

    return False


def validate_title(title):
    return bool(title.strip())


def validate_author(author):
    return bool(author.strip())


def validate_copies(copies):
    try:
        return int(copies) > 0
    except ValueError:
        return False
