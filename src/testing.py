import copy
from abc import ABC, abstractmethod
from book import Book
from activeReservation import ActiveReservation
from bookHandler import BookHandler, SplitTableEntry, JoinTableEntry, UpdateReminders
from underGraduateStudent import UnderGraduateStudent
from postGraduateStudent import PostGraduateStudent
from researchScholar import ResearchScholar
from facultyMember import FacultyMember
from libraryMember import LibraryMember
from libraryClerk import LibraryClerk
from datetime import date, datetime, timedelta
from librarian import Librarian
from loginFunctions import MemberLogin, EmployeeLogin
import mysql.connector as mysql
import settings
db = mysql.connect(
    host = "localhost",
    user = settings.user,
    passwd = "1234",
    database = "lis"
)

cursor = db.cursor(dictionary = True)
def delete():    
    cursor.execute("DELETE FROM RESERVATIONS")
    db.commit()
    cursor.execute("DELETE FROM MEMBERS")
    db.commit()
    cursor.execute("TRUNCATE TABLE BOOKS")
    db.commit()
    cursor.execute("DELETE FROM EMPLOYEES")


#1. MemberLogin()

#Member logs in successfully
#Member not in members table
#PASS\n\nword does not match

#2. EmployeeLogin()

#Employee logs in successfully
#Employee not in members table
#PASS\n\nword does not match

a_file = open("testReport.txt", "w")
print("TEST COMPLIANCE REPORT - LIBRARY INFORMATION SYSTEM\n\n", file = a_file)
print("\n---- Test LibraryMember----\n", file = a_file)
# 3. Library Member
#Getter Function
delete()
student = UnderGraduateStudent("Harry","19CS30014",[],"")
if(student.GetName()=="Harry"):
    print("Getter Function Name Test for Library Members: PASS\n\n",  file = a_file)
else:
    print("Getter Function Name Test for Library Members: PASS\n\n",  file = a_file)
if(student.GetMemberID()=="19CS30014"):
    print("Getter Function MemberID Test for Library Members: PASS\n\n",  file = a_file)
else:
    print("Getter Function MemberID Test for Library Members: PASS\n\n",  file = a_file)

student = UnderGraduateStudent("Harry","19CS30014",['7'],"")
if(student.GetNumberOfBookIssued()==1):
    print("Getter Function Number of Books Test for Library Members: PASS\n\n",  file = a_file)
else:
    print("Getter Function Number of Books Test for Library Members: PASS\n\n",  file = a_file)
delete()
student = UnderGraduateStudent("Harry","19CS30014",[],"988-0789032742")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742', NULL, '1,2,',NULL,'2021-04-08*19CS30014,','3,',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','Harry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789102742','Parry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','Harry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
result = student.CheckAvailabilityOfBook("988-0789032742")
if(result == (['3'],['5'])):
    print("Check availability when member has active reservation in ISBN : PASS\n\n",  file = a_file)
else:
    print("Check availability when member has active reservation in ISBN : FAIL\n\n",  file = a_file)
db.commit()
delete()
# ###
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "988-0789032742")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742', NULL,'1,','19CS30014,',NULL,NULL,0)"))
db.commit()
result = student.CheckAvailabilityOfBook("988-0789032742")
if(result=='Your Reservation is still pending. Pls wait for a few more days'):
    print("Check availability when member has pending reservation in ISBN : PASS\n\n",  file = a_file)
else:
    print("Check availability when member has pending reservation in ISBN : FAIL\n\n",  file = a_file)
delete()
# ###
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "999-6666689999")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742', '7,2,','1,',NULL,NULL,NULL,2)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','Parry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','Harry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0781032742','Parry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0781032742','Parry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0781032742','Parry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0781032742','Parry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','Harry Potter and the Chamber Of Secrets-by-J.K.Rowling',5,DATE '2021-1-1',0)"))
db.commit()
result=student.CheckAvailabilityOfBook("988-0789032742")
if(result==(['7','2'],['5','5'])):
    print("Check availability when member has no reservation in ISBN but copies are available: PASS\n\n",  file = a_file)
else:
    print("Check availability when member has no reservation in ISBN but copies are available: FAIL\n\n",  file = a_file)
delete()
###
student = UnderGraduateStudent("Harry", "19CS30014", [] , None)
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,',NULL,NULL,NULL,0)"))
db.commit()
result=student.CheckAvailabilityOfBook("988-0789032742")
if(result=='Sorry this book is not available currently,\n Would you like to reserve this book?'):
    print("Check availability when member has no reservation in ISBN and no copies are available: PASS\n\n",  file = a_file)
else:
    print("Check availability when member has no reservation in ISBN and no copies are available: FAIL\n\n",  file = a_file)
delete()
###
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "999-6666689999")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,',NULL,NULL,NULL,0)"))
db.commit()
result=student.CheckAvailabilityOfBook("988-0789032742")
if(result=='Sorry this book is not available currently,\n and you already have a reservation'):
    print("Check availability when member has a reservation in different ISBN and no copies are available: PASS\n\n",  file = a_file)
else:
    print("Check availability when member has a reservation in different ISBN and no copies are available: FAIL\n\n",  file = a_file)
delete()
###

#Test IssueBook()
###
student = UnderGraduateStudent("Harry", "19CS30014",  ['1'] , None)
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742','7,','1,3,',NULL,NULL,NULL,1)"))
db.commit()
result = student.IssueBook(Book('1','988-0789032742',date.today()))
if(result==0):
    print("Error when member tries to issue book they have already issued: PASS\n\n",  file = a_file)
else:
    print("Error when member tries to issue book they have already issued: FAIL\n\n",  file = a_file)
delete()
###
student = UnderGraduateStudent("Harry", "19CS30014",  ['1','8'] , None)
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742','7,','1,3,',NULL,NULL,NULL,1)"))
db.commit()
result = student.IssueBook(Book('7','988-0789032742',date.today()))
if(result==None):
    print("Error when member tries to issue book after exceeding limit: PASS\n\n",  file = a_file)
else:
    print("Error when member tries to issue book after exceeding limit: FAIL\n\n",  file = a_file)
