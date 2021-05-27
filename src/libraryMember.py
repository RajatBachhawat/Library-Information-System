import copy
from abc import ABC, abstractmethod
from book import Book
from bookHandler import BookHandler, SplitTableEntry, JoinTableEntry, UpdateReminders
from datetime import date, datetime, timedelta
import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)

class LibraryMember(ABC):
    def __init__(self, *args):
        ABC.__init__(self)
        if len(args) == 1:
            orig = args[0]
            self._memberID = copy.deepcopy(orig._memberID)
            self._name = copy.deepcopy(orig._name)
            self._listOfBooksIssued = copy.deepcopy(orig._listOfBooksIssued)
            self._reservedBook = copy.deepcopy(orig._reservedBook) # consider changing the name to reserved ISBN?
            self._numberOfBooksIssued = orig._numberOfBooksIssued
        else:
            self._memberID = args[1]
            self._name = args[0]
            self._listOfBooksIssued = args[2]
            self._reservedBook = args[3]
            self._numberOfBooksIssued = len(self._listOfBooksIssued)
    def __str__(self):
        return '(' + str(self._memberID) + ', ' + str(self._name) + ', ' + str(self._listOfBooksIssued) + ', ' + str(self._reservedBook) + ', ' + str(self._numberOfBooksIssued) + ')'

    def GetMemberID(self):
        return self._memberID
    def GetName(self):
        return self._name
    def GetNumberOfBookIssued(self):
        return self._numberOfBooksIssued
    def GetReservedBook(self):
        return self._reservedBook

    def CheckForReminder(self):
        # UpdateReminders()
        overdue = []
        stro = {
            'MemberID': self._memberID
        }
        cursor.execute(("SELECT GotReminder from members WHERE MemberID = %(MemberID)s"), stro)
        row = cursor.fetchone()
        db.commit()
        if(row['GotReminder']):
            for UID in self._listOfBooksIssued:
                book = {
                    'bookUID' : int(UID)
                }
                cursor2 = db.cursor(dictionary = True)
                cursor2.execute(("SELECT LastIssued FROM BOOKS WHERE UniqueID = %(bookUID)s"),book)
                row2 = cursor2.fetchone()
                db.commit()
                if (date.today() - row2["LastIssued"]).days > 30*self.GetMaxMonthsAllowed():
                    overdue.append(UID)
        if not overdue:
            mem = {
                'memId' : self._memberID
            }
            cursor.execute(("UPDATE MEMBERS SET GotReminder = 0 WHERE MemberID = %(memId)s"), mem)
            db.commit()
        return overdue
                    
    def SearchBook(self, searchString):
        # searchKey = input("Enter your search string: ")
        searchKey = '%' + searchString + '%'
        searchBooks = "SELECT DISTINCT ISBN, BookName FROM BOOKS WHERE BookName LIKE %(search)s"
        searchParam = {
            "search" : searchKey
        }
        cursor.execute(searchBooks, searchParam)
        # db.commit()
        searchResults = []
        for row in cursor:
            searchResults.append(("{ISBN}".format(ISBN=row['ISBN']),"{BookName}".format(BookName=row['BookName'])))
        # print(searchResults)
        db.commit()
        return searchResults

    def CheckAvailabilityOfBook(self, ISBN: str):
        bH = BookHandler.Create()
        bH.OpenBook(ISBN)
        bH.UpdateBook()
        if (self._reservedBook == ISBN):
            if(bH.IsActive(self._memberID)):
                rackNos = []
                for UID in bH.GetActiveReservedUIDs():
                    book = {
                        'UniqueID' : int(UID)
                    }
                    cursor.execute("SELECT RackNumber FROM BOOKS WHERE UniqueID = %(UniqueID)s", book)
                    row = cursor.fetchone()
                    db.commit()
                    rackNos.append(str(row['RackNumber']))
                aru = copy.deepcopy(bH.GetActiveReservedUIDs())
                bH.CloseBook()
                return (aru,rackNos)

            else:
                bH.CloseBook()
                return 'Your Reservation is still pending. Pls wait for a few more days'
        else:
            if (bH.GetAvailableUIDs()!=[]):
                rackNos = []
                for UID in bH.GetAvailableUIDs():
                    book = {
                        'UniqueID' : int(UID)
                    }
                    cursor.execute("SELECT RackNumber FROM BOOKS WHERE UniqueID = %(UniqueID)s", book)
                    row = cursor.fetchone()
                    db.commit()
                    rackNos.append(str(row['RackNumber']))
                au = copy.deepcopy(bH.GetAvailableUIDs())
                bH.CloseBook()
                return (au, rackNos)
            else:
                if (self._reservedBook == None):
                    bH.CloseBook()
                    return 'Sorry this book is not available currently,\n Would you like to reserve this book?'
                else:
                    bH.CloseBook()
                    return 'Sorry this book is not available currently,\n and you already have a reservation'
         
    def IssueBook(self, book: Book):
        if not self.CanIssue() :
            # raise ValueError("Issue Limit Exceeded.")
            # print("Hello")
            return None
        if (str(book.GetUID()) in self._listOfBooksIssued):
            # raise ValueError("Book already issued.")
            # print("Yo")
            return 0

        bH = BookHandler.Create()
        bH.CloseBook()
        bH.OpenBook(book)
        bH.IssueSelected(self._memberID)
        self._listOfBooksIssued.append(str(book.GetUID()))
        joined_string = ",".join(self._listOfBooksIssued)
        joined_string = joined_string+','
        cursor.execute(str("UPDATE MEMBERS SET ListOfBooksIssued = \""+joined_string+"\" WHERE MemberID = \""+self._memberID+"\""))
        self._numberOfBooksIssued += 1
        db.commit()
        self.UpdateFromDatabase()
        bH.CloseBook()
        
        # print("Hi")
        return 1

    def ReserveBook(self, ISBN: str):
        if(self.GetReservedBook()!=None):
            raise ValueError("Member can not reserve more than one book.")
        bH = BookHandler.Create()
        bH.CloseBook()
        bH.OpenBook(ISBN)
        if(len(bH.available)!=0):
            bH.CloseBook()
            raise ValueError("Member cannot reserve an ISBN with available UID.")
        bH.ReserveSelected(self._memberID)
        bH.CloseBook()
        self._reservedBook = ISBN
        command = "UPDATE MEMBERS SET ReservedBook = %(book)s WHERE MemberID = %(MemberID)s"
        dici = {
            'book' : ISBN,
            'MemberID' : self._memberID
        }
        cursor.execute(command,dici)
        db.commit()

    #call this on every login
    def UpdateFromDatabase(self):
        if(self._reservedBook!=None):
            bH = BookHandler.Create()
            bH.OpenBook(self._reservedBook)
            bH.UpdateBook()
            bH.CloseBook()
        selectMember = ("SELECT * FROM MEMBERS WHERE MemberID = %(MemberID)s")
        member = {
            'MemberID' : self._memberID
        }
        cursor.execute(selectMember, member)
        #db.commit()
        for row in cursor:
            self._memberID = row['MemberID']
            self._name = row['MemberName']
            self._listOfBooksIssued = SplitTableEntry(row['ListOfBooksIssued'])
            self._reservedBook = row['ReservedBook']
        db.commit()
    @abstractmethod
    def CanIssue(self):
        pass
    @abstractmethod
    def GetMaxBooksAllowed(self):
        pass
    @abstractmethod
    def GetMaxMonthsAllowed(self):
        pass
