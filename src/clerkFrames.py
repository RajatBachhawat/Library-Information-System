from tkinter import *
from colors import *
from tkinter import ttk
from librarianFrames import GetLibraryMember
from helperFunctions import GetLibraryMember, GetBookInfoFromUID
from book import Book
import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)


class AddBookFrame(Frame):
    def __init__(self, master, clerk):
        super().__init__(master)
        self.master = master
        self.clerk = clerk

        self.config(bg=lightorange, padx=370, pady=290)

        self.ISBN = StringVar()
        self.name = StringVar()
        self.author = StringVar()
        self.rackNo = StringVar()

        self.titleLabel = Label(self, text="Add Book")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.ISBNFrame = Frame(self)
        self.ISBNFrame.config(bg=lightorange)
        self.ISBNLabel = Label(self.ISBNFrame, text = " ISBN: ")
        self.ISBNLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.ISBNLabel.grid(column=0, row=0, padx=10)
        self.ISBNEntry = Entry(self.ISBNFrame, textvariable = self.ISBN)
        self.ISBNEntry.grid(column=1, row=0)
        self.ISBNEntry.config(bg=lightorange, fg=white)
        self.ISBNFrame.grid(column=0, row=1, pady=10)

        self.nameFrame = Frame(self)
        self.nameFrame.config(bg=lightorange)
        self.nameLabel = Label(self.nameFrame, text = " Name: ")
        self.nameLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.nameLabel.grid(column=0, row=0, padx=10)
        self.nameEntry = Entry(self.nameFrame, textvariable = self.name)
        self.nameEntry.grid(column=1, row=0)
        self.nameEntry.config(bg=lightorange, fg=white)
        self.nameFrame.grid(column=0, row=2, pady=10)

        self.authorFrame = Frame(self)
        self.authorFrame.config(bg=lightorange)
        self.authorLabel = Label(self.authorFrame, text = " Author: ")
        self.authorLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.authorLabel.grid(column=0, row=0, padx=10)
        self.authorEntry = Entry(self.authorFrame, textvariable = self.author)
        self.authorEntry.grid(column=1, row=0)
        self.authorEntry.config(bg=lightorange, fg=white)
        self.authorFrame.grid(column=0, row=3, pady=10)

        self.rackFrame = Frame(self)
        self.rackFrame.config(bg=lightorange)
        self.rackLabel = Label(self.rackFrame, text = " Rack No.: ")
        self.rackLabel.config(font=(12), bg=orange, fg=white, width=10)
        self.rackLabel.grid(column=0, row=0, padx=10)
        self.rackEntry = Entry(self.rackFrame, textvariable = self.rackNo)
        self.rackEntry.grid(column=1, row=0)
        self.rackEntry.config(bg=lightorange, fg=white)
        self.rackFrame.grid(column=0, row=4, pady=10)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)

        self.addBookButton = Button(self, bg=orange, fg=white, text="Add Book to the Library", command=self.AddBook)
        self.addBookButton.grid(column=0, row=5)

        # self.DisplayError("ERROR")

    def AddBook(self):
        self.RemoveError()
        success = True
        try:
            self.clerk.AddBook([self.ISBN.get(), self.name.get(), self.author.get(), self.rackNo.get()])
        except ValueError as e:
            self.DisplayError(e)
            success = False

        if success:
            self.DisplayError("Book Added Successfully.")

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=6, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget()
    

class DeleteBookFrame(Frame):
    def __init__(self, master, clerk):
        super().__init__(master)
        self.master = master
        self.clerk = clerk

        self.config(bg=lightorange, padx=370, pady=240) 

        self.disposed = self.GetDisposed()

        self.titleLabel = Label(self, text="Delete Books")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.messageLabel = Label(self, text="Here is the list of disposed books,\n Press the button to delete them all.")
        self.messageLabel.config(font=(40), bg=orange, fg=white)
        self.messageLabel.grid(column=0, row=1, pady=10)

        self.disposedFrame = Frame(self)
        self.disposedFrame.config(bg=lightorange)
        # self.scroll = Scrollbar(self.disposedFrame)
        # self.scroll.pack(side = RIGHT, fill = Y)

        # self.disposedListbox = Listbox(self.disposedFrame, yscrollcommand = self.scroll.set, font = ("Arial", 10), selectbackground=orange,
        #         foreground=white, background=lightorange)
        # self.disposedListbox.pack(side = LEFT, fill = BOTH)
        # self.scroll.config(command = self.disposedListbox.yview)

        cols = ('ISBN', 'UID')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self.disposedFrame, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)   
        for book in self.disposed:
            self.listBox.insert("", "end", values=(book[0], book[1]))

        self.listBox.grid(column=0, row=0)

        self.UpdateList()

        self.disposedFrame.grid(column=0, row=2)

        self.deleteBookButton = Button(self, bg=orange, fg=white, text="Delete Books", command=self.DeleteBook)
        self.deleteBookButton.grid(column=0, row=3)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)



    def DeleteBook(self):
        self.RemoveError()
        try:
            self.clerk.DeleteBook()
            self.disposed = self.GetDisposed()
            self.UpdateList()
            self.DisplayError("Books Deleted Successfully")
        except ValueError as e:
            self.DisplayError(e)
    
    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=4, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget() 

    def GetDisposed(self):
        searchBooks = "SELECT ISBN, UniqueID FROM BOOKS WHERE IsDisposed = 1"
        cursor.execute(searchBooks)
        disposed = []
        for row in cursor:
            disposed.append((row['ISBN'],row['UniqueID']))
        db.commit()
        return disposed

    def UpdateList(self):
        self.listBox.delete(*self.listBox.get_children())
        for book in self.disposed:
            self.listBox.insert("", "end", values=(book[0], book[1]))