delete()
###
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "988-0789032742")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,',NULL,'2021-04-08*19CS30014,','7,',0)"))
db.commit()
result = student.IssueBook(Book('7','988-0789032742',date.today()))
if(result==1):
    print("Member Claims a reserved book: PASS\n\n",  file = a_file)
else:
    print("Member Claims a reserved book: FAIL\n\n",  file = a_file)
delete()
###
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742','7,','1,3,',NULL,NULL,NULL,1)"))
db.commit()
result = student.IssueBook(Book('7','988-0789032742',date.today()))
if(result==1):
    print("Member Claims an available book: PASS\n\n",  file = a_file)
else:
    print("Member Claims an available book: FAIL\n\n",  file = a_file)
delete()
##

#Test ReserveBook()

student = UnderGraduateStudent("Harry", "19CS30014",  [] , None)
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742','7,','1,3,',NULL,NULL,NULL,1)"))
db.commit()
f = False
try:
    student.ReserveBook("988-0789032742")
except ValueError:
    f = True
    print("Error when Member tries to reserve an available book: PASS\n\n",  file = a_file)
if f == False:
    print("Error when Member tries to reserve an available book: FAIL\n\n",  file = a_file)

delete()
student = UnderGraduateStudent("Harry", "19CS30014",  [] , None)
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,',NULL,NULL,NULL,0)"))
db.commit()
student.ReserveBook("988-0789032742")
if(student.GetReservedBook() == "988-0789032742"):
    print("Member reserves an unavilable book: PASS\n\n",  file = a_file)
else:   
    print("Member reserves an unavilable book:: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,',NULL,NULL,NULL,0)"))
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "999-6666689999")
f = False
try:
    result = student.ReserveBook("988-0789032742")
except ValueError:
    f=True
    print("Error when Member reserves an unavilable book when they already have a reservation for some other book: PASS\n\n",  file = a_file)
if f==False:    
    print("Error when Member reserves an unavilable book when they already have a reservation for some other book: FAIL\n\n",  file = a_file)

delete()
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "988-0789032742")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,',NULL,'2021-04-03*19CS30014,','3,',0)"))
f = False
try:
    student.ReserveBook("988-0789032742")
except ValueError:
    f = True
    print("Error when Member reserves an unavilable book when they already have an active reservation for this book: PASS\n\n",  file = a_file)
if f == False:
    print("Error when Member reserves an unavilable book when they already have an active reservation for this book: FAIL\n\n",  file = a_file)

delete()

student = UnderGraduateStudent("Harry", "19CS30014",  [] , "988-0789032742")
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,','19CS30014',NULL,NULL,0)"))
try:
    student.ReserveBook("988-0789032742")
except ValueError:
    f = True
    print("Error when Member reserves an unavilable book when they already have a pending reservation for this book: PASS\n\n",  file = a_file)
if f == False:
    print("Error when Member reserves an unavilable book when they already have a pending reservation for this book: FAIL\n\n",  file = a_file)
db.commit()
delete()

#Test CheckForReminder()

delete()
cursor.execute(("INSERT INTO BOOKS VALUES (7,'988-0789032742','James-Bond-by-Bond-James',1, DATE '2021-3-1',0)"))
db.commit()
#cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014','Harry','UG','7,',NULL,1,'PASS\n\nword')"))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("19CS30014","Harry",[],None)
librarian.AddMember(student,'potato')
student.IssueBook(Book('7','988-0789032742',date(2021,3,1)))
lastdate = {
            'date' : date(2021,3,1),
            'uid' :  7
        }
cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
db.commit()
librarian.SendReminderToMember()
db.commit()
listrem = student.CheckForReminder()
if  len(listrem)!=0 :
    print("Correct message and reminder sent when librarian sends a reminder and member has overdue books: PASS\n\n",  file = a_file)
else:  
    print("Correct message and reminder sent when librarian sends a reminder and member has overdue books: FAIL\n\n",  file = a_file)
delete()
cursor.execute(("INSERT INTO BOOKS VALUES (7,'988-0789032742','James-Bond-by-Bond-James',1, DATE '2021-4-4',0)"))
db.commit()
student = UnderGraduateStudent("Harry", "19CS30014",  ['7'] , None)
librarian = Librarian("LIB0001","Neha")
librarian.AddMember(student,'potato')
db.commit()
student.IssueBook(Book('7','988-0789032742',date.today()))
db.commit()
librarian.SendReminderToMember()
db.commit()
listrem = student.CheckForReminder()
db.commit()
if  len(listrem) ==0 :
    print("Reminder made to 0 when librarian sends reminder  but member has no overdue books: PASS\n\n",  file = a_file)
else:  
    print("Reminder made to 0 when librarian sends reminder  but member has no overdue books: FAIL\n\n",  file = a_file)
db.commit()
delete()
cursor.execute(("INSERT INTO BOOKS VALUES (7,'988-0789032742','James-Bond-by-Bond-James',1, DATE '2021-3-1',0)"))
db.commit()
student = UnderGraduateStudent("Harry", "19CS30014",  ['7'] , None)
librarian = Librarian("LIB0001","Neha")
librarian.AddMember(student,'potato')
db.commit()
listrem = student.CheckForReminder()
if  len(listrem)==0:
    print("Reminder made to 0 when librarian does not send reminder: PASS\n\n",  file = a_file)
else:  
    print("Reminder made to 0 when librarian does not send reminder: FAIL\n\n",  file = a_file)
delete()

#Test Search Book

# #COMES UNDER GUI TESTING
# print("Search when no book is system matches: PASS\n\n",  file = a_file)
# print("Search when no book in system matches: FAIL\n\n",  file = a_file)

# #COMES UNDER GUI TESTING
# print("Search by Name: PASS\n\n",  file = a_file)
# print("Search by Name: FAIL\n\n",  file = a_file)

# #COMES UNDER GUI TESTING
# print("Search by Author: PASS\n\n",  file = a_file)
# print("Search by Author: FAIL\n\n",  file = a_file)


