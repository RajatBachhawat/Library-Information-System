from tkinter import *
from colors import *
from clerkFrames import *

class ClerkHomeWindow(Frame):
    # pass member object
    def __init__(self, master, mainWindow, clerk):
        super().__init__(master)
        self.master = master
        self.mainWindow = mainWindow
        self.clerk = clerk

        self.currFrame = ""

        self.config(bg=orange)

        self.leftFrame = Frame(self)
        self.leftFrame.config(bg=orange)

        self.employeeIDFrame = Frame(self.leftFrame)
        self.employeeIDFrame.config(bg=lightorange)
        self.employeeIDLabel = Label(self.employeeIDFrame, text="Employee ID: " + self.clerk._employeeID)
        self.employeeIDLabel.config(font=(12), bg=orange, fg=white)
        self.employeeIDLabel.grid(column=0, row=0, padx=80, pady=5)
        self.employeeIDFrame.grid(column=0, row=0, padx=5, pady=5)

        self.employeeOptionsFrame = Frame(self.leftFrame)
        self.employeeOptionsFrame.config(bg=lightorange)
        self.homeButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Home", command=self.ShowHome)
        self.homeButton.grid(column=0, row=0, pady=10, padx=80)
        self.addBookButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Add Book", command=self.ShowAddBook)
        self.addBookButton.grid(column=0, row=1, pady=10, padx=80)
        self.deleteBookButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Delete Book", command=self.ShowDeleteBook)
        self.deleteBookButton.grid(column=0, row=2, pady=10, padx=120)
        self.returnBookButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Return Book", command=self.ShowReturnBook)
        self.returnBookButton.grid(column=0, row=3, pady=10, padx=120)
        self.logoutButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Logout", command=self.Logout)
        self.logoutButton.grid(column=0, row=4, pady=10, padx=80)
        self.blankLabel = Label(self.employeeOptionsFrame, bg=lightorange)
        self.blankLabel.grid(column=0, row=5, pady=250)
        self.employeeOptionsFrame.grid(column=0, row=1, padx=5, pady=5)

        self.leftFrame.grid(column=0, row=0)

        self.rightFrame = Frame(self)
        self.rightFrame.config(bg=lightorange)
        self.rightFrame.grid(column=1, row=0)

        # # self.ShowReminder("Hello World")
        # # self.RemoveReminder()
        self.ShowHome()
        # self.ShowSearchBook()

    def ShowHome(self):
        if self.currFrame:
            self.currFrame.grid_forget()
        if not hasattr(self, 'homeFrame'):
            self.homeFrame = Frame(self.rightFrame)
            self.homeFrame.config(bg=lightorange)
            self.welcomeLabel = Label(self.homeFrame, text="Welcome to Library Information System!\n We hope you have a great day at the library.")
            self.welcomeLabel.config(font=(12), bg=orange, fg=white)
            self.welcomeLabel.grid(column=0, row=0, padx = 350, pady = 395)
        self.currFrame = self.homeFrame
        self.homeFrame.grid(column=0, row = 0)

    def ShowAddBook(self):
        if self.currFrame:
            self.currFrame.grid_forget()
        if not hasattr(self, 'addBookFrame'):
            self.addBookFrame = AddBookFrame(self.rightFrame, self.clerk)
            
        self.currFrame = self.addBookFrame
        self.addBookFrame.grid(column=0, row=0, pady=10)

    def ShowDeleteBook(self):
        if self.currFrame:
            self.currFrame.grid_forget()
        if not hasattr(self, 'deleteBookFrame'):
            self.deleteBookFrame = DeleteBookFrame(self.rightFrame, self.clerk)
            
        self.currFrame = self.deleteBookFrame
        self.deleteBookFrame.grid(column=0, row=0, pady=10)

    def ShowReturnBook(self):
        if self.currFrame:
            self.currFrame.grid_forget()

        if not hasattr(self, 'returnBookFrame'):
            self.returnBookFrame = ReturnBookFrame(self.rightFrame, self.clerk)
            
        self.currFrame = self.returnBookFrame
        self.returnBookFrame.grid(column=0, row=0, pady=10)

    def Logout(self):
        self.mainWindow.ShowLogin()