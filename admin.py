from tkinter import *
from PIL import Image, ImageTk
import random
import smtplib #mail
from email.mime.text import MIMEText#mail
import mysql.connector
from admin_page import AdminPage

class AdminWindow:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Admin Login")

        # Screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        admin_window_width = 600
        admin_window_height = 500

        x = int((screen_width / 2) - (admin_window_width / 2))
        y = int((screen_height / 2) - (admin_window_height / 2))

        self.window.geometry(f"{admin_window_width}x{admin_window_height}+{x}+{y}")

        self.bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/pexels-emily-252615-768125.jpg")
        self.bg_image = self.bg_image.resize((admin_window_width, admin_window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        bg_label = Label(self.window, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        lbl_username = Label(self.window, text="Username:", font=("Arial", 14), bg="white")
        lbl_username.pack(pady=(30, 10))
        self.entry_username = Entry(self.window, font=("Arial", 14))
        self.entry_username.pack(pady=5)

        lbl_password = Label(self.window, text="Password:", font=("Arial", 14), bg="white")
        lbl_password.pack(pady=(30, 10))
        self.entry_password = Entry(self.window, font=("Arial", 14), show="*")
        self.entry_password.pack(pady=5)

        btn_login = Button(self.window, text="Log In", font=("Arial", 14), command=self.submit)
        btn_login.pack(pady=(10, 10))

        btn_register = Button(self.window, text="Register", font=("Arial", 14), command=self.open_register_window)
        btn_register.pack(pady=(10, 20))

    def submit(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kaleem@123',
            database='Library_Database'
        )
        cursor = conn.cursor()

        query = "SELECT * FROM Admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            print("Login successful, opening Admin Dashboard.")
            self.window.destroy()
            AdminPage(self.window.master)
        else:
            print("Invalid username or password.")

        cursor.close()
        conn.close()

    def open_register_window(self):
        RegisterWindow(self.window)

class RegisterWindow:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Admin Registration")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        register_window_width = 600
        register_window_height = 400

        x = int((screen_width / 2) - (register_window_width / 2))
        y = int((screen_height / 2) - (register_window_height / 2))

        self.window.geometry(f"{register_window_width}x{register_window_height}+{x}+{y}")

        self.bg_image = Image.open("/Users/macbookairm3/Desktop/image of library/pexels-emily-252615-768125.jpg")
        self.bg_image = self.bg_image.resize((register_window_width, register_window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        bg_label = Label(self.window, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        lbl_username = Label(self.window, text="Username:", font=("Arial", 14), bg="white")
        lbl_username.pack(pady=(30, 10))
        self.entry_username = Entry(self.window, font=("Arial", 14))
        self.entry_username.pack(pady=5)

        lbl_email = Label(self.window, text="Email:", font=("Arial", 14), bg="white")
        lbl_email.pack(pady=(10, 10))
        self.entry_email = Entry(self.window, font=("Arial", 14))
        self.entry_email.pack(pady=5)

        btn_register = Button(self.window, text="Register", font=("Arial", 14), command=self.register)
        btn_register.pack(pady=(20, 20))

    def generate_password(self):
        return ''.join(random.choices('0123456789', k=4))

    def register(self):
        username = self.entry_username.get()
        email = self.entry_email.get()

        if not username or not email:
            print("Please fill out both Username and Email fields.")
            return

        password = self.generate_password()

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Kaleem@123',
            database='Library_Database'
        )
        cursor = conn.cursor()

        try:
            query = "INSERT INTO Admins (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            conn.commit()
            print(f"Admin {username} registered successfully.")

            success = self.send_password_to_email(email, password)
            if success:
                print("Password email sent successfully!")
            else:
                print("Failed to send password email.")

        except mysql.connector.Error as err:
            print(f"Database error: {err}")

        cursor.close()
        conn.close()

    def send_password_to_email(self, to_email, password):
        from_email = "kaleem9739613@gmail.com"
        from_password = "cxxjwngoesoehaqc"  # App-specific password

        subject = "Your Admin Registration Password"
        body = f"Hello,\n\nYour admin registration was successful. Your generated 4-digit password is: {password}\n\nPlease keep it safe."

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
            print(f"Password successfully sent to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

if __name__ == "__main__":
    root = Tk()
    app = AdminWindow(root)
    root.mainloop()
