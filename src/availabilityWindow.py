from tkinter import *
from colors import *
from availabilityFrames import *
from underGraduateStudent import UnderGraduateStudent

class AvailabiltyWindow():
    def __init__(self, mode, member, response):
        self.member = member
        self.response = response
        self.mode = mode

        self.availRoot = Tk()
        self.availRoot.geometry("600x500")
        self.availRoot.wm_title("Check Availability")
        self.availRoot.config(bg=orange)

        self.frames = [
            AvailableFrame(self.availRoot, self.member, self.response),
            ClaimFrame(self.availRoot, self.member, self.response),
            PendingFrame(self.availRoot, self.member, self.response),
            ReserveFrame(self.availRoot, self.member, self.response),
            NoReserveFrame(self.availRoot, self.member, self.response)
        ]
        # print(type(self.frames[self.mode]))
        self.frames[self.mode].grid(column=0, row=0)

        self.availRoot.mainloop()


# for i in range(5):
# a = AvailabiltyWindow(4, UnderGraduateStudent("Chappidi Yoga Satwik", "19CS30013", [], None), "")
