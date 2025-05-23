import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import Toplevel, Frame, Label, messagebox,ttk
from datetime import datetime
import tkinter as tk
import os


##############################################################################################################
class AddBookPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Add New Book")
        self.window.geometry("600x500")

        # Load and set background image
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/6920933.jpg")
            bg_image = bg_image.resize((600, 500), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        # Form fields
        Label(self.window, text="Title:", font=("Arial", 12), bg="#ffffff").place(x=50, y=50)
        self.title_entry = Entry(self.window, width=40)
        self.title_entry.place(x=180, y=50)

        Label(self.window, text="Author:", font=("Arial", 12), bg="#ffffff").place(x=50, y=100)
        self.author_entry = Entry(self.window, width=40)
        self.author_entry.place(x=180, y=100)

        Label(self.window, text="Genre:", font=("Arial", 12), bg="#ffffff").place(x=50, y=150)
        self.genre_entry = Entry(self.window, width=40)
        self.genre_entry.place(x=180, y=150)

        Label(self.window, text="Quantity:", font=("Arial", 12), bg="#ffffff").place(x=50, y=200)
        self.quantity_entry = Entry(self.window, width=40)
        self.quantity_entry.place(x=180, y=200)

        Button(self.window, text="Submit", font=("Arial", 12), command=self.submit_book).place(x=250, y=270)

    def submit_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        quantity = self.quantity_entry.get().strip()

        if not (title and author and genre and quantity):
            messagebox.showerror("Input Error", "Please fill all fields")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter numeric value for quantity")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Check for duplicate book title
            cursor.execute("SELECT * FROM Books WHERE title = %s", (title,))
            if cursor.fetchone():
                messagebox.showerror("Duplicate Entry", "Book already exists")
                return

            # Insert new book
            cursor.execute("""
                INSERT INTO Books (title, author, genre, quantity)
                VALUES (%s, %s, %s, %s)
            """, (title, author, genre, quantity))
            conn.commit()

            messagebox.showinfo("Success", "Book added successfully!")
            self.window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
###############################################################################################################





##################################################################################################################
class ViewBooksPage:


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
        table_frame = Frame(self.window, bg="#ffffff")  # Set frame bg white for better readability
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

        # Configure striped row tags
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
class ViewMembersPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("View Members")
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
        Label(self.window, text="Search by Department:", font=("Arial", 12), bg="#ffffff").place(x=20, y=20)
        self.search_dept = Entry(self.window, width=30)
        self.search_dept.place(x=150, y=20)

        Label(self.window, text="Search by Name:", font=("Arial", 12), bg="#ffffff").place(x=470, y=20)
        self.search_name = Entry(self.window, width=30)
        self.search_name.place(x=600, y=20)

        Button(self.window, text="Search", font=("Arial", 12), command=self.search_members).place(x=400, y=60)

        # --- Table Section ---
        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=110, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Member ID", "Name", "Email", "Phone", "Department"),
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
        self.tree.heading("Member ID", text="Member ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Department", text="Department")

        # Define column widths
        self.tree.column("Member ID", anchor=CENTER, width=100)
        self.tree.column("Name", anchor=W, width=200)
        self.tree.column("Email", anchor=W, width=200)
        self.tree.column("Phone", anchor=W, width=150)
        self.tree.column("Department", anchor=W, width=150)

        # Configure striped row tags
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_all_members()

    def update_table(self, members):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, member in enumerate(members):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", END, values=member, tags=(tag,))

    def load_all_members(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT member_id, name, email, phone, department FROM Members")
            members = cursor.fetchall()

            self.update_table(members)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def search_members(self):
        department = self.search_dept.get().strip()
        name = self.search_name.get().strip()

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = "SELECT member_id, name, email, phone, department FROM Members WHERE 1=1"
            values = []

            if department:
                query += " AND department LIKE %s"
                values.append(f"%{department}%")
            if name:
                query += " AND name LIKE %s"
                values.append(f"%{name}%")

            cursor.execute(query, tuple(values))
            members = cursor.fetchall()

            self.update_table(members)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################







##################################################################################################################
class AddPublisherPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Add Publisher")
        self.window.geometry("600x400")

        # Load and set background image
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/top-view-books-with-copy-space.jpg")
            bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        # Labels and Entries
        Label(self.window, text="Publisher Name:", font=("Arial", 12), bg="#ffffff").place(x=50, y=50)
        self.name_entry = Entry(self.window, width=40)
        self.name_entry.place(x=200, y=50)

        Label(self.window, text="Email:", font=("Arial", 12), bg="#ffffff").place(x=50, y=100)
        self.email_entry = Entry(self.window, width=40)
        self.email_entry.place(x=200, y=100)

        Label(self.window, text="Phone:", font=("Arial", 12), bg="#ffffff").place(x=50, y=150)
        self.phone_entry = Entry(self.window, width=40)
        self.phone_entry.place(x=200, y=150)

        Label(self.window, text="Address:", font=("Arial", 12), bg="#ffffff").place(x=50, y=200)
        self.address_entry = Entry(self.window, width=40)
        self.address_entry.place(x=200, y=200)

        Button(self.window, text="Submit", font=("Arial", 12), command=self.submit_publisher).place(x=250, y=270)

    def submit_publisher(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        if not (name and email and phone and address):
            messagebox.showerror("Input Error", "Please fill all fields")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Check for duplicate publisher name
            cursor.execute("SELECT * FROM Publishers WHERE name = %s", (name,))
            if cursor.fetchone():
                messagebox.showerror("Duplicate Entry", "Publisher already exists")
                return

            # Insert new publisher
            cursor.execute("""
                INSERT INTO Publishers (name, email, phone, address)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, address))
            conn.commit()

            messagebox.showinfo("Success", "Publisher added successfully!")
            self.window.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################








#################################################################################################################
class ViewPublishersPage:

    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("View Publishers")
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
        Label(self.window, text="Search by Name:", font=("Arial", 12), bg="#ffffff").place(x=20, y=20)
        self.search_name = Entry(self.window, width=30)
        self.search_name.place(x=160, y=20)

        Button(self.window, text="Search", font=("Arial", 12), command=self.search_publishers).place(x=400, y=60)

        # --- Table Section ---
        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=110, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Name", "Address", "Email", "Phone"),
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
        self.tree.heading("Name", text="Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")

        # Define column widths
        self.tree.column("Name", anchor=W, width=200)
        self.tree.column("Address", anchor=W, width=250)
        self.tree.column("Email", anchor=W, width=200)
        self.tree.column("Phone", anchor=CENTER, width=150)

        # Configure striped row tags
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_all_publishers()

    def update_table(self, publishers):
        self.tree.delete(*self.tree.get_children())
        for i, publisher in enumerate(publishers):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", END, values=publisher, tags=(tag,))

    def load_all_publishers(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT name, address, email, phone FROM Publishers")
            publishers = cursor.fetchall()
            self.update_table(publishers)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def search_publishers(self):
        name = self.search_name.get().strip()

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = "SELECT name, address, email, phone FROM Publishers WHERE 1=1"
            values = []

            if name:
                query += " AND name LIKE %s"
                values.append(f"%{name}%")

            cursor.execute(query, tuple(values))
            publishers = cursor.fetchall()

            self.update_table(publishers)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################







##################################################################################################################
class AdminBorrowRequestsPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("View Borrow Requests")
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

        Label(self.window, text="Borrow Requests:", font=("Arial", 14), bg="#ffffff").place(x=20, y=20)

        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=60, width=860, height=450)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("RequestID", "MemberID", "BookID", "BookTitle", "RequestDate", "Status"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        self.tree.heading("RequestID", text="Request ID")
        self.tree.heading("MemberID", text="Member ID")
        self.tree.heading("BookID", text="Book ID")
        self.tree.heading("BookTitle", text="Book Title")
        self.tree.heading("RequestDate", text="Request Date")
        self.tree.heading("Status", text="Status")

        self.tree.column("RequestID", width=80, anchor=CENTER)
        self.tree.column("MemberID", width=80, anchor=CENTER)
        self.tree.column("BookID", width=80, anchor=CENTER)
        self.tree.column("BookTitle", width=250, anchor=W)
        self.tree.column("RequestDate", width=120, anchor=CENTER)
        self.tree.column("Status", width=100, anchor=CENTER)

        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_requests()

        # Approve and Reject Buttons
        Button(self.window, text="Approve", font=("Arial", 14), command=self.approve_request).place(x=300, y=530)
        Button(self.window, text="Reject", font=("Arial", 14), command=self.reject_request).place(x=450, y=530)

    def load_requests(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Join to get book title
            query = """
                SELECT br.request_id, br.member_id, br.book_id, b.title, br.request_date, br.status
                FROM BorrowRequests br
                JOIN Books b ON br.book_id = b.book_id
                WHERE br.status = 'Pending'
            """
            cursor.execute(query)
            requests = cursor.fetchall()

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, req in enumerate(requests):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert("", END, values=req, tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def approve_request(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a request to approve.")
            return

        request = self.tree.item(selected, 'values')
        request_id, member_id, book_id, title, request_date, status = request

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Check if enough quantity is available
            cursor.execute("SELECT quantity FROM Books WHERE book_id = %s", (book_id,))
            quantity = cursor.fetchone()[0]

            if quantity <= 0:
                messagebox.showerror("Error", "No copies available to approve this request.")
                return

            # Update BorrowRequests status to 'Approved'
            cursor.execute("UPDATE BorrowRequests SET status = 'Approved' WHERE request_id = %s", (request_id,))

            # Reduce quantity by 1
            cursor.execute("UPDATE Books SET quantity = quantity - 1 WHERE book_id = %s", (book_id,))

            # Insert into Transactions: new borrow record with current date, no return date
            borrow_date = datetime.now().strftime('%Y-%m-%d')
            cursor.execute(
                "INSERT INTO Transactions (member_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, NULL)",
                (member_id, book_id, borrow_date)
            )

            conn.commit()
            messagebox.showinfo("Success", f"Request {request_id} approved.")

            self.load_requests()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def reject_request(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a request to reject.")
            return

        request = self.tree.item(selected, 'values')
        request_id = request[0]

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Update BorrowRequests status to 'Rejected'
            cursor.execute("UPDATE BorrowRequests SET status = 'Rejected' WHERE request_id = %s", (request_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Request {request_id} rejected.")

            self.load_requests()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################




##################################################################################################################
class ViewBorrowedBooksPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("View Borrowed Books")
        self.window.geometry("950x600")

        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/6920933.jpg")
            bg_image = bg_image.resize((950, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        Label(self.window, text="Search by Member Name:", font=("Arial", 12), bg="#ffffff").place(x=20, y=20)
        self.search_member_name = Entry(self.window, width=30)
        self.search_member_name.place(x=200, y=20)

        Label(self.window, text="Search by Book Title:", font=("Arial", 12), bg="#ffffff").place(x=500, y=20)
        self.search_book_title = Entry(self.window, width=30)
        self.search_book_title.place(x=650, y=20)

        Button(self.window, text="Search", font=("Arial", 12), command=self.search_borrowed_books).place(x=420, y=60)

        table_frame = Frame(self.window, bg="#ffffff")
        table_frame.place(x=20, y=110, width=910, height=460)

        self.tree_scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.tree_scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("Member ID", "Member Name", "Book Title", "Borrow Date", "Return Date"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=1)

        self.tree.heading("Member ID", text="Member ID")
        self.tree.heading("Member Name", text="Member Name")
        self.tree.heading("Book Title", text="Book Title")
        self.tree.heading("Borrow Date", text="Borrow Date")
        self.tree.heading("Return Date", text="Return Date")

        self.tree.column("Member ID", anchor=CENTER, width=80)
        self.tree.column("Member Name", anchor=W, width=180)
        self.tree.column("Book Title", anchor=W, width=250)
        self.tree.column("Borrow Date", anchor=CENTER, width=150)
        self.tree.column("Return Date", anchor=CENTER, width=150)

        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='#f0f0ff')

        self.load_all_borrowed_books()

    def update_table(self, records):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, row in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            # Format dates nicely; show 'Not Returned' if return_date is NULL
            borrow_date = row[3].strftime('%Y-%m-%d') if row[3] else "N/A"
            return_date = row[4].strftime('%Y-%m-%d') if row[4] else "Not Returned"
            self.tree.insert("", END, values=(row[0], row[1], row[2], borrow_date, return_date), tags=(tag,))

    def load_all_borrowed_books(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = """
                SELECT m.member_id, m.name, b.title, t.borrow_date, t.return_date
                FROM Transactions t
                JOIN Members m ON t.member_id = m.member_id
                JOIN Books b ON t.book_id = b.book_id
                ORDER BY t.borrow_date DESC
            """
            cursor.execute(query)
            records = cursor.fetchall()

            self.update_table(records)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def search_borrowed_books(self):
        member_name = self.search_member_name.get().strip()
        book_title = self.search_book_title.get().strip()

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = """
                SELECT m.member_id, m.name, b.title, t.borrow_date, t.return_date
                FROM Transactions t
                JOIN Members m ON t.member_id = m.member_id
                JOIN Books b ON t.book_id = b.book_id
                WHERE 1=1
            """
            params = []
            if member_name:
                query += " AND m.name LIKE %s"
                params.append(f"%{member_name}%")
            if book_title:
                query += " AND b.title LIKE %s"
                params.append(f"%{book_title}%")

            query += " ORDER BY t.borrow_date DESC"

            cursor.execute(query, tuple(params))
            records = cursor.fetchall()

            self.update_table(records)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
##################################################################################################################





##################################################################################################################
class ViewFinesWindow:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("View Fines")
        self.window.geometry("900x600")

        # Set background image FIRST before anything else
        self.set_background()

        # Treeview Frame on top of background
        tree_frame = tk.Frame(self.window, bg="#ffffff", bd=2, relief=tk.RIDGE)
        tree_frame.place(x=50, y=50, width=800, height=500)

        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        columns = ("Fine ID", "Member ID", "Name", "Email", "Department", "Amount", "Status", "Transaction ID")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        # Column Headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        self.load_fines()

    def set_background(self):
        try:
            image_path = "/Users/macbookairm3/Desktop/image of library/6920933.jpg"
            if not os.path.isfile(image_path):
                raise FileNotFoundError(f"Image not found at path: {image_path}")

            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((900, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            # Label for background image
            self.bg_label = Label(self.window, image=self.bg_photo)
            self.bg_label.image = self.bg_photo  # Prevent garbage collection
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image:\n{e}")

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
            SELECT f.fine_id, m.member_id, m.name, m.email, m.department, f.amount, f.status, f.transaction_id
            FROM Fines f
            JOIN Members m ON f.member_id = m.member_id
            WHERE f.status = 'Paid';
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("No Records", "No members have paid fines yet.")
                return

            for row in rows:
                self.tree.insert("", tk.END, values=row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            self.window.destroy()
##################################################################################################################





###############################################################################################################
class UpdateBookCopiesPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Update Book Copies")
        self.window.geometry("600x500")

        # Load and set background image
        try:
            bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/6920933.jpg")
            bg_image = bg_image.resize((600, 500), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.window, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        # Title Label
        Label(self.window, text="Update Book Quantity", font=("Arial", 16, "bold"), bg="#f5f5dc").place(x=180, y=40)

        # Book Title
        Label(self.window, text="Book Title:", font=("Arial", 12), bg="#f5f5dc").place(x=100, y=100)
        self.entry_title = Entry(self.window, font=("Arial", 12))
        self.entry_title.place(x=220, y=100, width=250)

        # Genre
        Label(self.window, text="Genre:", font=("Arial", 12), bg="#f5f5dc").place(x=100, y=160)
        self.entry_genre = Entry(self.window, font=("Arial", 12))
        self.entry_genre.place(x=220, y=160, width=250)

        # New Copies
        Label(self.window, text="New Copies:", font=("Arial", 12), bg="#f5f5dc").place(x=100, y=220)
        self.entry_new_copies = Entry(self.window, font=("Arial", 12))
        self.entry_new_copies.place(x=220, y=220, width=250)

        # Submit Button
        Button(self.window, text="Update", font=("Arial", 12, "bold"), bg="green", fg="white",
               command=self.update_book_copies).place(x=250, y=300, width=100, height=40)

    def update_book_copies(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        new_copies = self.entry_new_copies.get().strip()

        if not title or not genre or not new_copies:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        if not new_copies.isdigit():
            messagebox.showwarning("Input Error", "Copies must be a number.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            # Step 1: Check if the book exists and fetch current quantity
            cursor.execute("SELECT quantity FROM Books WHERE title = %s AND genre = %s", (title, genre))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Not Found", "No book found with the given title and genre.")
                return

            current_quantity = result[0]
            added_copies = int(new_copies)
            updated_quantity = current_quantity + added_copies

            # Step 2: Update with the new total
            cursor.execute("UPDATE Books SET quantity = %s WHERE title = %s AND genre = %s",
                           (updated_quantity, title, genre))
            conn.commit()
            messagebox.showinfo(
                "Success",
                f"Book quantity updated successfully.\nPrevious: {current_quantity}, "
                f"Added: {added_copies}, New Total: {updated_quantity}"
            )

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


###############################################################################################################







##################################################################################################################
class AdminPage:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Admin Dashboard")

        # Get screen size dynamically
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")

        # Load and resize background image
        image_2 = Image.open("/Users/macbookairm3/Desktop/image of library/pexels-rafael-cosquiere-1059286-2041540.jpg")
        image_2 = image_2.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.photo_2 = ImageTk.PhotoImage(image_2)

        self.bg_label = Label(self.window, image=self.photo_2)
        self.bg_label.image = self.photo_2  # Keep a reference
        self.bg_label.place(x=0, y=0, width=screen_width, height=screen_height)

        # Button layout settings
        btn_width = 240
        btn_height = 60
        x_gap = 50
        y_gap = 30
        cols = 3
        rows = 3

        total_width = btn_width * cols + x_gap * (cols - 1)
        total_height = btn_height * rows + y_gap * (rows - 1)

        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2

        def place_button(text, row, col, command=None):
            x = start_x + col * (btn_width + x_gap)
            y = start_y + row * (btn_height + y_gap)
            Button(self.window, text=text, font=("Arial", 16), command=command).place(x=x, y=y, width=btn_width, height=btn_height)

        # Link "Add Books" to AddBookPage
        place_button("Add Books", 0, 0, command=lambda: AddBookPage(self.window))
        place_button("View Books", 0, 1, command=lambda: ViewBooksPage(self.window))
        place_button("View Members", 0, 2, command=lambda: ViewMembersPage(self.window))


        place_button("Add Publishers", 1, 0, command=lambda: AddPublisherPage(self.window))

        place_button("View Publishers", 1, 1, command=lambda: ViewPublishersPage(self.window))

        place_button("View Borrow Request", 1, 2, command=lambda: AdminBorrowRequestsPage(self.window))

        place_button("View Borrowed Books", 2, 0, command=lambda: ViewBorrowedBooksPage(self.window))
        place_button("View Fine", 2, 1, command=lambda: ViewFinesWindow(self.window))
        place_button("Log Out", 2, 2, command=self.window.destroy)
        place_button("Update Book Copies", 3, 1, command=lambda: UpdateBookCopiesPage(self.window))
##################################################################################################################






##################################################################################################################
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    AdminPage(root)
    root.mainloop()
