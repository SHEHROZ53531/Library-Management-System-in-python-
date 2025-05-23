from tkinter import*
from PIL import ImageTk, Image
from admin import AdminWindow  
from member import MemberWindow

class Library:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("2304x111800")


        image_1 = Image.open("/Users/macbookairm3/Desktop/image of library/top-view-books-with-copy-space.jpg")
        image_1 = image_1.resize((2304, 1118), Image.Resampling.LANCZOS)
        self.photo_1 = ImageTk.PhotoImage(image_1)

        Label_Image_1 = Label(self.root, image=self.photo_1)
        Label_Image_1.place(x=0, y=0, width=2304, height=1118)



        # Add Buttons on the right side
        btn_admin = Button(self.root, text="Librarian", font=("Arial", 35), width=15, command=self.admin_action)
        btn_admin.place(relx=0.70, rely=0.3)

        btn_member = Button(self.root, text="Reader", font=("Arial", 35), width=15, command=self.member_action)
        btn_member.place(relx=0.70, rely=0.5)

    def admin_action(self):
        AdminWindow(self.root)  # open the admin window

    def member_action(self):
        MemberWindow(self.root) 







if __name__ == "__main__":
    root = Tk()
    library = Library(root)
    root.mainloop()

      
