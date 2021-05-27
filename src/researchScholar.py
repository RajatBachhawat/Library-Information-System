from libraryMember import LibraryMember


class ResearchScholar(LibraryMember):
    __maxBooksAllowed = 6
    __maxMonthsAllowed = 3

    def __init__(self, *args):
        LibraryMember.__init__(self, *args)


    def CanIssue(self):
        return (self._numberOfBooksIssued < ResearchScholar.__maxBooksAllowed)

    def GetMaxBooksAllowed(self):
        return ResearchScholar.__maxBooksAllowed
    def GetMaxMonthsAllowed(self):
        return ResearchScholar.__maxMonthsAllowed