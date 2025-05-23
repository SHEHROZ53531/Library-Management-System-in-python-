from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from datetime import date, timedelta
import os
import tkinter as tk
from tkinter import Toplevel, Label, Frame, Scrollbar, messagebox, ttk


##################################################################################################################
class SearchBooksPage:

    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("View Books")
        self.window.geometry("900x600")

        # Load and set background image
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/6920933.jpg")
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        # --- Search Section ---
        Label(self.window, text="Search by Title:", font=("Arial", 12), bg="#ffffff").place(x=20, y=20)
        self.search_title = Entry(self.window, width=30)
        self.search_title.place(x=150, y=20)

        Label(self.window, text="Search by Genre:", font=("Arial", 12), bg="#ffffff").place(x=470, y=20)
        self.search_genre = Entry(self.window, width=30)
        self.search_genre.place(x=600, y=20)

        Button(self.window, text="Search", font=("Arial", 12), command=self.search_books).place(x=400, y=60)

        # --- Table Section ---
        table_frame = Frame(self.window, bg="#ffffff")  # White bg for readability
        table_frame.place(x=20, y=110, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Title", "Author", "Genre", "Quantity"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        # Define headings
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Quantity", text="Quantity")

        # Define column widths
        self.tree.column("Title", anchor=W, width=250)
        self.tree.column("Author", anchor=W, width=200)
        self.tree.column("Genre", anchor=W, width=150)
        self.tree.column("Quantity", anchor=CENTER, width=100)

        # Configure striped rows for better readability
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_all_books()

    def update_table(self, books):
        # Clear current data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data with striped rows
        for i, book in enumerate(books):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", END, values=book, tags=(tag,))

    def load_all_books(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT title, author, genre, quantity FROM Books")
            books = cursor.fetchall()

            self.update_table(books)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def search_books(self):
        title = self.search_title.get().strip()
        genre = self.search_genre.get().strip()

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = "SELECT title, author, genre, quantity FROM Books WHERE 1=1"
            values = []

            if title:
                query += " AND title LIKE %s"
                values.append(f"%{title}%")
            if genre:
                query += " AND genre LIKE %s"
                values.append(f"%{genre}%")

            cursor.execute(query, tuple(values))
            books = cursor.fetchall()

            self.update_table(books)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################






##################################################################################################################
class RequestBookPage:
    def __init__(self, master, member_id):
        self.member_id = member_id
        self.window = Toplevel(master)
        self.window.title("Request Book")
        self.window.geometry("900x600")

        # Background image (optional)
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/6920933.jpg")
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        Label(self.window, text="Select a Book to Request:", font=("Arial", 14), bg="#ffffff").place(x=20, y=20)

        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=60, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Title", "Author", "Genre", "Quantity"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Quantity", text="Quantity")

        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.column("Title", width=250, anchor=W)
        self.tree.column("Author", width=200, anchor=W)
        self.tree.column("Genre", width=150, anchor=W)
        self.tree.column("Quantity", width=100, anchor=CENTER)

        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_books()

        Button(self.window, text="Request Borrow", font=("Arial", 14), command=self.request_borrow).place(x=350, y=530)

    def load_books(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author, genre, quantity FROM Books WHERE quantity > 0")
            books = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, book in enumerate(books):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", END, values=book, tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def request_borrow(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a book to request.")
            return

        book = self.tree.item(selected, 'values')
        book_id = book[0]

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Check existing request status
            check_query = """
                SELECT COUNT(*) FROM BorrowRequests
                WHERE member_id = %s AND book_id = %s AND status IN ('Pending', 'Approved')
            """
            cursor.execute(check_query, (self.member_id, book_id))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showinfo("Request Exists", "You already have a pending or approved request for this book.")
                return

            insert_query = """
                INSERT INTO BorrowRequests (member_id, book_id, request_date, status)
                VALUES (%s, %s, CURDATE(), 'Pending')
            """
            cursor.execute(insert_query, (self.member_id, book_id))
            conn.commit()

            messagebox.showinfo("Request Sent", "Your borrow request has been sent to the admin.")
            self.load_books()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################





##################################################################################################################
class ViewBorrowedBooksPage:
    def __init__(self, master, member_id):
        self.member_id = member_id
        self.window = Toplevel(master)
        self.window.withdraw()  # Hide window initially

        self.window.title("Borrowed Books")
        self.window.geometry("900x600")

        # Load background image
        try:
            image_path = "/Users/macbookairm3/Desktop/image of library/6920933.jpg"
            if not os.path.isfile(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")

            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.bg_label = Label(self.window, image=self.bg_photo)
            self.bg_label.image = self.bg_photo  # prevent garbage collection
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()

        except Exception as e:
            print(f"[ERROR] Background image loading failed: {e}")
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        # Title label
        tk.Label(self.window, text="Books You Have Borrowed:", font=("Arial", 14, "bold"), bg="#ffffff").place(x=20, y=20)

        # Frame for table
        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=60, width=860, height=450)

        # Scrollbars
        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        # Treeview style
        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")
        style.map('mystyle.Treeview', background=[('selected', '#347083')])

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Title", "Author", "BorrowDate"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
            style="mystyle.Treeview"
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        # Column setup
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("BorrowDate", text="Borrow Date")

        self.tree.column("Title", anchor=W, width=300)
        self.tree.column("Author", anchor=W, width=200)
        self.tree.column("BorrowDate", anchor=CENTER, width=120)

        # Row tags
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        # Load data
        self.load_borrowed_books()

        self.window.update_idletasks()
        self.window.deiconify()  # Show window after layout is ready

    def load_borrowed_books(self):
        print(f"[DEBUG] Loading borrowed books for member ID: {self.member_id}")

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = """
                SELECT b.title, b.author, t.borrow_date
                FROM Transactions t
                JOIN Books b ON t.book_id = b.book_id
                WHERE t.member_id = %s AND t.return_date IS NULL
            """
            cursor.execute(query, (self.member_id,))
            books = cursor.fetchall()

            print(f"[DEBUG] Books fetched from DB: {books}")

            self.tree.delete(*self.tree.get_children())

            if not books:
                messagebox.showinfo("No Borrowed Books", "You have not borrowed any books.")
                return

            for i, (title, author, borrow_date) in enumerate(books):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                if hasattr(borrow_date, 'strftime'):
                    borrow_date = borrow_date.strftime("%Y-%m-%d")
                self.tree.insert("", END, values=(title, author, borrow_date), tags=(tag,))

        except mysql.connector.Error as err:
            print(f"[ERROR] Database error: {err}")
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()          
##################################################################################################################




##################################################################################################################
class ReturnBookPage:
    def __init__(self, master, member_id):
        self.member_id = member_id
        self.window = Toplevel(master)
        self.window.title("Return Book")
        self.window.geometry("900x600")

        # Background
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/6920933.jpg")
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        Label(self.window, text="Books to Return:", font=("Arial", 14, "bold"), bg="#ffffff").place(x=20, y=20)

        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=60, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("TransactionID", "Title", "Author", "BorrowDate"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        self.tree.heading("TransactionID", text="Transaction ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("BorrowDate", text="Borrow Date")

        self.tree.column("TransactionID", width=120, anchor=CENTER)
        self.tree.column("Title", width=250, anchor=W)
        self.tree.column("Author", width=200, anchor=W)
        self.tree.column("BorrowDate", width=120, anchor=CENTER)

        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_borrowed_books()

        Button(self.window, text="Return Selected Book", font=("Arial", 14), command=self.return_book).place(x=330, y=530)

    def load_borrowed_books(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()
            query = """
                SELECT t.transaction_id, b.title, b.author, t.borrow_date
                FROM Transactions t
                JOIN Books b ON t.book_id = b.book_id
                WHERE t.member_id = %s AND t.return_date IS NULL
            """
            cursor.execute(query, (self.member_id,))
            books = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, book in enumerate(books):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                borrow_date = book[3].strftime("%Y-%m-%d") if hasattr(book[3], 'strftime') else book[3]
                self.tree.insert("", END, values=(book[0], book[1], book[2], borrow_date), tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def return_book(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a book to return.")
            return

        transaction = self.tree.item(selected, 'values')
        transaction_id = transaction[0]

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Update the return_date to today's date
            update_query = """
                UPDATE Transactions
                SET return_date = CURDATE()
                WHERE transaction_id = %s AND member_id = %s AND return_date IS NULL
            """
            cursor.execute(update_query, (transaction_id, self.member_id))
            if cursor.rowcount == 0:
                messagebox.showerror("Return Error", "This book has already been returned or does not exist.")
                return

            # Optionally, update Books quantity by incrementing by 1
            # First get the book_id related to this transaction
            cursor.execute("SELECT book_id FROM Transactions WHERE transaction_id = %s", (transaction_id,))
            book_id = cursor.fetchone()[0]

            cursor.execute("UPDATE Books SET quantity = quantity + 1 WHERE book_id = %s", (book_id,))

            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
            self.load_borrowed_books()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################





##################################################################################################################
class ViewFinesPage:
    def __init__(self, master, member_id):
        self.member_id = member_id
        self.window = Toplevel(master)
        self.window.withdraw()  # Hide window immediately

        self.window.title("My Fines")
        self.window.geometry("900x600")

        try:
            image_path = "/Users/macbookairm3/Desktop/image of library/6920933.jpg"
            if not os.path.isfile(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")

            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            self.bg_label = Label(self.window, image=self.bg_photo)
            self.bg_label.image = self.bg_photo
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()

        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image:\n{e}")

        # Setup widgets on top
        tk.Label(self.window, text="My Fines", font=("Arial", 16, "bold"), bg="#ffffff").place(x=20, y=20)

        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=60, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("FineID", "TransactionID", "Amount", "Status"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        self.tree.heading("FineID", text="Fine ID")
        self.tree.heading("TransactionID", text="Transaction ID")
        self.tree.heading("Amount", text="Amount (AED)")
        self.tree.heading("Status", text="Status")

        self.tree.column("FineID", width=80, anchor=CENTER)
        self.tree.column("TransactionID", width=120, anchor=CENTER)
        self.tree.column("Amount", width=100, anchor=E)
        self.tree.column("Status", width=100, anchor=CENTER)

        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_fines()

        self.window.update_idletasks()
        self.window.deiconify()  # Show window when fully ready

    # ... load_fines method unchanged ...


    def load_fines(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = """
                SELECT fine_id, transaction_id, amount, status
                FROM Fines
                WHERE member_id = %s
                ORDER BY fine_id DESC
            """
            cursor.execute(query, (self.member_id,))
            fines = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())

            if not fines:
                messagebox.showinfo("No Fines", "You have no fines at the moment.")
                return

            for i, fine in enumerate(fines):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, values=fine, tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error loading fines: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################






##################################################################################################################
class UpdateProfilePage:
    def __init__(self, master, member_id):
        self.member_id = member_id
        self.window = Toplevel(master)
        self.window.title("Update Profile")
        self.window.geometry("900x600")

        # Background
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/top-view-books-with-copy-space.jpg")
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        Label(self.window, text="Update Your Profile", font=("Arial", 16, "bold"), bg="#ffffff").place(x=330, y=30)

        # Checkboxes to choose what to update
        self.update_email = BooleanVar()
        self.update_phone = BooleanVar()
        self.update_dept = BooleanVar()

        Checkbutton(self.window, text="Update Email", variable=self.update_email,
                    font=("Arial", 25), bg="#ffffff", command=self.toggle_fields).place(x=100, y=100)
        Checkbutton(self.window, text="Update Phone", variable=self.update_phone,
                    font=("Arial", 25), bg="#ffffff", command=self.toggle_fields).place(x=100, y=200)
        Checkbutton(self.window, text="Update Department", variable=self.update_dept,
                    font=("Arial", 25), bg="#ffffff", command=self.toggle_fields).place(x=100, y=300)

        # Input fields (initially hidden)
        self.email_label = Label(self.window, text="New Email:", font=("Arial", 12), bg="#ffffff")
        self.email_entry = Entry(self.window, width=40)

        self.phone_label = Label(self.window, text="New Phone:", font=("Arial", 12), bg="#ffffff")
        self.phone_entry = Entry(self.window, width=40)

        self.dept_label = Label(self.window, text="New Department:", font=("Arial", 12), bg="#ffffff")
        self.dept_entry = Entry(self.window, width=40)

        # Update Button
        Button(self.window, text="Update", font=("Arial", 20), command=self.update_profile).place(x=400, y=400)

    def toggle_fields(self):
    # Show/hide email field next to its checkbox
        if self.update_email.get():
            self.email_label.place(x=350, y=100)
            self.email_entry.place(x=450, y=100)
        else:
            self.email_label.place_forget()
            self.email_entry.place_forget()

    # Show/hide phone field next to its checkbox
        if self.update_phone.get():
            self.phone_label.place(x=350, y=200)
            self.phone_entry.place(x=450, y=200)
        else:
            self.phone_label.place_forget()
            self.phone_entry.place_forget()

    # Show/hide department field next to its checkbox
        if self.update_dept.get():
            self.dept_label.place(x=380, y=300)
            self.dept_entry.place(x=500, y=300)
        else:
            self.dept_label.place_forget()
            self.dept_entry.place_forget()


    def update_profile(self):
        update_fields = []
        update_values = []

        if self.update_email.get():
            email = self.email_entry.get().strip()
            if not email:
                messagebox.showwarning("Input Error", "Please enter a new email.")
                return
            update_fields.append("email = %s")
            update_values.append(email)

        if self.update_phone.get():
            phone = self.phone_entry.get().strip()
            if not phone:
                messagebox.showwarning("Input Error", "Please enter a new phone number.")
                return
            update_fields.append("phone = %s")
            update_values.append(phone)

        if self.update_dept.get():
            dept = self.dept_entry.get().strip()
            if not dept:
                messagebox.showwarning("Input Error", "Please enter a new department.")
                return
            update_fields.append("department = %s")
            update_values.append(dept)

        if not update_fields:
            messagebox.showwarning("No Selection", "Please select at least one field to update.")
            return

        update_query = f"UPDATE Members SET {', '.join(update_fields)} WHERE member_id = %s"
        update_values.append(self.member_id)

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()
            cursor.execute(update_query, tuple(update_values))
            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################





##################################################################################################################
class MemberPage:
    def __init__(self, master, member_id):
        self.member_id = member_id  # ✅ This fixes the error
        self.window = Toplevel(master)
        self.window.title(f"Member Page - ID: {self.member_id}")

        # You can add other widgets below as needed
        label = Label(self.window, text=f"Welcome Member ID: {self.member_id}", font=("Arial", 14))
        label.pack(pady=20)

        # Continue building your MemberPage GUI here
        # Get screen size dynamically
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")

        # Load and resize background image
        image_2 = Image.open("/Users/macbookairm3/Desktop/image of library/pexels-rafael-cosquiere-1059286-2041540.jpg")
        image_2 = image_2.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.photo_2 = ImageTk.PhotoImage(image_2)

        self.bg_label = Label(self.window, image=self.photo_2)
        self.bg_label.image = self.photo_2  # keep a reference
        self.bg_label.place(x=0, y=0, width=screen_width, height=screen_height)

        # Button layout settings
        btn_width = 240
        btn_height = 60
        x_gap = 50  # Smaller gaps look better visually when centered
        y_gap = 30
        cols = 3
        rows = 3

        # Calculate actual width and height of grid
        total_width = btn_width * cols + x_gap * (cols - 1)
        total_height = btn_height * rows + y_gap * (rows - 1)

        # Perfectly center the grid
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        # Function to place a button at grid position
        def place_button(text, row, col, command=None):
            x = start_x + col * (btn_width + x_gap)
            y = start_y + row * (btn_height + y_gap)
            Button(self.window, text=text, font=("Arial", 16), width=20, command=command).place(x=x, y=y, width=btn_width, height=btn_height)

        # Grid placement of buttons
        place_button("Search Books", 0, 0, command=lambda: SearchBooksPage(self.window))
        place_button("View Borrowed Books", 0, 1, command=lambda: ViewBorrowedBooksPage(self.window, member_id=self.member_id))

        place_button("Request Book", 0, 2, command=lambda: RequestBookPage(self.window, member_id=self.member_id))
            # Replace with actual member ID


        place_button("Return Book", 1, 0 , command=lambda: ReturnBookPage(self.window, member_id=self.member_id))
        place_button("View Fine", 1, 1, command=lambda: ViewFinesPage(self.window, member_id=self.member_id))

        place_button("Update Profile", 1, 2, command=lambda: UpdateProfilePage(self.window, member_id=self.member_id))
        place_button("Log Out", 2, 1, command=self.window.destroy)
##################################################################################################################






##################################################################################################################
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    MemberPage(root)
    root.mainloop()
