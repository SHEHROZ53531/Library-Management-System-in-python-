import random
import string
import smtplib # mail
from email.mime.text import MIMEText # mail
import mysql.connector
from tkinter import *
from member_page import MemberPage
from PIL import Image, ImageTk
from tkinter import Toplevel, Label, Entry, Button, messagebox




# --------------------- Member Login Window ---------------------
class MemberWindow:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Member Login")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        member_window_width = 600
        member_window_height = 500

        x = int((screen_width / 2) - (member_window_width / 2))
        y = int((screen_height / 2) - (member_window_height / 2))

        self.window.geometry(f"{member_window_width}x{member_window_height}+{x}+{y}")

        self.bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/🔥 Free download Bookshelf on WallpaperSafari.jpeg")
        self.bg_image = self.bg_image.resize((member_window_width, member_window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        bg_label = Label(self.window, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        lbl_name = Label(self.window, text="Name:", font=("Arial", 14), bg="white")
        lbl_name.pack(pady=(30, 10))
        self.entry_name = Entry(self.window, font=("Arial", 14))
        self.entry_name.pack(pady=5)

        lbl_password = Label(self.window, text="Password:", font=("Arial", 14), bg="white")
        lbl_password.pack(pady=(30, 10))
        self.entry_password = Entry(self.window, font=("Arial", 14), show="*")
        self.entry_password.pack(pady=5)

        btn_login = Button(self.window, text="Log In", font=("Arial", 14), command=self.submit)
        btn_login.pack(pady=(10, 10))

        btn_register = Button(self.window, text="Register", font=("Arial", 14), command=self.open_register_window)
        btn_register.pack(pady=(10, 20))

    def submit(self):
        name = self.entry_name.get()
        password = self.entry_password.get()

        if not name or not password:
            messagebox.showwarning("Input Error", "Please enter both Name and Password.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            query = "SELECT member_id FROM Members WHERE name = %s AND password = %s"
            cursor.execute(query, (name, password))
            result = cursor.fetchone()

            if result:
                member_id = result[0]
                messagebox.showinfo("Login Success", f"Welcome, {name}!")
                # Pass member_id to MemberPage
                MemberPage(self.window, member_id)
                self.window.withdraw()  # hide login window
            else:
                messagebox.showerror("Login Failed", "Invalid name or password.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def open_register_window(self):
        MemberRegisterWindow(self.window)



# --------------------- Member Registration Window ---------------------
class MemberRegisterWindow:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Member Registration")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        register_window_width = 600
        register_window_height = 550

        x = int((screen_width / 2) - (register_window_width / 2))
        y = int((screen_height / 2) - (register_window_height / 2))

        self.window.geometry(f"{register_window_width}x{register_window_height}+{x}+{y}")

        self.bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/🔥 Free download Bookshelf on WallpaperSafari.jpeg")
        self.bg_image = self.bg_image.resize((register_window_width, register_window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        bg_label = Label(self.window, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(self.window, text="Name:", font=("Arial", 14), bg="white").pack(pady=(20, 5))
        self.entry_name = Entry(self.window, font=("Arial", 14))
        self.entry_name.pack(pady=5)

        Label(self.window, text="Email:", font=("Arial", 14), bg="white").pack(pady=5)
        self.entry_email = Entry(self.window, font=("Arial", 14))
        self.entry_email.pack(pady=5)

        Label(self.window, text="Phone:", font=("Arial", 14), bg="white").pack(pady=5)
        self.entry_phone = Entry(self.window, font=("Arial", 14))
        self.entry_phone.pack(pady=5)

        Label(self.window, text="Department:", font=("Arial", 14), bg="white").pack(pady=5)
        self.entry_department = Entry(self.window, font=("Arial", 14))
        self.entry_department.pack(pady=5)

        btn_register = Button(self.window, text="Register", font=("Arial", 14), command=self.register)
        btn_register.pack(pady=(20, 10))

    def generate_password(self):
        # You can adjust this to generate a stronger password if needed
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def register(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        department = self.entry_department.get()

        if not name or not email or not phone or not department:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        password = self.generate_password()

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Kaleem@123',
                database='Library_Database'
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Members WHERE email = %s", (email,))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Email already registered.")
                return

            query = "INSERT INTO Members (name, email, phone, department, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, email, phone, department, password))
            conn.commit()

            success = self.send_password_email(email, password)
            if success:
                messagebox.showinfo("Registration Success", f"Member registered successfully! Password sent to {email}")
            else:
                messagebox.showwarning("Email Error", f"Password: {password} generated but email failed to send.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def send_password_email(self, to_email, password):
        from_email = "kaleem9739613@gmail.com"
        from_password = "cxxjwngoesoehaqc"  # Your app password

        subject = "Your Library Member Password"
        body = (f"Hello,\n\nYour registration was successful.\n"
                f"Your password is: {password}\n\n"
                f"Please use your name and this password to log in.")

        msg = MIMEText(body)
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False


# --------------------- Main ---------------------
if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # hide main root window
    app = MemberWindow(root)
    root.mainloop()
