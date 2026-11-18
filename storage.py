
import json
import os

BOOKS_FILE = "books.json"
MEMBERS_FILE = "members.json"


def load_data(filename):
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read {filename}. Starting with empty data.")
        return []


def save_data(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_books():
    return load_data(BOOKS_FILE)


def save_books(books):
    save_data(BOOKS_FILE, books)


def load_members():
    return load_data(MEMBERS_FILE)


def save_members(members):
    save_data(MEMBERS_FILE, members)