class ReturnBookFrame(Frame):
    def __init__(self, master, clerk):
        super().__init__(master)
        self.master = master
        self.clerk = clerk

        self.config(bg=lightorange, padx=340, pady=200)     

        self.memberID = StringVar()
        self.issued = []
        self.amount = 0

        self.titleLabel = Label(self, text="Return Book")
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

        self.selectButton = Button(self, bg=orange, fg=white, text="Select", command=self.SelectMember)
        self.selectButton.grid(column=0, row=2)

        self.issuedLabel = Label(self, text="Issued Books: ")
        self.issuedLabel.config(font=(12), bg=orange, fg=white)
        self.issuedLabel.grid(column=0, row=3, padx = 5, pady = 5)

        self.issuedFrame = Frame(self)
        self.issuedFrame.config(bg=lightorange)
        # self.scroll = Scrollbar(self.issuedFrame)
        # self.scroll.pack(side = RIGHT, fill = Y)

        # self.issuedListbox = Listbox(self.issuedFrame, yscrollcommand = self.scroll.set, font = ("Arial", 10), selectbackground=orange,
        #         foreground=white, background=lightorange)
        # self.issuedListbox.pack(side = LEFT, fill = BOTH)
        # self.scroll.config(command = self.issuedListbox.yview)

        cols = ('UniqueID', 'LastIssued')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self.issuedFrame, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)   
        for book in self.issued:
            self.listBox.insert("", "end", values=(book['UniqueID'], book['LastIssued']))

        self.UpdateList()
        self.listBox.grid(column=0, row=0)


        self.issuedFrame.grid(column=0, row=4, pady=10)

        self.returnButton = Button(self, bg=orange, fg=white, text="Return Book", command=self.ReturnBook)
        self.returnButton.grid(column=0, row=5)

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white)

        # self.ShowFine()

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=6, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget() 
    
    def SelectMember(self):
        self.RemoveError()
        # success = True
        if self.issued:
            self.previssued = self.issued
        del self.issued
        self.issued = []
        try:
            member = GetLibraryMember(self.memberID.get())
            for issuedUID in member._listOfBooksIssued:
                self.issued.append(GetBookInfoFromUID(int(issuedUID))) 
            if not self.issued:
                raise ValueError("No Books Issued.")
        except ValueError as e:
            self.DisplayError(e)

        self.UpdateList()
        

    def UpdateList(self):
        if hasattr(self, "previssued"):
            self.listBox.delete(*self.listBox.get_children())
            del self.previssued

        for book in self.issued:
            self.listBox.insert("", "end", values=(book['UniqueID'], book['LastIssued']))

    def ReturnBook(self):
        if not self.listBox.selection():
            self.DisplayError("No book selected.")
            return
        self.RemoveError()
        success = True
        try:
            member = GetLibraryMember(self.memberID.get())
            bookInfo = GetBookInfoFromUID(int(self.listBox.item(self.listBox.selection()[0], "value")[0]))
            book = Book(bookInfo['UniqueID'], bookInfo['ISBN'], bookInfo['LastIssued'])
            self.amount = self.clerk.CollectPenalty(member, book)
            self.clerk.ReturnBook(member, book)
            if self.amount:
                self.ShowFine()
        except ValueError as e:
            self.DisplayError(e)
            success = False
        
        if success:
            self.DisplayError("Book Returned Successfully.")
            self.SelectMember()
            # self.UpdateList()

    def ShowFine(self):
        self.fineRoot = Tk()
        self.fineRoot.geometry("250x150")
        self.fineRoot.wm_title("Fine Collection")
        self.fineRoot.config(bg=orange)
        self.fineFrame = Frame(self.fineRoot)
        self.fineFrame.config(bg=lightorange)#, pady=5, padx=5)
        self.fineLabel = Label(self.fineFrame, text="Please collect " + str(self.amount) + " Rupees.")
        self.fineLabel.config(font=(12), bg=orange, fg=white)
        self.fineLabel.grid(column=0,row=0, pady=10)
        self.fineButton = Button(self.fineFrame, bg=orange, fg=white, text="Collect Fine", command=self.CollectFine)
        self.fineButton.grid(column=0, row=1, pady=10)
        self.fineFrame.grid(column=0, row=0, padx=10, pady=10)

    def CollectFine(self):
        self.fineRoot.destroy()
        self.amount = 0
        # self.DisplayError("Book Returned Successfully.")