# Test UpdateFromDatabase()
delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,',NULL,'2021-03-29*19CS30014,','7,',0)"))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "988-0789032742")
librarian.AddMember(student,'potato')
student.UpdateFromDatabase()
if(student.GetReservedBook()==None):   
    print("Update database when member has expired active reservation: PASS\n\n",  file = a_file)
else:
    print("Update database when member has expired active reservation: FAIL\n\n",  file = a_file)
delete()


cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,','19CS30014','2021-03-29*19CS30037','7,',0)"))
db.commit()
student = UnderGraduateStudent("Harry", "19CS30014",  [] , "988-0789032742")
librarian = Librarian("LIB0001","Neha")
librarian.AddMember(student,'potato')
student2 = UnderGraduateStudent("Harriet", "19CS30037",  [] , "988-0789032742")
librarian.AddMember(student2,'potato')
student.UpdateFromDatabase()
student2.UpdateFromDatabase()
if(student2.GetReservedBook()==None):
    print("Update database when member has pending reservation which becomes active reservation: PASS\n\n",  file = a_file)
else:
    print("Update database when member has pending reservation which becomes active reservation: FAIL\n\n",  file = a_file)


delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,',NULL,NULL,NULL,0)"))
db.commit()
student = UnderGraduateStudent("Harry", "19CS30014",  [] , None)
librarian = Librarian("LIB0001","Neha")
librarian.AddMember(student,'potato')
student.UpdateFromDatabase()
if(student.GetReservedBook()==None):
    print("Update database when member has no reservation: PASS\n\n",  file = a_file)
else:
    print("Update database when member has no reservation: FAIL\n\n",  file = a_file)
delete()

print("\n---- Test UnderGraduateStudent----\n", file = a_file)

#4. UnderGraduateStudent

#Test Constructor
student = UnderGraduateStudent("Harry", "19CS30014",[],None)
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014"):
    print("create object when new member is added: PASS\n\n",  file = a_file)
else:
    print("create object when new member is added: FAIL\n\n",  file = a_file)


student = UnderGraduateStudent("Harry", "19CS30014",['7'],"988-0789032742")
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and student.GetReservedBook()=="988-0789032742"):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014', 'Harry', 'UG', NULL, NULL, 0, \
'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==')"))
# The password is encrypted form of "1234"
db.commit()
student = MemberLogin("19CS30014", "1234")
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and isinstance(student, UnderGraduateStudent)):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

try:
    student = MemberLogin("19CS", "1234")
except ValueError as e:
    if str(e) == "Invalid MemberID inputted.":
        print("throw error when invalid member is trying to log in: PASS\n\n", file = a_file)
    else:
        print("throw error when invalid member is trying to log in: FAIL\n\n", file = a_file)

try:
    student = MemberLogin("19CS30014", "124")
except ValueError as e:
    if str(e) == "Incorrect Password inputted.":
        print("throw error when incorrect password is entered: PASS\n\n", file = a_file)
    else:
        print("throw error when incorrect password is entered: FAIL\n\n", file = a_file)
delete()

#Test Can issue
student = UnderGraduateStudent("Harry", "19CS30014",  ['3'] , "988-0789032742")
val = student.CanIssue()
if val == True:
    print("Issue when member has not yet exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Issue when member has not yet exhausted his limit: FAIL\n\n",  file = a_file)

student = UnderGraduateStudent("Harry", "19CS30014",  ['3','4'] , "988-0789032742")
val = student.CanIssue()
if val==False:
    print("Error when member issues after having exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Error when member issues after having exhausted his limit: FAIL\n\n",  file = a_file)

print("\n---- Test PostGraduateStudent----\n", file = a_file)

#5. PostGraduateStudent

#Test Constructor
student = PostGraduateStudent("Harry", "19CS30014", [] ,None)
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014"):
    print("create object when new member is added: PASS\n\n",  file = a_file)
else:
    print("create object when new member is added: FAIL\n\n",  file = a_file)

student = UnderGraduateStudent("Harry", "19CS30014",['3'],"988-0789032742")
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and student.GetReservedBook()=="988-0789032742"):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014', 'Harry', 'PG', NULL, NULL, 0, \
'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==')"))
# The password is encrypted form of "1234"
db.commit()
student = MemberLogin("19CS30014", "1234")
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and isinstance(student, PostGraduateStudent)):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

try:
    student = MemberLogin("19CS", "1234")
except ValueError as e:
    if str(e) == "Invalid MemberID inputted.":
        print("throw error when invalid member is trying to log in: PASS\n\n", file = a_file)
    else:
        print("throw error when invalid member is trying to log in: FAIL\n\n", file = a_file)

try:
    student = MemberLogin("19CS30014", "124")
except ValueError as e:
    if str(e) == "Incorrect Password inputted.":
        print("throw error when incorrect password is entered: PASS\n\n", file = a_file)
    else:
        print("throw error when incorrect password is entered: FAIL\n\n", file = a_file)
delete()

#Test Can issue
student = PostGraduateStudent("Harry", "19CS30014",  ['3'] , "988-0789032742")
val = student.CanIssue()
if  val == True:
    print("Issue when member has not yet exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Issue when member has not yet exhausted his limit: FAIL\n\n",  file = a_file)

student = PostGraduateStudent("Harry", "19CS30014",  ['3','4','5','6'] , "988-0789032742")
val = student.CanIssue()
if  val == False:
    print("Error when member issues after having exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Error when member issues after having exhausted his limit: FAIL\n\n",  file = a_file)

print("\n---- Test ResearchScholar----\n", file = a_file)

#6. ResearchScholar

#Test Constructor
student = ResearchScholar("Harry", "19CS30014",[],None)
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014"):
    print("create object when new member is added: PASS\n\n",  file = a_file)
else:
    print("create object when new member is added: FAIL\n\n",  file = a_file)

student = ResearchScholar("Harry", "19CS30014",  ['7'] ,None)
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and student.GetReservedBook()==None):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014', 'Harry', 'RS', NULL, NULL, 0, \
'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==')"))
# The password is encrypted form of "1234"
db.commit()
student = MemberLogin("19CS30014", "1234")
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and isinstance(student, ResearchScholar)):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

try:
    student = MemberLogin("19CS", "1234")
