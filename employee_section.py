"""
Employee Management Section Module
Handles employee records, attendance, commissions, and performance
"""
import customtkinter as ctk
from datetime import datetime
from ui_utils import *
from database import db

class EmployeeSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the employee section UI"""
        # Header
        header = create_section_header(self.frame, "Employee Management")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Employees")
        self.tabview.add("Attendance")
        self.tabview.add("Reports")
        
        self.setup_employees_tab()
        self.setup_attendance_tab()
        self.setup_reports_tab()
    
    def setup_employees_tab(self):
        """Setup employee management interface"""
        tab = self.tabview.tab("Employees")
        
        # Add employee form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Add Employee", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Name:").pack(pady=5)
        self.emp_name_entry = GlassEntry(form_frame, width=300)
        self.emp_name_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Phone:").pack(pady=5)
        self.emp_phone_entry = GlassEntry(form_frame, width=300)
        self.emp_phone_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Role:").pack(pady=5)
        self.emp_role_entry = GlassEntry(form_frame, width=300)
        self.emp_role_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Section:").pack(pady=5)
        self.emp_section_var = ctk.StringVar(value="Salon")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.emp_section_var,
            values=["Salon", "Cafe", "Gamnet", "Management"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Base Salary:").pack(pady=5)
        self.emp_salary_entry = GlassEntry(form_frame, width=300)
        self.emp_salary_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Commission Rate (%):").pack(pady=5)
        self.emp_commission_entry = GlassEntry(form_frame, width=300)
        self.emp_commission_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Add Employee", command=self.add_employee).pack(pady=20)
        
        # Employees list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="All Employees", font=FONTS['subheading']).pack(pady=10)
        
        self.employees_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.employees_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_employees()
    
    def setup_attendance_tab(self):
        """Setup attendance tracking interface"""
        tab = self.tabview.tab("Attendance")
        
        # Check-in form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Attendance", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Employee:").pack(pady=5)
        self.attendance_emp_var = ctk.StringVar(value="Select Employee")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.attendance_emp_var,
            values=self.get_employees(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassButton(form_frame, text="Check In", command=self.check_in,
                   fg_color=COLORS['success']).pack(pady=10)
        GlassButton(form_frame, text="Check Out", command=self.check_out,
                   fg_color=COLORS['warning']).pack(pady=10)
        
        # Today's attendance
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Today's Attendance", font=FONTS['subheading']).pack(pady=10)
        
        self.attendance_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.attendance_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_attendance()
    
    def setup_reports_tab(self):
        """Setup employee reports interface"""
        tab = self.tabview.tab("Reports")
        
        # Report options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Employee Reports", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(options_frame, text="Select Employee:").pack(pady=5)
        self.report_emp_var = ctk.StringVar(value="Select Employee")
        ctk.CTkOptionMenu(
            options_frame,
            variable=self.report_emp_var,
            values=self.get_employees(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassButton(options_frame, text="Performance Report", 
                   command=self.show_performance).pack(pady=5)
        GlassButton(options_frame, text="Commission Report", 
                   command=self.show_commissions).pack(pady=5)
        GlassButton(options_frame, text="Attendance Report", 
                   command=self.show_attendance_report).pack(pady=5)
        
        # Report display
        report_frame = GlassFrame(tab)
        report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.report_text = ctk.CTkTextbox(
            report_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def get_employees(self):
        """Get list of employees"""
        employees = db.fetchall("SELECT id, name, section FROM employees WHERE is_active = 1")
        if employees:
            return [f"{e['id']}: {e['name']} ({e['section']})" for e in employees]
        return ["No employees"]
    
    def add_employee(self):
        """Add a new employee"""
        name = self.emp_name_entry.get()
        phone = self.emp_phone_entry.get()
        role = self.emp_role_entry.get()
        section = self.emp_section_var.get()
        salary = float(self.emp_salary_entry.get())
        commission = float(self.emp_commission_entry.get())
        
        db.execute(
            """INSERT INTO employees 
               (name, phone, role, section, base_salary, commission_rate, hire_date)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, phone, role, section, salary, commission, datetime.now().strftime('%Y-%m-%d'))
        )
        
        self.refresh_employees()
        
        # Clear form
        self.emp_name_entry.delete(0, 'end')
        self.emp_phone_entry.delete(0, 'end')
        self.emp_role_entry.delete(0, 'end')
        self.emp_salary_entry.delete(0, 'end')
        self.emp_commission_entry.delete(0, 'end')
    
    def check_in(self):
        """Check in an employee"""
        emp_text = self.attendance_emp_var.get()
        if ':' not in emp_text:
            return
        
        emp_id = int(emp_text.split(':')[0])
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Check if already checked in
        existing = db.fetchone(
            "SELECT id FROM attendance WHERE employee_id = ? AND date = ?",
            (emp_id, today)
        )
        
        if existing:
            return  # Already checked in
        
        # Determine if late (after 9 AM)
        is_late = 1 if datetime.now().hour >= 9 else 0
        
        db.execute(
            """INSERT INTO attendance (employee_id, date, check_in_time, is_late)
               VALUES (?, ?, ?, ?)""",
            (emp_id, today, current_time, is_late)
        )
        
        # Update last work date
        db.execute(
            "UPDATE employees SET last_work_date = ? WHERE id = ?",
            (today, emp_id)
        )
        
        self.refresh_attendance()
    
    def check_out(self):
        """Check out an employee"""
        emp_text = self.attendance_emp_var.get()
        if ':' not in emp_text:
            return
        
        emp_id = int(emp_text.split(':')[0])
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        db.execute(
            """UPDATE attendance 
               SET check_out_time = ?
               WHERE employee_id = ? AND date = ? AND check_out_time IS NULL""",
            (current_time, emp_id, today)
        )
        
        self.refresh_attendance()
    
    def refresh_employees(self):
        """Refresh employees list"""
        self.employees_text.delete('1.0', 'end')
        employees = db.fetchall("SELECT * FROM employees WHERE is_active = 1")
        
        for emp in employees:
            self.employees_text.insert('end',
                f"{emp['name']} - {emp['role']} ({emp['section']}) - "
                f"Salary: ${emp['base_salary']}, Commission: {emp['commission_rate']}%\n"
            )
    
    def refresh_attendance(self):
        """Refresh attendance list"""
        self.attendance_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        
        attendance = db.fetchall(
            """SELECT a.*, e.name
               FROM attendance a
               JOIN employees e ON a.employee_id = e.id
               WHERE a.date = ?""",
            (today,)
        )
        
        for att in attendance:
            status = "Checked Out" if att['check_out_time'] else "Checked In"
            late = " (Late)" if att['is_late'] else ""
            self.attendance_text.insert('end',
                f"{att['name']}: In at {att['check_in_time']}{late} - {status}\n"
            )
    
    def show_performance(self):
        """Show employee performance report"""
        emp_text = self.report_emp_var.get()
        if ':' not in emp_text:
            return
        
        emp_id = int(emp_text.split(':')[0])
        emp = db.fetchone("SELECT * FROM employees WHERE id = ?", (emp_id,))
        
        self.report_text.delete('1.0', 'end')
        self.report_text.insert('end', f"Performance Report for {emp['name']}\n\n")
        
        # Get service records and ratings
        if emp['section'] == 'Salon':
            records = db.fetchall(
                """SELECT COUNT(*) as count, AVG(rating) as avg_rating, SUM(price) as revenue
                   FROM salon_service_records
                   WHERE stylist_id = ?""",
                (emp_id,)
            )
            if records and records[0]['count']:
                self.report_text.insert('end', f"Services Performed: {records[0]['count']}\n")
                self.report_text.insert('end', f"Average Rating: {records[0]['avg_rating']:.2f}\n")
                self.report_text.insert('end', f"Total Revenue: ${records[0]['revenue']:.2f}\n")
        
        # Get commissions
        commissions = db.fetchall(
            """SELECT SUM(amount) as total FROM employee_commissions WHERE employee_id = ?""",
            (emp_id,)
        )
        if commissions and commissions[0]['total']:
            self.report_text.insert('end', f"Total Commissions: ${commissions[0]['total']:.2f}\n")
    
    def show_commissions(self):
        """Show employee commission report"""
        emp_text = self.report_emp_var.get()
        if ':' not in emp_text:
            return
        
        emp_id = int(emp_text.split(':')[0])
        emp = db.fetchone("SELECT * FROM employees WHERE id = ?", (emp_id,))
        
        self.report_text.delete('1.0', 'end')
        self.report_text.insert('end', f"Commission Report for {emp['name']}\n\n")
        
        commissions = db.fetchall(
            """SELECT * FROM employee_commissions 
               WHERE employee_id = ? 
               ORDER BY service_date DESC
               LIMIT 20""",
            (emp_id,)
        )
        
        total = 0
        for comm in commissions:
            paid = "Paid" if comm['is_paid'] else "Unpaid"
            self.report_text.insert('end',
                f"{comm['service_date']} - {comm['service_type']}: ${comm['amount']:.2f} ({paid})\n"
            )
            total += comm['amount']
        
        self.report_text.insert('end', f"\nTotal: ${total:.2f}\n")
    
    def show_attendance_report(self):
        """Show employee attendance report"""
        emp_text = self.report_emp_var.get()
        if ':' not in emp_text:
            return
        
        emp_id = int(emp_text.split(':')[0])
        emp = db.fetchone("SELECT * FROM employees WHERE id = ?", (emp_id,))
        
        self.report_text.delete('1.0', 'end')
        self.report_text.insert('end', f"Attendance Report for {emp['name']}\n\n")
        
        attendance = db.fetchall(
            """SELECT * FROM attendance 
               WHERE employee_id = ? 
               ORDER BY date DESC
               LIMIT 30""",
            (emp_id,)
        )
        
        late_count = 0
        for att in attendance:
            late = " (Late)" if att['is_late'] else ""
            if att['is_late']:
                late_count += 1
            self.report_text.insert('end',
                f"{att['date']}: {att['check_in_time']} - {att['check_out_time'] or 'Not checked out'}{late}\n"
            )
        
        self.report_text.insert('end', f"\nTotal Days: {len(attendance)}, Late: {late_count}\n")
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
