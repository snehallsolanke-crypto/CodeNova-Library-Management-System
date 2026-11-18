
from datetime import datetime

from storage import load_books, load_members, save_books, save_members
from validation import validate_author, validate_copies, validate_isbn, validate_title


DEFAULT_BOOKS = [
    {"ISBN": "9780306406157", "Title": "The Design of Everyday Things", "Author": "Don Norman", "Copies": 3},
    {"ISBN": "9780735211292", "Title": "Atomic Habits", "Author": "James Clear", "Copies": 3},
    {"ISBN": "9780061122415", "Title": "The Alchemist", "Author": "Paulo Coelho", "Copies": 2},
    {"ISBN": "9788172234980", "Title": "Wings of Fire", "Author": "A.P.J. Abdul Kalam", "Copies": 5},
    {"ISBN": "9781501196058", "Title": "Think Like a Monk", "Author": "Jay Shetty", "Copies": 3},
    {"ISBN": "9781786330895", "Title": "Ikigai", "Author": "Hector Garcia", "Copies": 4},
    {"ISBN": "9780735214149", "Title": "The Power of Habit", "Author": "Charles Duhigg", "Copies": 2},
    {"ISBN": "9780062315007", "Title": "The Sapiens", "Author": "Yuval Noah Harari", "Copies": 4},
]


def normalize_isbn(isbn):
    return isbn.replace("-", "").replace(" ", "").upper()


def find_book(books, isbn):
    normalized = normalize_isbn(isbn)
    return next((book for book in books if normalize_isbn(str(book["ISBN"])) == normalized), None)


def seed_catalog():
    books = load_books()
    old_isbn = "9780143442286"
    for book in books:
        if normalize_isbn(str(book["ISBN"])) == old_isbn:
            book["ISBN"] = "9781501196058"
            book["Title"] = "Think Like a Monk"
            book["Author"] = "Jay Shetty"
            break

    existing = {normalize_isbn(str(book["ISBN"])) for book in books}
    for book in DEFAULT_BOOKS:
        if book["ISBN"] not in existing:
            books.append(book)
    save_books(books)
    return books


def print_book(book):
    print(f"ISBN: {book['ISBN']} | Title: {book['Title']} | Author: {book['Author']} | Copies: {book['Copies']}")


def add_book(books):
    isbn = normalize_isbn(input("Enter ISBN: ").strip())
    if not validate_isbn(isbn):
        print("Invalid ISBN-10 or ISBN-13.")
        return
    if find_book(books, isbn):
        print("This ISBN already exists!")
        return

    title = input("Enter book title: ").strip()
    if not validate_title(title):
        print("Title cannot be empty.")
        return

    author = input("Enter author name: ").strip()
    if not validate_author(author):
        print("Author cannot be empty.")
        return

    copies_input = input("Enter number of copies: ").strip()
    if not validate_copies(copies_input):
        print("Copies must be a positive whole number.")
        return

    books.append({"ISBN": isbn, "Title": title, "Author": author, "Copies": int(copies_input)})
    save_books(books)
    print("Book added successfully!")


def view_books(books):
    if not books:
        print("No books available.")
        return
    for book in books:
        print_book(book)


def search_books(books):
    query = input("Enter title or author to search: ").strip().lower()
    if not query:
        print("Search text cannot be empty.")
        return

    matches = [
        book for book in books
        if query in book["Title"].lower() or query in book["Author"].lower()
    ]
    if not matches:
        print("Book not found.")
        return
    for book in matches:
        print_book(book)


def remove_book(books, members):
    isbn = input("Enter ISBN to remove: ").strip()
    book = find_book(books, isbn)
    if not book:
        print("Book not found.")
        return

    active_loans = [
        member for member in members
        if normalize_isbn(str(member["ISBN"])) == normalize_isbn(str(book["ISBN"]))
    ]
    if active_loans:
        print("Cannot remove this book while it has active borrowing records.")
        return

    confirmation = input(
        f"Remove '{book['Title']}' (ISBN: {book['ISBN']})? (y/n): "
    ).strip().lower()
    if confirmation not in ("y", "yes"):
        print("Book removal cancelled.")
        return

    books.remove(book)
    save_books(books)
    print("Book removed successfully!")


def borrow_book(books, members):
    isbn = input("Enter ISBN to borrow: ").strip()
    book = find_book(books, isbn)
    if not book:
        print("Book not found.")
        return
    if book["Copies"] <= 0:
        print("No copies available.")
        return

    member_id = input("Enter member ID: ").strip()
    member_name = input("Enter member name: ").strip()
    if not member_id or not member_name:
        print("Member ID and name are required.")
        return

    book["Copies"] -= 1
    members.append({
        "MemberID": member_id,
        "MemberName": member_name,
        "ISBN": book["ISBN"],
        "Title": book["Title"],
        "BorrowedAt": datetime.now().isoformat(timespec="minutes"),
    })
    save_books(books)
    save_members(members)
    print("Book borrowed successfully!")


def return_book(books, members):
    isbn = input("Enter ISBN to return: ").strip()
    member_id = input("Enter member ID: ").strip()
    book = find_book(books, isbn)
    if not book:
        print("Book not found.")
        return

    record = next(
        (item for item in members
         if item["MemberID"] == member_id and normalize_isbn(str(item["ISBN"])) == normalize_isbn(isbn)),
        None,
    )
    if not record:
        print("No borrowing record found for this member and book.")
        return

    members.remove(record)
    book["Copies"] += 1
    save_books(books)
    save_members(members)
    print("Book returned successfully!")


def main():
    books = seed_catalog()
    members = load_members()

    while True:
        print("\n===== LIBRARY BOOK CATALOG =====")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Remove Book")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_book(books)
        elif choice == "2":
            view_books(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            remove_book(books, members)
        elif choice == "5":
            borrow_book(books, members)
        elif choice == "6":
            return_book(books, members)
        elif choice == "7":
            print("Thank you!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
