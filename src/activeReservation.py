from datetime import date
class ActiveReservation:
    def __init__(self, memberID, claimByDate):
        self.memberID = memberID
        self.claimByDate = claimByDate
    
    def __str__(self):
        return '(' + str(self.memberID) + ', ' + str(self.claimByDate) + ')'