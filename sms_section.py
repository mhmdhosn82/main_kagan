"""
SMS Panel Section Module
Handles SMS sending interface and history
"""
import customtkinter as ctk
from ui_utils import *
from database import db
from translations import tr
from sms_service import sms_service
from tkinter import messagebox

class SMSSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the SMS section UI"""
        # Header
        header = create_section_header(self.frame, tr('sms_panel'))
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add(tr('manual_sms'))
        self.tabview.add(tr('sms_history'))
        self.tabview.add(tr('automatic_sms'))
        
        self.setup_manual_tab()
        self.setup_history_tab()
        self.setup_automatic_tab()
    
    def setup_manual_tab(self):
        """Setup manual SMS sending interface"""
        tab = self.tabview.tab(tr('manual_sms'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text=tr('send_sms'), font=FONTS['heading']).pack(pady=10)
        
        # Recipient selection
        GlassLabel(form_frame, text="Send To:").pack(pady=5)
        
        send_type_var = ctk.StringVar(value="single")
        
        single_radio = ctk.CTkRadioButton(
            form_frame,
            text="Single Customer",
            variable=send_type_var,
            value="single"
        )
        single_radio.pack(pady=2)
        
        all_radio = ctk.CTkRadioButton(
            form_frame,
            text="All Customers",
            variable=send_type_var,
            value="all"
        )
        all_radio.pack(pady=2)
        
        active_radio = ctk.CTkRadioButton(
            form_frame,
            text="Active Customers (last 30 days)",
            variable=send_type_var,
            value="active"
        )
        active_radio.pack(pady=2)
        
        inactive_radio = ctk.CTkRadioButton(
            form_frame,
            text="Inactive Customers (30+ days)",
            variable=send_type_var,
            value="inactive"
        )
        inactive_radio.pack(pady=2)
        
        # Customer phone (for single)
        GlassLabel(form_frame, text="Customer Phone (for single):").pack(pady=5)
        phone_entry = GlassEntry(form_frame, width=300)
        phone_entry.pack(pady=5)
        
        # Message template
        GlassLabel(form_frame, text="Message Template:").pack(pady=5)
        template_var = ctk.StringVar(value="custom")
        template_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=template_var,
            values=["custom", "birthday", "promotional", "reactivation"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary'],
            command=lambda choice: self.load_template(choice, message_text)
        )
        template_menu.pack(pady=5)
        
        # Message text
        GlassLabel(form_frame, text="Message:").pack(pady=5)
        message_text = ctk.CTkTextbox(
            form_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text'],
            height=150,
            width=400
        )
        message_text.pack(pady=5)
        
        # Character counter
        char_count_label = GlassLabel(form_frame, text="Characters: 0", font=FONTS['small'])
        char_count_label.pack(pady=2)
        
        def update_char_count(*args):
            count = len(message_text.get('1.0', 'end-1c'))
            char_count_label.configure(text=f"Characters: {count}")
        
        message_text.bind('<KeyRelease>', update_char_count)
        
        # Send button
        def send_sms():
            send_type = send_type_var.get()
            message = message_text.get('1.0', 'end-1c').strip()
            
            if not message:
                messagebox.showerror("Error", "Please enter a message")
                return
            
            if send_type == "single":
                phone = phone_entry.get().strip()
                if not phone:
                    messagebox.showerror("Error", "Please enter customer phone")
                    return
                
                customer = db.fetchone("SELECT * FROM customers WHERE phone = ?", (phone,))
                if not customer:
                    messagebox.showerror("Error", "Customer not found")
                    return
                
                result = sms_service.send_sms(phone, message, 'manual', customer['id'])
                if result['success']:
                    messagebox.showinfo("Success", "SMS sent successfully!")
                else:
                    messagebox.showwarning("Warning", f"SMS logged but not sent: {result['message']}")
            
            else:
                # Get recipients based on type
                if send_type == "all":
                    customers = db.fetchall("SELECT * FROM customers")
                elif send_type == "active":
                    customers = db.fetchall(
                        """SELECT * FROM customers 
                           WHERE last_visit_date IS NOT NULL
                           AND julianday('now') - julianday(last_visit_date) <= 30"""
                    )
                else:  # inactive
                    customers = db.fetchall(
                        """SELECT * FROM customers 
                           WHERE last_visit_date IS NULL
                           OR julianday('now') - julianday(last_visit_date) > 30"""
                    )
                
                if not customers:
                    messagebox.showinfo("Info", "No customers found for this criteria")
                    return
                
                # Send to all
                sent_count = 0
                for customer in customers:
                    result = sms_service.send_sms(customer['phone'], message, 'manual', customer['id'])
                    if result.get('success'):
                        sent_count += 1
                
                messagebox.showinfo("Success", 
                    f"SMS sent to {sent_count}/{len(customers)} customers")
            
            # Refresh history
            self.refresh_history()
        
        GlassButton(
            form_frame,
            text=tr('send_sms'),
            command=send_sms,
            fg_color=COLORS['success'],
            width=200
        ).pack(pady=20)
    
    def load_template(self, template_type, text_widget):
        """Load message template"""
        templates = {
            'birthday': """سلام {name} عزیز،
