from tkinter import *
from colors import *
from memberFrames import *
from helperFrames import ScrollableFrame

class MemberHomeWindow(Frame):
    # pass member object
    def __init__(self, master, mainWindow, member):
        super().__init__(master)
        self.master = master
        self.mainWindow = mainWindow
        self.member = member

        self.member.UpdateFromDatabase()

        self.currFrame = ""

        self.config(bg=orange)

        self.leftFrame = Frame(self)
        self.leftFrame.config(bg=orange)

        self.memberIDFrame = Frame(self.leftFrame)
        self.memberIDFrame.config(bg=lightorange)
        self.memberIDLabel = Label(self.memberIDFrame, text="Member ID: " + self.member._memberID)
        self.memberIDLabel.config(font=(12), bg=orange, fg=white)
        self.memberIDLabel.grid(column=0, row=0, padx=80, pady=5)
        self.memberIDFrame.grid(column=0, row=0, padx=5, pady=5)

        self.memberOptionsFrame = Frame(self.leftFrame)
        self.memberOptionsFrame.config(bg=lightorange)
        self.homeButton = Button(self.memberOptionsFrame, bg=orange, fg=white, text="Home", command=self.ShowHome)
        self.homeButton.grid(column=0, row=0, pady=10, padx=80)
        self.profileButton = Button(self.memberOptionsFrame, bg=orange, fg=white, text="Your Profile", command=self.ShowProfile)
        self.profileButton.grid(column=0, row=1, pady=10, padx=80)
        self.searchBookButton = Button(self.memberOptionsFrame, bg=orange, fg=white, text="Search Book", command=self.ShowSearchBook)
        self.searchBookButton.grid(column=0, row=2, pady=10, padx=120)
        self.logoutButton = Button(self.memberOptionsFrame, bg=orange, fg=white, text="Logout", command=self.Logout)
        self.logoutButton.grid(column=0, row=3, pady=10, padx=80)
        self.blankLabel = Label(self.memberOptionsFrame, bg=lightorange)
        self.blankLabel.grid(column=0, row=4, pady=150)
        self.memberOptionsFrame.grid(column=0, row=1, padx=5, pady=5)

        self.reminderFrame = Frame(self.leftFrame)
        self.reminderFrame.config(bg=lightorange)
        self.reminderLabel = Label(self.reminderFrame, text="Reminders")
        self.reminderLabel.config(font=(12), bg=orange, fg=white, width=20)
        self.reminderLabel.grid(column=0, row=0, padx=75, pady=5)
        # self.messageLabel = Label(self.reminderFrame)
        # self.messageLabel.config(font=(12), bg=lightorange, fg=white)
        # self.messageLabel.grid(column=0, row=1, padx=10, pady=5)
        # self.blankLabel2 = Label(self.reminderFrame, bg=lightorange)
        # self.blankLabel2.grid(column=0, row=2, pady=85)
        overdue = self.member.CheckForReminder()
        # overdue = ['5', '7']
        cols = ('Reminders')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self.reminderFrame, columns=cols, show='tree')
        # for col in cols:
        #     self.listBox.heading(col, text=col)   
        for uid in overdue:
            self.listBox.insert("", "end", text=uid + ": Book is overdue")

        self.listBox.grid(column=0, row=1)
        self.reminderFrame.grid(column=0, row=2, padx=5, pady=5)

        self.leftFrame.grid(column=0, row=0)

        self.rightFrame = Frame(self)
        self.rightFrame.config(bg=lightorange)
        # self.rightLabel = Label(self.rightFrame, text="right")
        # self.rightLabel.grid(column=0, row=0, padx = 100)
        self.rightFrame.grid(column=1, row=0)

        # self.ShowReminder("Hello World")
        # self.RemoveReminder()
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
            self.welcomeLabel.grid(column=0, row=0, padx = 370, pady = 395)
        self.currFrame = self.homeFrame
        self.homeFrame.grid(column=0, row = 0)

    def ShowProfile(self):
        if self.currFrame:
            self.currFrame.grid_forget()
        if not hasattr(self, 'profileFrame'):
            self.profileFrame = ProfileFrame(self.rightFrame, self.member)
        
        self.profileFrame.Update()
        self.currFrame = self.profileFrame
        self.profileFrame.grid(column=0, row=0, pady=10)

    def ShowSearchBook(self):
        if self.currFrame:
            self.currFrame.grid_forget()
        if not hasattr(self, 'searchFrame'):
            self.searchFrame = SearchFrame(self.rightFrame, self.member)
            
        self.currFrame = self.searchFrame
        self.searchFrame.grid(column=0, row=0, pady=10)

    def Logout(self):
        self.mainWindow.ShowLogin()

    # def ShowReminder(self, message):
    #     self.messageLabel.config(text=message, bg=orange, fg=white)
    #     self.messageLabel.grid(column=0, row=1, padx=10, pady = 5)
    #     self.blankLabel2.grid(column=0, row=2, pady=85)

    # def RemoveReminder(self):
    #     self.messageLabel.config(text="", bg=lightorange)
    #     self.messageLabel.grid(column=0, row=1, pady = 5)
    #     self.blankLabel2.grid(column=0, row=2, pady=85)



