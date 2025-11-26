# views/teacher_view.py
import customtkinter as ctk
import tkinter.messagebox as tkmb
from tkinter import filedialog
import csv
from datetime import datetime

class TeacherView(ctk.CTkFrame):
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
        self.tabview.add("All Complaints")
        self.tabview.add("Dashboard")
        self.tabview.add("Profile")
        
        # Build tabs
        self.build_complaints_tab()
        self.build_dashboard_tab()
        self.build_profile_tab()
    
    def create_header(self):
        header = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="#7c2d12")
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text=f"Welcome, {self.user[4]} 👨‍🏫", 
                    font=("Helvetica", 22, "bold"), text_color="white").pack(side="left", padx=30)
        
        ctk.CTkLabel(header, text=f"Department: {self.user[6]}", 
                    font=("Helvetica", 14), text_color="#fcd34d").pack(side="left", padx=10)
        
        ctk.CTkButton(header, text="Logout", command=self.logout_callback,
                     fg_color="#dc2626", hover_color="#991b1b", width=100).pack(side="right", padx=30)
    
    def build_complaints_tab(self):
        tab = self.tabview.tab("All Complaints")
        
        # Filters and search
        filter_frame = ctk.CTkFrame(tab, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=20)
        
        # Search
        ctk.CTkLabel(filter_frame, text="Search:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(filter_frame, textvariable=self.search_var, width=200)
        self.search_entry.grid(row=0, column=1, padx=5)
        
        # Status filter
        ctk.CTkLabel(filter_frame, text="Status:", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=5)
        self.status_filter = ctk.CTkComboBox(filter_frame, values=["All", "Open", "In Progress", "Resolved", "Closed"], width=120)
        self.status_filter.set("All")
        self.status_filter.grid(row=0, column=3, padx=5)
        
        # Category filter
        ctk.CTkLabel(filter_frame, text="Category:", font=("Helvetica", 12, "bold")).grid(row=0, column=4, padx=5)
        categories = ["All"] + self.db.get_categories()
        self.category_filter = ctk.CTkComboBox(filter_frame, values=categories, width=150)
        self.category_filter.set("All")
        self.category_filter.grid(row=0, column=5, padx=5)
        
        # Priority filter
        ctk.CTkLabel(filter_frame, text="Priority:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=10)
        self.priority_filter = ctk.CTkComboBox(filter_frame, values=["All", "Low", "Medium", "High", "Critical"], width=120)
        self.priority_filter.set("All")
        self.priority_filter.grid(row=1, column=1, padx=5, pady=10)
        
        # Buttons
        ctk.CTkButton(filter_frame, text="🔍 Search", command=self.load_complaints, width=100).grid(row=1, column=2, padx=5)
        ctk.CTkButton(filter_frame, text="🔄 Refresh", command=self.load_complaints, width=100).grid(row=1, column=3, padx=5)
        ctk.CTkButton(filter_frame, text="📊 Export CSV", command=self.export_to_csv, 
                     fg_color="#10b981", hover_color="#059669", width=120).grid(row=1, column=4, padx=5)
        
        # Complaints list
        self.complaints_frame = ctk.CTkScrollableFrame(tab)
        self.complaints_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.load_complaints()
    
    def build_dashboard_tab(self):
        tab = self.tabview.tab("Dashboard")
        
        # Title
        ctk.CTkLabel(tab, text="Analytics Dashboard", 
                    font=("Helvetica", 28, "bold")).pack(pady=20)
        
        # Stats container
        stats_container = ctk.CTkFrame(tab, fg_color="transparent")
        stats_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Get statistics
        stats = self.db.get_statistics()
        
        # Stats cards
        cards_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
        cards_frame.pack(fill="x", pady=20)
        
        # Total complaints
        self.create_stat_card(cards_frame, "Total Complaints", stats['total'], "#3b82f6", 0)
        
        # Open complaints
        open_count = stats['by_status'].get('Open', 0)
        self.create_stat_card(cards_frame, "Open", open_count, "#ef4444", 1)
        
        # In Progress
        progress_count = stats['by_status'].get('In Progress', 0)
        self.create_stat_card(cards_frame, "In Progress", progress_count, "#f59e0b", 2)
        
        # Resolved
        resolved_count = stats['by_status'].get('Resolved', 0)
        self.create_stat_card(cards_frame, "Resolved", resolved_count, "#10b981", 3)
        
        # By Category
        category_frame = ctk.CTkFrame(stats_container, corner_radius=15)
        category_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(category_frame, text="Complaints by Category", 
                    font=("Helvetica", 20, "bold")).pack(pady=15)
        
        for category, count in sorted(stats['by_category'].items(), key=lambda x: x[1], reverse=True):
            row = ctk.CTkFrame(category_frame, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=5)
            
            ctk.CTkLabel(row, text=category, font=("Helvetica", 14), anchor="w", width=200).pack(side="left")
            ctk.CTkLabel(row, text=str(count), font=("Helvetica", 14, "bold"), 
                        fg_color="#3b82f6", corner_radius=5, width=60, text_color="white").pack(side="right")
        
        # By Department
        dept_frame = ctk.CTkFrame(stats_container, corner_radius=15)
        dept_frame.pack(fill="both", expand=True, pady=20)
        
        ctk.CTkLabel(dept_frame, text="Complaints by Department", 
                    font=("Helvetica", 20, "bold")).pack(pady=15)
        
        for dept, count in sorted(stats['by_department'].items(), key=lambda x: x[1], reverse=True)[:5]:
            row = ctk.CTkFrame(dept_frame, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=5)
            
            ctk.CTkLabel(row, text=dept, font=("Helvetica", 14), anchor="w", width=200).pack(side="left")
            ctk.CTkLabel(row, text=str(count), font=("Helvetica", 14, "bold"), 
                        fg_color="#7c2d12", corner_radius=5, width=60, text_color="white").pack(side="right")
    
    def create_stat_card(self, parent, title, value, color, column):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=color)
        card.grid(row=0, column=column, padx=10, sticky="ew")
        parent.columnconfigure(column, weight=1)
        
        ctk.CTkLabel(card, text=title, font=("Helvetica", 16), 
                    text_color="white").pack(pady=(20, 5))
        ctk.CTkLabel(card, text=str(value), font=("Helvetica", 36, "bold"), 
                    text_color="white").pack(pady=(5, 20))
    
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
            ("Role", self.user[3]),
            ("Account Created", str(self.user[8])[:16] if len(self.user) > 8 else "N/A")
        ]
        
        for label, value in info:
            row = ctk.CTkFrame(profile_frame, fg_color="transparent")
            row.pack(fill="x", padx=40, pady=10)
            
            ctk.CTkLabel(row, text=f"{label}:", font=("Helvetica", 14, "bold"), 
                        anchor="w", width=150).pack(side="left")
            ctk.CTkLabel(row, text=str(value), font=("Helvetica", 14), 
                        anchor="w").pack(side="left", padx=20)
    
    def load_complaints(self):
        for widget in self.complaints_frame.winfo_children():
            widget.destroy()
        
        search = self.search_var.get()
        status = self.status_filter.get()
        category = self.category_filter.get()
        priority = self.priority_filter.get()
        
        complaints = self.db.get_all_complaints(search, status, category, priority)
        
        if not complaints:
            ctk.CTkLabel(self.complaints_frame, text="No complaints found", 
                        font=("Helvetica", 16)).pack(pady=50)
            return
        
        # Header
        header = ctk.CTkFrame(self.complaints_frame, fg_color="#1e293b", corner_radius=8)
        header.pack(fill="x", pady=(0, 10), padx=5)
        
        ctk.CTkLabel(header, text="ID", font=("Helvetica", 12, "bold"), 
                    width=50, text_color="white").grid(row=0, column=0, padx=5, pady=10)
        ctk.CTkLabel(header, text="Name", font=("Helvetica", 12, "bold"), 
                    width=120, text_color="white").grid(row=0, column=1, padx=5, pady=10)
        ctk.CTkLabel(header, text="Roll No", font=("Helvetica", 12, "bold"), 
                    width=100, text_color="white").grid(row=0, column=2, padx=5, pady=10)
        ctk.CTkLabel(header, text="Department", font=("Helvetica", 12, "bold"), 
                    width=150, text_color="white").grid(row=0, column=3, padx=5, pady=10)
        ctk.CTkLabel(header, text="Category", font=("Helvetica", 12, "bold"), 
                    width=120, text_color="white").grid(row=0, column=4, padx=5, pady=10)
        ctk.CTkLabel(header, text="Priority", font=("Helvetica", 12, "bold"), 
                    width=80, text_color="white").grid(row=0, column=5, padx=5, pady=10)
        ctk.CTkLabel(header, text="Status", font=("Helvetica", 12, "bold"), 
                    width=100, text_color="white").grid(row=0, column=6, padx=5, pady=10)
        ctk.CTkLabel(header, text="Actions", font=("Helvetica", 12, "bold"), 
                    width=100, text_color="white").grid(row=0, column=7, padx=5, pady=10)
        
        for comp in complaints:
            self.create_complaint_row(comp)
    
    def create_complaint_row(self, comp):
        row = ctk.CTkFrame(self.complaints_frame, corner_radius=8)
        row.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(row, text=str(comp[0]), width=50).grid(row=0, column=0, padx=5, pady=10)
        ctk.CTkLabel(row, text=comp[1][:15], width=120).grid(row=0, column=1, padx=5, pady=10)
        ctk.CTkLabel(row, text=comp[2] if comp[2] else "N/A", width=100).grid(row=0, column=2, padx=5, pady=10)
        ctk.CTkLabel(row, text=comp[3][:15], width=150).grid(row=0, column=3, padx=5, pady=10)
        ctk.CTkLabel(row, text=comp[7], width=120).grid(row=0, column=4, padx=5, pady=10)
        
        # Priority badge
        priority_colors = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444", "Critical": "#7c2d12"}
        ctk.CTkLabel(row, text=comp[8], width=80, 
                    fg_color=priority_colors.get(comp[8], "#6b7280"),
                    corner_radius=5, text_color="white").grid(row=0, column=5, padx=5, pady=10)
        
        # Status badge
        status_colors = {"Open": "#ef4444", "In Progress": "#f59e0b", "Resolved": "#10b981", "Closed": "#6b7280"}
        ctk.CTkLabel(row, text=comp[9], width=100, 
                    fg_color=status_colors.get(comp[9], "#6b7280"),
                    corner_radius=5, text_color="white").grid(row=0, column=6, padx=5, pady=10)
        
        # Actions
        ctk.CTkButton(row, text="Manage", command=lambda: self.manage_complaint(comp[0]),
                     width=100, height=30).grid(row=0, column=7, padx=5, pady=10)
    
    def manage_complaint(self, complaint_id):
        ManageComplaintWindow(self, self.db, complaint_id, self.user, self.load_complaints)
    
    def export_to_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"complaints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not file_path:
                return
            
            search = self.search_var.get()
            status = self.status_filter.get()
            category = self.category_filter.get()
            priority = self.priority_filter.get()
            
            complaints = self.db.get_all_complaints(search, status, category, priority)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Name', 'Roll No', 'Department', 'Course', 'Gender', 
                               'Complaint', 'Category', 'Priority', 'Status', 'Submitted At'])
                
                for comp in complaints:
                    writer.writerow(comp[:11])
            
            tkmb.showinfo("Success", f"Exported {len(complaints)} complaints to CSV successfully!")
        except Exception as e:
            tkmb.showerror("Error", f"Failed to export: {str(e)}")


class ManageComplaintWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, complaint_id, user, refresh_callback):
        super().__init__(parent)
        
        self.db = db
        self.complaint_id = complaint_id
        self.user = user
        self.refresh_callback = refresh_callback
        
        self.title(f"Manage Complaint #{complaint_id}")
        self.geometry("800x700")
        
        # Load complaint
        complaint = db.get_complaint_by_id(complaint_id)
        
        if not complaint:
            self.destroy()
            return
        
        self.complaint = complaint
        
        # Main frame
        main = ctk.CTkScrollableFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ctk.CTkFrame(main, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(title_frame, text=f"Complaint #{complaint[0]}", 
                    font=("Helvetica", 24, "bold")).pack(side="left")
        
        # Status change
        status_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        status_frame.pack(side="right")
        
        ctk.CTkLabel(status_frame, text="Change Status:", 
                    font=("Helvetica", 12, "bold")).pack(side="left", padx=5)
        
        self.status_var = ctk.StringVar(value=complaint[10])
        status_combo = ctk.CTkComboBox(status_frame, values=["Open", "In Progress", "Resolved", "Closed"],
                                      variable=self.status_var, width=120)
        status_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(status_frame, text="Update", command=self.update_status,
                     width=80, fg_color="#10b981", hover_color="#059669").pack(side="left", padx=5)
        
        # Info
        info_frame = ctk.CTkFrame(main, corner_radius=10)
        info_frame.pack(fill="x", pady=10)
        
        info = [
            ("Name", complaint[2]),
            ("Roll No", complaint[3]),
            ("Department", complaint[4]),
            ("Course", complaint[5]),
            ("Gender", complaint[6]),
            ("Category", complaint[8]),
            ("Priority", complaint[9]),
            ("Status", complaint[10]),
            ("Submitted", str(complaint[11])[:16]),
            ("Submitter Email", complaint[14] if len(complaint) > 14 else "N/A")
        ]
        
        for i, (label, value) in enumerate(info):
            row = i // 2
            col = i % 2
            
            frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            frame.grid(row=row, column=col, padx=15, pady=8, sticky="w")
            
            ctk.CTkLabel(frame, text=f"{label}:", font=("Helvetica", 12, "bold"), 
                        width=120, anchor="w").pack(side="left")
            ctk.CTkLabel(frame, text=str(value), font=("Helvetica", 12), 
                        anchor="w").pack(side="left", padx=10)
        
        # Complaint text
        ctk.CTkLabel(main, text="Complaint Description:", 
                    font=("Helvetica", 14, "bold"), anchor="w").pack(fill="x", pady=(20, 5))
        
        complaint_box = ctk.CTkTextbox(main, height=120, wrap="word")
        complaint_box.insert("1.0", complaint[7])
        complaint_box.configure(state="disabled")
        complaint_box.pack(fill="x", pady=(0, 20))
        
        # Add response section
        response_section = ctk.CTkFrame(main, corner_radius=10, fg_color="#f0f9ff")
        response_section.pack(fill="x", pady=10)
        
        ctk.CTkLabel(response_section, text="Add Response:", 
                    font=("Helvetica", 14, "bold"), anchor="w").pack(fill="x", padx=15, pady=(15, 5))
        
        self.response_text = ctk.CTkTextbox(response_section, height=100)
        self.response_text.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkButton(response_section, text="Submit Response", command=self.add_response,
                     height=35, fg_color="#3b82f6", hover_color="#2563eb").pack(padx=15, pady=(0, 15))
        
        # Previous responses
        ctk.CTkLabel(main, text="Response History:", font=("Helvetica", 14, "bold"), 
                    anchor="w").pack(fill="x", pady=(20, 10))
        
        responses = db.get_responses(complaint_id)
        
        if responses:
            for resp in responses:
                self.create_response_card(main, resp)
        else:
            ctk.CTkLabel(main, text="No responses yet", 
                        font=("Helvetica", 12), text_color="gray").pack(pady=10)
        
        # Delete button
        ctk.CTkButton(main, text="🗑️ Delete Complaint", command=self.delete_complaint,
                     fg_color="#dc2626", hover_color="#991b1b", height=40).pack(pady=20)
    
    def update_status(self):
        new_status = self.status_var.get()
        
        if new_status == self.complaint[10]:
            tkmb.showinfo("Info", "Status is already set to this value")
            return
        
        self.db.update_complaint_status(self.complaint_id, new_status, self.user[0])
        tkmb.showinfo("Success", f"Status updated to: {new_status}")
        self.refresh_callback()
        self.destroy()
    
    def add_response(self):
        response = self.response_text.get("1.0", "end").strip()
        
        if len(response) < 10:
            tkmb.showerror("Error", "Response must be at least 10 characters!")
            return
        
        self.db.add_response(self.complaint_id, self.user[0], response)
        tkmb.showinfo("Success", "Response added successfully!")
        self.destroy()
        self.refresh_callback()
    
    def delete_complaint(self):
        if tkmb.askyesno("Confirm Delete", "Are you sure you want to delete this complaint? This action cannot be undone!"):
            self.db.delete_complaint(self.complaint_id)
            tkmb.showinfo("Success", "Complaint deleted successfully!")
            self.refresh_callback()
            self.destroy()
    
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
                    anchor="w", justify="left", wraplength=700).pack(fill="x", padx=10, pady=(0, 10))
