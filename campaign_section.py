"""
Campaigns and Marketing Section Module
Handles discount campaigns, SMS notifications, and coupons
"""
import customtkinter as ctk
from datetime import datetime
from ui_utils import *
from database import db
import random
import string

class CampaignSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the campaign section UI"""
        # Header
        header = create_section_header(self.frame, "Campaigns & Marketing")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Campaigns")
        self.tabview.add("Messages")
        self.tabview.add("Analytics")
        
        self.setup_campaigns_tab()
        self.setup_messages_tab()
        self.setup_analytics_tab()
    
    def setup_campaigns_tab(self):
        """Setup campaign creation interface"""
        tab = self.tabview.tab("Campaigns")
        
        # Create campaign form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Create Campaign", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Campaign Name:").pack(pady=5)
        self.campaign_name_entry = GlassEntry(form_frame, width=300)
        self.campaign_name_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Description:").pack(pady=5)
        self.campaign_desc_entry = GlassEntry(form_frame, width=300)
        self.campaign_desc_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Discount Percentage:").pack(pady=5)
        self.campaign_discount_entry = GlassEntry(form_frame, width=300)
        self.campaign_discount_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Start Date (YYYY-MM-DD):").pack(pady=5)
        self.campaign_start_entry = GlassEntry(form_frame, width=300)
        self.campaign_start_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.campaign_start_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="End Date (YYYY-MM-DD):").pack(pady=5)
        self.campaign_end_entry = GlassEntry(form_frame, width=300)
        self.campaign_end_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Create Campaign", command=self.create_campaign).pack(pady=20)
        
        # Campaigns list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Active Campaigns", font=FONTS['subheading']).pack(pady=10)
        
        self.campaigns_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.campaigns_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_campaigns()
    
    def setup_messages_tab(self):
        """Setup messaging interface"""
        tab = self.tabview.tab("Messages")
        
        # Message form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Send Messages", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(form_frame, text="Send Birthday Greetings", 
                   command=self.send_birthday_messages).pack(pady=10)
        GlassButton(form_frame, text="Send to Inactive Customers", 
                   command=self.send_inactive_messages).pack(pady=10)
        GlassButton(form_frame, text="Send Campaign Notifications", 
                   command=self.send_campaign_messages).pack(pady=10)
        
        # Messages display
        messages_frame = GlassFrame(tab)
        messages_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(messages_frame, text="Message Queue", font=FONTS['subheading']).pack(pady=10)
        
        self.messages_text = ctk.CTkTextbox(
            messages_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.messages_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_messages()
    
    def setup_analytics_tab(self):
        """Setup campaign analytics interface"""
        tab = self.tabview.tab("Analytics")
        
        # Analytics options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Campaign Analytics", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(options_frame, text="Campaign Usage Report", 
                   command=self.show_campaign_usage).pack(pady=10)
        GlassButton(options_frame, text="Customer Engagement", 
                   command=self.show_engagement).pack(pady=10)
        
        # Analytics display
        analytics_frame = GlassFrame(tab)
        analytics_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.analytics_text = ctk.CTkTextbox(
            analytics_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.analytics_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def generate_code(self):
        """Generate a random campaign code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    def create_campaign(self):
        """Create a new campaign"""
        name = self.campaign_name_entry.get()
        description = self.campaign_desc_entry.get()
        discount = float(self.campaign_discount_entry.get())
        start_date = self.campaign_start_entry.get()
        end_date = self.campaign_end_entry.get()
        code = self.generate_code()
        
        db.execute(
            """INSERT INTO campaigns 
               (name, description, discount_percentage, code, start_date, end_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, description, discount, code, start_date, end_date)
        )
        
        self.refresh_campaigns()
        
        # Clear form
        self.campaign_name_entry.delete(0, 'end')
        self.campaign_desc_entry.delete(0, 'end')
        self.campaign_discount_entry.delete(0, 'end')
        self.campaign_end_entry.delete(0, 'end')
    
    def refresh_campaigns(self):
        """Refresh campaigns list"""
        self.campaigns_text.delete('1.0', 'end')
        campaigns = db.fetchall(
            """SELECT * FROM campaigns 
               WHERE is_active = 1 
               ORDER BY start_date DESC"""
        )
        
        for campaign in campaigns:
            self.campaigns_text.insert('end',
                f"{campaign['name']} - {campaign['discount_percentage']}% off\n"
                f"  Code: {campaign['code']}\n"
                f"  Valid: {campaign['start_date']} to {campaign['end_date']}\n"
                f"  {campaign['description']}\n\n"
            )
    
    def send_birthday_messages(self):
        """Send birthday greetings to customers"""
        today = datetime.now().strftime('%m-%d')
        
        customers = db.fetchall(
            """SELECT id, name, phone FROM customers 
               WHERE substr(birthdate, 6, 5) = ?""",
            (today,)
        )
        
        for customer in customers:
            message = f"Happy Birthday {customer['name']}! Enjoy a special 20% discount today!"
            db.execute(
                """INSERT INTO messages 
                   (recipient_type, recipient_id, message_type, content, sent_date)
                   VALUES ('customer', ?, 'birthday', ?, ?)""",
                (customer['id'], message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
        
        self.refresh_messages()
    
    def send_inactive_messages(self):
        """Send messages to inactive customers"""
        # Customers who haven't visited in 30 days
        customers = db.fetchall(
            """SELECT id, name, phone FROM customers 
               WHERE last_visit_date IS NULL 
               OR julianday('now') - julianday(last_visit_date) > 30
               LIMIT 50"""
        )
        
        for customer in customers:
            message = f"We miss you {customer['name']}! Come back and get 15% off your next visit!"
            db.execute(
                """INSERT INTO messages 
                   (recipient_type, recipient_id, message_type, content, sent_date)
                   VALUES ('customer', ?, 'promotional', ?, ?)""",
                (customer['id'], message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
        
        self.refresh_messages()
    
    def send_campaign_messages(self):
        """Send campaign notifications to all customers"""
        campaigns = db.fetchall(
            """SELECT * FROM campaigns 
               WHERE is_active = 1 
               AND date('now') BETWEEN start_date AND end_date
               LIMIT 1"""
        )
        
        if not campaigns:
            return
        
        campaign = campaigns[0]
        customers = db.fetchall("SELECT id, name, phone FROM customers LIMIT 100")
        
        for customer in customers:
            message = f"Special offer for you! {campaign['name']}: {campaign['description']} Use code: {campaign['code']}"
            db.execute(
                """INSERT INTO messages 
                   (recipient_type, recipient_id, message_type, content, sent_date)
                   VALUES ('customer', ?, 'campaign', ?, ?)""",
                (customer['id'], message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
        
        self.refresh_messages()
    
    def refresh_messages(self):
        """Refresh messages list"""
        self.messages_text.delete('1.0', 'end')
        messages = db.fetchall(
            """SELECT m.*, c.name, c.phone
               FROM messages m
               JOIN customers c ON m.recipient_id = c.id
               WHERE m.recipient_type = 'customer'
               ORDER BY m.sent_date DESC
               LIMIT 50"""
        )
        
        for msg in messages:
            sent = "Sent" if msg['is_sent'] else "Pending"
            self.messages_text.insert('end',
                f"[{msg['message_type']}] To: {msg['name']} ({msg['phone']}) - {sent}\n"
                f"  {msg['content']}\n\n"
            )
    
    def show_campaign_usage(self):
        """Show campaign usage statistics"""
        self.analytics_text.delete('1.0', 'end')
        
        campaigns = db.fetchall(
            """SELECT c.name, c.code, COUNT(i.id) as uses, SUM(i.discount_amount) as total_discount
               FROM campaigns c
               LEFT JOIN invoices i ON c.code = i.campaign_code
               GROUP BY c.id
               ORDER BY uses DESC"""
        )
        
        self.analytics_text.insert('end', "Campaign Usage Report\n\n")
        for campaign in campaigns:
            uses = campaign['uses'] or 0
            discount = campaign['total_discount'] or 0
            self.analytics_text.insert('end',
                f"{campaign['name']} ({campaign['code']}): {uses} uses, ${discount:.2f} in discounts\n"
            )
    
    def show_engagement(self):
        """Show customer engagement metrics"""
        self.analytics_text.delete('1.0', 'end')
        
        # Customer statistics
        total = db.fetchone("SELECT COUNT(*) as count FROM customers")['count']
        active = db.fetchone(
            """SELECT COUNT(*) as count FROM customers 
               WHERE last_visit_date IS NOT NULL 
               AND julianday('now') - julianday(last_visit_date) <= 30"""
        )['count']
        
        self.analytics_text.insert('end', "Customer Engagement Metrics\n\n")
        self.analytics_text.insert('end', f"Total Customers: {total}\n")
        self.analytics_text.insert('end', f"Active Customers (30 days): {active}\n")
        self.analytics_text.insert('end', f"Inactive Customers: {total - active}\n")
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
