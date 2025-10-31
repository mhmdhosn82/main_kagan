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
        
        # Check SMS configuration status
        from sms_service import sms_service
        
        def check_and_show_warning():
            """Check configuration and show warning if not configured"""
            is_configured = sms_service.is_configured()
            if not is_configured:
                # Show warning if not configured
                warning_frame = GlassFrame(tab)
                warning_frame.pack(fill='x', padx=10, pady=10)
                
                GlassLabel(
                    warning_frame,
                    text="⚠️ SMS Not Configured",
                    font=FONTS['heading'],
                    text_color=COLORS['error']
                ).pack(pady=10)
                
                GlassLabel(
                    warning_frame,
                    text="SMS API is not configured. Please configure SMS settings before sending SMS.",
                    font=FONTS['normal']
                ).pack(pady=5)
                
                def open_settings():
                    # This would need to navigate to settings tab
                    messagebox.showinfo("Info", "Please go to Settings > SMS Configuration to configure SMS API")
                
                GlassButton(
                    warning_frame,
                    text="Go to SMS Settings",
                    command=open_settings,
                    fg_color=COLORS['primary'],
                    width=200
                ).pack(pady=20)
            return is_configured
        
        check_and_show_warning()
        
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
            # Check if SMS is configured
            if not sms_service.is_configured():
                messagebox.showerror(
                    "SMS Not Configured",
                    "SMS API is not configured. Please go to Settings > SMS Configuration to set up your SMS provider, API key, and sender number before sending SMS."
                )
                return
            
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
                    messagebox.showerror("Error", f"Failed to send SMS: {result['message']}")
            
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
                
                # Confirm bulk send
                if not messagebox.askyesno("Confirm", f"Send SMS to {len(customers)} customers?"):
                    return
                
                # Send to all
                sent_count = 0
                failed_count = 0
                for customer in customers:
                    result = sms_service.send_sms(customer['phone'], message, 'manual', customer['id'])
                    if result.get('success'):
                        sent_count += 1
                    else:
                        failed_count += 1
                
                messagebox.showinfo("Complete", 
                    f"SMS sent to {sent_count} customers\nFailed: {failed_count}")
            
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
                'not_configured': '⚙',
                'no_api_key': '🔑',
                'error': '⚠'
            }.get(sms['status'], '?')
            
            self.history_text.insert('end',
                f"{status_color} {sms['sent_date']} | {customer_name} ({sms['phone_number']}) | "
                f"Type: {sms['sms_type']} | Status: {sms['status']}\n"
                f"   Message: {sms['message'][:80]}...\n"
            )
            
            # Show error message if present
            if sms.get('error_message'):
                self.history_text.insert('end', f"   Error: {sms['error_message']}\n")
            
            self.history_text.insert('end', '\n')
    
    def setup_automatic_tab(self):
        """Setup manual campaign SMS interface (formerly automatic)"""
        tab = self.tabview.tab(tr('automatic_sms'))
        
        info_frame = GlassFrame(tab)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(info_frame, text="Campaign SMS (Manual)", font=FONTS['heading']).pack(pady=10)
        
        info_text = ctk.CTkTextbox(
            info_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text'],
            height=300
        )
        info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        info_text.insert('1.0', """Campaign SMS Features (All Manual):

All SMS sending now requires explicit user action and proper API configuration.
Automatic SMS sending has been removed for better control and cost management.

Available Campaign Types:

1. Survey SMS
   - Send manually to customers after service
   - Requests feedback and rating
   - Helps improve service quality

2. Birthday SMS
   - Send manually on customer's birthday
   - Includes special birthday wishes
   - Can include birthday discount codes

3. Reactivation SMS
   - Send manually to inactive customers
   - Encourages return visits
   - Can include special comeback offers

4. Promotional SMS
   - Send to specific customer groups
   - Used for special offers and campaigns
   - Customizable messages

How to Use:
1. Configure SMS API in Settings > SMS Configuration
2. Set provider, API key, and sender number
3. Go to "Manual SMS" tab to send messages
4. Select customer group or individual customer
5. Choose template or write custom message
6. Send SMS manually

Important Notes:
- SMS provider must be properly configured before sending
- All SMS require explicit user action
- No automatic scheduling or background sending
- Check SMS history to track sent messages
""")
        info_text.configure(state='disabled')
        
        # Manual campaign buttons
        actions_frame = GlassFrame(tab)
        actions_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(actions_frame, text="Quick Campaign Actions:", font=FONTS['subheading']).pack(pady=10)
        
        GlassLabel(
            actions_frame,
            text="Use these buttons to find and send campaign SMS to specific groups",
            font=FONTS['small']
        ).pack(pady=5)
        
        def send_birthday_campaigns():
            from datetime import datetime
            from sms_service import sms_service
            
            # Check if SMS is configured
            if not sms_service.is_configured():
                messagebox.showerror(
                    "SMS Not Configured",
                    "SMS API is not configured. Please go to Settings > SMS Configuration first."
                )
                return
            
            now = datetime.now()
            today_birthday = f"%-{now.month:02d}-{now.day:02d}"
            birthdays = db.fetchall(
                """SELECT * FROM customers 
                   WHERE birthdate LIKE ?""",
                (today_birthday,)
            )
            
            if not birthdays:
                messagebox.showinfo("Info", "No birthdays today")
                return
            
            if messagebox.askyesno("Confirm", f"Send birthday SMS to {len(birthdays)} customers?"):
                sent = 0
                for customer in birthdays:
                    result = sms_service.send_birthday_sms(customer['id'])
                    if result and result.get('success'):
                        sent += 1
                messagebox.showinfo("Complete", f"Birthday SMS sent to {sent} customers")
                self.refresh_history()
        
        def send_reactivation_campaigns():
            from datetime import datetime, timedelta
            from sms_service import sms_service
            
            # Check if SMS is configured
            if not sms_service.is_configured():
                messagebox.showerror(
                    "SMS Not Configured",
                    "SMS API is not configured. Please go to Settings > SMS Configuration first."
                )
                return
            
            thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            inactive = db.fetchall(
                """SELECT * FROM customers 
                   WHERE last_visit_date < ?""",
                (thirty_days_ago,)
            )
            
            if not inactive:
                messagebox.showinfo("Info", "No inactive customers found")
                return
            
            if messagebox.askyesno("Confirm", f"Send reactivation SMS to {len(inactive)} customers?"):
                sent = 0
                for customer in inactive:
                    result = sms_service.send_inactive_customer_sms(customer['id'])
                    if result and result.get('success'):
                        sent += 1
                messagebox.showinfo("Complete", f"Reactivation SMS sent to {sent} customers")
                self.refresh_history()
        
        GlassButton(
            actions_frame,
            text="Send Birthday SMS (Today's Birthdays)",
            command=send_birthday_campaigns,
            width=300,
            fg_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassButton(
            actions_frame,
            text="Send Reactivation SMS (Inactive 30+ Days)",
            command=send_reactivation_campaigns,
            width=300,
            fg_color=COLORS['warning']
        ).pack(pady=5)
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
