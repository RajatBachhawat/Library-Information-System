from tkinter import *
from tkinter import ttk
from colors import *
from availabilityWindow import *
from helperFrames import ScrollableFrame
from bookHandler import SplitTableEntry, JoinTableEntry
from helperFunctions import GetBookInfoFromUID, GetLibraryMember, IsReservationActive

class ProfileFrame(Frame):
    def __init__(self, master, member):
        super().__init__(master)
        self.master = master
        self.member = member
        self.member = GetLibraryMember(member.GetMemberID())

        self.config(bg = lightorange, pady=210)

        self.titleLabel = Label(self, text="Your Profile")
        self.titleLabel.config(font=(40), bg=orange, fg=white)
        self.titleLabel.grid(column=0, row=0, pady=10)

        self.nameFrame = Frame(self)
        self.nameFrame.config(bg=lightorange)
        self.nameLabel = Label(self.nameFrame, text="Name: " + self.member._name) 
        self.nameLabel.config(font=(12), bg=orange, fg=white)
        self.nameLabel.grid(column=0, row=0, padx = 5, pady = 5)
        self.blanknameLabel = Label(self.nameFrame, bg=lightorange)
        self.blanknameLabel.grid(column=1, row=0, padx=440)
        # self.memberNameLabel = Label(self.nameFrame, text="Chappidi Yoga Satwik")
        # self.memberNameLabel.config(font=(12), bg=orange, fg=white)
        # self.memberNameLabel.grid(column=1, row=0, padx = 5, pady = 5)
        self.nameFrame.grid(column=0, row=1)

        type_shortHand = {
            '<class \'underGraduateStudent.UnderGraduateStudent\'>':'UG',
            '<class \'postGraduateStudent.PostGraduateStudent\'>':'PG',
            '<class \'researchScholar.ResearchScholar\'>':'RS',
            '<class \'facultyMember.FacultyMember\'>':'FM'
        }

        self.memberTypeFrame = Frame(self)
        self.memberTypeFrame.config(bg=lightorange)
        self.memberTypeLabel = Label(self.memberTypeFrame, text="Member Type: " + type_shortHand[str(type(self.member))]) 
        self.memberTypeLabel.config(font=(12), bg=orange, fg=white)
        self.memberTypeLabel.grid(column=0, row=0, padx = 5, pady = 5)
        self.blankmemberTypeLabel = Label(self.memberTypeFrame, bg=lightorange)
        self.blankmemberTypeLabel.grid(column=1, row=0, padx=460)
        # self.memberNameLabel = Label(self.nameFrame, text="Chappidi Yoga Satwik")
        # self.memberNameLabel.config(font=(12), bg=orange, fg=white)
        # self.memberNameLabel.grid(column=1, row=0, padx = 5, pady = 5)
        self.memberTypeFrame.grid(column=0, row=2)

        self.IDFrame = Frame(self)
        self.IDFrame.config(bg=lightorange)
        self.IDLabel = Label(self.IDFrame, text="Member ID: " + self.member._memberID)
        self.IDLabel.config(font=(12), bg=orange, fg=white)
        self.IDLabel.grid(column=0, row=0, padx = 5, pady = 5)
        self.blankIDLabel = Label(self.IDFrame, bg=lightorange)
        self.blankIDLabel.grid(column=1, row=0, padx=460)
        # self.memberIDLabel = Label(self.IDFrame, text="19CS30013")
        # self.memberIDLabel.config(font=(12), bg=orange, fg=white)
        # self.memberIDLabel.grid(column=1, row=0, padx = 5, pady = 5)
        self.IDFrame.grid(column=0, row=3)
        
        self.issuedFrame = Frame(self)
        self.issuedFrame.config(bg=lightorange)
        self.issuedLabel = Label(self.issuedFrame, text="Issued Books:")
        self.issuedLabel.config(font=(12), bg=orange, fg=white)
        self.issuedLabel.grid(column=0, row=0, padx = 5, pady = 5)
        self.blankissuedLabel = Label(self.issuedFrame, bg=lightorange)
        self.blankissuedLabel.grid(column=1, row=0, padx=470)
        self.issuedFrame.grid(column=0, row=4)
        # Show List of Issued books
        # books = [{"Title": "Curry Patter", "UID": "1", "DueDate": "01/07/2021"},
        #          {"Title": "Harry Potter", "UID": "2", "DueDate": "01/08/2021"}
        #         ]
        books = []
        for uid in self.member._listOfBooksIssued:
            books.append(GetBookInfoFromUID(int(uid)))
        
        cols = ('Title', 'UID', 'Issue Date')
        ttk.Style().configure("Treeview", background=orange,
                foreground=white, fieldbackground=lightorange)
        self.listBox = ttk.Treeview(self, columns=cols, show='headings')
        for col in cols:
            self.listBox.heading(col, text=col)   
        for book in books:
            self.listBox.insert("", "end", values=(book["BookName"], book["UniqueID"], book["LastIssued"]))

        self.listBox.grid(column=0, row=5)

        self.reservedFrame = Frame(self)
        self.reservedFrame.config(bg=lightorange)
        self.reservedLabel = Label(self.reservedFrame, text="")
        self.reservedLabel.config(font=(12), bg=orange, fg=white)
        self.reservedLabel.grid(column=0, row=0, padx = 5, pady = 5)
        self.blankreservedLabel = Label(self.reservedFrame, bg=lightorange)
        self.blankreservedLabel.grid(column=1, row=0, padx=420)
        self.reservedFrame.grid(column=0, row=6)
        self.Update()


    def ReservedString(self):
        self.reservedLabel.config(text="Reserved Book: " + str(self.member._reservedBook) + IsReservationActive(str(self.member._reservedBook), self.member._memberID))
        # return str(self.member._reservedBook) + IsReservationActive(str(self.member._reservedBook), self.member._memberID)

    def Update(self):
        self.member = GetLibraryMember(self.member.GetMemberID())
        self.listBox.delete(*self.listBox.get_children())
        self.ReservedString()
        books = []
        for uid in self.member._listOfBooksIssued:
            books.append(GetBookInfoFromUID(int(uid)))
        for book in books:
            self.listBox.insert("", "end", values=(book["BookName"], book["UniqueID"], book["LastIssued"]))

