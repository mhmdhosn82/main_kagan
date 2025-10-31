"""
Salon Section Module
Handles appointments, services, stylist management, and customer ratings
"""
import customtkinter as ctk
from datetime import datetime
from ui_utils import *
from database import db

class SalonSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the salon section UI"""
        # Header
        header = create_section_header(self.frame, "Men's Salon Management")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Appointments")
        self.tabview.add("Services")
        self.tabview.add("Service Records")
        
        self.setup_appointments_tab()
        self.setup_services_tab()
        self.setup_records_tab()
    
    def setup_appointments_tab(self):
        """Setup appointments booking interface"""
        tab = self.tabview.tab("Appointments")
        
        # Booking form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Book Appointment", font=FONTS['heading']).pack(pady=10)
        
        # Customer selection
        GlassLabel(form_frame, text="Customer Phone:").pack(pady=5)
        self.customer_phone_entry = GlassEntry(form_frame, width=300)
        self.customer_phone_entry.pack(pady=5)
        
        # Date
        GlassLabel(form_frame, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.appointment_date_entry = GlassEntry(form_frame, width=300)
        self.appointment_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.appointment_date_entry.pack(pady=5)
        
        # Time
        GlassLabel(form_frame, text="Time (HH:MM):").pack(pady=5)
        self.appointment_time_entry = GlassEntry(form_frame, width=300)
        self.appointment_time_entry.pack(pady=5)
        
        # Stylist selection
        GlassLabel(form_frame, text="Stylist:").pack(pady=5)
        self.stylist_var = ctk.StringVar(value="Select Stylist")
        self.stylist_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.stylist_var,
            values=self.get_stylists(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        self.stylist_dropdown.pack(pady=5)
        
        # Service type
        GlassLabel(form_frame, text="Service Type:").pack(pady=5)
        self.service_type_var = ctk.StringVar(value="Select Service")
        self.service_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.service_type_var,
            values=self.get_services(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        self.service_dropdown.pack(pady=5)
        
        # Book button
        GlassButton(form_frame, text="Book Appointment", command=self.book_appointment).pack(pady=20)
        
        # Appointments list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Today's Appointments", font=FONTS['subheading']).pack(pady=10)
        
        self.appointments_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.appointments_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_appointments()
    
    def setup_services_tab(self):
        """Setup services management interface"""
        tab = self.tabview.tab("Services")
        
        # Add service form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Add New Service", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Service Name:").pack(pady=5)
        self.service_name_entry = GlassEntry(form_frame, width=300)
        self.service_name_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Price:").pack(pady=5)
        self.service_price_entry = GlassEntry(form_frame, width=300)
        self.service_price_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Duration (minutes):").pack(pady=5)
        self.service_duration_entry = GlassEntry(form_frame, width=300)
        self.service_duration_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Commission Rate (%):").pack(pady=5)
        self.service_commission_entry = GlassEntry(form_frame, width=300)
        self.service_commission_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Add Service", command=self.add_service).pack(pady=20)
        
        # Services list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Available Services", font=FONTS['subheading']).pack(pady=10)
        
        self.services_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.services_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_services()
    
    def setup_records_tab(self):
        """Setup service records and ratings interface"""
        tab = self.tabview.tab("Service Records")
        
        # Record service form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Record Service", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Customer Phone:").pack(pady=5)
        self.record_customer_entry = GlassEntry(form_frame, width=300)
        self.record_customer_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Stylist:").pack(pady=5)
        self.record_stylist_var = ctk.StringVar(value="Select Stylist")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.record_stylist_var,
            values=self.get_stylists(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Service:").pack(pady=5)
        self.record_service_var = ctk.StringVar(value="Select Service")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.record_service_var,
            values=self.get_services(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Rating (1-5):").pack(pady=5)
        self.rating_entry = GlassEntry(form_frame, width=300)
        self.rating_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Review:").pack(pady=5)
        self.review_entry = GlassEntry(form_frame, width=300)
        self.review_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Record Service", command=self.record_service).pack(pady=20)
    
    def get_stylists(self):
        """Get list of stylists from database"""
        stylists = db.fetchall("SELECT id, name FROM employees WHERE section = 'Salon' AND is_active = 1")
        if stylists:
            return [f"{s['id']}: {s['name']}" for s in stylists]
        return ["No stylists available"]
    
    def get_services(self):
        """Get list of services from database"""
        services = db.fetchall("SELECT id, name, price FROM salon_services")
        if services:
            return [f"{s['id']}: {s['name']} (${s['price']})" for s in services]
        return ["No services available"]
    
    def book_appointment(self):
        """Book a new appointment"""
        phone = self.customer_phone_entry.get()
        date = self.appointment_date_entry.get()
        time = self.appointment_time_entry.get()
        
        # Get customer ID
        customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        if not customer:
            # Create new customer
            db.execute(
                "INSERT INTO customers (name, phone, registration_date) VALUES (?, ?, ?)",
                (f"Customer {phone}", phone, datetime.now().strftime('%Y-%m-%d'))
            )
            customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        
        customer_id = customer['id']
        
        # Get stylist ID
        stylist_text = self.stylist_var.get()
        if ':' in stylist_text:
            stylist_id = int(stylist_text.split(':')[0])
        else:
            stylist_id = None
        
        # Get service
        service_text = self.service_type_var.get()
        if ':' in service_text:
            service_type = service_text.split(':')[1].split('(')[0].strip()
        else:
            service_type = "General"
        
        # Insert appointment
        db.execute(
            """INSERT INTO salon_appointments 
               (customer_id, stylist_id, appointment_date, appointment_time, service_type, status)
               VALUES (?, ?, ?, ?, ?, 'pending')""",
            (customer_id, stylist_id, date, time, service_type)
        )
        
        self.refresh_appointments()
        
        # Clear form
        self.customer_phone_entry.delete(0, 'end')
        self.appointment_time_entry.delete(0, 'end')
    
    def add_service(self):
        """Add a new service"""
        name = self.service_name_entry.get()
        price = float(self.service_price_entry.get())
        duration = int(self.service_duration_entry.get())
        commission = float(self.service_commission_entry.get())
        
        db.execute(
            """INSERT INTO salon_services (name, price, duration_minutes, commission_rate)
               VALUES (?, ?, ?, ?)""",
            (name, price, duration, commission)
        )
        
        self.refresh_services()
        
        # Clear form
        self.service_name_entry.delete(0, 'end')
        self.service_price_entry.delete(0, 'end')
        self.service_duration_entry.delete(0, 'end')
        self.service_commission_entry.delete(0, 'end')
    
    def record_service(self):
        """Record a completed service"""
        phone = self.record_customer_entry.get()
        
        # Get customer
        customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        if not customer:
            return
        
        # Get stylist ID
        stylist_text = self.record_stylist_var.get()
        if ':' in stylist_text:
            stylist_id = int(stylist_text.split(':')[0])
        else:
            return
        
        # Get service ID
        service_text = self.record_service_var.get()
        if ':' in service_text:
            service_id = int(service_text.split(':')[0])
        else:
            return
        
        # Get service details
        service = db.fetchone("SELECT price, commission_rate FROM salon_services WHERE id = ?", (service_id,))
        price = service['price']
        commission = price * (service['commission_rate'] / 100)
        
        rating = int(self.rating_entry.get()) if self.rating_entry.get() else None
        review = self.review_entry.get()
        
        # Insert record
        db.execute(
            """INSERT INTO salon_service_records 
               (customer_id, stylist_id, service_id, service_date, price, commission, rating, review)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (customer['id'], stylist_id, service_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
             price, commission, rating, review)
        )
        
        # Record commission
        db.execute(
            """INSERT INTO employee_commissions (employee_id, service_date, service_type, amount)
               VALUES (?, ?, 'Salon', ?)""",
            (stylist_id, datetime.now().strftime('%Y-%m-%d'), commission)
        )
        
        # Clear form
        self.record_customer_entry.delete(0, 'end')
        self.rating_entry.delete(0, 'end')
        self.review_entry.delete(0, 'end')
    
    def refresh_appointments(self):
        """Refresh appointments list"""
        self.appointments_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        appointments = db.fetchall(
            """SELECT a.*, c.name as customer_name, c.phone, e.name as stylist_name
               FROM salon_appointments a
               LEFT JOIN customers c ON a.customer_id = c.id
               LEFT JOIN employees e ON a.stylist_id = e.id
               WHERE a.appointment_date = ?
               ORDER BY a.appointment_time""",
            (today,)
        )
        
        for apt in appointments:
            self.appointments_text.insert('end', 
                f"{apt['appointment_time']} - {apt['customer_name']} ({apt['phone']}) "
                f"with {apt['stylist_name']} for {apt['service_type']} - {apt['status']}\n"
            )
    
    def refresh_services(self):
        """Refresh services list"""
        self.services_text.delete('1.0', 'end')
        services = db.fetchall("SELECT * FROM salon_services")
        
        for svc in services:
            self.services_text.insert('end',
                f"{svc['name']} - ${svc['price']} ({svc['duration_minutes']} min) "
                f"- Commission: {svc['commission_rate']}%\n"
            )
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
