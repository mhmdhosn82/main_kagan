"""
Gamnet (Gaming Net) Section Module
Handles device management, timers, reservations, and customer credits
"""
import customtkinter as ctk
from datetime import datetime, timedelta
from ui_utils import *
from database import db

class GamnetSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.active_sessions = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the gamnet section UI"""
        # Header
        header = create_section_header(self.frame, "Gamnet (Gaming Net) Management")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Devices")
        self.tabview.add("Sessions")
        self.tabview.add("Reservations")
        self.tabview.add("Reports")
        
        self.setup_devices_tab()
        self.setup_sessions_tab()
        self.setup_reservations_tab()
        self.setup_reports_tab()
    
    def setup_devices_tab(self):
        """Setup device management interface"""
        tab = self.tabview.tab("Devices")
        
        # Add device form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Add Gaming Device", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Device Number:").pack(pady=5)
        self.device_number_entry = GlassEntry(form_frame, width=300)
        self.device_number_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Device Type:").pack(pady=5)
        self.device_type_var = ctk.StringVar(value="PC")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.device_type_var,
            values=["PC", "PlayStation", "Xbox", "VR"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Hourly Rate:").pack(pady=5)
        self.hourly_rate_entry = GlassEntry(form_frame, width=300)
        self.hourly_rate_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Add Device", command=self.add_device).pack(pady=20)
        
        # Devices list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Gaming Devices", font=FONTS['subheading']).pack(pady=10)
        
        self.devices_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.devices_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_devices()
    
    def setup_sessions_tab(self):
        """Setup gaming sessions interface"""
        tab = self.tabview.tab("Sessions")
        
        # Start session form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Manage Gaming Sessions", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Customer Phone:").pack(pady=5)
        self.session_customer_entry = GlassEntry(form_frame, width=300)
        self.session_customer_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Device:").pack(pady=5)
        self.session_device_var = ctk.StringVar(value="Select Device")
        self.session_device_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.session_device_var,
            values=self.get_available_devices(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        self.session_device_dropdown.pack(pady=5)
        
        GlassButton(form_frame, text="Start Session", command=self.start_session,
                   fg_color=COLORS['success']).pack(pady=10)
        GlassButton(form_frame, text="End Session", command=self.end_session,
                   fg_color=COLORS['error']).pack(pady=10)
        
        # Active sessions display
        sessions_frame = GlassFrame(tab)
        sessions_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(sessions_frame, text="Active Sessions", font=FONTS['subheading']).pack(pady=10)
        
        self.sessions_text = ctk.CTkTextbox(
            sessions_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.sessions_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_sessions()
    
    def setup_reservations_tab(self):
        """Setup reservations interface"""
        tab = self.tabview.tab("Reservations")
        
        # Reservation form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Make Reservation", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Customer Phone:").pack(pady=5)
        self.reservation_customer_entry = GlassEntry(form_frame, width=300)
        self.reservation_customer_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Device:").pack(pady=5)
        self.reservation_device_var = ctk.StringVar(value="Select Device")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.reservation_device_var,
            values=self.get_all_devices(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.reservation_date_entry = GlassEntry(form_frame, width=300)
        self.reservation_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.reservation_date_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Time (HH:MM):").pack(pady=5)
        self.reservation_time_entry = GlassEntry(form_frame, width=300)
        self.reservation_time_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Duration (minutes):").pack(pady=5)
        self.reservation_duration_entry = GlassEntry(form_frame, width=300)
        self.reservation_duration_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Make Reservation", command=self.make_reservation).pack(pady=20)
        
        # Reservations list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Upcoming Reservations", font=FONTS['subheading']).pack(pady=10)
        
        self.reservations_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.reservations_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_reservations()
    
    def setup_reports_tab(self):
        """Setup usage reports interface"""
        tab = self.tabview.tab("Reports")
        
        # Report options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Usage Reports", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(options_frame, text="Daily Usage Report", 
                   command=self.show_daily_usage).pack(pady=5)
        GlassButton(options_frame, text="Peak Hours Analysis", 
                   command=self.show_peak_hours).pack(pady=5)
        GlassButton(options_frame, text="Device Performance", 
                   command=self.show_device_performance).pack(pady=5)
        
        # Report display
        report_frame = GlassFrame(tab)
        report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.report_text = ctk.CTkTextbox(
            report_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def get_available_devices(self):
        """Get list of available devices"""
        devices = db.fetchall("SELECT id, device_number, device_type FROM gamnet_devices WHERE is_available = 1")
        if devices:
            return [f"{d['id']}: {d['device_number']} ({d['device_type']})" for d in devices]
        return ["No devices available"]
    
    def get_all_devices(self):
        """Get list of all devices"""
        devices = db.fetchall("SELECT id, device_number, device_type FROM gamnet_devices")
        if devices:
            return [f"{d['id']}: {d['device_number']} ({d['device_type']})" for d in devices]
        return ["No devices"]
    
    def add_device(self):
        """Add a new gaming device"""
        number = self.device_number_entry.get()
        device_type = self.device_type_var.get()
        rate = float(self.hourly_rate_entry.get())
        
        db.execute(
            """INSERT INTO gamnet_devices (device_number, device_type, hourly_rate)
               VALUES (?, ?, ?)""",
            (number, device_type, rate)
        )
        
        self.refresh_devices()
        
        # Clear form
        self.device_number_entry.delete(0, 'end')
        self.hourly_rate_entry.delete(0, 'end')
    
    def start_session(self):
        """Start a gaming session"""
        phone = self.session_customer_entry.get()
        
        # Get or create customer
        customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        if not customer:
            db.execute(
                "INSERT INTO customers (name, phone, registration_date) VALUES (?, ?, ?)",
                (f"Customer {phone}", phone, datetime.now().strftime('%Y-%m-%d'))
            )
            customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        
        # Get device ID
        device_text = self.session_device_var.get()
        if ':' not in device_text:
            return
        
        device_id = int(device_text.split(':')[0])
        
        # Start session
        db.execute(
            """INSERT INTO gamnet_sessions (device_id, customer_id, start_time)
               VALUES (?, ?, ?)""",
            (device_id, customer['id'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        
        # Mark device as unavailable
        db.execute("UPDATE gamnet_devices SET is_available = 0, status = 'in_use' WHERE id = ?", (device_id,))
        
        self.refresh_sessions()
        self.session_customer_entry.delete(0, 'end')
    
    def end_session(self):
        """End a gaming session"""
        device_text = self.session_device_var.get()
        if ':' not in device_text:
            return
        
        device_id = int(device_text.split(':')[0])
        
        # Get active session
        session = db.fetchone(
            """SELECT * FROM gamnet_sessions 
               WHERE device_id = ? AND end_time IS NULL
               ORDER BY start_time DESC LIMIT 1""",
            (device_id,)
        )
        
        if not session:
            return
        
        # Calculate duration and charge
        start_time = datetime.strptime(session['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60  # in minutes
        
        # Get device rate
        device = db.fetchone("SELECT hourly_rate FROM gamnet_devices WHERE id = ?", (device_id,))
        charge = (duration / 60) * device['hourly_rate']
        
        # Update session
        db.execute(
            """UPDATE gamnet_sessions 
               SET end_time = ?, duration_minutes = ?, charge = ?
               WHERE id = ?""",
            (end_time.strftime('%Y-%m-%d %H:%M:%S'), int(duration), charge, session['id'])
        )
        
        # Mark device as available
        db.execute("UPDATE gamnet_devices SET is_available = 1, status = 'available' WHERE id = ?", (device_id,))
        
        self.refresh_sessions()
    
    def make_reservation(self):
        """Make a device reservation"""
        phone = self.reservation_customer_entry.get()
        
        # Get or create customer
        customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        if not customer:
            db.execute(
                "INSERT INTO customers (name, phone, registration_date) VALUES (?, ?, ?)",
                (f"Customer {phone}", phone, datetime.now().strftime('%Y-%m-%d'))
            )
            customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        
        # Get device ID
        device_text = self.reservation_device_var.get()
        if ':' not in device_text:
            return
        
        device_id = int(device_text.split(':')[0])
        date = self.reservation_date_entry.get()
        time = self.reservation_time_entry.get()
        duration = int(self.reservation_duration_entry.get())
        
        # Create reservation
        db.execute(
            """INSERT INTO gamnet_reservations 
               (device_id, customer_id, reservation_date, reservation_time, duration_minutes)
               VALUES (?, ?, ?, ?, ?)""",
            (device_id, customer['id'], date, time, duration)
        )
        
        self.refresh_reservations()
        
        # Clear form
        self.reservation_customer_entry.delete(0, 'end')
        self.reservation_time_entry.delete(0, 'end')
        self.reservation_duration_entry.delete(0, 'end')
    
    def refresh_devices(self):
        """Refresh devices list"""
        self.devices_text.delete('1.0', 'end')
        devices = db.fetchall("SELECT * FROM gamnet_devices")
        
        for device in devices:
            status = "Available" if device['is_available'] else "In Use"
            self.devices_text.insert('end',
                f"{device['device_number']} ({device['device_type']}) - "
                f"${device['hourly_rate']}/hr - {status}\n"
            )
    
    def refresh_sessions(self):
        """Refresh active sessions list"""
        self.sessions_text.delete('1.0', 'end')
        sessions = db.fetchall(
            """SELECT s.*, d.device_number, c.name as customer_name, c.phone
               FROM gamnet_sessions s
               JOIN gamnet_devices d ON s.device_id = d.id
               JOIN customers c ON s.customer_id = c.id
               WHERE s.end_time IS NULL"""
        )
        
        for session in sessions:
            start_time = datetime.strptime(session['start_time'], '%Y-%m-%d %H:%M:%S')
            duration = (datetime.now() - start_time).total_seconds() / 60
            self.sessions_text.insert('end',
                f"{session['device_number']} - {session['customer_name']} ({session['phone']}) - "
                f"{int(duration)} minutes\n"
            )
    
    def refresh_reservations(self):
        """Refresh reservations list"""
        self.reservations_text.delete('1.0', 'end')
        reservations = db.fetchall(
            """SELECT r.*, d.device_number, c.name as customer_name, c.phone
               FROM gamnet_reservations r
               JOIN gamnet_devices d ON r.device_id = d.id
               JOIN customers c ON r.customer_id = c.id
               WHERE r.status = 'pending'
               ORDER BY r.reservation_date, r.reservation_time"""
        )
        
        for res in reservations:
            self.reservations_text.insert('end',
                f"{res['reservation_date']} {res['reservation_time']} - "
                f"{res['device_number']} - {res['customer_name']} ({res['phone']}) - "
                f"{res['duration_minutes']} min\n"
            )
    
    def show_daily_usage(self):
        """Show daily usage report"""
        self.report_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        
        sessions = db.fetchall(
            """SELECT COUNT(*) as count, SUM(duration_minutes) as total_minutes, SUM(charge) as revenue
               FROM gamnet_sessions
               WHERE DATE(start_time) = ? AND end_time IS NOT NULL""",
            (today,)
        )
        
        if sessions and sessions[0]['count']:
            self.report_text.insert('end', f"Daily Usage Report for {today}\n\n")
            self.report_text.insert('end', f"Total Sessions: {sessions[0]['count']}\n")
            self.report_text.insert('end', f"Total Minutes: {sessions[0]['total_minutes']}\n")
            self.report_text.insert('end', f"Total Revenue: ${sessions[0]['revenue']:.2f}\n")
        else:
            self.report_text.insert('end', "No sessions today yet.")
    
    def show_peak_hours(self):
        """Show peak hours analysis"""
        self.report_text.delete('1.0', 'end')
        
        # Simple peak hours analysis
        self.report_text.insert('end', "Peak Hours Analysis\n\n")
        self.report_text.insert('end', "Most active times will be shown here based on historical data.\n")
    
    def show_device_performance(self):
        """Show device performance report"""
        self.report_text.delete('1.0', 'end')
        
        devices = db.fetchall(
            """SELECT d.device_number, d.device_type, 
                      COUNT(s.id) as sessions, SUM(s.charge) as revenue
               FROM gamnet_devices d
               LEFT JOIN gamnet_sessions s ON d.id = s.device_id
               GROUP BY d.id
               ORDER BY revenue DESC"""
        )
        
        self.report_text.insert('end', "Device Performance Report\n\n")
        for device in devices:
            sessions = device['sessions'] or 0
            revenue = device['revenue'] or 0
            self.report_text.insert('end',
                f"{device['device_number']} ({device['device_type']}): "
                f"{sessions} sessions, ${revenue:.2f} revenue\n"
            )
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
