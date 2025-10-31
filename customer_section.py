"""
Customer Management Section Module
Handles customer registration, loyalty points, wallet, and history
"""
import customtkinter as ctk
from datetime import datetime
from ui_utils import *
from database import db

class CustomerSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the customer section UI"""
        # Header
        header = create_section_header(self.frame, "Customer Management")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Customers")
        self.tabview.add("History")
        self.tabview.add("Loyalty & Wallet")
        
        self.setup_customers_tab()
        self.setup_history_tab()
        self.setup_loyalty_tab()
    
    def setup_customers_tab(self):
        """Setup customer registration interface"""
        tab = self.tabview.tab("Customers")
        
        # Add customer form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Register Customer", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Name:").pack(pady=5)
        self.customer_name_entry = GlassEntry(form_frame, width=300)
        self.customer_name_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Phone:").pack(pady=5)
        self.customer_phone_entry = GlassEntry(form_frame, width=300)
        self.customer_phone_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Birthdate (YYYY-MM-DD):").pack(pady=5)
        self.customer_birthdate_entry = GlassEntry(form_frame, width=300)
        self.customer_birthdate_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Register Customer", command=self.register_customer).pack(pady=20)
        
        # Customers list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="All Customers", font=FONTS['subheading']).pack(pady=10)
        
        self.customers_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.customers_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_customers()
    
    def setup_history_tab(self):
        """Setup customer history interface"""
        tab = self.tabview.tab("History")
        
        # Search form
        search_frame = GlassFrame(tab)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(search_frame, text="Customer History", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(search_frame, text="Phone Number:").pack(pady=5)
        self.history_phone_entry = GlassEntry(search_frame, width=300)
        self.history_phone_entry.pack(pady=5)
        
        GlassButton(search_frame, text="View History", command=self.view_history).pack(pady=20)
        
        # History display
        history_frame = GlassFrame(tab)
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.history_text = ctk.CTkTextbox(
            history_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.history_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_loyalty_tab(self):
        """Setup loyalty points and wallet interface"""
        tab = self.tabview.tab("Loyalty & Wallet")
        
        # Loyalty management
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Manage Loyalty & Wallet", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Phone Number:").pack(pady=5)
        self.loyalty_phone_entry = GlassEntry(form_frame, width=300)
        self.loyalty_phone_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Add Points:").pack(pady=5)
        self.points_entry = GlassEntry(form_frame, width=300)
        self.points_entry.pack(pady=5)
        GlassButton(form_frame, text="Add Points", command=self.add_points).pack(pady=10)
        
        GlassLabel(form_frame, text="Add to Wallet ($):").pack(pady=5)
        self.wallet_entry = GlassEntry(form_frame, width=300)
        self.wallet_entry.pack(pady=5)
        GlassButton(form_frame, text="Add to Wallet", command=self.add_to_wallet).pack(pady=10)
        
        GlassButton(form_frame, text="View Customer Info", command=self.view_customer_info).pack(pady=20)
        
        # Info display
        info_frame = GlassFrame(tab)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.loyalty_text = ctk.CTkTextbox(
            info_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.loyalty_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def register_customer(self):
        """Register a new customer"""
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        birthdate = self.customer_birthdate_entry.get()
        
        # Check if customer exists
        existing = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        
        if existing:
            # Update existing customer
            db.execute(
                """UPDATE customers SET name = ?, birthdate = ? WHERE phone = ?""",
                (name, birthdate, phone)
            )
        else:
            # Create new customer
            db.execute(
                """INSERT INTO customers (name, phone, birthdate, registration_date)
                   VALUES (?, ?, ?, ?)""",
                (name, phone, birthdate, datetime.now().strftime('%Y-%m-%d'))
            )
        
        self.refresh_customers()
        
        # Clear form
        self.customer_name_entry.delete(0, 'end')
        self.customer_phone_entry.delete(0, 'end')
        self.customer_birthdate_entry.delete(0, 'end')
    
    def refresh_customers(self):
        """Refresh customers list"""
        self.customers_text.delete('1.0', 'end')
        customers = db.fetchall(
            """SELECT * FROM customers 
               ORDER BY registration_date DESC 
               LIMIT 50"""
        )
        
        for customer in customers:
            self.customers_text.insert('end',
                f"{customer['name']} - {customer['phone']} - "
                f"Points: {customer['loyalty_points']} - "
                f"Wallet: ${customer['wallet_balance']:.2f}\n"
            )
    
    def view_history(self):
        """View customer purchase history"""
        phone = self.history_phone_entry.get()
        customer = db.fetchone("SELECT * FROM customers WHERE phone = ?", (phone,))
        
        if not customer:
            self.history_text.delete('1.0', 'end')
            self.history_text.insert('end', "Customer not found.")
            return
        
        self.history_text.delete('1.0', 'end')
        self.history_text.insert('end', f"History for {customer['name']} ({phone})\n\n")
        
        # Salon services
        salon = db.fetchall(
            """SELECT s.service_date, sv.name, s.price
               FROM salon_service_records s
               JOIN salon_services sv ON s.service_id = sv.id
               WHERE s.customer_id = ?
               ORDER BY s.service_date DESC
               LIMIT 10""",
            (customer['id'],)
        )
        
        if salon:
            self.history_text.insert('end', "=== Salon Services ===\n")
            for svc in salon:
                self.history_text.insert('end', f"{svc['service_date']}: {svc['name']} - ${svc['price']:.2f}\n")
        
        # Cafe orders
        cafe = db.fetchall(
            """SELECT order_date, total_amount
               FROM cafe_orders
               WHERE customer_id = ?
               ORDER BY order_date DESC
               LIMIT 10""",
            (customer['id'],)
        )
        
        if cafe:
            self.history_text.insert('end', "\n=== Cafe Orders ===\n")
            for order in cafe:
                self.history_text.insert('end', f"{order['order_date']}: ${order['total_amount']:.2f}\n")
        
        # Gaming sessions
        gaming = db.fetchall(
            """SELECT start_time, duration_minutes, charge
               FROM gamnet_sessions
               WHERE customer_id = ? AND end_time IS NOT NULL
               ORDER BY start_time DESC
               LIMIT 10""",
            (customer['id'],)
        )
        
        if gaming:
            self.history_text.insert('end', "\n=== Gaming Sessions ===\n")
            for session in gaming:
                self.history_text.insert('end', 
                    f"{session['start_time']}: {session['duration_minutes']} min - ${session['charge']:.2f}\n")
    
    def add_points(self):
        """Add loyalty points to customer"""
        phone = self.loyalty_phone_entry.get()
        points = int(self.points_entry.get())
        
        db.execute(
            """UPDATE customers 
               SET loyalty_points = loyalty_points + ?
               WHERE phone = ?""",
            (points, phone)
        )
        
        self.points_entry.delete(0, 'end')
        self.view_customer_info()
    
    def add_to_wallet(self):
        """Add money to customer wallet"""
        phone = self.loyalty_phone_entry.get()
        amount = float(self.wallet_entry.get())
        
        db.execute(
            """UPDATE customers 
               SET wallet_balance = wallet_balance + ?
               WHERE phone = ?""",
            (amount, phone)
        )
        
        self.wallet_entry.delete(0, 'end')
        self.view_customer_info()
    
    def view_customer_info(self):
        """View customer loyalty and wallet info"""
        phone = self.loyalty_phone_entry.get()
        customer = db.fetchone("SELECT * FROM customers WHERE phone = ?", (phone,))
        
        if not customer:
            self.loyalty_text.delete('1.0', 'end')
            self.loyalty_text.insert('end', "Customer not found.")
            return
        
        self.loyalty_text.delete('1.0', 'end')
        self.loyalty_text.insert('end', f"Customer: {customer['name']}\n")
        self.loyalty_text.insert('end', f"Phone: {customer['phone']}\n")
        self.loyalty_text.insert('end', f"Loyalty Points: {customer['loyalty_points']}\n")
        self.loyalty_text.insert('end', f"Wallet Balance: ${customer['wallet_balance']:.2f}\n")
        self.loyalty_text.insert('end', f"Total Spent: ${customer['total_spent']:.2f}\n")
        self.loyalty_text.insert('end', f"Last Visit: {customer['last_visit_date'] or 'Never'}\n")
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
