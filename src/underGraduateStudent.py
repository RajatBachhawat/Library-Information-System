from datetime import date, datetime, timedelta
from book import Book
from libraryMember import LibraryMember

class UnderGraduateStudent(LibraryMember):
    __maxBooksAllowed = 2
    __maxMonthsAllowed = 1

    def __init__(self, *args):
        LibraryMember.__init__(self, *args)

    def CanIssue(self):
        # print(self._numberOfBooksIssued)
        # print(UnderGraduateStudent.__maxBooksAllowed)
        return (self._numberOfBooksIssued < UnderGraduateStudent.__maxBooksAllowed)

    def GetMaxBooksAllowed(self):
        return UnderGraduateStudent.__maxBooksAllowed
    def GetMaxMonthsAllowed(self):
        return UnderGraduateStudent.__maxMonthsAllowed

# mem = UnderGraduateStudent('19CS30056', 'Neha', ["3"], None, 1)
# print(mem.CheckForReminder())
# mem.UpdateFromDatabase()
# print(mem.CheckAvailabilityOfBook('998-0767892743'))
# mem.IssueBook(Book(6, '998-0767892743',None,None))