# database.py
import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self, dbname="college_complaints.db"):
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.init_db()
    
    def init_db(self):
        c = self.conn.cursor()
        
        # Users table (students and teachers)
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        email TEXT,
                        department TEXT,
                        roll_no TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Complaints table
        c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        roll_no TEXT,
                        department TEXT NOT NULL,
                        course TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        complaint TEXT NOT NULL,
                        category TEXT DEFAULT 'General',
                        priority TEXT DEFAULT 'Medium',
                        status TEXT DEFAULT 'Open',
                        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
        
        # Complaint responses table
        c.execute('''CREATE TABLE IF NOT EXISTS complaint_responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        complaint_id INTEGER NOT NULL,
                        responder_id INTEGER NOT NULL,
                        response TEXT NOT NULL,
                        responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (complaint_id) REFERENCES complaints(id),
                        FOREIGN KEY (responder_id) REFERENCES users(id))''')
        
        # Status history table
        c.execute('''CREATE TABLE IF NOT EXISTS status_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        complaint_id INTEGER NOT NULL,
                        old_status TEXT,
                        new_status TEXT NOT NULL,
                        changed_by INTEGER NOT NULL,
                        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (complaint_id) REFERENCES complaints(id),
                        FOREIGN KEY (changed_by) REFERENCES users(id))''')
        
        # Categories table
        c.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        description TEXT)''')
        
        # Initialize default categories
        default_categories = [
            ('Academic', 'Issues related to teaching, exams, courses'),
            ('Infrastructure', 'Building, classroom, lab issues'),
            ('Hostel', 'Hostel accommodation and facilities'),
            ('Library', 'Library resources and services'),
            ('Canteen', 'Food and canteen services'),
            ('Transport', 'College bus and transport'),
            ('Administration', 'Administrative procedures'),
            ('Harassment', 'Ragging, bullying, harassment'),
            ('Other', 'Other complaints')
        ]
        
        for cat_name, cat_desc in default_categories:
            try:
                c.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (cat_name, cat_desc))
            except sqlite3.IntegrityError:
                pass
        
        # Create default admin account
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        try:
            c.execute("""INSERT INTO users (username, password_hash, role, full_name, email, department) 
                        VALUES (?, ?, ?, ?, ?, ?)""", 
                     ("admin", admin_hash, "Teacher", "Administrator", "admin@college.edu", "Administration"))
        except sqlite3.IntegrityError:
            pass
        
        self.conn.commit()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    # User Management
    def register_user(self, username, password, role, full_name, email, department, roll_no=None):
        c = self.conn.cursor()
        password_hash = self.hash_password(password)
        try:
            c.execute("""INSERT INTO users (username, password_hash, role, full_name, email, department, roll_no) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                     (username, password_hash, role, full_name, email, department, roll_no))
            self.conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists!"
    
    def authenticate_user(self, username, password, role):
        c = self.conn.cursor()
        password_hash = self.hash_password(password)
        c.execute("SELECT * FROM users WHERE username=? AND password_hash=? AND role=?", 
                 (username, password_hash, role))
        user = c.fetchone()
        return user
    
    def get_user_by_id(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return c.fetchone()
    
    # Complaint Management
    def add_complaint(self, user_id, name, roll_no, department, course, gender, complaint, category, priority):
        c = self.conn.cursor()
        c.execute("""INSERT INTO complaints (user_id, name, roll_no, department, course, gender, complaint, category, priority) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (user_id, name, roll_no, department, course, gender, complaint, category, priority))
        self.conn.commit()
        return c.lastrowid
    
    def get_all_complaints(self, search=None, status_filter=None, category_filter=None, priority_filter=None):
        c = self.conn.cursor()
        query = """SELECT c.id, c.name, c.roll_no, c.department, c.course, c.gender, c.complaint, 
                         c.category, c.priority, c.status, c.submitted_at, c.user_id
                   FROM complaints c WHERE 1=1"""
        params = []
        
        if search:
            query += " AND (c.name LIKE ? OR c.complaint LIKE ? OR c.roll_no LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
        
        if status_filter and status_filter != "All":
            query += " AND c.status = ?"
            params.append(status_filter)
        
        if category_filter and category_filter != "All":
            query += " AND c.category = ?"
            params.append(category_filter)
        
        if priority_filter and priority_filter != "All":
            query += " AND c.priority = ?"
            params.append(priority_filter)
        
        query += " ORDER BY c.submitted_at DESC"
        c.execute(query, params)
        return c.fetchall()
    
    def get_user_complaints(self, user_id):
        c = self.conn.cursor()
        c.execute("""SELECT id, name, roll_no, department, course, gender, complaint, 
                           category, priority, status, submitted_at 
                    FROM complaints WHERE user_id=? ORDER BY submitted_at DESC""", (user_id,))
        return c.fetchall()
    
    def get_complaint_by_id(self, complaint_id):
        c = self.conn.cursor()
        c.execute("""SELECT c.*, u.full_name as submitter_name, u.email as submitter_email
                    FROM complaints c 
                    JOIN users u ON c.user_id = u.id 
                    WHERE c.id=?""", (complaint_id,))
        return c.fetchone()
    
    def update_complaint_status(self, complaint_id, new_status, changed_by):
        c = self.conn.cursor()
        # Get old status
        c.execute("SELECT status FROM complaints WHERE id=?", (complaint_id,))
        old_status = c.fetchone()[0]
        
        # Update status
        c.execute("UPDATE complaints SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", 
                 (new_status, complaint_id))
        
        # Record in history
        c.execute("""INSERT INTO status_history (complaint_id, old_status, new_status, changed_by) 
                    VALUES (?, ?, ?, ?)""", (complaint_id, old_status, new_status, changed_by))
        self.conn.commit()
    
    def delete_complaint(self, complaint_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM complaint_responses WHERE complaint_id=?", (complaint_id,))
        c.execute("DELETE FROM status_history WHERE complaint_id=?", (complaint_id,))
        c.execute("DELETE FROM complaints WHERE id=?", (complaint_id,))
        self.conn.commit()
    
    def add_response(self, complaint_id, responder_id, response):
        c = self.conn.cursor()
        c.execute("""INSERT INTO complaint_responses (complaint_id, responder_id, response) 
                    VALUES (?, ?, ?)""", (complaint_id, responder_id, response))
        self.conn.commit()
    
    def get_responses(self, complaint_id):
        c = self.conn.cursor()
        c.execute("""SELECT cr.*, u.full_name, u.role 
                    FROM complaint_responses cr
                    JOIN users u ON cr.responder_id = u.id
                    WHERE cr.complaint_id=? ORDER BY cr.responded_at ASC""", (complaint_id,))
        return c.fetchall()
    
    def get_status_history(self, complaint_id):
        c = self.conn.cursor()
        c.execute("""SELECT sh.*, u.full_name 
                    FROM status_history sh
                    JOIN users u ON sh.changed_by = u.id
                    WHERE sh.complaint_id=? ORDER BY sh.changed_at ASC""", (complaint_id,))
        return c.fetchall()
    
    # Analytics
    def get_statistics(self):
        c = self.conn.cursor()
        stats = {}
        
        # Total complaints
        c.execute("SELECT COUNT(*) FROM complaints")
        stats['total'] = c.fetchone()[0]
        
        # By status
        c.execute("SELECT status, COUNT(*) FROM complaints GROUP BY status")
        stats['by_status'] = dict(c.fetchall())
        
        # By category
        c.execute("SELECT category, COUNT(*) FROM complaints GROUP BY category")
        stats['by_category'] = dict(c.fetchall())
        
        # By priority
        c.execute("SELECT priority, COUNT(*) FROM complaints GROUP BY priority")
        stats['by_priority'] = dict(c.fetchall())
        
        # By department
        c.execute("SELECT department, COUNT(*) FROM complaints GROUP BY department")
        stats['by_department'] = dict(c.fetchall())
        
        return stats
    
    def get_categories(self):
        c = self.conn.cursor()
        c.execute("SELECT name FROM categories ORDER BY name")
        return [row[0] for row in c.fetchall()]
    
    def close(self):
        self.conn.close()
