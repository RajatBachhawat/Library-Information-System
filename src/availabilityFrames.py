from tkinter import *
from colors import *
from tkinter import ttk
from helperFunctions import GetLibraryMember, GetBookInfoFromUID, IsBookDisposed
from book import Book

class AvailableFrame(Frame):
    def __init__(self, master, member, response):
        super().__init__(master)

        self.master = master
        self.member = member
        self.response = response

        self.config(bg = lightorange, pady=0)

        self.titleLabel = Label(self, text="Available Books")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text="The following copies of the book are available.\n Please select one to issue.")
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)


        cols = ('UID', 'Rack No.')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self, columns=cols, show='headings', selectmode="browse")
        for col in cols:
            self.listBox.heading(col, text=col)   
        for i in range(len(response[1][0])):
            self.listBox.insert("", "end", values=(response[1][0][i], response[1][1][i]))

        self.listBox.grid(column=0, row=2, padx=10, pady=10)

        self.buttonFrame = Frame(self)
        self.buttonFrame.config(bg=lightorange)
        self.issueButton = Button(self.buttonFrame, bg=orange, fg=white, text="Issue Book", command=self.IssueBook)
        self.issueButton.grid(column=0, row=0, padx=10, pady=10)
        self.cancelButton = Button(self.buttonFrame, bg=orange, fg=white, text="Go Back", command=self.master.destroy)
        self.cancelButton.grid(column=1, row=0)
        self.buttonFrame.grid(column=0,row=3, padx=10, pady=10)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)

    def UpdateList(self):
        response = self.member.CheckAvailabilityOfBook(self.response[0])
        self.listBox.delete(*self.listBox.get_children())
        if not isinstance(response, str):
            for i in range(len(response[0])):
                self.listBox.insert("", "end", values=(response[0][i], response[1][i]))

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=4, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()
    
    def IssueBook(self):
        self.RemoveError()
        success = True
        try:
            bookInfo = GetBookInfoFromUID(int(self.listBox.item(self.listBox.selection()[0], "value")[0]))
            book = Book(bookInfo['UniqueID'], bookInfo['ISBN'], bookInfo['LastIssued'])
            # self.member.IssueBook(book)
        except ValueError as e:
            self.DisplayError(e)
            success = False

        if IsBookDisposed(book.GetUID()) == -1:
            self.DisplayError("Book is marked as Disposed")
            return

        response = self.member.IssueBook(book)
        # print(type(response))
        # print(response)
        
        if response == None:
            self.RemoveError()
            success = False
            self.DisplayError("Issue Limit Exceeded")

        if response == 0:
            self.RemoveError()
            success = False
            self.DisplayError("Book already issued.")
        
        if success:
            self.RemoveError()
            self.DisplayError("Book Issued Successfully.")
            self.UpdateList()

        # self.member.IssueBook()
        # print(self.listBox.item(self.listBox.selection()[0], "value"))
        

