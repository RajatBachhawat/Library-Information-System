from tkinter import *
from colors import *
from underGraduateStudent import UnderGraduateStudent
from postGraduateStudent import PostGraduateStudent
from researchScholar import ResearchScholar
from facultyMember import FacultyMember
from bookHandler import JoinTableEntry, SplitTableEntry
from helperFunctions import GetLibraryMember, GetBookInfoFromUID
from tkinter import ttk

import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)

class AddMemberFrame(Frame):
    def __init__(self, master, librarian):
        super().__init__(master)
        self.master = master
        self.librarian = librarian

        self.config(bg=lightorange, padx=380, pady=270) 

        self.memberID = StringVar()
        self.name = StringVar()
        self.password = StringVar()
        self.type = StringVar()
        self.optionList = ["UG", "PG", "RS", "FM"]
        self.type.set(self.optionList[0])

        self.titleLabel = Label(self, text="Add Member")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.memberIDFrame = Frame(self)
        self.memberIDFrame.config(bg=lightorange)
        self.memberIDLabel = Label(self.memberIDFrame, text = " Member ID: ")
        self.memberIDLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.memberIDLabel.grid(column=0, row=0, padx=10)
        self.memberIDEntry = Entry(self.memberIDFrame, textvariable = self.memberID)
        self.memberIDEntry.grid(column=1, row=0)
        self.memberIDEntry.config(bg=lightorange, fg=white)
        self.memberIDFrame.grid(column=0, row=1, pady=10)

        self.nameFrame = Frame(self)
        self.nameFrame.config(bg=lightorange)
        self.nameLabel = Label(self.nameFrame, text = " Name: ")
        self.nameLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.nameLabel.grid(column=0, row=0, padx=10)
        self.nameEntry = Entry(self.nameFrame, textvariable = self.name)
        self.nameEntry.grid(column=1, row=0)
        self.nameEntry.config(bg=lightorange, fg=white)
        self.nameFrame.grid(column=0, row=2, pady=10)

        self.passFrame = Frame(self)
        self.passFrame.config(bg=lightorange)
        self.passLabel = Label(self.passFrame, text = " Password: ")
        self.passLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.passLabel.grid(column=0, row=0, padx=10)
        self.passEntry = Entry(self.passFrame, textvariable = self.password, show="*")
        self.passEntry.grid(column=1, row=0)
        self.passEntry.config(bg=lightorange, fg=white)
        self.passFrame.grid(column=0, row=3, pady=10)

        self.opt = OptionMenu(self, self.type, *self.optionList, command=self.SetType)
        self.opt.config(font=(12), bg=orange, fg=label_fg)
        self.opt.grid(column=0, row=4, pady=10)

        self.addMemberButton = Button(self, bg=orange, fg=white, text="Add Member to the System", command=self.AddMember)
        self.addMemberButton.grid(column=0, row=5)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)

        # self.DisplayError("HI")


    def SetType(self, selection):
        self.type.set(selection)

    def AddMember(self):
        self.RemoveError()
        if self.type.get() == "UG":
            self.member = UnderGraduateStudent(self.name.get(), self.memberID.get(), [], None)
        if self.type.get() == "PG":
            self.member = PostGraduateStudent(self.name.get(), self.memberID.get(), [], None)
        if self.type.get() == "RS":
            self.member = ResearchScholar(self.name.get(), self.memberID.get(), [], None)
        if self.type.get() == "FM":
            self.member = FacultyMember(self.name.get(), self.memberID.get(), [], None)
        # print("Adding Member")
        success = True

        if self.password.get() == "":
            self.DisplayError("Required field password is missing.")
            return

        try:
            self.librarian.AddMember(self.member, self.password.get())
        except ValueError as e:
            self.DisplayError(e)
            success = False
        
        if success:
            self.DisplayError("Member Successfully Added.")

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=6, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()

