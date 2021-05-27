from tkinter import *
from colors import *
from loginWindow import LoginWindow
from memberHomeWindow import MemberHomeWindow
from clerkHomeWindow import ClerkHomeWindow
from librarianHomeWindow import LibrarianHomeWindow
from underGraduateStudent import UnderGraduateStudent
from libraryClerk import LibraryClerk
from librarian import Librarian
import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)

class MainWindow():
    def __init__(self, master):
        self.master = master
        self.master.title("Library Information System")
        self.master.geometry('1500x900')
        self.master.config(bg=orange)

        self.title = Label(self.master, text="Library Information System", padx=700, pady=10)
        self.title.config(width=10, font=(12), bg=orange, fg=white)
        self.title.grid(column=0, row=0)
        self.currWindow = ""
        self.ShowLogin()
        # self.currWindow.grid_forget()
        # self.ShowMemberHome(UnderGraduateStudent("Chappidi Yoga Satwik", "19CS30013", [], None))
        # self.ShowClerkHome(LibraryClerk("LIB0021", "Sam"))
        # self.ShowLibrarianHome(Librarian("LIB0001", "Harry"))

    def ShowLogin(self):
        if self.currWindow:
            self.currWindow.grid_forget()
        if not hasattr(self, 'login'):
            self.login = LoginWindow(self.master, self)
        self.currWindow = self.login
        self.login.grid(column=0, row=1)

    def ShowMemberHome(self, member):
        if self.currWindow:
            self.currWindow.grid_forget()
        if hasattr(self, 'memberHome'):
            del self.memberHome
        self.memberHome = MemberHomeWindow(self.master, self, member)
        self.currWindow = self.memberHome
        self.memberHome.grid(column=0, row=1)

    def ShowClerkHome(self, clerk):
        if self.currWindow:
            self.currWindow.grid_forget()
        if hasattr(self, 'clerkHome'):
            del self.clerkHome
        self.clerkHome = ClerkHomeWindow(self.master, self, clerk)
        self.currWindow = self.clerkHome
        self.clerkHome.grid(column=0, row=1)

    def ShowLibrarianHome(self, librarian):
        if self.currWindow:
            self.currWindow.grid_forget()
        if hasattr(self, 'librarianHome'):
            del self.librarianHome
        self.librarianHome = LibrarianHomeWindow(self.master, self, librarian)
        self.currWindow = self.librarianHome
        self.librarianHome.grid(column=0, row=1)


# INSERT IGNORE INTO EMPLOYEES VALUES ('LIB0001', 'Neha', 'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==');
cursor.execute("INSERT IGNORE INTO EMPLOYEES VALUES ('LIB0001', 'Neha', 'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==');")
db.commit()
cursor.execute("INSERT IGNORE INTO EMPLOYEES VALUES ('LIB0068', 'Rajat', 'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==');")
db.commit()
root = Tk()
app = MainWindow(root)
root.mainloop()