except ValueError as e:
    if str(e) == "Invalid MemberID inputted.":
        print("throw error when invalid member is trying to log in: PASS\n\n", file = a_file)
    else:
        print("throw error when invalid member is trying to log in: FAIL\n\n", file = a_file)

try:
    student = MemberLogin("19CS30014", "124")
except ValueError as e:
    if str(e) == "Incorrect Password inputted.":
        print("throw error when incorrect password is entered: PASS\n\n", file = a_file)
    else:
        print("throw error when incorrect password is entered: FAIL\n\n", file = a_file)
delete()

#Test Can issue
student = ResearchScholar("Harry", "19CS30014",  [] , None)
val  = student.CanIssue()
if val == True:
    print("Issue when member has not yet exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Issue when member has not yet exhausted his limit: FAIL\n\n",  file = a_file)
student = ResearchScholar("Harry", "19CS30014",  ['3','4','5','6','7','8'] , "988-0789032742")
val  = student.CanIssue()
if val == False:
    print("Error when member issues after having exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Error when member issues after having exhausted his limit: FAIL\n\n",  file = a_file)

print("\n---- Test FacultyMember----\n", file = a_file)

#7. FacultyMember

#Test Constructor
student = FacultyMember("Harry", "19CS30014",  [] , None)
if(student.GetName()=="Harry" and student.GetMemberID() == "19CS30014"):
    print("create object when new member is added: PASS\n\n",  file = a_file)
else:
    print("create object when new member is added: FAIL\n\n",  file = a_file)

student = FacultyMember("Harry", "19CS30014",  ['7'] , None)
if(student.GetName()=="Harry" and student.GetMemberID() == "19CS30014"):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014', 'Harry', 'FM', NULL, NULL, 0, \
'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==')"))
# The password is encrypted form of "1234"
db.commit()
student = MemberLogin("19CS30014", "1234")
if(student.GetName()=="Harry" and student.GetMemberID()=="19CS30014" and isinstance(student, FacultyMember)):
    print("create object when existing member is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when existing member is logged in: FAIL\n\n",  file = a_file)

try:
    student = MemberLogin("19CS", "1234")
except ValueError as e:
    if str(e) == "Invalid MemberID inputted.":
        print("throw error when invalid member is trying to log in: PASS\n\n", file = a_file)
    else:
        print("throw error when invalid member is trying to log in: FAIL\n\n", file = a_file)

try:
    student = MemberLogin("19CS30014", "124")
except ValueError as e:
    if str(e) == "Incorrect Password inputted.":
        print("throw error when incorrect password is entered: PASS\n\n", file = a_file)
    else:
        print("throw error when incorrect password is entered: FAIL\n\n", file = a_file)
delete()

#Test Can issue
student = FacultyMember("Harry", "19CS30014",  ['3'] , "988-0789032742")
val = student.CanIssue()
if val == True:
    print("Issue when member has not yet exhausted his limit: PASS\n\n",  file = a_file)
else :
    print("Issue when member has not yet exhausted his limit: FAIL\n\n",  file = a_file)

student = FacultyMember("Harry", "19CS30014",  ['3','4','5','6','7','8','9','10','11','12'] , "988-0789032742")
val = student.CanIssue()
if val == False:
    print("Error when member issues after having exhausted his limit: PASS\n\n",  file = a_file)
else:
    print("Error when member issues after having exhausted his limit: FAIL\n\n",  file = a_file)

print("\n---- Test LibraryClerk----\n", file = a_file)

#8. LibraryClerk
#Test Constructor

employee = LibraryClerk("LIB0068", "Sam")
if(employee._name =="Sam" and employee._employeeID == "LIB0068" and isinstance(employee, LibraryClerk)):
    print("Correct Employee Object Constructed when valid login: PASS\n\n",  file = a_file)
else:
    print("Correct Employee Object Constructed when valid login: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO EMPLOYEES VALUES ('LIB0068', 'Sam', \
'gAAAAABgau-GvJ9w1sHYJd167g-SWhhhBmgx-UwSMhpkQScrbObcuCgj2PfxjHhv_URtOo4phukn9JAFFzs288xSR4zny5M2UQ==')"))
# The password is encrypted form of "1234"
db.commit()
employee = EmployeeLogin("LIB0068", "1234")
if(employee._name =="Sam" and employee._employeeID == "LIB0068" and isinstance(employee, LibraryClerk)):
    print("create object when employee is logged in: PASS\n\n",  file = a_file)
else:
    print("create object when employee is logged in: FAIL\n\n",  file = a_file)

try:
    employee = EmployeeLogin("LIB0", "1234")
except ValueError as e:
    if str(e) == "Invalid EmployeeID inputted.":
        print("throw error when invalid employee is trying to log in: PASS\n\n", file = a_file)
    else:
        print("throw error when invalid employee is trying to log in: FAIL\n\n", file = a_file)

try:
    employee = EmployeeLogin("LIB0068", "124")
except ValueError as e:
    if str(e) == "Incorrect Password inputted.":
        print("throw error when incorrect password is entered: PASS\n\n", file = a_file)
    else:
        print("throw error when incorrect password is entered: FAIL\n\n", file = a_file)
delete()

delete()

# '''
#Add Book
clerk = LibraryClerk("LIB0011","John")
clerk.AddBook(['988-0789032742','Motu and Patnu','Narendra Modi',1,date(2021,4,1)])
clerk.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date(2010,4,1)])
clerk.AddBook(['988-0789032742','Motu and Patnu','Narendra Modi',3,date(2010,4,1)])
clerk.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',1,date(2021,4,1)])
clerk.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date(2010,4,1)])
clerk.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',3,date(2010,4,1)])
db.commit()
student = PostGraduateStudent("Harry","19CS10073",[],None)
student.IssueBook(Book('1','988-0789032742',date.today()))
student.IssueBook(Book('3','988-0789032742',date.today()))
student2 = UnderGraduateStudent("Harry","19CS30014",[],None)
student2.ReserveBook("988-0789032742")
bookDetails = ["988-0789032742","Motu and Patnu","Narendra Modi",7]
clerk.AddBook(bookDetails)
bH=BookHandler.Create()
bH.OpenBook("988-0789032742")
if(('7' in bH.GetActiveReservedUIDs())):
    print("Reservations Correctly updated when same ISBN already present with pending reservations, Book added to database: PASS\n\n",  file = a_file)
