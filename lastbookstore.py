import sqlite3

# Create book table if not exists and add default values
def create_table():
    connection = sqlite3.connect ( "ebookstore.db" )
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)")
    connection.commit()
    cursor.execute("SELECT * FROM book ")
    books = cursor.fetchall()
    if not books:
        add_default_records()
    connection.close()

# adding default values into the book table
def add_default_records():
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
   
    cursor.execute("INSERT OR REPLACE INTO book (id, title, author, qty) VALUES (?,?, ?, ?)", (3001, "A Tale of Two Cities", "Charles Dickens", 30))
    cursor.execute("INSERT OR REPLACE INTO book (id, title, author, qty) VALUES (?,?, ?, ?)", (3002, "Harry Potter and the Philospher's Stone", "J.K. Rowling", 40))
    cursor.execute("INSERT OR REPLACE INTO book (id, title, author, qty) VALUES (?,?, ?, ?)", (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25))
    cursor.execute("INSERT OR REPLACE INTO book (id, title, author, qty) VALUES (?,?, ?, ?)", (3004, "The Lord of the Rings", "J.R.R Tolkien", 37))
    cursor.execute("INSERT OR REPLACE INTO book (id, title, author, qty) VALUES (?,?, ?, ?)", (3005, "Alice in Wonderland", "Lewis Caroll", 12))
   
    connection.commit()
    connection.close()
    
 # This function shows all records 
def show_all_books():
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM book ")
    books = cursor.fetchall()
    for book in books:
        print(book)
    connection.close()
     
# takes quantity value from user and returns integer
def get_quantity(allow_blank = False):
    qty = -1
    while True:
        try:
            if allow_blank:
                # In update process, we allow user to skip via blank value
                # In this case we do not validate if input is integer or not
                qty_str = input("Enter new quantity (leave blank to skip): ")
                if qty_str == " ":
                    break
            else:
                qty_str = input("Enter quantity: ")
            
            qty = int(qty_str)
            if qty > -1:
                break
            else:
                print("Invalid quantity value!")
        except:
            print("Invalid quantity value!")
            
    return qty

#Provide a way for the user to obtain the book ID when updating or deleting books
def get_book_id(title):
    # Function to retrieve book ID using the book title
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM book WHERE title=?", (title,))
    book_id = cursor.fetchone()
    connection.close()
    return book_id[0] if book_id else None

# adds new book record into the book table
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    qty = get_quantity()

    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO book (title, author, qty) VALUES (?, ?, ?)", (title, author, qty))
    connection.commit()
    connection.close()
    print("Book added successfully!")
 
    
# updates book record according to it's ID   
def update_book():
    # get the ID of book via title of the book
    title = input("Enter the title of the book to update: ")
    book_id = get_book_id(title)

    if book_id is None:
        print("Book not found.")
        return

    new_title = input("Enter new book title (leave blank to skip): ")
    new_author = input("Enter new author (leave blank to skip): ")
    new_qty = get_quantity(True)

    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()

    # Update fields only if they are not blank
    if new_title != " " :
        cursor.execute("UPDATE book SET title=? WHERE id=?", (new_title, book_id))
    if new_author != " " :
        cursor.execute("UPDATE book SET author=? WHERE id=?", (new_author, book_id))
    if new_qty > -1:
        cursor.execute("UPDATE book SET qty=? WHERE id=?", (new_qty, book_id))

    connection.commit()
    connection.close()    
    print("Book updated successfully!")


# deletes book record according to it's ID
def delete_book():
    title = input("Enter the title of the book to delete: ")
    book_id = get_book_id(title)

    if book_id is None:
        print("Book not found.")
        return

    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM book WHERE id=?", (book_id,))
    connection.commit()
    connection.close()
    print("Book deleted successfully!")
    
    
# Search for a specific book
def search_book():
    valid_search = True
    connection = sqlite3.connect("ebookstore.db")
    cursor = connection.cursor()
    # Get user's selection for searching the book
    while True:
        print("\Search Options:")
        print("1. ID")
        print("2. Title")
        print("3. Author")
        print("4. Quantity")
        print("0. Main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            search_id = input("Enter the Id of the book: ")
            cursor.execute("SELECT * FROM book WHERE Id=?", (search_id,))
            break
        elif choice == "2":
            search_title = input("Enter the title of the book: ")
            cursor.execute("SELECT * FROM book WHERE Title = ?", (search_title,))
            break
        elif choice == "3":
            search_author = input("Enter the author of the book: ")
            cursor.execute("SELECT * FROM book WHERE author = ?", (search_author,))
            break
        elif choice == "4":
            search_qty = get_quantity()
            cursor.execute("SELECT * FROM book WHERE qty=?", (search_qty,))
            break
        elif choice == "0":
            valid_search = False
            break
        else:
            print("Invalid choice. Please try again.")
    
    if valid_search == True:
        books = cursor.fetchall()
        if books:
            print("Found books:")
            for book in books:
                print(book)
        else:
            print("Book not found.")
    connection.close()
    
    
# Main program with user selects
create_table()
while True:
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. Show all books")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        update_book()
    elif choice == "3":
        delete_book()
    elif choice == "4":
        search_book()
    elif choice == "5":
        show_all_books()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please try again.")