class DeleteMemberFrame(Frame):
    def __init__(self, master, librarian):
        super().__init__(master)
        self.master = master
        self.librarian = librarian

        self.config(bg=lightorange, padx=370, pady=350) 

        self.memberID = StringVar()

        self.titleLabel = Label(self, text="Delete Member")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.memberIDFrame = Frame(self)
        self.memberIDFrame.config(bg=lightorange)
        self.memberIDLabel = Label(self.memberIDFrame, text = " Member ID: ")
        self.memberIDLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.memberIDLabel.grid(column=0, row=0, padx=10)
        self.memberIDEntry = Entry(self.memberIDFrame, textvariable = self.memberID)
        self.memberIDEntry.grid(column=1, row=0)
        self.memberIDEntry.config(bg=lightorange, fg=white)
        self.memberIDFrame.grid(column=0, row=1, pady=10)

        self.deleteMemberButton = Button(self, bg=orange, fg=white, text="Delete Member from the System", command=self.DeleteMember)
        self.deleteMemberButton.grid(column=0, row=5)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white) 

    def DeleteMember(self):
        self.RemoveError()
        success = True
        try:
            member = GetLibraryMember(self.memberID.get())
            self.librarian.RemoveMember(member)
        except ValueError as e:
            self.DisplayError(e)
            success = False
        
        if success:
            self.DisplayError("Member Successfully deleted.")
        # print("Deleting Member")

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=6, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()       


class SendReminderFrame(Frame):
    def __init__(self, master, librarian):
        super().__init__(master)
        self.master = master
        self.librarian = librarian

        self.config(bg=lightorange, padx=340, pady=350) 

        self.titleLabel = Label(self, text="Send Reminders")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text="All members with overdue books will be sent a notiication.")
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        self.sendReminderButton = Button(self, bg=orange, fg=white, text="Send Reminders", command=self.SendReminder)
        self.sendReminderButton.grid(column=0, row=2)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white) 

    def SendReminder(self):
        self.RemoveError()
        try:
            self.librarian.SendReminderToMember()
            self.DisplayError("Reminders Sent Successfully")
        except ValueError as e:
            self.DisplayError(e)
    
    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=3, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget() 

class CheckIssueStats(Frame):
    def __init__(self, master, librarian):
        super().__init__(master)
        self.master = master
        self.librarian = librarian

        self.config(bg=lightorange, padx=340, pady=250)

        self.notIssued = self.GetNotIssued()

        self.titleLabel = Label(self, text="Check Issue Statistics")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text="Here's the list of books that haven't been return in 5 years.\n Select one by one and press Dispose")
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        self.notIssuedFrame = Frame(self)
        self.notIssuedFrame.config(bg=lightorange)
        # self.scroll = Scrollbar(self.notIssuedFrame)
        # self.scroll.pack(side = RIGHT, fill = Y)

        # self.notIssuedListbox = Listbox(self.notIssuedFrame, yscrollcommand = self.scroll.set, font = ("Arial", 10), selectbackground=orange,
        #         foreground=white, background=lightorange)
        # self.notIssuedListbox.pack(side = LEFT, fill = BOTH)
        # self.scroll.config(command = self.notIssuedListbox.yview)

        cols = ('UniqueID', 'LastIssued')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self.notIssuedFrame, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)   
        for book in self.notIssued:
            self.listBox.insert("", "end", values=(book[0], book[1]))

        self.listBox.grid(column=0, row=0)

        self.UpdateList()

        self.notIssuedFrame.grid(column=0, row=2, pady=10)

        self.disposeButton = Button(self, bg=orange, fg=white, text="Dispose Book", command=self.DisposeBook)
        self.disposeButton.grid(column=0, row=3)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white) 

    def GetNotIssued(self):
        return self.librarian.CheckBookIssueStats()

    def UpdateList(self):
        self.listBox.delete(*self.listBox.get_children())
        for book in self.notIssued:
            self.listBox.insert("", "end", values=(book[0], book[1]))

    def DisposeBook(self):
        self.RemoveError()
        success = True

        try:
            self.librarian.DisposeBook(self.listBox.item(self.listBox.selection()[0], "values")[0])
        except ValueError as e:
            self.DisplayError(e)
            success = False
        
        if success:
            self.DisplayError("Book successfully disposed")
        # print("Book Disposed")
    
    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=4, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()         


