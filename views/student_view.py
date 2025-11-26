# views/student_view.py
import customtkinter as ctk
import tkinter.messagebox as tkmb
from datetime import datetime

class StudentView(ctk.CTkFrame):
    def __init__(self, parent, db, user, logout_callback):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.logout_callback = logout_callback
        
        self.configure(fg_color="#f0f0f0")
        
        # Header
        self.create_header()
        
        # Tabview
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tabs
        self.tabview.add("Submit Complaint")
        self.tabview.add("My Complaints")
        self.tabview.add("Profile")
        
        # Build tabs
        self.build_submit_tab()
        self.build_complaints_tab()
        self.build_profile_tab()
    
    def create_header(self):
        header = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="#1e3a8a")
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text=f"Welcome, {self.user[4]} 👨‍🎓", 
                    font=("Helvetica", 22, "bold"), text_color="white").pack(side="left", padx=30)
        
        ctk.CTkLabel(header, text=f"Roll No: {self.user[7]}", 
                    font=("Helvetica", 14), text_color="#a8dadc").pack(side="left", padx=10)
        
        ctk.CTkButton(header, text="Logout", command=self.logout_callback,
                     fg_color="#dc2626", hover_color="#991b1b", width=100).pack(side="right", padx=30)
    
    def build_submit_tab(self):
        tab = self.tabview.tab("Submit Complaint")
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(scroll_frame, text="Submit New Complaint", 
                    font=("Helvetica", 24, "bold")).pack(pady=(0, 20))
        
        # Form
        form = ctk.CTkFrame(scroll_frame, corner_radius=15)
        form.pack(fill="x", pady=10)
        
        # Name
        ctk.CTkLabel(form, text="Full Name*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(20, 5))
        self.name_entry = ctk.CTkEntry(form, placeholder_text="Enter your full name", height=35)
        self.name_entry.insert(0, self.user[4])
        self.name_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Roll No
        ctk.CTkLabel(form, text="Roll Number*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        self.rollno_entry = ctk.CTkEntry(form, placeholder_text="Enter roll number", height=35)
        self.rollno_entry.insert(0, self.user[7] if self.user[7] else "")
        self.rollno_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Department
        ctk.CTkLabel(form, text="Department*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        departments = ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical", 
                      "Information Technology", "Chemical", "Biotechnology"]
        self.dept_combo = ctk.CTkComboBox(form, values=departments, height=35)
        self.dept_combo.set(self.user[6] if self.user[6] else departments[0])
        self.dept_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Course
        ctk.CTkLabel(form, text="Course/Program*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        courses = ["B.Tech", "M.Tech", "B.Sc", "M.Sc", "BCA", "MCA", "Diploma", "PhD"]
        self.course_combo = ctk.CTkComboBox(form, values=courses, height=35)
        self.course_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Gender
        ctk.CTkLabel(form, text="Gender*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        gender_frame = ctk.CTkFrame(form, fg_color="transparent")
        gender_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.gender_var = ctk.StringVar(value="Male")
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side="left", padx=10)
        ctk.CTkRadioButton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(side="left", padx=10)
        
        # Category
        ctk.CTkLabel(form, text="Complaint Category*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        categories = self.db.get_categories()
        self.category_combo = ctk.CTkComboBox(form, values=categories, height=35)
        self.category_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Priority
        ctk.CTkLabel(form, text="Priority Level*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        self.priority_combo = ctk.CTkComboBox(form, values=["Low", "Medium", "High", "Critical"], height=35)
        self.priority_combo.set("Medium")
        self.priority_combo.pack(fill="x", padx=20, pady=(0, 15))
        
        # Complaint
        ctk.CTkLabel(form, text="Complaint Description*", anchor="w", font=("Helvetica", 12, "bold")).pack(fill="x", padx=20, pady=(0, 5))
        self.complaint_text = ctk.CTkTextbox(form, height=150)
        self.complaint_text.pack(fill="x", padx=20, pady=(0, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkButton(btn_frame, text="Submit Complaint", command=self.submit_complaint,
                     height=40, font=("Helvetica", 14, "bold"),
                     fg_color="#10b981", hover_color="#059669").pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="Clear Form", command=self.clear_form,
                     height=40, font=("Helvetica", 14, "bold"),
                     fg_color="#6b7280", hover_color="#4b5563").pack(side="left", padx=5)
    
    def build_complaints_tab(self):
        tab = self.tabview.tab("My Complaints")
        
        # Header
        header_frame = ctk.CTkFrame(tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(header_frame, text="My Complaints", 
                    font=("Helvetica", 24, "bold")).pack(side="left")
        
        ctk.CTkButton(header_frame, text="🔄 Refresh", command=self.load_complaints,
                     width=100).pack(side="right", padx=5)
        
        # Complaints list
        self.complaints_frame = ctk.CTkScrollableFrame(tab)
        self.complaints_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.load_complaints()
    
    def build_profile_tab(self):
        tab = self.tabview.tab("Profile")
        
        profile_frame = ctk.CTkFrame(tab, corner_radius=15)
        profile_frame.pack(fill="both", expand=True, padx=100, pady=50)
        
        ctk.CTkLabel(profile_frame, text="Profile Information", 
                    font=("Helvetica", 24, "bold")).pack(pady=30)
        
        info = [
            ("Username", self.user[1]),
            ("Full Name", self.user[4]),
            ("Email", self.user[5]),
            ("Department", self.user[6]),
            ("Roll Number", self.user[7]),
            ("Account Created", str(self.user[8])[:16] if len(self.user) > 8 else "N/A")
        ]
        
        for label, value in info:
            row = ctk.CTkFrame(profile_frame, fg_color="transparent")
            row.pack(fill="x", padx=40, pady=10)
            
            ctk.CTkLabel(row, text=f"{label}:", font=("Helvetica", 14, "bold"), 
                        anchor="w", width=150).pack(side="left")
            ctk.CTkLabel(row, text=str(value), font=("Helvetica", 14), 
                        anchor="w").pack(side="left", padx=20)
    
    def submit_complaint(self):
        name = self.name_entry.get().strip()
        roll_no = self.rollno_entry.get().strip()
        department = self.dept_combo.get()
        course = self.course_combo.get()
        gender = self.gender_var.get()
        complaint = self.complaint_text.get("1.0", "end").strip()
        category = self.category_combo.get()
        priority = self.priority_combo.get()
        
        # Validation
        if not all([name, roll_no, department, course, complaint]):
            tkmb.showerror("Error", "Please fill all required fields!")
            return
        
        if len(complaint) < 20:
            tkmb.showerror("Error", "Complaint must be at least 20 characters!")
            return
        
        # Submit
        self.db.add_complaint(self.user[0], name, roll_no, department, course, gender, complaint, category, priority)
        tkmb.showinfo("Success", "Complaint submitted successfully!")
        self.clear_form()
        self.load_complaints()
    
    def clear_form(self):
        self.complaint_text.delete("1.0", "end")
        self.priority_combo.set("Medium")
    
    def load_complaints(self):
        for widget in self.complaints_frame.winfo_children():
            widget.destroy()
        
        complaints = self.db.get_user_complaints(self.user[0])
        
        if not complaints:
            ctk.CTkLabel(self.complaints_frame, text="No complaints yet", 
                        font=("Helvetica", 16)).pack(pady=50)
            return
        
        for comp in complaints:
            self.create_complaint_card(comp)
    
    def create_complaint_card(self, comp):
        card = ctk.CTkFrame(self.complaints_frame, corner_radius=10)
        card.pack(fill="x", pady=10, padx=10)
        
        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(header, text=f"Complaint #{comp[0]}", 
                    font=("Helvetica", 16, "bold")).pack(side="left")
        
        # Status badge
        status_colors = {"Open": "#ef4444", "In Progress": "#f59e0b", "Resolved": "#10b981", "Closed": "#6b7280"}
        status_label = ctk.CTkLabel(header, text=comp[9], 
                                   font=("Helvetica", 12, "bold"),
                                   fg_color=status_colors.get(comp[9], "#6b7280"),
                                   corner_radius=5, text_color="white")
        status_label.pack(side="right", padx=5)
        
        # Priority badge
        priority_colors = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444", "Critical": "#7c2d12"}
        priority_label = ctk.CTkLabel(header, text=comp[8], 
                                     font=("Helvetica", 12, "bold"),
                                     fg_color=priority_colors.get(comp[8], "#6b7280"),
                                     corner_radius=5, text_color="white")
        priority_label.pack(side="right", padx=5)
        
        # Details
        details = ctk.CTkFrame(card, fg_color="transparent")
        details.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(details, text=f"Category: {comp[7]} | Course: {comp[4]} | Submitted: {comp[10][:16]}", 
                    font=("Helvetica", 11), text_color="gray").pack(anchor="w")
        
        # Complaint text
        complaint_label = ctk.CTkLabel(card, text=comp[6], font=("Helvetica", 12),
                                      anchor="w", justify="left", wraplength=800)
        complaint_label.pack(fill="x", padx=15, pady=(5, 15))
        
        # View details button
        ctk.CTkButton(card, text="View Details", command=lambda: self.view_complaint_details(comp[0]),
                     width=120, height=30).pack(anchor="e", padx=15, pady=(0, 15))
    
    def view_complaint_details(self, complaint_id):
        ComplaintDetailWindow(self, self.db, complaint_id, self.user)


class ComplaintDetailWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, complaint_id, user):
        super().__init__(parent)
        
        self.db = db
        self.complaint_id = complaint_id
        self.user = user
        
        self.title(f"Complaint #{complaint_id} Details")
        self.geometry("700x600")
        
        # Load complaint
        complaint = db.get_complaint_by_id(complaint_id)
        
        if not complaint:
            self.destroy()
            return
        
        # Main frame
        main = ctk.CTkScrollableFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(main, text=f"Complaint #{complaint[0]}", 
                    font=("Helvetica", 22, "bold")).pack(pady=(0, 20))
        
        # Info grid
        info_frame = ctk.CTkFrame(main, corner_radius=10)
        info_frame.pack(fill="x", pady=10)
        
        info = [
            ("Name", complaint[2]),
            ("Roll No", complaint[3]),
            ("Department", complaint[4]),
            ("Course", complaint[5]),
            ("Category", complaint[8]),
            ("Priority", complaint[9]),
            ("Status", complaint[10]),
            ("Submitted", str(complaint[11])[:16])
        ]
        
        for i, (label, value) in enumerate(info):
            row = i // 2
            col = i % 2
            
            frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            frame.grid(row=row, column=col, padx=15, pady=8, sticky="w")
            
            ctk.CTkLabel(frame, text=f"{label}:", font=("Helvetica", 12, "bold")).pack(side="left")
            ctk.CTkLabel(frame, text=str(value), font=("Helvetica", 12)).pack(side="left", padx=10)
        
        # Complaint text
        ctk.CTkLabel(main, text="Complaint Description:", 
                    font=("Helvetica", 14, "bold"), anchor="w").pack(fill="x", pady=(20, 5))
        
        complaint_box = ctk.CTkTextbox(main, height=100, wrap="word")
        complaint_box.insert("1.0", complaint[7])
        complaint_box.configure(state="disabled")
        complaint_box.pack(fill="x", pady=(0, 20))
        
        # Responses
        ctk.CTkLabel(main, text="Responses:", font=("Helvetica", 14, "bold"), 
                    anchor="w").pack(fill="x", pady=(10, 5))
        
        responses = db.get_responses(complaint_id)
        
        if responses:
            for resp in responses:
                self.create_response_card(main, resp)
        else:
            ctk.CTkLabel(main, text="No responses yet", 
                        font=("Helvetica", 12), text_color="gray").pack(pady=10)
    
    def create_response_card(self, parent, response):
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color="#e0f2fe")
        card.pack(fill="x", pady=5)
        
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(header, text=f"{response[4]} ({response[5]})", 
                    font=("Helvetica", 12, "bold")).pack(side="left")
        ctk.CTkLabel(header, text=str(response[3])[:16], 
                    font=("Helvetica", 10), text_color="gray").pack(side="right")
        
        ctk.CTkLabel(card, text=response[2], font=("Helvetica", 11),
                    anchor="w", justify="left", wraplength=600).pack(fill="x", padx=10, pady=(0, 10))
