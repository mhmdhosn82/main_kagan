"""
Reports and Analytics Section Module
Handles overall business reports, charts, and statistics with Persian calendar support
"""
import customtkinter as ctk
from datetime import datetime, timedelta
from ui_utils import *
from database import db
from translations import tr
try:
    import jdatetime
    JALALI_SUPPORT = True
except ImportError:
    JALALI_SUPPORT = False

class ReportsSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the reports section UI"""
        # Header
        header = create_section_header(self.frame, tr('reports_analytics'))
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add(tr('sales_reports'))
        self.tabview.add(tr('section_performance'))
        self.tabview.add(tr('overall_stats'))
        self.tabview.add("Advanced Analytics")
        
        self.setup_sales_tab()
        self.setup_performance_tab()
        self.setup_stats_tab()
        self.setup_advanced_tab()
    
    def setup_sales_tab(self):
        """Setup sales reports interface"""
        tab = self.tabview.tab(tr('sales_reports'))
        
        # Date range filter
        filter_frame = GlassFrame(tab)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(filter_frame, text="Time Period:", font=FONTS['subheading']).pack(pady=5)
        
        period_var = ctk.StringVar(value="daily")
        periods = [
            ("Daily", "daily"),
            ("Weekly", "weekly"),
            ("Monthly", "monthly"),
            ("Quarterly", "quarterly"),
            ("Yearly", "yearly"),
            ("Custom Range", "custom")
        ]
        
        for text, value in periods:
            ctk.CTkRadioButton(
                filter_frame,
                text=text,
                variable=period_var,
                value=value
            ).pack(pady=2, padx=20, anchor='w')
        
        # Custom date range
        date_frame = GlassFrame(filter_frame)
        date_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(date_frame, text="From:").pack(side='left', padx=5)
        from_date_entry = GlassEntry(date_frame, width=120)
        from_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        from_date_entry.pack(side='left', padx=5)
        
        GlassLabel(date_frame, text="To:").pack(side='left', padx=5)
        to_date_entry = GlassEntry(date_frame, width=120)
        to_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        to_date_entry.pack(side='left', padx=5)
        
        # Calendar type toggle
        if JALALI_SUPPORT:
            calendar_var = ctk.BooleanVar(value=True)
            calendar_check = ctk.CTkCheckBox(
                filter_frame,
                text="Use Persian Calendar (Jalali)",
                variable=calendar_var
            )
            calendar_check.pack(pady=5)
        
        # Generate button
        def generate_report():
            period = period_var.get()
            if period == "custom":
                start_date = from_date_entry.get()
                end_date = to_date_entry.get()
            else:
                start_date, end_date = self.get_date_range_for_period(period)
            
            self.show_sales_report(start_date, end_date, period)
        
        GlassButton(
            filter_frame,
            text="Generate Report",
            command=generate_report,
            fg_color=COLORS['success']
        ).pack(pady=10)
        
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
    
    def get_date_range_for_period(self, period):
        """Get start and end dates for a period"""
        today = datetime.now()
        
        if period == "daily":
            start = today.strftime('%Y-%m-%d')
            end = today.strftime('%Y-%m-%d')
        elif period == "weekly":
            start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')
            end = today.strftime('%Y-%m-%d')
        elif period == "monthly":
            start = today.replace(day=1).strftime('%Y-%m-%d')
            end = today.strftime('%Y-%m-%d')
        elif period == "quarterly":
            quarter = (today.month - 1) // 3
            start = today.replace(month=quarter*3+1, day=1).strftime('%Y-%m-%d')
            end = today.strftime('%Y-%m-%d')
        elif period == "yearly":
            start = today.replace(month=1, day=1).strftime('%Y-%m-%d')
            end = today.strftime('%Y-%m-%d')
        else:
            start = end = today.strftime('%Y-%m-%d')
        
        return start, end
    
    def show_sales_report(self, start_date, end_date, period_type):
        """Show sales report for date range"""
        self.sales_text.delete('1.0', 'end')
        
        # Header
        self.sales_text.insert('end', f"Sales Report ({period_type})\n")
        self.sales_text.insert('end', f"Period: {start_date} to {end_date}\n")
        self.sales_text.insert('end', "=" * 80 + "\n\n")
        
        # Total revenue
        revenue = db.fetchone(
            """SELECT SUM(final_amount) as total, COUNT(*) as count
               FROM invoices
               WHERE DATE(invoice_date) BETWEEN ? AND ? AND is_paid = 1""",
            (start_date, end_date)
        )
        
        total_revenue = revenue['total'] or 0
        invoice_count = revenue['count'] or 0
        
        self.sales_text.insert('end', f"Total Revenue: ${total_revenue:.2f}\n")
        self.sales_text.insert('end', f"Total Invoices: {invoice_count}\n")
        self.sales_text.insert('end', f"Average Invoice: ${(total_revenue/invoice_count if invoice_count > 0 else 0):.2f}\n\n")
        
        # Revenue by section (estimated from services/orders)
        self.sales_text.insert('end', "Revenue Breakdown by Section:\n")
        self.sales_text.insert('end', "-" * 40 + "\n")
        
        # Salon revenue
        salon_revenue = db.fetchone(
            """SELECT SUM(price) as total FROM salon_service_records
               WHERE DATE(service_date) BETWEEN ? AND ?""",
            (start_date, end_date)
        )
        salon_total = salon_revenue['total'] or 0
        self.sales_text.insert('end', f"Salon: ${salon_total:.2f}\n")
        
        # Cafe revenue
        cafe_revenue = db.fetchone(
            """SELECT SUM(total_amount) as total FROM cafe_orders
               WHERE DATE(order_date) BETWEEN ? AND ?""",
            (start_date, end_date)
        )
        cafe_total = cafe_revenue['total'] or 0
        self.sales_text.insert('end', f"Cafe: ${cafe_total:.2f}\n")
        
        # Gamnet revenue
        gamnet_revenue = db.fetchone(
            """SELECT SUM(charge) as total FROM gamnet_sessions
               WHERE DATE(start_time) BETWEEN ? AND ? AND end_time IS NOT NULL""",
            (start_date, end_date)
        )
        gamnet_total = gamnet_revenue['total'] or 0
        self.sales_text.insert('end', f"Gamnet: ${gamnet_total:.2f}\n\n")
        
        # Payment methods
        self.sales_text.insert('end', "Payment Methods:\n")
        self.sales_text.insert('end', "-" * 40 + "\n")
        
        payments = db.fetchall(
            """SELECT payment_method, SUM(final_amount) as total, COUNT(*) as count
               FROM invoices
               WHERE DATE(invoice_date) BETWEEN ? AND ? AND is_paid = 1
               GROUP BY payment_method""",
            (start_date, end_date)
        )
        
        for payment in payments:
            method = payment['payment_method'] or 'Unknown'
            self.sales_text.insert('end', 
                f"{method}: ${payment['total']:.2f} ({payment['count']} transactions)\n"
            )
        
        # Top services/products
        self.sales_text.insert('end', "\nTop Services:\n")
        self.sales_text.insert('end', "-" * 40 + "\n")
        
        top_services = db.fetchall(
            """SELECT s.name, COUNT(*) as count, SUM(sr.price) as revenue
               FROM salon_service_records sr
               JOIN salon_services s ON sr.service_id = s.id
               WHERE DATE(sr.service_date) BETWEEN ? AND ?
               GROUP BY sr.service_id
               ORDER BY revenue DESC
               LIMIT 5""",
            (start_date, end_date)
        )
        
        for service in top_services:
            self.sales_text.insert('end',
                f"{service['name']}: {service['count']} services, ${service['revenue']:.2f}\n"
            )
    
    def setup_advanced_tab(self):
        """Setup advanced analytics tab"""
        tab = self.tabview.tab("Advanced Analytics")
        
        info_frame = GlassFrame(tab)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(info_frame, text="Advanced Analytics", font=FONTS['heading']).pack(pady=10)
        
        # Buttons for different analytics
        GlassButton(
            info_frame,
            text="Customer Analytics & Segmentation",
            command=self.show_customer_analytics,
            width=300
        ).pack(pady=5)
        
        GlassButton(
            info_frame,
            text="Profit & Loss Statement",
            command=self.show_profit_loss,
            width=300
        ).pack(pady=5)
        
        GlassButton(
            info_frame,
            text="Employee Performance Report",
            command=self.show_detailed_employee_performance,
            width=300
        ).pack(pady=5)
        
        GlassButton(
            info_frame,
            text="Inventory Status & Alerts",
            command=self.show_inventory_status,
            width=300
        ).pack(pady=5)
        
        # Analytics display
        self.analytics_text = ctk.CTkTextbox(
            info_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.analytics_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def show_customer_analytics(self):
        """Show detailed customer analytics"""
        self.analytics_text.delete('1.0', 'end')
        self.analytics_text.insert('end', "Customer Analytics & Segmentation\n")
        self.analytics_text.insert('end', "=" * 80 + "\n\n")
        
        # Total customers
        total = db.fetchone("SELECT COUNT(*) as count FROM customers")
        self.analytics_text.insert('end', f"Total Customers: {total['count']}\n\n")
        
        # Customer segments
        self.analytics_text.insert('end', "Customer Segmentation:\n")
        self.analytics_text.insert('end', "-" * 40 + "\n")
        
        # VIP customers (top 10% by spending)
        vip_count = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE total_spent > (SELECT AVG(total_spent) * 2 FROM customers)"""
        )
        self.analytics_text.insert('end', f"VIP Customers (high spenders): {vip_count['count']}\n")
        
        # Regular customers
        regular = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE last_visit_date IS NOT NULL
               AND julianday('now') - julianday(last_visit_date) <= 30"""
        )
        self.analytics_text.insert('end', f"Regular Customers (active): {regular['count']}\n")
        
        # At-risk customers
        at_risk = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE last_visit_date IS NOT NULL
               AND julianday('now') - julianday(last_visit_date) BETWEEN 30 AND 90"""
        )
        self.analytics_text.insert('end', f"At-Risk Customers (30-90 days inactive): {at_risk['count']}\n")
        
        # Lost customers
        lost = db.fetchone(
            """SELECT COUNT(*) as count FROM customers
               WHERE last_visit_date IS NOT NULL
               AND julianday('now') - julianday(last_visit_date) > 90"""
        )
        self.analytics_text.insert('end', f"Lost Customers (90+ days inactive): {lost['count']}\n\n")
        
        # Customer lifetime value
        avg_ltv = db.fetchone("SELECT AVG(total_spent) as avg FROM customers")
        self.analytics_text.insert('end', f"Average Customer Lifetime Value: ${avg_ltv['avg'] or 0:.2f}\n")
    
    def show_profit_loss(self):
        """Show profit and loss statement"""
        self.analytics_text.delete('1.0', 'end')
        self.analytics_text.insert('end', "Profit & Loss Statement (Current Month)\n")
        self.analytics_text.insert('end', "=" * 80 + "\n\n")
        
        # Get current month dates
        today = datetime.now()
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        
        # Revenue
        revenue = db.fetchone(
            """SELECT SUM(final_amount) as total FROM invoices
               WHERE DATE(invoice_date) BETWEEN ? AND ? AND is_paid = 1""",
            (start_date, end_date)
        )
        total_revenue = revenue['total'] or 0
        
        self.analytics_text.insert('end', "REVENUE:\n")
        self.analytics_text.insert('end', f"  Total Revenue: ${total_revenue:.2f}\n\n")
        
        # Expenses
        expenses = db.fetchall(
            """SELECT category, SUM(amount) as total FROM expenses
               WHERE DATE(expense_date) BETWEEN ? AND ?
               GROUP BY category""",
            (start_date, end_date)
        )
        
        self.analytics_text.insert('end', "EXPENSES:\n")
        total_expenses = 0
        for expense in expenses:
            amount = expense['total'] or 0
            total_expenses += amount
            self.analytics_text.insert('end', f"  {expense['category']}: ${amount:.2f}\n")
        
        self.analytics_text.insert('end', f"\n  Total Expenses: ${total_expenses:.2f}\n\n")
        
        # Profit/Loss
        profit_loss = total_revenue - total_expenses
        self.analytics_text.insert('end', "=" * 40 + "\n")
        self.analytics_text.insert('end', f"NET {'PROFIT' if profit_loss >= 0 else 'LOSS'}: ${abs(profit_loss):.2f}\n")
        
        if total_revenue > 0:
            margin = (profit_loss / total_revenue) * 100
            self.analytics_text.insert('end', f"Profit Margin: {margin:.1f}%\n")
    
    def show_detailed_employee_performance(self):
        """Show detailed employee performance"""
        self.analytics_text.delete('1.0', 'end')
        self.analytics_text.insert('end', "Employee Performance Report\n")
        self.analytics_text.insert('end', "=" * 80 + "\n\n")
        
        employees = db.fetchall(
            """SELECT e.*, 
                   (SELECT COUNT(*) FROM salon_service_records WHERE stylist_id = e.id) as service_count,
                   (SELECT SUM(amount) FROM employee_commissions WHERE employee_id = e.id) as total_commissions
               FROM employees e
               WHERE e.is_active = 1
               ORDER BY total_commissions DESC"""
        )
        
        for emp in employees:
            self.analytics_text.insert('end', f"\n{emp['name']} - {emp['role']} ({emp['section']})\n")
            self.analytics_text.insert('end', "-" * 40 + "\n")
            self.analytics_text.insert('end', f"  Services Performed: {emp['service_count'] or 0}\n")
            self.analytics_text.insert('end', f"  Total Commissions: ${emp['total_commissions'] or 0:.2f}\n")
            self.analytics_text.insert('end', f"  Commission Rate: {emp['commission_rate']}%\n")
    
    def show_inventory_status(self):
        """Show inventory status and alerts"""
        self.analytics_text.delete('1.0', 'end')
        self.analytics_text.insert('end', "Inventory Status & Alerts\n")
        self.analytics_text.insert('end', "=" * 80 + "\n\n")
        
        # Low stock items
        low_stock = db.fetchall(
            """SELECT * FROM inventory_items
               WHERE quantity <= reorder_level
               ORDER BY (reorder_level - quantity) DESC"""
        )
        
        if low_stock:
            self.analytics_text.insert('end', f"⚠ {len(low_stock)} items need reordering:\n\n")
            for item in low_stock:
                shortage = (item['reorder_level'] or 0) - (item['quantity'] or 0)
                self.analytics_text.insert('end',
                    f"  {item['name']} ({item['section']}): {item['quantity']:.1f} {item['unit'] or 'units'} "
                    f"(shortage: {shortage:.1f})\n"
                )
        else:
            self.analytics_text.insert('end', "✓ All inventory levels are adequate.\n")
        
        # Total inventory value
        self.analytics_text.insert('end', "\n" + "=" * 40 + "\n")
        total_value = db.fetchone(
            "SELECT SUM(quantity * unit_cost) as total FROM inventory_items"
        )
        self.analytics_text.insert('end', 
            f"Total Inventory Value: ${total_value['total'] or 0:.2f}\n"
        )
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
