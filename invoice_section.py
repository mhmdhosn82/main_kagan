"""
Invoice and Cashier Section Module
Handles unified invoicing, payments, and cashier operations
"""
import customtkinter as ctk
from datetime import datetime
from ui_utils import *
from database import db

class InvoiceSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.current_invoice_items = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the invoice section UI"""
        # Header
        header = create_section_header(self.frame, "Invoice & Cashier")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Create Invoice")
        self.tabview.add("Payment")
        self.tabview.add("Invoice History")
        
        self.setup_create_tab()
        self.setup_payment_tab()
        self.setup_history_tab()
    
    def setup_create_tab(self):
        """Setup invoice creation interface"""
        tab = self.tabview.tab("Create Invoice")
        
        # Invoice form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Create Unified Invoice", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Customer Phone:").pack(pady=5)
        self.invoice_customer_entry = GlassEntry(form_frame, width=300)
        self.invoice_customer_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Add Services/Items:").pack(pady=10)
        
        # Service type selection
        GlassLabel(form_frame, text="Type:").pack(pady=5)
        self.service_type_var = ctk.StringVar(value="Salon")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.service_type_var,
            values=["Salon", "Cafe", "Gamnet"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Description:").pack(pady=5)
        self.item_desc_entry = GlassEntry(form_frame, width=300)
        self.item_desc_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Amount ($):").pack(pady=5)
        self.item_amount_entry = GlassEntry(form_frame, width=300)
        self.item_amount_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Add to Invoice", command=self.add_to_invoice).pack(pady=10)
        
        GlassLabel(form_frame, text="Campaign Code:").pack(pady=5)
        self.campaign_code_entry = GlassEntry(form_frame, width=300)
        self.campaign_code_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Apply Campaign", command=self.apply_campaign).pack(pady=10)
        
        GlassButton(form_frame, text="Create Invoice", command=self.create_invoice,
                   fg_color=COLORS['success']).pack(pady=20)
        
        # Current invoice display
        invoice_frame = GlassFrame(tab)
        invoice_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(invoice_frame, text="Current Invoice", font=FONTS['subheading']).pack(pady=10)
        
        self.current_invoice_text = ctk.CTkTextbox(
            invoice_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.current_invoice_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.discount_amount = 0
    
    def setup_payment_tab(self):
        """Setup payment processing interface"""
        tab = self.tabview.tab("Payment")
        
        # Payment form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Process Payment", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Invoice ID:").pack(pady=5)
        self.payment_invoice_entry = GlassEntry(form_frame, width=300)
        self.payment_invoice_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Payment Method:").pack(pady=5)
        self.payment_method_var = ctk.StringVar(value="Cash")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.payment_method_var,
            values=["Cash", "Card", "Wallet"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassButton(form_frame, text="Process Payment", command=self.process_payment,
                   fg_color=COLORS['success']).pack(pady=20)
        
        # Payment display
        payment_frame = GlassFrame(tab)
        payment_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.payment_text = ctk.CTkTextbox(
            payment_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.payment_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_history_tab(self):
        """Setup invoice history interface"""
        tab = self.tabview.tab("Invoice History")
        
        # Search form
        search_frame = GlassFrame(tab)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(search_frame, text="Invoice History", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(search_frame, text="Show Today's Invoices", 
                   command=self.show_todays_invoices).pack(pady=10)
        
        # History display
        history_frame = GlassFrame(tab)
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.history_text = ctk.CTkTextbox(
            history_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.history_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def add_to_invoice(self):
        """Add item to current invoice"""
        service_type = self.service_type_var.get()
        description = self.item_desc_entry.get()
        amount = float(self.item_amount_entry.get())
        
        self.current_invoice_items.append({
            'type': service_type,
            'description': description,
            'amount': amount
        })
        
        self.refresh_current_invoice()
        
        # Clear entries
        self.item_desc_entry.delete(0, 'end')
        self.item_amount_entry.delete(0, 'end')
    
    def apply_campaign(self):
        """Apply campaign code discount"""
        code = self.campaign_code_entry.get()
        
        campaign = db.fetchone(
            """SELECT * FROM campaigns 
               WHERE code = ? AND is_active = 1 
               AND date('now') BETWEEN start_date AND end_date""",
            (code,)
        )
        
        if campaign:
            total = sum(item['amount'] for item in self.current_invoice_items)
            self.discount_amount = total * (campaign['discount_percentage'] / 100)
            self.refresh_current_invoice()
    
    def refresh_current_invoice(self):
        """Refresh current invoice display"""
        self.current_invoice_text.delete('1.0', 'end')
        
        total = 0
        for item in self.current_invoice_items:
            self.current_invoice_text.insert('end',
                f"[{item['type']}] {item['description']}: ${item['amount']:.2f}\n"
            )
            total += item['amount']
        
        self.current_invoice_text.insert('end', f"\nSubtotal: ${total:.2f}\n")
        if self.discount_amount > 0:
            self.current_invoice_text.insert('end', f"Discount: -${self.discount_amount:.2f}\n")
        final = total - self.discount_amount
        self.current_invoice_text.insert('end', f"Total: ${final:.2f}\n")
    
    def create_invoice(self):
        """Create and save invoice"""
        if not self.current_invoice_items:
            return
        
        phone = self.invoice_customer_entry.get()
        
        # Get or create customer
        customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        if not customer:
            db.execute(
                "INSERT INTO customers (name, phone, registration_date) VALUES (?, ?, ?)",
                (f"Customer {phone}", phone, datetime.now().strftime('%Y-%m-%d'))
            )
            customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        
        # Calculate totals
        total = sum(item['amount'] for item in self.current_invoice_items)
        final = total - self.discount_amount
        
        # Create invoice
        campaign_code = self.campaign_code_entry.get() or None
        
        db.execute(
            """INSERT INTO invoices 
               (customer_id, invoice_date, total_amount, discount_amount, final_amount, campaign_code)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (customer['id'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
             total, self.discount_amount, final, campaign_code)
        )
        
        invoice_id = db.fetchone("SELECT last_insert_rowid() as id")['id']
        
        # Show invoice ID
        self.current_invoice_text.insert('end', f"\n\nInvoice #{invoice_id} created!\n")
        
        # Clear for next invoice
        self.current_invoice_items = []
        self.discount_amount = 0
        self.invoice_customer_entry.delete(0, 'end')
        self.campaign_code_entry.delete(0, 'end')
    
    def process_payment(self):
        """Process payment for an invoice"""
        invoice_id = int(self.payment_invoice_entry.get())
        payment_method = self.payment_method_var.get()
        
        invoice = db.fetchone("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
        
        if not invoice:
            self.payment_text.delete('1.0', 'end')
            self.payment_text.insert('end', "Invoice not found.")
            return
        
        if invoice['is_paid']:
            self.payment_text.delete('1.0', 'end')
            self.payment_text.insert('end', "Invoice already paid.")
            return
        
        # Process payment
        if payment_method == "Wallet":
            # Deduct from wallet
            db.execute(
                """UPDATE customers 
                   SET wallet_balance = wallet_balance - ?
                   WHERE id = ?""",
                (invoice['final_amount'], invoice['customer_id'])
            )
        
        # Mark as paid
        db.execute(
            """UPDATE invoices 
               SET is_paid = 1, payment_method = ?
               WHERE id = ?""",
            (payment_method, invoice_id)
        )
        
        # Update customer stats
        db.execute(
            """UPDATE customers 
               SET total_spent = total_spent + ?, 
                   last_visit_date = ?,
                   loyalty_points = loyalty_points + ?
               WHERE id = ?""",
            (invoice['final_amount'], datetime.now().strftime('%Y-%m-%d'), 
             int(invoice['final_amount']), invoice['customer_id'])
        )
        
        self.payment_text.delete('1.0', 'end')
        self.payment_text.insert('end', f"Payment processed successfully!\n")
        self.payment_text.insert('end', f"Invoice #{invoice_id}\n")
        self.payment_text.insert('end', f"Amount: ${invoice['final_amount']:.2f}\n")
        self.payment_text.insert('end', f"Method: {payment_method}\n")
        
        self.payment_invoice_entry.delete(0, 'end')
    
    def show_todays_invoices(self):
        """Show today's invoices"""
        self.history_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        
        invoices = db.fetchall(
            """SELECT i.*, c.name, c.phone
               FROM invoices i
               JOIN customers c ON i.customer_id = c.id
               WHERE DATE(i.invoice_date) = ?
               ORDER BY i.invoice_date DESC""",
            (today,)
        )
        
        total_revenue = 0
        for inv in invoices:
            paid = "Paid" if inv['is_paid'] else "Unpaid"
            self.history_text.insert('end',
                f"Invoice #{inv['id']} - {inv['name']} ({inv['phone']}) - "
                f"${inv['final_amount']:.2f} - {inv['payment_method'] or 'N/A'} - {paid}\n"
            )
            if inv['is_paid']:
                total_revenue += inv['final_amount']
        
        self.history_text.insert('end', f"\nTotal Revenue Today: ${total_revenue:.2f}\n")
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