class ClaimFrame(Frame):
    def __init__(self, master, member, response):
        super().__init__(master)

        self.master = master
        self.member = member
        self.response = response

        self.config(bg = lightorange, pady=0)

        self.titleLabel = Label(self, text="Claim Available Books")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text="You have an active reservation for this book.\n Please select one to issue.")
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        # response = ([1, 2], [1, 2])
        cols = ('UID', 'Rack No.')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)   
        for i in range(len(response[1][0])):
            self.listBox.insert("", "end", values=(response[1][0][i], response[1][1][i]))

        self.listBox.grid(column=0, row=2, padx=10, pady=10)

        self.buttonFrame = Frame(self)
        self.buttonFrame.config(bg=lightorange)
        self.claimButton = Button(self.buttonFrame, bg=orange, fg=white, text="Claim Book", command=self.ClaimBook)
        self.claimButton.grid(column=0, row=0, padx=10, pady=10)
        self.cancelButton = Button(self.buttonFrame, bg=orange, fg=white, text="Go Back", command=self.master.destroy)
        self.cancelButton.grid(column=1, row=0)
        self.buttonFrame.grid(column=0,row=3, padx=10, pady=10)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)

    def UpdateList(self):
        response = self.member.CheckAvailabilityOfBook(self.response[0])
        self.listBox.delete(*self.listBox.get_children())
        if not isinstance(response, str):
            for i in range(len(response[0])):
                self.listBox.insert("", "end", values=(response[0][i], response[1][i]))


    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=4, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()
    
    def ClaimBook(self):
        self.RemoveError()
        success = True
        try:
            bookInfo = GetBookInfoFromUID(int(self.listBox.item(self.listBox.selection()[0], "value")[0]))
            book = Book(bookInfo['UniqueID'], bookInfo['ISBN'], bookInfo['LastIssued'])
        except ValueError as e:
            self.DisplayError(e)
            success = False
        
        if IsBookDisposed(book.GetUID()) == -1:
            self.DisplayError("Book is marked as Disposed")
            return

        response = self.member.IssueBook(book)

        if response == None:
            success = False
            self.DisplayError("Issue Limit Exceeded")

        if response == 0:
            self.RemoveError()
            success = False
            self.DisplayError("Book already claimed.")

        if success:
            self.DisplayError("Book Issued Successfully.")
            self.UpdateList()
        

class PendingFrame(Frame):
    def __init__(self, master, member, response):
        super().__init__(master)

        self.config(bg = lightorange, pady=0)

        self.titleLabel = Label(self, text="Pending Reservation")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text=response[1])
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        self.buttonFrame = Frame(self)
        self.buttonFrame.config(bg=lightorange)
        # self.claimButton = Button(self.buttonFrame, bg=orange, fg=white, text="Claim Book", command=self.ClaimBook)
        # self.claimButton.grid(column=0, row=0, padx=10, pady=10)
        self.cancelButton = Button(self.buttonFrame, bg=orange, fg=white, text="Go Back", command=self.master.destroy)
        self.cancelButton.grid(column=0, row=0)
        self.buttonFrame.grid(column=0,row=2, padx=10, pady=10)

class ReserveFrame(Frame):
    def __init__(self, master, member, response):
        super().__init__(master)

        self.master = master
        self.member = member
        self.response = response

        self.config(bg = lightorange, pady=0)

        self.titleLabel = Label(self, text="Reserve Book")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text=response[1])
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        self.buttonFrame = Frame(self)
        self.buttonFrame.config(bg=lightorange)
        self.reserveButton = Button(self.buttonFrame, bg=orange, fg=white, text="Reserve Book", command=self.ReserveBook)
        self.reserveButton.grid(column=0, row=0, padx=10, pady=10)
        self.cancelButton = Button(self.buttonFrame, bg=orange, fg=white, text="Go Back", command=self.master.destroy)
        self.cancelButton.grid(column=1, row=0)
        self.buttonFrame.grid(column=0,row=2, padx=10, pady=10)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=3, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()

    def ReserveBook(self):
        self.RemoveError()
        try:
            self.member.ReserveBook(self.response[0])
            self.DisplayError("Book Reserved Successfully")
        except ValueError as e:
            self.DisplayError(e)

class NoReserveFrame(Frame):
    def __init__(self, master, member, response):
        super().__init__(master)

        self.config(bg = lightorange, pady=0)

        self.titleLabel = Label(self, text="Reserve Book")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text=response[1])
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        self.buttonFrame = Frame(self)
        self.buttonFrame.config(bg=lightorange)
        # self.claimButton = Button(self.buttonFrame, bg=orange, fg=white, text="Claim Book", command=self.ClaimBook)
        # self.claimButton.grid(column=0, row=0, padx=10, pady=10)
        self.cancelButton = Button(self.buttonFrame, bg=orange, fg=white, text="Go Back", command=self.master.destroy)
        self.cancelButton.grid(column=0, row=0)
        self.buttonFrame.grid(column=0,row=2, padx=10, pady=10)