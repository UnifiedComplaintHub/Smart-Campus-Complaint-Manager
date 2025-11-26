# views/login_view.py
import customtkinter as ctk
import tkinter.messagebox as tkmb

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, db, on_success_callback):
        super().__init__(parent)
        self.db = db
        self.on_success_callback = on_success_callback
        
        self.configure(fg_color="#1a1a2e")
        
        # Center frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        center_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=20)
        center_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(center_frame, text="🎓 College Complaint Management", 
                            font=("Helvetica", 28, "bold"), text_color="#00d9ff")
        title.grid(row=0, column=0, columnspan=2, pady=(30, 10))
        
        subtitle = ctk.CTkLabel(center_frame, text="Secure Login Portal", 
                               font=("Helvetica", 14), text_color="#a8dadc")
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Role selection
        self.role_var = ctk.StringVar(value="Student")
        
        role_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        role_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(role_frame, text="Login as:", font=("Helvetica", 14, "bold")).pack(side="left", padx=10)
        
        student_radio = ctk.CTkRadioButton(role_frame, text="Student 👨‍🎓", variable=self.role_var, 
                                          value="Student", font=("Helvetica", 12))
        student_radio.pack(side="left", padx=10)
        
        teacher_radio = ctk.CTkRadioButton(role_frame, text="Teacher 👨‍🏫", variable=self.role_var, 
                                          value="Teacher", font=("Helvetica", 12))
        teacher_radio.pack(side="left", padx=10)
        
        # Username
        ctk.CTkLabel(center_frame, text="Username:", font=("Helvetica", 13)).grid(row=3, column=0, 
                                                                                  sticky="w", padx=40, pady=10)
        self.username_entry = ctk.CTkEntry(center_frame, width=300, height=40, 
                                          placeholder_text="Enter username", font=("Helvetica", 12))
        self.username_entry.grid(row=3, column=1, padx=40, pady=10)
        
        # Password
        ctk.CTkLabel(center_frame, text="Password:", font=("Helvetica", 13)).grid(row=4, column=0, 
                                                                                  sticky="w", padx=40, pady=10)
        self.password_entry = ctk.CTkEntry(center_frame, width=300, height=40, show="*",
                                          placeholder_text="Enter password", font=("Helvetica", 12))
        self.password_entry.grid(row=4, column=1, padx=40, pady=10)
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Buttons
        btn_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        login_btn = ctk.CTkButton(btn_frame, text="Login", width=140, height=40,
                                 command=self.login, font=("Helvetica", 14, "bold"),
                                 fg_color="#00d9ff", hover_color="#00b8d4")
        login_btn.pack(side="left", padx=10)
        
        register_btn = ctk.CTkButton(btn_frame, text="Register", width=140, height=40,
                                    command=self.show_register, font=("Helvetica", 14, "bold"),
                                    fg_color="#4a4e69", hover_color="#22223b")
        register_btn.pack(side="left", padx=10)
        
        # Info label
        info = ctk.CTkLabel(center_frame, text="Default Admin: username=admin, password=admin123", 
                           font=("Helvetica", 10), text_color="#777")
        info.grid(row=6, column=0, columnspan=2, pady=(10, 20))
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()
        
        if not username or not password:
            tkmb.showerror("Error", "Please enter both username and password!")
            return
        
        user = self.db.authenticate_user(username, password, role)
        
        if user:
            tkmb.showinfo("Success", f"Welcome, {user[4]}!")
            self.on_success_callback(user, role)
        else:
            tkmb.showerror("Error", "Invalid credentials or role!")
    
    def show_register(self):
        RegisterWindow(self, self.db, self.role_var.get())


class RegisterWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, default_role):
        super().__init__(parent)
        
        self.db = db
        self.title("Register New Account")
        self.geometry("550x800")
        self.resizable(False, False)
        
        # Configure
        self.configure(fg_color="#1a1a2e")
        
        main_frame = ctk.CTkFrame(self, fg_color="#16213e", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(main_frame, text="Create New Account", 
                    font=("Helvetica", 24, "bold"), text_color="#00d9ff").pack(pady=20)
        
        # Role
        role_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        role_frame.pack(pady=10)
        
        ctk.CTkLabel(role_frame, text="Register as:", font=("Helvetica", 12, "bold")).pack(side="left", padx=10)
        
        self.role_var = ctk.StringVar(value=default_role)
        ctk.CTkRadioButton(role_frame, text="Student", variable=self.role_var, value="Student",
                          command=self.toggle_role).pack(side="left", padx=5)
        ctk.CTkRadioButton(role_frame, text="Teacher", variable=self.role_var, value="Teacher",
                          command=self.toggle_role).pack(side="left", padx=5)
        
        # Form fields - using scrollable frame for better visibility
        form_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Username
        ctk.CTkLabel(form_frame, text="Username*", anchor="w").pack(fill="x", pady=(10, 5))
        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="Choose a username", height=35)
        self.username_entry.pack(fill="x", pady=(0, 10))
        
        # Password
        ctk.CTkLabel(form_frame, text="Password*", anchor="w").pack(fill="x", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Choose a password", show="*", height=35)
        self.password_entry.pack(fill="x", pady=(0, 10))
        
        # Confirm Password
        ctk.CTkLabel(form_frame, text="Confirm Password*", anchor="w").pack(fill="x", pady=(0, 5))
        self.confirm_password_entry = ctk.CTkEntry(form_frame, placeholder_text="Re-enter password", show="*", height=35)
        self.confirm_password_entry.pack(fill="x", pady=(0, 10))
        
        # Full Name
        ctk.CTkLabel(form_frame, text="Full Name*", anchor="w").pack(fill="x", pady=(0, 5))
        self.fullname_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter your full name", height=35)
        self.fullname_entry.pack(fill="x", pady=(0, 10))
        
        # Email
        ctk.CTkLabel(form_frame, text="Email*", anchor="w").pack(fill="x", pady=(0, 5))
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="your.email@college.edu", height=35)
        self.email_entry.pack(fill="x", pady=(0, 10))
        
        # Department
        ctk.CTkLabel(form_frame, text="Department*", anchor="w").pack(fill="x", pady=(0, 5))
        departments = ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical", 
                      "Information Technology", "Chemical", "Biotechnology", "Mathematics", "Physics"]
        self.department_combo = ctk.CTkComboBox(form_frame, values=departments, height=35)
        self.department_combo.pack(fill="x", pady=(0, 10))
        
        # Roll No (for students only)
        self.rollno_label = ctk.CTkLabel(form_frame, text="Roll Number*", anchor="w")
        self.rollno_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g., 2021CS001", height=35)
        
        self.toggle_role()
        
        # Register button - FIXED: Placed outside scrollable frame
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkButton(button_frame, text="Register Account", command=self.register,
                     height=40, width=200, font=("Helvetica", 14, "bold"),
                     fg_color="#00d9ff", hover_color="#00b8d4").pack(side="left", expand=True, padx=5)
        
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy,
                     height=40, width=100, font=("Helvetica", 14, "bold"),
                     fg_color="#6b7280", hover_color="#4b5563").pack(side="left", padx=5)
    
    def toggle_role(self):
        if self.role_var.get() == "Student":
            self.rollno_label.pack(fill="x", pady=(0, 5))
            self.rollno_entry.pack(fill="x", pady=(0, 10))
        else:
            self.rollno_label.pack_forget()
            self.rollno_entry.pack_forget()
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        full_name = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        department = self.department_combo.get()
        role = self.role_var.get()
        roll_no = self.rollno_entry.get().strip() if role == "Student" else None
        
        # Validation
        if not all([username, password, full_name, email, department]):
            tkmb.showerror("Error", "Please fill all required fields!")
            return
        
        if role == "Student" and not roll_no:
            tkmb.showerror("Error", "Roll number is required for students!")
            return
        
        if password != confirm_password:
            tkmb.showerror("Error", "Passwords do not match!")
            return
        
        if len(password) < 6:
            tkmb.showerror("Error", "Password must be at least 6 characters!")
            return
        
        if "@" not in email:
            tkmb.showerror("Error", "Please enter a valid email!")
            return
        
        # Register user
        success, message = self.db.register_user(username, password, role, full_name, email, department, roll_no)
        
        if success:
            tkmb.showinfo("Success", message)
            self.destroy()
        else:
            tkmb.showerror("Error", message)
