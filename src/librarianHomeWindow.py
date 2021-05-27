from tkinter import *
from colors import *
from librarianFrames import *
from clerkHomeWindow import ClerkHomeWindow
# from libraryMember import 

class LibrarianHomeWindow(ClerkHomeWindow):
    def __init__(self, master, mainWindow, librarian):
        super().__init__(master, mainWindow, librarian)
        self.master = master
        self.mainWindow = mainWindow
        self.librarian = librarian

        self.config(bg=orange)

        self.addMemberButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Add Member", command=self.ShowAddMember)
        self.addMemberButton.grid(column=0, row=5, pady=10, padx=80)
        
        self.deleteMemberButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Delete Member", command=self.ShowDeleteMember)
        self.deleteMemberButton.grid(column=0, row=6, pady=10, padx=80)
        
        self.checkStatsButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Check Issue Statistics", command=self.ShowCheckStats)
        self.checkStatsButton.grid(column=0, row=7, pady=10, padx=120)
        
        self.sendRemButton = Button(self.employeeOptionsFrame, bg=orange, fg=white, text="Send Reminders", command=self.ShowSendRem)
        self.sendRemButton.grid(column=0, row=8, pady=10, padx=120)
        
        self.blankLabel.grid(column=0, row=10, pady=150, padx=80)
        self.logoutButton.grid(column=0, row=9, pady=10, padx=80)

    def ShowAddMember(self):
        if self.currFrame:
            self.currFrame.grid_forget()

        if not hasattr(self, 'addMemberFrame'):
            self.addMemberFrame = AddMemberFrame(self.rightFrame, self.librarian)
            
        self.currFrame = self.addMemberFrame
        self.addMemberFrame.grid(column=0, row=0, pady=10)
    
    def ShowDeleteMember(self):
        if self.currFrame:
            self.currFrame.grid_forget()
        
        if not hasattr(self, 'deleteMemberFrame'):
            self.deleteMemberFrame = DeleteMemberFrame(self.rightFrame, self.librarian)
            
        self.currFrame = self.deleteMemberFrame
        self.deleteMemberFrame.grid(column=0, row=0, pady=10)

    def ShowCheckStats(self):
        if self.currFrame:
            self.currFrame.grid_forget()

        if not hasattr(self, 'checkStatsFrame'):
            self.checkStatsFrame = CheckIssueStats(self.rightFrame, self.librarian)
            
        self.currFrame = self.checkStatsFrame
        self.checkStatsFrame.grid(column=0, row=0, pady=10)

    def ShowSendRem(self):
        if self.currFrame:
            self.currFrame.grid_forget()

        if not hasattr(self, 'sendRemFrame'):
            self.sendRemFrame = SendReminderFrame(self.rightFrame, self.librarian)
            
        self.currFrame = self.sendRemFrame
        self.sendRemFrame.grid(column=0, row=0, pady=10)