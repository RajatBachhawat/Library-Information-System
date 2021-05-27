import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)
cursor = db.cursor(dictionary = True)

from underGraduateStudent import UnderGraduateStudent
from postGraduateStudent import PostGraduateStudent
from researchScholar import ResearchScholar
from facultyMember import FacultyMember
from bookHandler import SplitTableEntry, JoinTableEntry
from librarian import Librarian, encode_message, decode_message
from libraryClerk import LibraryClerk

def MemberLogin(memberID: str, password: str):
    if memberID == "":
        raise ValueError("MemberID missing.")

    if not password:
        raise ValueError("Password missing.")
    
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

    # PassWord Auth
    decodedPassword = decode_message(bytes((correctRow["PassWd"]),'utf-8'))
    if decodedPassword != password:
        raise ValueError("Incorrect Password inputted.")

    if correctRow["MemberType"] == "UG":
        return UnderGraduateStudent(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])
    if correctRow["MemberType"] == "PG":
        return PostGraduateStudent(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])
    if correctRow["MemberType"] == "RS":
        return ResearchScholar(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])
    if correctRow["MemberType"] == "FM":
        return FacultyMember(correctRow['MemberName'], correctRow['MemberID'], SplitTableEntry(correctRow['ListOfBooksIssued']), correctRow['ReservedBook'])

    
def EmployeeLogin(employeeID: str, password: str):
    if employeeID == "":
        raise ValueError("EmployeeID missing.")

    if not password:
        raise ValueError("Password missing.")
    
    findEmployee = ("SELECT * FROM EMPLOYEES")
    cursor.execute(findEmployee)
    found = False
    correctRow = {}
    for row in cursor:
        if row["EmployeeID"] == employeeID:
            correctRow = row
            found = True
    db.commit()

    if not found:
        raise ValueError("Invalid EmployeeID inputted.")

    decodedPassword = decode_message(bytes((correctRow["PassWd"]),'utf-8'))
    if decodedPassword != password:
        raise ValueError("Incorrect Password inputted.")

    if correctRow['EmployeeID'] == "LIB0001":
        return Librarian(correctRow['EmployeeID'], correctRow['EmployeeName'])
    else:
        return LibraryClerk(correctRow['EmployeeID'], correctRow['EmployeeName'])

    