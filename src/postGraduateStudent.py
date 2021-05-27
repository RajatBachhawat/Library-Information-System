from libraryMember import LibraryMember


class PostGraduateStudent(LibraryMember):
    __maxBooksAllowed = 4
    __maxMonthsAllowed = 1

    def __init__(self, *args):
        LibraryMember.__init__(self, *args)

    def CanIssue(self):
        return (self._numberOfBooksIssued < PostGraduateStudent.__maxBooksAllowed)
    def GetMaxBooksAllowed(self):
        return PostGraduateStudent.__maxBooksAllowed
    def GetMaxMonthsAllowed(self):
        return PostGraduateStudent.__maxMonthsAllowed