class SearchFrame(Frame):
    def __init__(self, master, member):
        super().__init__(master)
        self.master = master
        self.member = member
        
        self.config(bg = lightorange, pady=230, padx=250)

        self.searchLabel = Label(self, text="Search by Name/Author")
        self.searchLabel.config(font=(12), bg=orange, fg=white)
        self.searchLabel.grid(column=0, row=0, padx=10, pady=10)
        
        self.searchString = StringVar()
        self.searchString.trace("w", lambda name, index, mode, sv=self.searchString: self.SearchBook(sv))

        self.searchEntry = Entry(self, textvariable = self.searchString)
        self.searchEntry.grid(column=0, row=1, ipady=5, ipadx=200)
        self.searchEntry.config(bg=lightorange, fg=white)

        self.resultsFrame = Frame(self)
        self.resultsFrame.config(bg=lightorange)
        self.resultsFrame.grid(column=0, row=2, pady=10, padx=10)

        self.resultsScrollable = ScrollableFrame(self.resultsFrame)
        self.resultsScrollable.config(bg=lightorange)
        self.resultsScrollable.grid(column=0, row=0)

        # self.counter = 0
        self.results = []
        self.resultFrames = []

        self.errorLabel = Label(self, text="")
        self.errorLabel.config(font=(12), bg=orange, fg=white) 


    def SearchBook(self, searchString):
        # print(searchString.get())
        self.RemoveError()
        if self.results:
            del self.results
            self.results = []
        
        self.results = self.member.SearchBook(searchString.get())

        if not self.results:
            self.DisplayError("No results found.")

        if not searchString.get():
            self.RemoveError()
        
        # print(self.results)
        self.UpdateResults()

    def UpdateResults(self):
        if self.resultFrames:
            for frame in self.resultFrames:
                frame.grid_forget()
            del self.resultFrames
            self.resultFrames = []

        for i in range(len(self.results)):
            frame = Frame(self.resultsScrollable.scrollable_frame)
            frame.config(bg=lightorange)
            bookName = self.results[i][1].split('-')
            bookName = " ".join(bookName)
            # print(bookName)
            label = Label(frame, text=bookName)
            label.config(font=(12), bg=orange, fg=white, width=23)
            label.grid(column=0, row=0)

            button = Button(frame, text="Check Availability", command= lambda x=self.results[i]: self.CheckAvailability(x), bg=orange, fg=white)
            button.grid(column=1, row=0)
            frame.grid(column=0, row=i)
            self.resultFrames.append(frame)
            del frame

    def CheckAvailability(self, result):
        response = self.member.CheckAvailabilityOfBook(result[0])
        response = (result[0], response)
        if isinstance(response[1], str):
            if self.member._reservedBook == result[0]:
                self.availWindow = AvailabiltyWindow(2, self.member, response)
            elif self.member._reservedBook != None:
                self.availWindow = AvailabiltyWindow(4, self.member, response)
            else:
                self.availWindow = AvailabiltyWindow(3, self.member, response)
        elif isinstance(response[1], tuple):
            if self.member._reservedBook == result[0]:
                self.availWindow = AvailabiltyWindow(1, self.member, response)
            else:
                self.availWindow = AvailabiltyWindow(0, self.member, response)

    def DisplayError(self, message): 
        self.errorLabel.grid_forget()
        self.errorLabel.config(text=message)
        self.errorLabel.grid(column=0, row=3, pady=10)

    def RemoveError(self):
        self.errorLabel.grid_forget() 