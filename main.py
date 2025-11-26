# main.py
import customtkinter as ctk
import tkinter.messagebox as tkmb
from database import Database
from views.login_view import LoginView
from views.student_view import StudentView
from views.teacher_view import TeacherView

class ComplaintManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.title("College Complaint Management System")
        self.geometry("1200x700")
        self.resizable(True, True)
        
        # Initialize database
        self.db = Database()
        
        # Current user and view
        self.current_user = None
        self.current_view = None
        
        # Show login screen
        self.show_login()
    
    def show_login(self):
        """Display login screen"""
        if self.current_view:
            self.current_view.destroy()
        
        self.current_user = None
        self.current_view = LoginView(self, self.db, self.on_login_success)
        self.current_view.pack(fill="both", expand=True)
    
    def on_login_success(self, user, role):
        """Called when user successfully logs in"""
        self.current_user = user
        
        if self.current_view:
            self.current_view.destroy()
        
        if role == "Student":
            self.current_view = StudentView(self, self.db, user, self.logout)
        else:  # Teacher
            self.current_view = TeacherView(self, self.db, user, self.logout)
        
        self.current_view.pack(fill="both", expand=True)
    
    def logout(self):
        """Logout current user"""
        self.show_login()
    
    def on_closing(self):
        """Clean up on window close"""
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = ComplaintManagementApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