تولدت مبارک! 🎉
ما در مجموعه کاگان آرزوی سالی پر از شادی و موفقیت برای شما داریم.
هدیه ویژه تولد شما آماده است.
مجموعه کاگان""",
            
            'promotional': """سلام {name} عزیز،
پیشنهاد ویژه فقط برای شما!
با استفاده از کد تخفیف SPECIAL20 از 20% تخفیف بهره‌مند شوید.
مجموعه کاگان""",
            
            'reactivation': """سلام {name} عزیز،
مدتی است که شما را ندیده‌ایم و دلتنگ شما هستیم.
برای بازگشت شما تخفیف ویژه در نظر گرفته‌ایم.
منتظر دیدار شما هستیم.
مجموعه کاگان"""
        }
        
        if template_type in templates:
            text_widget.delete('1.0', 'end')
            text_widget.insert('1.0', templates[template_type])
    
    def setup_history_tab(self):
        """Setup SMS history interface"""
        tab = self.tabview.tab(tr('sms_history'))
        
        # Filters
        filter_frame = GlassFrame(tab)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(filter_frame, text="Filter by Type:").pack(side='left', padx=5)
        
        filter_var = ctk.StringVar(value="all")
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=filter_var,
            values=["all", "manual", "survey", "birthday", "promotional", "reactivation"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary'],
            command=lambda _: self.refresh_history(filter_var.get())
        )
        filter_menu.pack(side='left', padx=5)
        
        GlassButton(
            filter_frame,
            text=tr('refresh'),
            command=lambda: self.refresh_history(filter_var.get()),
            width=100
        ).pack(side='left', padx=5)
        
        # History display
        history_frame = GlassFrame(tab)
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.history_text = ctk.CTkTextbox(
            history_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.history_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_history()
    
    def refresh_history(self, filter_type="all"):
        """Refresh SMS history display"""
        self.history_text.delete('1.0', 'end')
        
        if filter_type == "all":
            history = sms_service.get_sms_history()
        else:
            history = db.fetchall(
                """SELECT sh.*, c.name as customer_name
                   FROM sms_history sh
                   LEFT JOIN customers c ON sh.customer_id = c.id
                   WHERE sh.sms_type = ?
                   ORDER BY sh.sent_date DESC
                   LIMIT 100""",
                (filter_type,)
            )
        
        for sms in history:
            customer_name = sms['customer_name'] or 'Unknown'
            status_color = {
                'sent': '✓',
                'failed': '✗',
                'pending': '⏳',
                'disabled': '⊝',
                'error': '⚠'
            }.get(sms['status'], '?')
            
            self.history_text.insert('end',
                f"{status_color} {sms['sent_date']} | {customer_name} ({sms['phone_number']}) | "
                f"Type: {sms['sms_type']} | Status: {sms['status']}\n"
                f"   Message: {sms['message'][:80]}...\n\n"
            )
    
    def setup_automatic_tab(self):
        """Setup automatic SMS configuration"""
        tab = self.tabview.tab(tr('automatic_sms'))
        
        info_frame = GlassFrame(tab)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(info_frame, text=tr('automatic_sms'), font=FONTS['heading']).pack(pady=10)
        
        info_text = ctk.CTkTextbox(
            info_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text'],
            height=300
        )
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        info_text.insert('1.0', """Automatic SMS Features:

1. Survey SMS (24 hours after service)
   - Sent automatically to customers 24 hours after receiving a service
   - Requests feedback and rating
   - Helps improve service quality

2. Birthday SMS
   - Sent automatically on customer's birthday
   - Includes special birthday wishes
   - Can include birthday discount codes

3. Reactivation SMS (Monthly)
   - Sent to customers who haven't visited in 30+ days
   - Encourages return visits
   - Can include special comeback offers

4. Promotional SMS
   - Sent manually to specific customer groups
   - Used for special offers and campaigns
   - Customizable messages

To enable automatic SMS:
1. Go to Settings > SMS Configuration
2. Configure your SMS provider (Twilio, Kavenegar, or Ghasedak)
3. Enter your API credentials
4. Automatic SMS will be sent based on customer activity

Note: SMS provider must be properly configured for automatic SMS to work.
""")
        info_text.configure(state='disabled')
        
        # Manual trigger buttons
        actions_frame = GlassFrame(tab)
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(actions_frame, text="Manual Triggers:", font=FONTS['subheading']).pack(pady=10)
        
        def trigger_surveys():
            sms_service.schedule_automatic_sms()
            messagebox.showinfo("Success", "Automatic SMS check completed!")
            self.refresh_history()
        
        GlassButton(
            actions_frame,
            text="Check & Send Pending Automatic SMS",
            command=trigger_surveys,
            width=300
        ).pack(pady=5)
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