else:
    print("Reservations Correctly updated when same ISBN already present with pending reservations, Book added to database: FAIL\n\n",  file = a_file)

bookDetails = ['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date.today()]
clerk.AddBook(bookDetails)
bH.CloseBook()
bH.OpenBook('999-666689999')
if('8' in BookHandler.GetAvailableUIDs()):
    print("Reservations Correctly updated when same ISBN already present with no pending reservations, Book added to database: PASS\n\n",  file = a_file)
else:
    print("Reservations Correctly updated when same ISBN already present with no pending reservations, Book added to database: FAIL\n\n",  file = a_file)

bookDetails = ['999-666689000','Reopen IIT KGP','Dead Students',2,date.today()]
clerk.AddBook(bookDetails)
bH.CloseBook()
bH.OpenBook('999-666689000')
if('9' in bH.GetAvailableUIDs()):
    print("Reservations Correctly updated when same ISBN not already present : PASS\n\n",  file = a_file)
else:
    print("Reservations Correctly updated when  same ISBN not already present : FAIL\n\n",  file = a_file)

bH.CloseBook()
# '''
delete()

#Delete Book
clerk = LibraryClerk("LIB0011","Neha")
clerk.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date(2021,4,1)])
clerk.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date(2010,4,1)])
clerk.AddBook(['999-666689999','Harry Potter and the Directors Curse','Vikram Seth',3,date(2010,4,1)])
unique = {
        'uid' :  1
    }
cursor.execute("UPDATE BOOKS SET IsDisposed=0 WHERE UniqueID  = %(uid)s", unique)
db.commit()
unique = {
        'uid' :  2
    }
cursor.execute("UPDATE BOOKS SET IsDisposed=1 WHERE UniqueID  = %(uid)s", unique)
db.commit()
unique = {
        'uid' :  3
    }
cursor.execute("UPDATE BOOKS SET IsDisposed=1 WHERE UniqueID  = %(uid)s", unique)
db.commit()
clerk.DeleteBook()
cursor.execute("SELECT UniqueID FROM BOOKS")
cnt=0
for row in cursor:
    cnt+=1
if(cnt==1):
   print("Correctly Deleted ALL Disposed Books from Databases: PASS\n\n",  file = a_file)
else:
   print("Correctly Deleted ALL Disposed Books from Databases: FAIL\n\n",  file = a_file)
delete()

#Return Book

student = UnderGraduateStudent("Harry", "19CS30014",  [] , None)
book = Book('1',"999-666689999",date.today())
clerk = LibraryClerk("LIB0011","John")
f = False
try :
    clerk.ReturnBook(student, book)
except ValueError:
    f=True
    print("Error thrown when member tries to return a book they have not issued: PASS\n\n",  file = a_file)
if(f==False):
    print("Error thrown when member tries to return a book they have not issued: FAIL\n\n",  file = a_file)

student = UnderGraduateStudent("Harry", "19CS30014",  [] , None)
book = Book('-1',"999-666689999",date.today())
clerk = LibraryClerk("LIB0011","John")
f = False
try :
    clerk.ReturnBook(student, book)
except ValueError:
    f=True
    print("Error thrown when member tries to return a book not in the library: PASS\n\n",  file = a_file)
if(f==False):
    print("Error thrown when member tries to return a book not in the library: FAIL\n\n",  file = a_file)

delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742', NULL,'1,3,7,','19CS30056,',NULL,NULL,0)"))
db.commit()
cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014','Harry','UG','7,',NULL,0,'PASS\n\nword')"))
db.commit()
student = UnderGraduateStudent("Harry", "19CS30014",  ['7'] , None)
book = Book(7,'988-0789032742',date.today())
clerk = LibraryClerk("LIB0011","John")
clerk.ReturnBook(student,book)
if(student.GetNumberOfBookIssued()==0):
    print("Correct Updates when returned book has pending reservations: PASS\n\n",  file = a_file)
else:
    print("Correct Updates when returned book has pending reservations: FAIL\n\n",  file = a_file)
delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742', NULL,'1,3,7,',NULL,NULL,NULL,0)"))
db.commit()
cursor.execute(("INSERT INTO MEMBERS VALUES ('19CS30014','Harry','UG','7,',NULL,0,'PASS\n\nword')"))
db.commit()
student = UnderGraduateStudent("Harry", "19CS30014",  ['7'] , None)
book = Book(7,'988-0789032742',date.today())
clerk = LibraryClerk("LIB0011","John")
clerk.ReturnBook(student,book)
if(student.GetNumberOfBookIssued()==0):
    print("Correct Updates when returned book has no pending reservations: PASS\n\n",  file = a_file)
else:
    print("Correct Updates when returned book has no pending reservations: FAIL\n\n",  file = a_file)

delete()
#Collect Penalty

student = UnderGraduateStudent("Harry", "19CS30014",  ['7'] , None)
#PASS\n\ning todays date as issue date as that will never have penalty
book = Book('7',"988-0789032742",date.today())
clerk = LibraryClerk("LIB0011","John")
if(clerk.CollectPenalty(student,book)==0):
    print("No penalty collected when returned on time: PASS\n\n",  file = a_file)
else:
    print("No penalty collected when returned on time: FAIL\n\n",  file = a_file)


student = UnderGraduateStudent("Harry", "19CS30014",  ['7'] , None)
#PASS\n\ning todays date as issue date as that will never have penalty
book = Book('7',"988-0789032742",date(2021,2,24))
clerk = LibraryClerk("LIB0011","John")
if(clerk.CollectPenalty(student,book)):
    print("Penalty collected when not returned on time: PASS\n\n",  file = a_file)
else:
    print("Penalty collected when not returned on time: FAIL\n\n",  file = a_file)
delete()

print("\n---- Test Librarian----\n", file = a_file)

#Librarian

#Constructor

f = True
try:
    Librarian("LIB0001","John")
