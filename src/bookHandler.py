import mysql.connector as mysql
from book import Book
from activeReservation import ActiveReservation
from datetime import date, datetime, timedelta
import mysql.connector as mysql
import copy
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)

# changes
## make all fucntions non static maybe
## no member called currUID
## changes in the arguments of a lot of functions
## might want to pass LIbrary member to IssueBook etc and make changes to its data members then update database using its own method
def UpdateReminders():
    cursor.execute("SELECT * FROM MEMBERS")
    changedMembers = []
    for row in cursor:
        if(row["GotReminder"]==False):
            continue
        BooksIssued = row["ListOfBooksIssued"]
        ListBooksIssued = SplitTableEntry(BooksIssued)
        period = 0
        if(row["MemberType"]=="UG"):
            period = 1
        elif row["MemberType"]=="PG":
            period = 1
        elif row["MemberType"]=="RS":
            period = 3
        else:
            period = 6
        flag = False
        for bookUID in ListBooksIssued:
            book = {
                'bookUID' : int(bookUID)
            }
            cursor2 = db.cursor(dictionary = True)
            cursor2.execute(("SELECT LastIssued FROM BOOKS WHERE UniqueID = %(bookUID)s"),book)
            row2 = cursor2.fetchone()
            db.commit()
            if (date.today() - row2["LastIssued"]).days > 30*self.GetMaxMonthsAllowed():
                flag = True
            # db.commit()
        if flag == False:
            changedMembers.append(row["MemberID"])
    db.commit()
    for member in changedMembers:
        mem = {
                'memId' : member
            }
        cursor.execute(("UPDATE MEMBERS SET GotReminder = 0 WHERE MemberID = %(memId)s"), mem)
        db.commit()
    # db.commit()

