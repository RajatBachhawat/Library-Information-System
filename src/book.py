from datetime import date
class Book():
    def __init__(self, UID, ISBN, dateOfIssue):
        self.__UID = UID
        self.__ISBN = ISBN
        self.__dateOfIssue = dateOfIssue
        self.__dueDate = None

    def GetUID(self):
        return self.__UID
    def GetISBN(self):
        return self.__ISBN
    def GetDateOfIssue(self):
        return self.__dateOfIssue