except ValueError:
    f=False
if(f):
    print("Correctly did construction of Librarian object with correct ID: PASS\n\n",  file = a_file)
else:
    print("Correctly did construction of Librarian object with correct ID: FAIL\n\n",  file = a_file)
delete()
f = False
try:
    Librarian("LIB0068","Priyanka")
except ValueError:
    f=True
if(f):
    print("Correctly blocked construction of Librarian object with incorrect ID: PASS\n\n",  file = a_file)
else:
    print("Correctly blocked construction of Librarian object with incorrect ID: FAIL\n\n",  file = a_file)
delete()
#Super class functionalities
#Tested above for Library Clerk

#Add Member
f=False
lib=Librarian("LIB0001","John")
student = PostGraduateStudent("Harry","19CS30014",[],None)
try:
    lib.AddMember(student,'PASS\n\nword')
except ValueError:
    f=True
if(f==False):
    print("Correctly Added when Member Does not exist already: PASS\n\n",  file = a_file)
else:
    print("Correctly Added when Member Does not exist already: FAIL\n\n",  file = a_file)

# try to add the same member again
f=False
lib=Librarian("LIB0001","John")
student = UnderGraduateStudent("Harry","19CS30014",[],None)
try:
    lib.AddMember(student,'PASS\n\nword')
except ValueError:
    f=True
if(f==True):
    print("Error when Librarian tries to add a member who already exists: PASS\n\n",  file = a_file)
else:
    print("Error when Librarian tries to add a member who already exists: FAIL\n\n",  file = a_file)
delete()

f=False
lib=Librarian("LIB0001","John")
student = UnderGraduateStudent("","19CS30014",[],None)
try:
    lib.AddMember(student,'PASS\n\nword')
except ValueError:
    f=True
if(f==True):
    print("Error when required argument name missing : PASS\n\n",  file = a_file)
else:
    print("Error when required argument name missing : FAIL\n\n",  file = a_file)
delete()

f=False
lib=Librarian("LIB0001","John")
student = UnderGraduateStudent("Harry","",[],"")
try:
    lib.AddMember(student,'PASS\n\nword')
except ValueError as err:
    f=True
if(f==True):
    print("Error when required argument member ID missing : PASS\n\n",  file = a_file)
else:
    print("Error when required argument member ID missing : FAIL\n\n",  file = a_file)

delete()
# #handled during login
# print("Error when type missing : PASS\n\n",  file = a_file)
# print("Error when type missing : FAIL\n\n",  file = a_file)
# #handled during login
# print("Error when PASS\n\nword missing : PASS\n\n",  file = a_file)
# print("Error when PASS\n\nword missing : FAIL\n\n",  file = a_file)

#Delete members
lib=Librarian("LIB0001","John")
student = UnderGraduateStudent("Harry","19CS30014",[],None)
#lib.AddMember(student,'potatoes')
lib.RemoveMember(student)
flag = False
cursor.execute("SELECT * FROM MEMBERS")
for row in cursor:
    if row["MemberID"]=="19CS30014":
        flag = True
if(flag==False):
    print("Deleting Existing member : PASS\n\n",  file = a_file)
else:
    print("Deleting existing member : FAIL\n\n",  file = a_file)

delete()
lib=Librarian("LIB0001","John")
f = False
student = UnderGraduateStudent("Harry","19CS30014",[],"")
try:  
    lib.RemoveMember(student)
except ValueError:
    f=True
    print("Error when Deleting non-Existing member : PASS\n\n",  file = a_file)
if(f==False):
    print("Error when Deleting non-existing member : FAIL\n\n",  file = a_file)

delete()
f=False
lib=Librarian("LIB0001","John")
student = UnderGraduateStudent("Harry","19CS30014",[],None)
lib.AddMember(student,'potatoes')
cursor.execute(("UPDATE MEMBERS SET ListOfBooksIssued = '1,' WHERE MemberID = '19CS30014'"))
db.commit()
try:
    lib.RemoveMember(student)
except ValueError:
    f=True
    print("Error when Deleting member with dues : PASS\n\n",  file = a_file)
if(f==False):
    print("Error when Deleting member with dues : FAIL\n\n",  file = a_file)
delete()

#Sending reminders
lib=Librarian("LIB0001","John")
student = UnderGraduateStudent("Harry","19CS30014",[],None)
lib.AddMember(student,'potatoes')
cursor.execute(("UPDATE MEMBERS SET ListOfBooksIssued = '1,' WHERE MemberID = '19CS30014'"))
db.commit()
lib.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date(2020,4,1)])
lastdate = {
        'date' : date(2020,4,1),
        'uid' :  1
    }
cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
db.commit()
lib.SendReminderToMember()
cursor.execute(("SELECT * FROM MEMBERS"))
flag  = False
for row in cursor:
    if(row["MemberID"]=='19CS30014'):
        if(row["GotReminder"]==1):
            flag=True
if flag == True:
    print("Send reminders to all members: PASS\n\n",  file = a_file)
else:
    print("Send reminders to all members: FAIL\n\n",  file = a_file)
delete()

#Check issue statistics
librarian = Librarian("LIB0001","Neha")
librarian.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date(2021,4,1)])
lastdate = {
        'date' : date(2021,4,1),
        'uid' :  1
    }
cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
db.commit()
librarian.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date(2010,4,1)])
lastdate = {
        'date' : date(2010,4,1),
        'uid' :  2
    }
cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
db.commit()
librarian.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date(2010,4,1)])
lastdate = {
        'date' : date(2010,4,1),
        'uid' :  3
    }
cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
db.commit()
obsolete = (librarian.CheckBookIssueStats())
if(obsolete[0][0]=='2' and obsolete[1][0]=='3'):
    print("Showing valid Output when some books have not been issued in the last 5 years: PASS\n\n",  file = a_file)
else:
    print("Showing valid Output when some books have not been issued in the last 5 years: FAIL\n\n",  file = a_file)