class BookHandler:
    instance = None
    currUID = None
    currISBN = None
    available = []
    taken = []
    waitList = []
    readyToClaimUsers = []
    readyToClaimUIDs = []
    numberOfCopies = 0
    
    @staticmethod 
    # Static Access Method
    def Create():
        if BookHandler.instance == None:
            BookHandler()
        return BookHandler.instance
    
    # Virtually private constructor
    def __init__(self):
        if BookHandler.instance != None:
            raise Exception("This class is a singleton!")
        else:
            BookHandler.instance = self

    @staticmethod 
    def OpenBook(book):
        if (isinstance(book,str)):
            BookHandler.currISBN = book
        elif(isinstance(book,Book)):
            BookHandler.currISBN = book.GetISBN()
            BookHandler.currUID = str(book.GetUID())

        selectISBN = ("SELECT * FROM RESERVATIONS WHERE ISBN = %(ISBN)s")
        isbn = {
            'ISBN' : BookHandler.currISBN
        }
        cursor.execute(selectISBN, isbn)
        for row in cursor:
            BookHandler.available = SplitTableEntry(row['AvailableUIDs'])
            BookHandler.taken = SplitTableEntry(row['TakenUIDs'])
            BookHandler.waitList = SplitTableEntry(row['PendingReservations'])
            
            activeReservationPair = [x.split('*') for x in SplitTableEntry(row['ActiveReservations'])]
            claimByDateYMD = [x[0].split('-') for x in activeReservationPair]
            claimByDateYMD = [date(int(x[0]), int(x[1]), int(x[2])) for x in claimByDateYMD]
            memberID = [x[1] for x in activeReservationPair]
            for i in range(len(memberID)):
                BookHandler.readyToClaimUsers.append(ActiveReservation(memberID[i], claimByDateYMD[i]))
            
            BookHandler.readyToClaimUIDs = SplitTableEntry(row['ActiveReservedUIDs'])
            BookHandler.numberOfCopies = row['NumberOfCopiesAvailable']
        db.commit()

    @staticmethod
    def UpdateBook():
        deleteMemberReservation = ("UPDATE MEMBERS SET ReservedBook = NULL WHERE MemberID = %(MemberID)s")
        member = {
            'MemberID' : None
        }
        for entry in BookHandler.readyToClaimUsers:
            member['MemberID'] = entry.memberID
            if entry.claimByDate < date.today():
            # if True:
                cursor.execute(deleteMemberReservation, member)
                db.commit()
                if len(BookHandler.waitList): # if pending reservations, then make them active
                    newActive = BookHandler.waitList.pop(0)
                    BookHandler.readyToClaimUsers.append(ActiveReservation(newActive, (datetime.now()+timedelta(days = 7)).date()))
                else:
                    reservationFree = BookHandler.readyToClaimUIDs.pop()
                    BookHandler.available.append(reservationFree)
        BookHandler.readyToClaimUsers = [item for item in BookHandler.readyToClaimUsers if item.claimByDate >= date.today()]
        BookHandler.numberOfCopies = len(BookHandler.available)
        
    
    @staticmethod
    def UpdateDatabase():
        copyavail = copy.deepcopy(BookHandler.available)
        for currUID in BookHandler.available:
            if(len(BookHandler.waitList)==0):
                break
            if(len(copyavail)==0):
                break
            BookHandler.readyToClaimUIDs.append(currUID)
            memberActivated = BookHandler.waitList.pop(0)
            newActive = ActiveReservation(memberActivated, (datetime.now()+timedelta(days = 7)).date())
            BookHandler.readyToClaimUsers.append(newActive)
            copyavail.remove(currUID)
        BookHandler.available = copyavail
        BookHandler.numberOfCopies = len(BookHandler.available)
        readyToClaimUsers = list(map(lambda x: str(x.claimByDate)+'*'+x.memberID, BookHandler.readyToClaimUsers))        
        updateReservationTable = ("UPDATE RESERVATIONS SET AvailableUIDs = %(AvailableUIDs)s, TakenUIDs = %(TakenUIDs)s, PendingReservations = %(PendingReservations)s, ActiveReservations = %(ActiveReservations)s, ActiveReservedUIDs = %(ActiveReservedUIDs)s, NumberOfCopiesAvailable = %(NumberOfCopiesAvailable)s WHERE ISBN = %(ISBN)s")
        dataReservation = {
            'ISBN' : str(BookHandler.currISBN),
            'AvailableUIDs' : JoinTableEntry(BookHandler.available),
            'TakenUIDs' : JoinTableEntry(BookHandler.taken),
            'PendingReservations' : JoinTableEntry(BookHandler.waitList),
            'ActiveReservations' : JoinTableEntry(readyToClaimUsers),
            'ActiveReservedUIDs' : JoinTableEntry(BookHandler.readyToClaimUIDs),
            'NumberOfCopiesAvailable' : BookHandler.numberOfCopies
        }
        cursor.execute(updateReservationTable, dataReservation)
        db.commit()
    
    @staticmethod
    def IssueSelected(memberID: str):
        BookHandler.taken.append(BookHandler.currUID)
        if(BookHandler.currUID in BookHandler.available):
            BookHandler.available.remove(BookHandler.currUID)
        elif(BookHandler.currUID in BookHandler.readyToClaimUIDs):
            BookHandler.readyToClaimUIDs.remove(BookHandler.currUID)
            BookHandler.readyToClaimUsers = [x for x in BookHandler.readyToClaimUsers if x.memberID != memberID]
            cursor.execute(str("UPDATE MEMBERS SET ReservedBook = NULL WHERE MemberId = \""+memberID+"\""))
            db.commit()
        lastdate = {
            'date' : date.today(),
            'uid' : int(BookHandler.currUID)
        }
        cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
        db.commit()
        BookHandler.UpdateDatabase()

    @staticmethod
    def ReturnSelected(memberID: str):
        BookHandler.taken.remove(str(BookHandler.currUID))
        if len(BookHandler.waitList)==0:
            BookHandler.available.append(BookHandler.currUID)
        else:
            BookHandler.readyToClaimUIDs.append(BookHandler.currUID)
            memberActivated = BookHandler.waitList.pop(0)
            newActive = ActiveReservation(memberActivated, (datetime.now()+timedelta(days = 7)).date())
            BookHandler.readyToClaimUsers.append(newActive)
        BookHandler.UpdateDatabase()

    @staticmethod
    def ReserveSelected(memberID : str):
        BookHandler.waitList.append(memberID)
        BookHandler.UpdateDatabase()
    
    def CloseBook(self):
        self.UpdateDatabase()
        BookHandler.currISBN = None
        BookHandler.available = []
        BookHandler.taken = []
        BookHandler.waitList = []
        BookHandler.readyToClaimUsers = []
        BookHandler.readyToClaimUIDs = []
        BookHandler.numberOfCopies = None

    @staticmethod
    def GetActiveReservedUIDs():
        return BookHandler.readyToClaimUIDs

    @staticmethod
    def GetAvailableUIDs():
        return BookHandler.available
    
    @staticmethod
    def GetActiveReservations():
        return BookHandler.readyToClaimUsers
    @staticmethod
    def IsActive(memberID: str):
        return memberID in [x.memberID for x in BookHandler.readyToClaimUsers] 
    
    @staticmethod
    def IsAvailable(UID: str):
        return UID in BookHandler.available

    @staticmethod
    def AddToPending(memberID: str):
        BookHandler.waitList.append(memberID)
    
def SplitTableEntry(s: str):
    if(s is None):
        return []
    return s.split(',')[0:-1]

def JoinTableEntry(l):
    if(len(l) == 0):
        return None
    return ','.join(l) + ','