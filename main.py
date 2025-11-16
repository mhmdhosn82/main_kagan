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

import sys
import traceback

import customtkinter as ctk

from ui_utils import *

# Import authentication - replaced with simple login
from auth import LoginScreen, session

# Import all sections
from salon_section import SalonSection
from cafe_section import CafeSection
from gamnet_section import GamnetSection
from employee_section import EmployeeSection
from customer_section import CustomerSection
from invoice_section import InvoiceSection
from campaign_section import CampaignSection
from reports_section import ReportsSection
from settings_section import SettingsSection
from sms_section import SMSSection
from inventory_section import InventorySection
from supplier_expense_section import SupplierSection, ExpenseSection

class SimpleLoginWindow(ctk.CTk):
    def __init__(self, on_success_callback):
        super().__init__()
        
        # Configure window
        self.title("Kagan Collection - Login")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Center the window
        self.update_idletasks()
        width = self.winfo.width()
        height = self.winfo.height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        self.on_success = on_success_callback
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login interface"""
        # Main frame
        main_frame = GlassFrame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = GlassLabel(main_frame, text="Kagan Collection\nManagement System", 
                               font=FONTS['title'])
        title_label.pack(pady=20)
        
        # Username
        username_label = GlassLabel(main_frame, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = GlassEntry(main_frame, width=250)
        self.username_entry.pack(pady=5)
        
        # Password
        password_label = GlassLabel(main_frame, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = GlassEntry(main_frame, width=250, show="*")
        self.password_entry.pack(pady=5)
        
        # Login button
        login_button = GlassButton(main_frame, text="Login", command=self.attempt_login)
        login_button.pack(pady=20)
        
        # Error message (initially hidden)
        self.error_label = GlassLabel(main_frame, text="", text_color=COLORS['error'])
        self.error_label.pack(pady=5)
    
    def attempt_login(self):
        """Attempt to login with provided credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Simple hardcoded credentials
        if username == "admin" and password == "admin":
            self.on_success()
            self.destroy()
        else:
            self.error_label.configure(text="Invalid username or password")
            # Clear password field
            self.password_entry.delete(0, 'end')


