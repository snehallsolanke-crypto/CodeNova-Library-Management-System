
import json
import os

if os.path.exists("books.json"):
    with open("books.json", "r") as file:
        books = json.load(file)
else:
    books = []

def save_books():
    with open("books.json", "w") as file:
        json.dump(books, file, indent=4)

default_books = [
    {"ISBN": "102", "Title": "Atomic Habits", "Author": "James Clear", "Copies": 3},
    {"ISBN": "103", "Title": "Rich Dad Poor Dad", "Author": "Robert Kiyosaki", "Copies": 4},
    {"ISBN": "104", "Title": "The Alchemist", "Author": "Paulo Coelho", "Copies": 2},
    {"ISBN": "105", "Title": "Wings of Fire", "Author": "A.P.J. Abdul Kalam", "Copies": 5},
    {"ISBN": "106", "Title": "Think Like a Monk", "Author": "Jay Shetty", "Copies": 3},
    {"ISBN": "107", "Title": "Ikigai", "Author": "Hector Garcia", "Copies": 4},
    {"ISBN": "108", "Title": "The Power of Habit", "Author": "Charles Duhigg", "Copies": 2}
]

for new_book in default_books:
    if not any(book["ISBN"] == new_book["ISBN"] for book in books):
        books.append(new_book)

save_books()

while True:
    print("\n===== LIBRARY BOOK CATALOG =====")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Remove Book")
    print("5. Borrow Book")
    print("6. Return Book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        isbn = input("Enter ISBN: ")

        if any(book["ISBN"] == isbn for book in books):
            print("This ISBN already exists!")
            continue

        title = input("Enter book title: ")
        author = input("Enter author name: ")

        try:
            copies = int(input("Enter number of copies: "))
            if copies <= 0:
                print("Copies must be greater than zero!")
                continue
        except ValueError:
            print("Please enter a valid number!")
            continue

        book = {
            "ISBN": isbn,
            "Title": title,
            "Author": author,
            "Copies": copies
        }

        books.append(book)
        save_books()
        print("Book added successfully!")

    elif choice == "2":
        if len(books) == 0:
            print("No books available.")
        else:
            for book in books:
                print(book)

    elif choice == "3":
        search = input("Enter book title or ISBN: ")
        found = False

        for book in books:
            if search.lower() == book["Title"].lower() or search == book["ISBN"]:
                print("Book Found!")
                print(book)
                found = True

        if not found:
            print("Book not found.")

    elif choice == "4":
        isbn = input("Enter ISBN to remove: ")

        for book in books:
            if book["ISBN"] == isbn:
                books.remove(book)
                save_books()
                print("Book removed successfully!")
                break
        else:
            print("Book not found.")

    elif choice == "5":
        isbn = input("Enter ISBN to borrow: ")

        for book in books:
            if book["ISBN"] == isbn:
                if book["Copies"] > 0:
                    book["Copies"] -= 1
                    save_books()
                    print("Book borrowed successfully!")
                else:
                    print("No copies available.")
                break
        else:
            print("Book not found.")

    elif choice == "6":
        isbn = input("Enter ISBN to return: ")

        for book in books:
            if book["ISBN"] == isbn:
                book["Copies"] += 1
                save_books()
                print("Book returned successfully!")
                break
        else:
            print("Book not found.")

    elif choice == "7":
        print("Thank you!")
        break

    else:
        print("Invalid choice! Please try again.")
