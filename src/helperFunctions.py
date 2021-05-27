import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)

from bookHandler import SplitTableEntry

from underGraduateStudent import UnderGraduateStudent
from postGraduateStudent import PostGraduateStudent
from researchScholar import ResearchScholar
from facultyMember import FacultyMember

def GetBookInfoFromUID(uid):
    findBook = ("SELECT * FROM BOOKS")
    cursor.execute(findBook)
    found = False
    correctRow = {}
    for row in cursor:
        if row["UniqueID"] == uid:
            correctRow = row
            found = True
    db.commit()
    if not found:
        raise ValueError("UniqueID not found.")

    return correctRow

def GetLibraryMember(memberID):
    findMember = ("SELECT * FROM MEMBERS")
    cursor.execute(findMember)
    found = False
    correctRow = {}
    for row in cursor:
        if row["MemberID"] == memberID:
            correctRow = row
            found = True
    db.commit()
    if not found:
        raise ValueError("Invalid MemberID inputted.")

    if correctRow["MemberType"] == "UG":
        return UnderGraduateStudent(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])
    if correctRow["MemberType"] == "PG":
        return PostGraduateStudent(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])
    if correctRow["MemberType"] == "RS":
        return ResearchScholar(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])
    if correctRow["MemberType"] == "FM":
        return FacultyMember(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])

def IsReservationActive(ISBN, memberID):
    if ISBN == "None":
        return ""
    # print(ISBN)
    getISBN = ("SELECT * FROM RESERVATIONS WHERE ISBN = %(ISBN)s")
    isbn = {
        'ISBN' : ISBN
    }
    cursor.execute(getISBN, isbn)
    row = cursor.fetchone()
    db.commit()
    
    active = False
    for res in SplitTableEntry(row['ActiveReservations']):
        if memberID in res:
            active = True
    
    if active:
        return " (Active)"
    else:
        return " (Pending)"

def IsBookDisposed(uid):
        uid_ = {
            'UID' : int(uid)
        }
        cursor.execute(("SELECT IsDisposed FROM BOOKS WHERE UniqueID = %(UID)s"),uid_)
        row = cursor.fetchone()
        db.commit()
        if (row['IsDisposed']==1):
            return -1
        return 1