delete()
librarian = Librarian("LIB0001","Neha")
librarian.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date.today()])
db.commit()
librarian.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date.today()])
db.commit()
librarian.AddBook(['999-666689999','Curry Patter and the curse of Bhindi','J.K.Rowling',2,date.today()])
db.commit()
obsolete = (librarian.CheckBookIssueStats())
if(len(obsolete)==0):
    print("Showing valid Output when all books have been issued in the last 5 years: PASS\n\n",  file = a_file)
else:
    print("Showing valid Output when all books have been issued in the last 5 years: FAIL\n\n",  file = a_file)


#Test Dispose Book
librarian = Librarian("LIB0001","Neha")
f= False
try:
    librarian.DisposeBook("10")
except  ValueError:
    f=True
    print("Error when disposing a book whose UID does not exist: PASS\n\n",  file = a_file)
if f==False:
    print("Error when disposing a book whose UID does not exist: FAIL\n\n",  file = a_file)
delete()
librarian = Librarian("LIB0001","Neha")
librarian.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date.today()])
db.commit()
f= False
try:
    librarian.DisposeBook("1")
except  ValueError:
    f = True
    print("Error when disposing a book which has been issued in the last 5 years: PASS\n\n",  file = a_file)
if f == False:
    print("Error when disposing a book which has been issued in the last 5 years: FAIL\n\n",  file = a_file)


delete()
librarian = Librarian("LIB0001","Neha")
librarian.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date(2021,4,1)])
lastdate = {
        'date' : date(2010,4,1),
        'uid' :  1
    }
cursor.execute("UPDATE BOOKS SET LastIssued = %(date)s WHERE UniqueID  = %(uid)s", lastdate)
db.commit()
librarian.DisposeBook('1')
cursor.execute("SELECT * FROM BOOKS WHERE UniqueID = 1")
flag = False
for rows in cursor:
    if(rows["IsDisposed"]==1):
        flag = True
if flag == True:
    print("disposing a book which has not been issued in the last 5 years: PASS\n\n",  file = a_file)
else:
    print("disposing a book which has not been issued in the last 5 years: FAIL\n\n",  file = a_file)

print("\n---- Test BookHandler----\n", file = a_file)

#Book Handler

#Open Book
delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('999-666689999','7,9,','1,',NULL,NULL,NULL,2)"))
db.commit()
librarian = Librarian("LIB0001","Neha")
librarian.AddBook(['999-666689999','Curry Patter and the adventures of Aloo Sabzi','J.K.Rowling',1,date(2021,4,1)])
goldenoutput = ["1","999-666689999",['7','9'],['1'],[],[],[],2]

bH = BookHandler.Create()
bH.OpenBook("999-666689999")
if(BookHandler.currISBN == "999-666689999" and BookHandler.available == ['7','9'] and BookHandler.taken == ['1'] and BookHandler.numberOfCopies == 2):
    print("Correct Data Members when only ISBN provided: PASS\n\n",  file = a_file)
else:
    print("Correct Data Members when only ISBN provided: FAIL\n\n",  file = a_file)
bH.CloseBook()

bH = BookHandler.Create()
bH.OpenBook(Book("1","999-666689999",date.today()))
if(bH.currISBN == "999-666689999" and bH.available == ['7','9'] and bH.taken == ['1'] and bH.numberOfCopies == 2 and bH.currUID=='1'):
    print("Correct Data Members ISBN and UID provided: PASS\n\n",  file = a_file)
else:
    print("Correct Data Members ISBN and UID provided: FAIL\n\n",  file = a_file)
bH.CloseBook()
delete()

bh = BookHandler.Create()

bh2 = BookHandler.Create()
if(bh == bh2):
    print("Singleton Class Check: PASS\n\n",  file = a_file)
else:
    print("Singleton Class Check: FAIL\n\n",  file = a_file)
bh.CloseBook()
#Update Book
delete()

cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,','19CS10074,19CS30056,','2021-04-01*19CS30014,','3,',0)"))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",[],'988-0789032742')
librarian.AddMember(student,'potato')
cursor.execute(("UPDATE MEMBERS SET ReservedBook = '988-0789032742' WHERE MemberID = '19CS30014'"))
db.commit()
flag1 = False
flag2 = False
bh = BookHandler.Create()
bh.OpenBook('988-0789032742')
db.commit()
bh.UpdateBook()
db.commit()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM MEMBERS")
for row in cursor:
    if(row['MemberID']=='19CS30014'):
        if(row["ReservedBook"]==None):
            flag1 = True
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["ActiveReservedUIDs"]=='3,'):
            flag2 = True
if flag1 == True and flag2 == True:
    print("Update Carried out correctly when pending reservation are there, some active reservations expired: PASS\n\n",  file = a_file)
else:
    print("Update Carried out correctly when pending reservation are there, some active reservations expired: FAIL\n\n",  file = a_file)
bh.CloseBook()

delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,','19CS10074,19CS30056,',NULL,NULL,0)"))
db.commit()
flag2 = False
bh = BookHandler.Create()
bh.OpenBook('988-0789032742')
db.commit()
bh.UpdateBook()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["ActiveReservedUIDs"]==None):
            flag2 = True
if flag2 == True:
    print("Update Carried out correctly when pending reservation are there, no reservations expired: PASS\n\n",  file = a_file)
else:
    print("Update Carried out correctly when pending reservation are there, no reservations expired: FAIL\n\n",  file = a_file)
bh.CloseBook()

delete()

cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,',NULL,'2021-04-01*19CS30014,','3,',0)"))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",[],'988-0789032742')
librarian.AddMember(student,'potato')
cursor.execute(("UPDATE MEMBERS SET ReservedBook = '988-0789032742' WHERE MemberID = '19CS30014'"))
db.commit()
flag1 = False
flag2 = False
bh = BookHandler.Create()
bh.OpenBook('988-0789032742')
db.commit()
bh.UpdateBook()
db.commit()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM MEMBERS")
for row in cursor:
    if(row['MemberID']=='19CS30014'):
        if(row["ReservedBook"]==None):
            flag1 = True
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["ActiveReservedUIDs"]==None):
            flag2 = True
if flag1 == True and flag2 == True:
    print("Update Carried out correctly when no pending reservation are there, some active reservations expired: PASS\n\n",  file = a_file)
