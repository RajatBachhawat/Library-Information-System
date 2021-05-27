from libraryMember import LibraryMember


class FacultyMember(LibraryMember):
    __maxBooksAllowed = 10
    __maxMonthsAllowed = 6

    def __init__(self, *args):
        LibraryMember.__init__(self, *args)


    def CanIssue(self):
        return (self._numberOfBooksIssued < FacultyMember.__maxBooksAllowed)
    
    def GetMaxBooksAllowed(self):
        return FacultyMember.__maxBooksAllowed
    def GetMaxMonthsAllowed(self):
        return FacultyMember.__maxMonthsAllowed