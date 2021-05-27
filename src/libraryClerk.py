from book import Book
from libraryMember import LibraryMember
from underGraduateStudent import UnderGraduateStudent
from bookHandler import BookHandler, JoinTableEntry, SplitTableEntry, UpdateReminders
from datetime import date, datetime, timedelta
from activeReservation import ActiveReservation
import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
db.autocommit = True
cursor = db.cursor(dictionary = True)

class LibraryClerk:
    _penaltyRate = 2
    def __init__(self, employeeID, name):
        self._employeeID = employeeID
        self._name = name
    
    def AddBook(self, bookDetails):
        if not bookDetails[0]:
            raise ValueError("ISBN is missing")

        if not bookDetails[1]:
            raise ValueError("Name is missing")

        if not bookDetails[2]:
            raise ValueError("Author is missing")

        if not bookDetails[3]:
            raise ValueError("Rack No. is missing")

        addBook = ("INSERT INTO BOOKS "
            "VALUES (%(UniqueID)s, %(ISBN)s, %(BookName)s, %(RackNumber)s, %(IssueDate)s, %(IsDisposed)s)")
        dataBook = {
            'UniqueID': None,
            'ISBN': bookDetails[0],
            'BookName': bookDetails[1] + '-by-' + bookDetails[2],
            'RackNumber': bookDetails[3],
            'IssueDate' : date.today(),
            'IsDisposed' : 0
        }
        cursor.execute(addBook, dataBook)
        db.commit()
        cursor.execute("SELECT ISBN FROM RESERVATIONS")
        flag=0
        for row in cursor:
            if(bookDetails[0] == row['ISBN']):
                flag=1
        db.commit()
        if(flag == 1):
            bH = BookHandler.Create()
            bH.CloseBook()
            bH.OpenBook(bookDetails[0])
            cursor.execute("SELECT * FROM BOOKS")
            for rows in cursor:
                if(rows["ISBN"]==bookDetails[0]):
                    if str(rows["UniqueID"]) not in bH.available and str(rows["UniqueID"]) not in bH.taken and str(rows["UniqueID"]) not in bH.readyToClaimUIDs:
                        bH.available.append(str(rows["UniqueID"]))
            db.commit()
            bH.UpdateDatabase()
            bH.CloseBook()
        else:
            book = {
                'ISBN' :  bookDetails[0]
            }
            cursor.execute(("SELECT UniqueID FROM BOOKS WHERE ISBN = %(ISBN)s"),book)
            row = {}
            for rows in cursor:
                row = rows
            db.commit()
            addISBN = ("INSERT INTO RESERVATIONS "
            "VALUES (%(ISBN)s, %(AvailableUIDs)s, %(TakenUIDs)s, %(PendingReservations)s, %(ActiveReservations)s, %(ActiveReservedUIDs)s, %(NumberOfCopiesAvailable)s)")
            dataISBN = {
                'ISBN' : bookDetails[0],
                'AvailableUIDs' : str(row['UniqueID']) + ',',
                'TakenUIDs' : None,
                'PendingReservations' : None,
                'ActiveReservations' : None,
                'ActiveReservedUIDs' : None,
                'NumberOfCopiesAvailable' : 1
            }
            cursor.execute(addISBN, dataISBN)
            db.commit()

    def DeleteBook(self):
        searchBooks = "SELECT ISBN, UniqueID FROM BOOKS WHERE IsDisposed = 1"
        cursor.execute(searchBooks)
        listOfDisposed = []
        for row in cursor:
            listOfDisposed.append([row['ISBN'],row['UniqueID']])
        db.commit()
        for book in listOfDisposed:
            bH = BookHandler.Create()
            bH.CloseBook()
            bH.OpenBook(book[0])
            bH.UpdateBook()
            deleteMemberReservation = ("UPDATE MEMBERS SET ReservedBook = NULL WHERE MemberID = %(MemberID)s")
            member = {
                'MemberID' : None
            }
            book[1]=str(book[1])
            if book[1] in BookHandler.GetAvailableUIDs():
                BookHandler.GetAvailableUIDs().remove(book[1])
            if book[1] in BookHandler.GetActiveReservedUIDs():
                BookHandler.GetActiveReservedUIDs().remove(book[1])
                mem = BookHandler.GetActiveReservations().pop()
                member['MemberID']=mem.memberID
                cursor.execute(deleteMemberReservation,member)
                db.commit()
            bH.CloseBook()
        deleteBook = ("DELETE FROM BOOKS WHERE IsDisposed = 1")
        cursor.execute(deleteBook)
        db.commit()


    def ReturnBook(self, libraryMember : LibraryMember, book : Book):
        if str(book.GetUID()) not in libraryMember._listOfBooksIssued:
            raise ValueError("Book has not been by the member.")
        libraryMember._listOfBooksIssued.remove(str(book.GetUID()))
        libraryMember._numberOfBooksIssued-=1
        joined_string = JoinTableEntry(libraryMember._listOfBooksIssued)
        memberUpdate = ("UPDATE MEMBERS SET ListOfBooksIssued = %(ListOfBooks)s WHERE MemberID = %(MemberID)s")
        listOfBooks = {
            'ListOfBooks' : joined_string,
            'MemberID' : libraryMember._memberID
        }
        cursor.execute(memberUpdate, listOfBooks)
        db.commit()
        bH = BookHandler.Create()
        bH.CloseBook()
        bH.OpenBook(book)
        bH.ReturnSelected(libraryMember._memberID)
        bH.CloseBook()
        # UpdateReminders()
    def CollectPenalty(self, libraryMember: LibraryMember,  book: Book):
        daysInPossession = (date.today()-book.GetDateOfIssue()).days
        daysOverdue = max(0,(daysInPossession - 30*libraryMember.GetMaxMonthsAllowed()))
        return daysOverdue*LibraryClerk._penaltyRate