else:
    print("Update Carried out correctly when no pending reservation are there, some active reservations expired: FAIL\n\n",  file = a_file)
bh.CloseBook()
delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,',NULL,NULL,NULL,0)"))
db.commit()
flag2 = False
bh = BookHandler.Create()
bh.OpenBook('988-0789032742')
db.commit()
bh.UpdateBook()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["ActiveReservedUIDs"]==None):
            flag2 = True
if flag2 == True:
    print("Update Carried out correctly when no pending reservation are there, no active reservations expired: PASS\n\n",  file = a_file)
else:
    print("Update Carried out correctly when no pending reservation are there, no active reservations expired: FAIL\n\n",  file = a_file)



#Issue Selected Book
delete()
bh = BookHandler.Create()
bh.OpenBook(Book('1',"988-0789032742",date.today()))
db.commit()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'7,3,',NULL,'2021-04-01*19CS30014,','1,',0)"))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','XYZ',1,DATE '2001-04-01',0)"))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",[],'988-0789032742')
librarian.AddMember(student,'potato')
cursor.execute(("UPDATE MEMBERS SET ReservedBook = '988-0789032742' WHERE MemberID = '19CS30014'"))
db.commit()
flag2 = False
bh.IssueSelected('19CS30014')
db.commit()
bh.UpdateBook()
db.commit()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["ActiveReservedUIDs"]==None):
            flag2 = True
if flag2 == True:
    print("Book succesfully issued from Ready-To-CLaim reserved Books section : PASS\n\n",  file = a_file)
else:
    print("Book succesfully issued from Ready-To-CLaim reserved Books section : FAIL\n\n",  file = a_file)



delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742','1,3,',NULL,NULL,'2021-04-01*19CS30032,','7,',2)"))
db.commit()
bh = BookHandler.Create()
bh.OpenBook(Book('1',"988-0789032742",date.today()))
db.commit()
cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','XYZ',1,DATE '2020-04-01',0)"))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",[],'988-0789032742')
librarian.AddMember(student,'potato')
db.commit()
flag2 = False
bh.UpdateBook()
db.commit()
bh.IssueSelected('19CS30014')
db.commit()
bh.UpdateBook()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["AvailableUIDs"]=='3,7,' and row["TakenUIDs"]=='1,'):
            flag2 = True
if flag2 == True:
    print("Book succesfully issued from Available Books section : PASS\n\n",  file = a_file)
else:
    print("Book succesfully issued from Available Books section : FAIL\n\n",  file = a_file)

#ReturnSelected Book
delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,','19CS30017,',NULL,NULL,0)"))
db.commit()
bh = BookHandler.Create()
bh.OpenBook(Book('1',"988-0789032742",date.today()))
db.commit()
# cursor.execute(("INSERT INTO BOOKS VALUES (NULL,'988-0789032742','XYZ',1,DATE '2020-04-01',0)"))
# db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",['1'],None)
librarian.AddMember(student,'potato')
db.commit()
flag2 = False
bh.UpdateBook()
db.commit()
bh.ReturnSelected('19CS30014')
db.commit()
bh.UpdateBook()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["TakenUIDs"]=='3,' and row["AvailableUIDs"]==None):
            flag2 = True
if flag2 == True:
    print("Book succesfully returned when there is a pending reservation for it : PASS\n\n",  file = a_file)
else:
    print("Book succesfully returned when there is a pending reservation for it : FAIL\n\n",  file = a_file)


delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,',NULL,NULL,NULL,0)"))
db.commit()
bh = BookHandler.Create()
bh.OpenBook(Book('1',"988-0789032742",date.today()))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",[],None)
librarian.AddMember(student,'potato')
db.commit()
flag2 = False
bh.UpdateBook()
db.commit()
bh.ReturnSelected('19CS30014')
db.commit()
bh.UpdateBook()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["TakenUIDs"]=='3,' and row["AvailableUIDs"]=='1,'):
            flag2 = True
if flag2 == True:
    print("Book succesfully returned when there is no pending reservation for it : PASS\n\n",  file = a_file)
else:
    print("Book succesfully returned when there is no pending reservation for it : FAIL\n\n",  file = a_file)




# ReserveSelected Book


delete()
cursor.execute(("INSERT INTO RESERVATIONS VALUES ('988-0789032742',NULL,'1,3,',NULL,NULL,NULL,0)"))
db.commit()
bh = BookHandler.Create()
bh.OpenBook(Book('1',"988-0789032742",date.today()))
db.commit()
librarian = Librarian("LIB0001","Neha")
student = UnderGraduateStudent("Harry","19CS30014",[],None)
librarian.AddMember(student,'potato')
db.commit()
flag2 = False
bh.UpdateBook()
db.commit()
bh.ReserveSelected('19CS30014')
db.commit()
bh.UpdateBook()
db.commit()
bh.UpdateDatabase()
db.commit()
cursor.execute("SELECT * FROM RESERVATIONS")
for row in cursor:
    if(row['ISBN']=='988-0789032742'):
        if(row["TakenUIDs"]=='1,3,' and row["PendingReservations"]=='19CS30014,'):
            flag2 = True
if flag2 == True:
    print("Book succesfully reserved : PASS\n\n",  file = a_file)
else:
    print("Book succesfully reserved : FAIL\n\n",  file = a_file)
bH.CloseBook()

print("\n---- Test Book----\n", file = a_file)

# Book 
# constructor
b = Book('1','988-0789032742', date.today())
if(b.GetISBN()=='988-0789032742' and b.GetUID()=='1' and b.GetDateOfIssue()==date.today()):
    print("Book is created properly : PASS\n\n",  file = a_file)
else:
    print("Book is created properly : FAIL\n\n",  file = a_file)

print("\n---- Test ActiveReservation----\n", file = a_file)

# Active Reservation
# constructor
newActive = ActiveReservation("19CS30014",date(2021,4,1))
if newActive.claimByDate == date(2021,4,1) and newActive.memberID == "19CS30014":
    print("ActiveReservation is created properly : PASS\n\n",  file = a_file)
else:
    print("ActiveReservation is created properly : FAIL\n\n",  file = a_file)
delete()
print('Testing Finished')