class KaganManagementApp(ctk.CTk):
    def __init__(self):
        # Flag to track if initialization completed successfully
        self.init_complete = False
        
        try:
            print("=== Starting Kagan Management Application ===")
            super().__init__()
            
            # Set up window close protocol handler
            self.protocol("WM_DELETE_WINDOW", self.on_window_close)
            
            # Show simple login screen first
            print("Withdrawing main window and showing login screen")
            self.withdraw()  # Hide main window
            self.login_window = SimpleLoginWindow(self.on_login_success)
            self.wait_window(self.login_window)
            
            # Check if login was successful (login window would destroy itself)
            if not hasattr(self, 'login_successful') or not self.login_successful:
                print("User did not log in, exiting application")
                self.destroy()
                return
            
            print(f"User logged in successfully")
            
            # Configure window
            print("Configuring main window")
            self.title("Kagan Collection Management System")
            self.geometry("1400x900")
            
            # Set theme
            print("Setting theme")
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # Configure grid
            print("Configuring grid layout")
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            # Create UI
            print("Setting up user interface")
            self.setup_ui()
            print("UI setup completed successfully")
            
            # Initialize database with sample data
            print("Initializing sample data")
            self.init_sample_data()
            print("Sample data initialization completed")
            
            # Show main window
            print("Making main window visible")
            self.deiconify()
            # Ensure window is visible and focused
            self.lift()  # Bring window to top
            self.focus_force()  # Force focus on the window
            self.attributes('-topmost', True)  # Set as topmost temporarily
            self.after(100, lambda: self.attributes('-topmost', False))  # Remove topmost after 100ms
            print("Main window is now visible and focused")
            
            # Mark initialization as complete
            self.init_complete = True
            print("Application initialization completed successfully")
            
        except Exception as e:
            print(f"Error during application initialization: {e}")
            self._show_error_dialog("Application Initialization Error", 
                                   f"Failed to start the application:\n{type(e).__name__}: {str(e)}\n\nPlease check the logs for details.")
            self.init_complete = False
            raise
    
    def on_window_close(self):
        """Handle window close event"""
        try:
            print("Window close event triggered by user")
            self.destroy()
        except Exception as e:
            print(f"Error during window close: {e}")
            self.destroy()
    
    def on_login_success(self):
        """Handle successful login"""
        print("Login success callback")
        self.login_successful = True
    
    def _show_error_dialog(self, title, message):
        """Show an error dialog to the user"""
        try:
            from tkinter import messagebox
            messagebox.showerror(title, message)
        except Exception as e:
            print(f"Failed to show error dialog: {e}")
            print(f"ERROR - {title}: {message}")
    
    def setup_ui(self):
        """Setup the main user interface"""
        try:
            print("Creating sidebar navigation")
            # Sidebar navigation
            sidebar_width = 220
            self.sidebar = GlassFrame(self, width=sidebar_width)
            
            self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.sidebar.grid_propagate(False)
            
            # Logo/Title
            print("Adding logo and title")
            logo_label = create_title_label(self.sidebar, "Kagan\nCollection")
            logo_label.pack(pady=20)
            
            # Navigation buttons
            print("Creating navigation buttons")
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
                    width=200,
                    height=35,
                    anchor="center"
                )
                btn.pack(pady=3, padx=10)
                self.nav_buttons[text] = btn
            
            # Logout button
            print("Adding logout button")
            logout_btn = GlassButton(
                self.sidebar,
                text="Logout",
                command=self.logout,
                width=200,
                height=35,
                fg_color=COLORS['error']
            )
            logout_btn.pack(side='bottom', pady=10, padx=10)
            
            # Main content area
            print("Creating main content area")
            self.content_frame = GlassFrame(self)
            self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
            
            # Initialize sections (lazy loading)
            self.sections = {}
            self.current_section = None
            
            # Show dashboard by default
            print("Showing default dashboard")
            self.show_dashboard()
            
        except Exception as e:
            print(f"Error in setup_ui: {e}")
            raise
    
    def logout(self):
        """Logout user"""
        from tkinter import messagebox
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy()
            # Restart application
            import sys
            import os
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    def hide_current_section(self):
        """Hide the current section"""
        if self.current_section:
            self.current_section.pack_forget()
    
    def show_section(self, section_name, section_class):
        """Show a specific section"""
        try:
            print(f"Showing section: {section_name}")
            self.hide_current_section()
            
            # Create section if it doesn't exist
            if section_name not in self.sections:
                print(f"Creating new section instance: {section_name}")
                self.sections[section_name] = section_class(self.content_frame)
            
            # Show section
            self.current_section = self.sections[section_name].get_frame()
            self.current_section.pack(fill='both', expand=True)
            print(f"Section {section_name} displayed successfully")
            
        except Exception as e:
            print(f"Error showing section '{section_name}': {e}")
            self._show_error_dialog("Section Error", 
                                   f"Failed to show {section_name} section:\n{type(e).__name__}: {str(e)}")
            # Try to show dashboard as fallback
            if section_name != 'dashboard':
                print("Attempting to show dashboard as fallback")
                self.show_dashboard()
    
    def show_dashboard(self):
        """Show dashboard with overview"""
        try:
            print("Showing dashboard")
            self.hide_current_section()
            
            if 'dashboard' not in self.sections:
                print("Creating dashboard widgets")
                dashboard = GlassScrollableFrame(self.content_frame)
                
                # Header
                header = create_section_header(dashboard, "Dashboard - Overview")
                header.pack(fill='x', padx=10, pady=10)
                
                # Quick stats
                stats_container = ctk.CTkFrame(dashboard, fg_color="transparent")
                stats_container.pack(fill='x', padx=10, pady=10)
                
                # Create stat cards
                print("Creating stat cards")
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
                print("Creating quick actions")
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
                print("Creating recent activity section")
                activity_frame = GlassFrame(dashboard)
                activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
                
                GlassLabel(activity_frame, text="Recent Activity", font=FONTS['heading']).pack(pady=10)
                
                activity_text = ctk.CTkTextbox(
                    activity_frame,
                    fg_color=COLORS['surface'],
                    text_color=COLORS['text']
                )
                activity_text.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Get recent invoices - simplified without db import
                try:
                    from database import db
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
                except:
                    activity_text.insert('end', "No recent activity data available.\n")
                
                self.sections['dashboard'] = type('Dashboard', (), {'get_frame': lambda: dashboard})()
            
            self.current_section = self.sections['dashboard'].get_frame()
            self.current_section.pack(fill='both', expand=True)
            print("Dashboard displayed successfully")
            
        except Exception as e:
            print(f"Error showing dashboard: {e}")
            # Create a simple error message in the content frame
            error_label = GlassLabel(
                self.content_frame,
                text=f"Error loading dashboard:\n{type(e).__name__}: {str(e)}",
                text_color=COLORS['error']
            )
            error_label.pack(expand=True)
    
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
        try:
            from datetime import datetime
            from database import db
            today = datetime.now().strftime('%Y-%m-%d')
            result = db.fetchone(
                """SELECT SUM(final_amount) as total FROM invoices
                   WHERE DATE(invoice_date) = ? AND is_paid = 1""",
                (today,)
            )
            return f"${result['total']:.2f}" if result and result['total'] else "$0.00"
        except:
            return "$0.00"
    
    def get_active_customers(self):
        """Get count of active customers"""
        try:
            from database import db
            result = db.fetchone(
                """SELECT COUNT(*) as count FROM customers
                   WHERE last_visit_date IS NOT NULL
                   AND julianday('now') - julianday(last_visit_date) <= 30"""
            )
            return result['count'] if result else 0
        except:
            return 0
    
    def get_pending_appointments(self):
        """Get count of pending appointments"""
        try:
            from datetime import datetime
            from database import db
            today = datetime.now().strftime('%Y-%m-%d')
            result = db.fetchone(
                """SELECT COUNT(*) as count FROM salon_appointments
                   WHERE appointment_date >= ? AND status = 'pending'""",
                (today,)
            )
            return result['count'] if result else 0
        except:
            return 0
    
    def get_active_sessions(self):
        """Get count of active gaming sessions"""
        try:
            from database import db
            result = db.fetchone(
                """SELECT COUNT(*) as count FROM gamnet_sessions
                   WHERE end_time IS NULL"""
            )
            return result['count'] if result else 0
        except:
            return 0
    
    def init_sample_data(self):
        """Initialize sample data for demonstration"""
        try:
            print("Checking for existing sample data")
            from database import db
            # Check if data already exists
            existing = db.fetchone("SELECT COUNT(*) as count FROM employees")
            if existing and existing['count'] > 0:
                print("Sample data already exists, skipping initialization")
                return
            
            print("Initializing sample data")
            
            # Add sample employees
            print("Adding sample employees")
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
            print("Adding sample salon services")
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
            print("Adding sample cafe menu items")
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
            print("Adding sample gaming devices")
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
            print("Adding sample campaign")
            from datetime import datetime, timedelta
            today = datetime.now()
            end_date = today + timedelta(days=30)
            
            db.execute(
                """INSERT INTO campaigns (name, description, discount_percentage, code, start_date, end_date)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                ("Welcome Offer", "20% off for new customers", 20.0, "WELCOME20",
                 today.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            )
            
            print("Sample data initialization completed successfully")
            
        except Exception as e:
            print(f"Error initializing sample data: {e}")
            # Don't raise - allow app to continue even if sample data fails
            print("Continuing application startup despite sample data error")


def main():
    """Main entry point"""    
    # Install global exception handler
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Global exception handler to catch any unhandled exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow keyboard interrupt to work normally
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        print(f"Unhandled exception: {exc_value}")
        print("=" * 70)
        print("UNHANDLED EXCEPTION")
        print("=" * 70)
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print("=" * 70)
        print("Please check for details.")
        print("=" * 70)
    
    sys.excepthook = handle_exception
    
    try:
        print("Starting Kagan Management Software")
        app = KaganManagementApp()
        
        # Only start mainloop if initialization completed successfully
        if not hasattr(app, 'init_complete') or not app.init_complete:
            print("Application initialization did not complete successfully")
            print("Exiting application")
            return
        
        print("Entering main event loop")
        
        # Wrap mainloop in try-except to catch any exceptions during event processing
        try:
            app.mainloop()
        except Exception as e:
            print(f"Error in main event loop: {e}")
            print("=" * 70)
            print("ERROR IN MAIN EVENT LOOP")
            print("=" * 70)
            traceback.print_exc()
            print("=" * 70)
            print("Please check for details.")
            print("=" * 70)
            raise
        
        print("Application closed normally")
    except Exception as e:
        print(f"Fatal error in main: {e}")
        print("=" * 70)
        print("FATAL ERROR - Application crashed")
        print("=" * 70)
        traceback.print_exc()
        print("=" * 70)
        print("Please check for details.")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()