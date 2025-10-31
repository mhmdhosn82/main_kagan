"""
Reports and Analytics Section Module
Handles overall business reports, charts, and statistics
"""
import customtkinter as ctk
from datetime import datetime, timedelta
from ui_utils import *
from database import db

class ReportsSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the reports section UI"""
        # Header
        header = create_section_header(self.frame, "Reports & Analytics")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Sales Reports")
        self.tabview.add("Section Performance")
        self.tabview.add("Overall Stats")
        
        self.setup_sales_tab()
        self.setup_performance_tab()
        self.setup_stats_tab()
    
    def setup_sales_tab(self):
        """Setup sales reports interface"""
        tab = self.tabview.tab("Sales Reports")
        
        # Report options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Sales Reports", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(options_frame, text="Daily Sales", 
                   command=self.show_daily_sales).pack(pady=5)
        GlassButton(options_frame, text="Weekly Sales", 
                   command=self.show_weekly_sales).pack(pady=5)
        GlassButton(options_frame, text="Monthly Sales", 
                   command=self.show_monthly_sales).pack(pady=5)
        
        # Report display
        report_frame = GlassFrame(tab)
        report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.sales_text = ctk.CTkTextbox(
            report_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.sales_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_performance_tab(self):
        """Setup section performance interface"""
        tab = self.tabview.tab("Section Performance")
        
        # Report options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Section Performance", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(options_frame, text="Salon Performance", 
                   command=self.show_salon_performance).pack(pady=5)
        GlassButton(options_frame, text="Cafe Performance", 
                   command=self.show_cafe_performance).pack(pady=5)
        GlassButton(options_frame, text="Gamnet Performance", 
                   command=self.show_gamnet_performance).pack(pady=5)
        GlassButton(options_frame, text="Compare Sections", 
                   command=self.compare_sections).pack(pady=5)
        
        # Report display
        report_frame = GlassFrame(tab)
        report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.performance_text = ctk.CTkTextbox(
            report_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.performance_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_stats_tab(self):
        """Setup overall statistics interface"""
        tab = self.tabview.tab("Overall Stats")
        
        # Report options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Overall Statistics", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(options_frame, text="Today's Overview", 
                   command=self.show_today_overview).pack(pady=5)
        GlassButton(options_frame, text="Customer Statistics", 
                   command=self.show_customer_stats).pack(pady=5)
        GlassButton(options_frame, text="Employee Performance", 
                   command=self.show_employee_performance).pack(pady=5)
        
        # Report display
        report_frame = GlassFrame(tab)
        report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = ctk.CTkTextbox(
            report_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.stats_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def show_daily_sales(self):
        """Show daily sales report"""
        self.sales_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        
        invoices = db.fetchall(
            """SELECT COUNT(*) as count, 
                      SUM(final_amount) as revenue,
                      AVG(final_amount) as avg_invoice
               FROM invoices
               WHERE DATE(invoice_date) = ? AND is_paid = 1""",
            (today,)
        )
        
        self.sales_text.insert('end', f"Daily Sales Report - {today}\n\n")
        
        if invoices and invoices[0]['count']:
            self.sales_text.insert('end', f"Total Invoices: {invoices[0]['count']}\n")
            self.sales_text.insert('end', f"Total Revenue: ${invoices[0]['revenue']:.2f}\n")
            self.sales_text.insert('end', f"Average Invoice: ${invoices[0]['avg_invoice']:.2f}\n")
        else:
            self.sales_text.insert('end', "No sales data for today.\n")
    
    def show_weekly_sales(self):
        """Show weekly sales report"""
        self.sales_text.delete('1.0', 'end')
        
        # Last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        invoices = db.fetchall(
            """SELECT COUNT(*) as count, 
                      SUM(final_amount) as revenue
               FROM invoices
               WHERE DATE(invoice_date) BETWEEN ? AND ? AND is_paid = 1""",
            (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        )
        
        self.sales_text.insert('end', f"Weekly Sales Report\n")
        self.sales_text.insert('end', f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n\n")
        
        if invoices and invoices[0]['count']:
            self.sales_text.insert('end', f"Total Invoices: {invoices[0]['count']}\n")
            self.sales_text.insert('end', f"Total Revenue: ${invoices[0]['revenue']:.2f}\n")
            self.sales_text.insert('end', f"Daily Average: ${invoices[0]['revenue'] / 7:.2f}\n")
        else:
            self.sales_text.insert('end', "No sales data for this week.\n")
    
    def show_monthly_sales(self):
        """Show monthly sales report"""
        self.sales_text.delete('1.0', 'end')
        
        # Current month
        now = datetime.now()
        start_date = now.replace(day=1)
        
        invoices = db.fetchall(
            """SELECT COUNT(*) as count, 
                      SUM(final_amount) as revenue
               FROM invoices
               WHERE DATE(invoice_date) >= ? AND is_paid = 1""",
            (start_date.strftime('%Y-%m-%d'),)
        )
        
        self.sales_text.insert('end', f"Monthly Sales Report - {now.strftime('%B %Y')}\n\n")
        
        if invoices and invoices[0]['count']:
            self.sales_text.insert('end', f"Total Invoices: {invoices[0]['count']}\n")
            self.sales_text.insert('end', f"Total Revenue: ${invoices[0]['revenue']:.2f}\n")
        else:
            self.sales_text.insert('end', "No sales data for this month.\n")
    
    def show_salon_performance(self):
        """Show salon section performance"""
        self.performance_text.delete('1.0', 'end')
        
        # Get salon statistics
        services = db.fetchall(
            """SELECT COUNT(*) as count, SUM(price) as revenue
               FROM salon_service_records
               WHERE DATE(service_date) >= date('now', '-30 days')"""
        )
        
        self.performance_text.insert('end', "Salon Performance (Last 30 Days)\n\n")
        
        if services and services[0]['count']:
            self.performance_text.insert('end', f"Services Performed: {services[0]['count']}\n")
            self.performance_text.insert('end', f"Revenue: ${services[0]['revenue']:.2f}\n")
            
            # Top stylists
            stylists = db.fetchall(
                """SELECT e.name, COUNT(*) as services, SUM(s.price) as revenue
                   FROM salon_service_records s
                   JOIN employees e ON s.stylist_id = e.id
                   WHERE DATE(s.service_date) >= date('now', '-30 days')
                   GROUP BY s.stylist_id
                   ORDER BY revenue DESC
                   LIMIT 5"""
            )
            
            self.performance_text.insert('end', "\nTop Stylists:\n")
            for stylist in stylists:
                self.performance_text.insert('end',
                    f"  {stylist['name']}: {stylist['services']} services, ${stylist['revenue']:.2f}\n"
                )
    
    def show_cafe_performance(self):
        """Show cafe section performance"""
        self.performance_text.delete('1.0', 'end')
        
        # Get cafe statistics
        orders = db.fetchall(
            """SELECT COUNT(*) as count, SUM(total_amount) as revenue
               FROM cafe_orders
               WHERE DATE(order_date) >= date('now', '-30 days')"""
        )
        
        self.performance_text.insert('end', "Cafe Performance (Last 30 Days)\n\n")
        
        if orders and orders[0]['count']:
            self.performance_text.insert('end', f"Orders: {orders[0]['count']}\n")
            self.performance_text.insert('end', f"Revenue: ${orders[0]['revenue']:.2f}\n")
            
            # Popular items
            items = db.fetchall(
                """SELECT m.name, SUM(oi.quantity) as sold, SUM(oi.price * oi.quantity) as revenue
                   FROM cafe_order_items oi
                   JOIN cafe_menu m ON oi.menu_item_id = m.id
                   JOIN cafe_orders o ON oi.order_id = o.id
                   WHERE DATE(o.order_date) >= date('now', '-30 days')
                   GROUP BY m.id
                   ORDER BY revenue DESC
                   LIMIT 5"""
            )
            
            self.performance_text.insert('end', "\nTop Items:\n")
            for item in items:
                self.performance_text.insert('end',
                    f"  {item['name']}: {item['sold']} sold, ${item['revenue']:.2f}\n"
                )
    
    def show_gamnet_performance(self):
        """Show gamnet section performance"""
        self.performance_text.delete('1.0', 'end')
        
        # Get gamnet statistics
        sessions = db.fetchall(
            """SELECT COUNT(*) as count, SUM(charge) as revenue, SUM(duration_minutes) as total_minutes
               FROM gamnet_sessions
               WHERE DATE(start_time) >= date('now', '-30 days') AND end_time IS NOT NULL"""
        )
        
        self.performance_text.insert('end', "Gamnet Performance (Last 30 Days)\n\n")
        
        if sessions and sessions[0]['count']:
            self.performance_text.insert('end', f"Sessions: {sessions[0]['count']}\n")
            self.performance_text.insert('end', f"Revenue: ${sessions[0]['revenue']:.2f}\n")
            self.performance_text.insert('end', f"Total Gaming Time: {sessions[0]['total_minutes']} minutes\n")
    
    def compare_sections(self):
        """Compare performance across all sections"""
        self.performance_text.delete('1.0', 'end')
        self.performance_text.insert('end', "Section Comparison (Last 30 Days)\n\n")
        
        # Salon
        salon = db.fetchone(
            """SELECT SUM(price) as revenue FROM salon_service_records
               WHERE DATE(service_date) >= date('now', '-30 days')"""
        )
        salon_rev = salon['revenue'] or 0
        
        # Cafe
        cafe = db.fetchone(
            """SELECT SUM(total_amount) as revenue FROM cafe_orders
               WHERE DATE(order_date) >= date('now', '-30 days')"""
        )
        cafe_rev = cafe['revenue'] or 0
        
        # Gamnet
        gamnet = db.fetchone(
            """SELECT SUM(charge) as revenue FROM gamnet_sessions
               WHERE DATE(start_time) >= date('now', '-30 days') AND end_time IS NOT NULL"""
        )
        gamnet_rev = gamnet['revenue'] or 0
        
        total = salon_rev + cafe_rev + gamnet_rev
        
        self.performance_text.insert('end', f"Salon: ${salon_rev:.2f} ({salon_rev/total*100 if total > 0 else 0:.1f}%)\n")
        self.performance_text.insert('end', f"Cafe: ${cafe_rev:.2f} ({cafe_rev/total*100 if total > 0 else 0:.1f}%)\n")
        self.performance_text.insert('end', f"Gamnet: ${gamnet_rev:.2f} ({gamnet_rev/total*100 if total > 0 else 0:.1f}%)\n")
        self.performance_text.insert('end', f"\nTotal Revenue: ${total:.2f}\n")
    
    def show_today_overview(self):
        """Show today's overview"""
        self.stats_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        
        self.stats_text.insert('end', f"Today's Overview - {today}\n\n")
        
        # Customers
        customers = db.fetchone(
            """SELECT COUNT(DISTINCT customer_id) as count FROM invoices
               WHERE DATE(invoice_date) = ?""",
            (today,)
        )
        self.stats_text.insert('end', f"Customers Served: {customers['count'] or 0}\n")
        
        # Appointments
        appointments = db.fetchone(
            """SELECT COUNT(*) as count FROM salon_appointments
               WHERE appointment_date = ?""",
            (today,)
        )
        self.stats_text.insert('end', f"Salon Appointments: {appointments['count'] or 0}\n")
        
        # Active gaming sessions
        active_sessions = db.fetchone(
            """SELECT COUNT(*) as count FROM gamnet_sessions
               WHERE DATE(start_time) = ? AND end_time IS NULL""",
            (today,)
        )
        self.stats_text.insert('end', f"Active Gaming Sessions: {active_sessions['count'] or 0}\n")
        
        # Revenue
        revenue = db.fetchone(
            """SELECT SUM(final_amount) as total FROM invoices
               WHERE DATE(invoice_date) = ? AND is_paid = 1""",
            (today,)
        )
        self.stats_text.insert('end', f"\nTotal Revenue: ${revenue['total'] or 0:.2f}\n")
    
    def show_customer_stats(self):
        """Show customer statistics"""
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('end', "Customer Statistics\n\n")
        
        # Total customers
        total = db.fetchone("SELECT COUNT(*) as count FROM customers")
        self.stats_text.insert('end', f"Total Customers: {total['count']}\n")
        
        # Active customers (visited in last 30 days)
        active = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE last_visit_date IS NOT NULL
               AND julianday('now') - julianday(last_visit_date) <= 30"""
        )
        self.stats_text.insert('end', f"Active (30 days): {active['count']}\n")
        
        # New customers this month
        now = datetime.now()
        new = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE DATE(registration_date) >= ?""",
            (now.replace(day=1).strftime('%Y-%m-%d'),)
        )
        self.stats_text.insert('end', f"New This Month: {new['count']}\n")
        
        # Top spending customers
        top = db.fetchall(
            """SELECT name, phone, total_spent FROM customers
               ORDER BY total_spent DESC
               LIMIT 10"""
        )
        
        self.stats_text.insert('end', "\nTop Customers:\n")
        for customer in top:
            self.stats_text.insert('end',
                f"  {customer['name']} ({customer['phone']}): ${customer['total_spent']:.2f}\n"
            )
    
    def show_employee_performance(self):
        """Show employee performance overview"""
        self.stats_text.delete('1.0', 'end')
        self.stats_text.insert('end', "Employee Performance Overview\n\n")
        
        # Top performing employees by commissions
        employees = db.fetchall(
            """SELECT e.name, e.section, SUM(c.amount) as total_commissions
               FROM employees e
               LEFT JOIN employee_commissions c ON e.id = c.employee_id
               WHERE e.is_active = 1
               GROUP BY e.id
               ORDER BY total_commissions DESC
               LIMIT 10"""
        )
        
        for emp in employees:
            commissions = emp['total_commissions'] or 0
            self.stats_text.insert('end',
                f"{emp['name']} ({emp['section']}): ${commissions:.2f} in commissions\n"
            )
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
