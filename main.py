#!/usr/bin/env python3
"""
Kagan Collection Management Software
Main application file with glassmorphism UI using customtkinter

A comprehensive management system integrating:
- Men's Salon
- Cafe Bar
- Gamnet (Gaming Net)

Features unified invoicing, employee management, customer relationship management,
campaigns, and comprehensive reporting.
"""

import customtkinter as ctk
from ui_utils import *
from database import db

# Import all sections
from salon_section import SalonSection
from cafe_section import CafeSection
from gamnet_section import GamnetSection
from employee_section import EmployeeSection
from customer_section import CustomerSection
from invoice_section import InvoiceSection
from campaign_section import CampaignSection
from reports_section import ReportsSection

class KaganManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Kagan Collection Management System")
        self.geometry("1400x900")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI
        self.setup_ui()
        
        # Initialize database with sample data
        self.init_sample_data()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Sidebar navigation
        self.sidebar = GlassFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.sidebar.grid_propagate(False)
        
        # Logo/Title
        logo_label = create_title_label(self.sidebar, "Kagan\nCollection")
        logo_label.pack(pady=20)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Salon", self.show_salon),
            ("Cafe Bar", self.show_cafe),
            ("Gamnet", self.show_gamnet),
            ("Invoices", self.show_invoices),
            ("Employees", self.show_employees),
            ("Customers", self.show_customers),
            ("Campaigns", self.show_campaigns),
            ("Reports", self.show_reports),
        ]
        
        for text, command in nav_items:
            btn = GlassButton(
                self.sidebar,
                text=text,
                command=command,
                width=180,
                height=40
            )
            btn.pack(pady=5, padx=10)
            self.nav_buttons[text] = btn
        
        # Main content area
        self.content_frame = GlassFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        
        # Initialize sections (lazy loading)
        self.sections = {}
        self.current_section = None
        
        # Show dashboard by default
        self.show_dashboard()
    
    def hide_current_section(self):
        """Hide the current section"""
        if self.current_section:
            self.current_section.pack_forget()
    
    def show_section(self, section_name, section_class):
        """Show a specific section"""
        self.hide_current_section()
        
        # Create section if it doesn't exist
        if section_name not in self.sections:
            self.sections[section_name] = section_class(self.content_frame)
        
        # Show section
        self.current_section = self.sections[section_name].get_frame()
        self.current_section.pack(fill='both', expand=True)
    
    def show_dashboard(self):
        """Show dashboard with overview"""
        self.hide_current_section()
        
        if 'dashboard' not in self.sections:
            dashboard = GlassScrollableFrame(self.content_frame)
            
            # Header
            header = create_section_header(dashboard, "Dashboard - Overview")
            header.pack(fill='x', padx=10, pady=10)
            
            # Quick stats
            stats_container = ctk.CTkFrame(dashboard, fg_color="transparent")
            stats_container.pack(fill='x', padx=10, pady=10)
            
            # Create stat cards
            stat_cards = [
                ("Today's Revenue", self.get_today_revenue()),
                ("Active Customers", self.get_active_customers()),
                ("Pending Appointments", self.get_pending_appointments()),
                ("Active Sessions", self.get_active_sessions()),
            ]
            
            for i, (title, value) in enumerate(stat_cards):
                card = GlassFrame(stats_container)
                card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
                
                GlassLabel(card, text=title, font=FONTS['subheading']).pack(pady=10)
                GlassLabel(card, text=str(value), font=FONTS['title']).pack(pady=10)
            
            stats_container.grid_columnconfigure(0, weight=1)
            stats_container.grid_columnconfigure(1, weight=1)
            
            # Quick actions
            actions_frame = GlassFrame(dashboard)
            actions_frame.pack(fill='x', padx=10, pady=20)
            
            GlassLabel(actions_frame, text="Quick Actions", font=FONTS['heading']).pack(pady=10)
            
            actions = [
                ("New Customer", self.show_customers),
                ("Create Invoice", self.show_invoices),
                ("Book Appointment", self.show_salon),
                ("Start Gaming Session", self.show_gamnet),
            ]
            
            for text, command in actions:
                GlassButton(actions_frame, text=text, command=command, width=300).pack(pady=5)
            
            # Recent activity
            activity_frame = GlassFrame(dashboard)
            activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            GlassLabel(activity_frame, text="Recent Activity", font=FONTS['heading']).pack(pady=10)
            
            activity_text = ctk.CTkTextbox(
                activity_frame,
                fg_color=COLORS['surface'],
                text_color=COLORS['text']
            )
            activity_text.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Get recent invoices
            recent = db.fetchall(
                """SELECT i.id, c.name, i.final_amount, i.invoice_date
                   FROM invoices i
                   JOIN customers c ON i.customer_id = c.id
                   ORDER BY i.invoice_date DESC
                   LIMIT 10"""
            )
            
            for inv in recent:
                activity_text.insert('end',
                    f"Invoice #{inv['id']} - {inv['name']} - ${inv['final_amount']:.2f} - {inv['invoice_date']}\n"
                )
            
            self.sections['dashboard'] = type('Dashboard', (), {'get_frame': lambda: dashboard})()
        
        self.current_section = self.sections['dashboard'].get_frame()
        self.current_section.pack(fill='both', expand=True)
    
    def show_salon(self):
        """Show salon section"""
        self.show_section('salon', SalonSection)
    
    def show_cafe(self):
        """Show cafe section"""
        self.show_section('cafe', CafeSection)
    
    def show_gamnet(self):
        """Show gamnet section"""
        self.show_section('gamnet', GamnetSection)
    
    def show_employees(self):
        """Show employee section"""
        self.show_section('employees', EmployeeSection)
    
    def show_customers(self):
        """Show customer section"""
        self.show_section('customers', CustomerSection)
    
    def show_invoices(self):
        """Show invoice section"""
        self.show_section('invoices', InvoiceSection)
    
    def show_campaigns(self):
        """Show campaigns section"""
        self.show_section('campaigns', CampaignSection)
    
    def show_reports(self):
        """Show reports section"""
        self.show_section('reports', ReportsSection)
    
    def get_today_revenue(self):
        """Get today's total revenue"""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        result = db.fetchone(
            """SELECT SUM(final_amount) as total FROM invoices
               WHERE DATE(invoice_date) = ? AND is_paid = 1""",
            (today,)
        )
        return f"${result['total']:.2f}" if result and result['total'] else "$0.00"
    
    def get_active_customers(self):
        """Get count of active customers"""
        result = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE last_visit_date IS NOT NULL
               AND julianday('now') - julianday(last_visit_date) <= 30"""
        )
        return result['count'] if result else 0
    
    def get_pending_appointments(self):
        """Get count of pending appointments"""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        result = db.fetchone(
            """SELECT COUNT(*) as count FROM salon_appointments
               WHERE appointment_date >= ? AND status = 'pending'""",
            (today,)
        )
        return result['count'] if result else 0
    
    def get_active_sessions(self):
        """Get count of active gaming sessions"""
        result = db.fetchone(
            """SELECT COUNT(*) as count FROM gamnet_sessions
               WHERE end_time IS NULL"""
        )
        return result['count'] if result else 0
    
    def init_sample_data(self):
        """Initialize sample data for demonstration"""
        # Check if data already exists
        existing = db.fetchone("SELECT COUNT(*) as count FROM employees")
        if existing and existing['count'] > 0:
            return
        
        # Add sample employees
        sample_employees = [
            ("Ali Karimi", "09121234567", "Senior Stylist", "Salon", 3000, 15),
            ("Reza Hosseini", "09121234568", "Junior Stylist", "Salon", 2000, 10),
            ("Sara Ahmadi", "09121234569", "Head Barista", "Cafe", 2500, 12),
            ("Mina Rezaei", "09121234570", "Barista", "Cafe", 1800, 8),
            ("Hassan Moradi", "09121234571", "Gaming Manager", "Gamnet", 2200, 5),
        ]
        
        for emp in sample_employees:
            db.execute(
                """INSERT INTO employees (name, phone, role, section, base_salary, commission_rate, hire_date)
                   VALUES (?, ?, ?, ?, ?, ?, date('now'))""",
                emp
            )
        
        # Add sample salon services
        sample_services = [
            ("Haircut", 25.0, 45, 15),
            ("Hair Coloring", 60.0, 90, 20),
            ("Beard Trim", 15.0, 20, 10),
            ("Hair Mask", 35.0, 60, 15),
            ("Full Service", 80.0, 120, 18),
        ]
        
        for svc in sample_services:
            db.execute(
                """INSERT INTO salon_services (name, price, duration_minutes, commission_rate)
                   VALUES (?, ?, ?, ?)""",
                svc
            )
        
        # Add sample cafe menu items
        sample_menu = [
            ("Espresso", "Drinks", 3.5, "Classic espresso shot"),
            ("Cappuccino", "Drinks", 4.5, "Espresso with steamed milk"),
            ("Latte", "Drinks", 5.0, "Smooth latte with milk foam"),
            ("Turkish Coffee", "Drinks", 4.0, "Traditional Turkish coffee"),
            ("Club Sandwich", "Food", 8.0, "Triple-decker club sandwich"),
            ("Burger", "Food", 10.0, "Classic burger with fries"),
            ("Cheesecake", "Desserts", 6.0, "New York style cheesecake"),
        ]
        
        for item in sample_menu:
            db.execute(
                """INSERT INTO cafe_menu (name, category, price, description)
                   VALUES (?, ?, ?, ?)""",
                item
            )
        
        # Add sample gaming devices
        sample_devices = [
            ("PC-01", "PC", 5.0),
            ("PC-02", "PC", 5.0),
            ("PC-03", "PC", 6.0),
            ("PS5-01", "PlayStation", 8.0),
            ("XBOX-01", "Xbox", 8.0),
            ("VR-01", "VR", 12.0),
        ]
        
        for device in sample_devices:
            db.execute(
                """INSERT INTO gamnet_devices (device_number, device_type, hourly_rate)
                   VALUES (?, ?, ?)""",
                device
            )
        
        # Add sample campaign
        from datetime import datetime, timedelta
        today = datetime.now()
        end_date = today + timedelta(days=30)
        
        db.execute(
            """INSERT INTO campaigns (name, description, discount_percentage, code, start_date, end_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            ("Welcome Offer", "20% off for new customers", 20.0, "WELCOME20",
             today.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        )

def main():
    """Main entry point"""
    app = KaganManagementApp()
    app.mainloop()

if __name__ == "__main__":
    main()
