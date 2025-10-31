"""
Cafe Bar Section Module
Handles menu management, orders, bill splitting, and sales reports
"""
import customtkinter as ctk
from datetime import datetime
from ui_utils import *
from database import db

class CafeSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.current_order_items = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the cafe section UI"""
        # Header
        header = create_section_header(self.frame, "Cafe Bar Management")
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Menu")
        self.tabview.add("Orders")
        self.tabview.add("Reports")
        
        self.setup_menu_tab()
        self.setup_orders_tab()
        self.setup_reports_tab()
    
    def setup_menu_tab(self):
        """Setup menu management interface"""
        tab = self.tabview.tab("Menu")
        
        # Add menu item form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Add Menu Item", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Item Name:").pack(pady=5)
        self.item_name_entry = GlassEntry(form_frame, width=300)
        self.item_name_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Category:").pack(pady=5)
        self.category_var = ctk.StringVar(value="Drinks")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.category_var,
            values=["Drinks", "Food", "Desserts", "Snacks"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Price:").pack(pady=5)
        self.item_price_entry = GlassEntry(form_frame, width=300)
        self.item_price_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Description:").pack(pady=5)
        self.item_description_entry = GlassEntry(form_frame, width=300)
        self.item_description_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Add Item", command=self.add_menu_item).pack(pady=20)
        
        # Menu list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="Current Menu", font=FONTS['subheading']).pack(pady=10)
        
        self.menu_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.menu_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_menu()
    
    def setup_orders_tab(self):
        """Setup orders management interface"""
        tab = self.tabview.tab("Orders")
        
        # Create order form
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text="Create Order", font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text="Customer Phone:").pack(pady=5)
        self.order_customer_entry = GlassEntry(form_frame, width=300)
        self.order_customer_entry.pack(pady=5)
        
        GlassLabel(form_frame, text="Barista:").pack(pady=5)
        self.barista_var = ctk.StringVar(value="Select Barista")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.barista_var,
            values=self.get_baristas(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Menu Item:").pack(pady=5)
        self.menu_item_var = ctk.StringVar(value="Select Item")
        ctk.CTkOptionMenu(
            form_frame,
            variable=self.menu_item_var,
            values=self.get_menu_items(),
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        ).pack(pady=5)
        
        GlassLabel(form_frame, text="Quantity:").pack(pady=5)
        self.quantity_entry = GlassEntry(form_frame, width=300)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Add to Order", command=self.add_to_order).pack(pady=10)
        
        GlassLabel(form_frame, text="Split Bill Among (people):").pack(pady=5)
        self.split_entry = GlassEntry(form_frame, width=300)
        self.split_entry.insert(0, "1")
        self.split_entry.pack(pady=5)
        
        GlassButton(form_frame, text="Complete Order", command=self.complete_order, 
                   fg_color=COLORS['success']).pack(pady=20)
        
        # Current order display
        order_frame = GlassFrame(tab)
        order_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(order_frame, text="Current Order", font=FONTS['subheading']).pack(pady=10)
        
        self.current_order_text = ctk.CTkTextbox(
            order_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text'],
            height=200
        )
        self.current_order_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_reports_tab(self):
        """Setup sales reports interface"""
        tab = self.tabview.tab("Reports")
        
        # Report options
        options_frame = GlassFrame(tab)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(options_frame, text="Sales Reports", font=FONTS['heading']).pack(pady=10)
        
        GlassButton(options_frame, text="Daily Sales Report", 
                   command=self.show_daily_sales).pack(pady=5)
        GlassButton(options_frame, text="Popular Items", 
                   command=self.show_popular_items).pack(pady=5)
        
        # Report display
        report_frame = GlassFrame(tab)
        report_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.report_text = ctk.CTkTextbox(
            report_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def get_baristas(self):
        """Get list of baristas from database"""
        baristas = db.fetchall("SELECT id, name FROM employees WHERE section = 'Cafe' AND is_active = 1")
        if baristas:
            return [f"{b['id']}: {b['name']}" for b in baristas]
        return ["No baristas available"]
    
    def get_menu_items(self):
        """Get list of menu items from database"""
        items = db.fetchall("SELECT id, name, price FROM cafe_menu WHERE is_available = 1")
        if items:
            return [f"{i['id']}: {i['name']} (${i['price']})" for i in items]
        return ["No items available"]
    
    def add_menu_item(self):
        """Add a new menu item"""
        name = self.item_name_entry.get()
        category = self.category_var.get()
        price = float(self.item_price_entry.get())
        description = self.item_description_entry.get()
        
        db.execute(
            """INSERT INTO cafe_menu (name, category, price, description)
               VALUES (?, ?, ?, ?)""",
            (name, category, price, description)
        )
        
        self.refresh_menu()
        
        # Clear form
        self.item_name_entry.delete(0, 'end')
        self.item_price_entry.delete(0, 'end')
        self.item_description_entry.delete(0, 'end')
    
    def add_to_order(self):
        """Add item to current order"""
        item_text = self.menu_item_var.get()
        if ':' not in item_text:
            return
        
        item_id = int(item_text.split(':')[0])
        quantity = int(self.quantity_entry.get())
        
        # Get item details
        item = db.fetchone("SELECT name, price FROM cafe_menu WHERE id = ?", (item_id,))
        
        self.current_order_items.append({
            'id': item_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': quantity
        })
        
        self.refresh_current_order()
    
    def complete_order(self):
        """Complete and save the order"""
        if not self.current_order_items:
            return
        
        phone = self.order_customer_entry.get()
        
        # Get or create customer
        customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        if not customer:
            db.execute(
                "INSERT INTO customers (name, phone, registration_date) VALUES (?, ?, ?)",
                (f"Customer {phone}", phone, datetime.now().strftime('%Y-%m-%d'))
            )
            customer = db.fetchone("SELECT id FROM customers WHERE phone = ?", (phone,))
        
        # Get barista ID
        barista_text = self.barista_var.get()
        if ':' in barista_text:
            barista_id = int(barista_text.split(':')[0])
        else:
            barista_id = None
        
        # Calculate total
        total = sum(item['price'] * item['quantity'] for item in self.current_order_items)
        split_count = int(self.split_entry.get())
        
        # Create order
        db.execute(
            """INSERT INTO cafe_orders (customer_id, barista_id, order_date, total_amount, split_count)
               VALUES (?, ?, ?, ?, ?)""",
            (customer['id'], barista_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total, split_count)
        )
        
        order_id = db.fetchone("SELECT last_insert_rowid() as id")['id']
        
        # Add order items
        for item in self.current_order_items:
            db.execute(
                """INSERT INTO cafe_order_items (order_id, menu_item_id, quantity, price)
                   VALUES (?, ?, ?, ?)""",
                (order_id, item['id'], item['quantity'], item['price'])
            )
        
        # Clear current order
        self.current_order_items = []
        self.refresh_current_order()
        self.order_customer_entry.delete(0, 'end')
    
    def refresh_current_order(self):
        """Refresh current order display"""
        self.current_order_text.delete('1.0', 'end')
        total = 0
        for item in self.current_order_items:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            self.current_order_text.insert('end',
                f"{item['name']} x{item['quantity']} = ${subtotal:.2f}\n"
            )
        self.current_order_text.insert('end', f"\nTotal: ${total:.2f}")
    
    def refresh_menu(self):
        """Refresh menu display"""
        self.menu_text.delete('1.0', 'end')
        items = db.fetchall("SELECT * FROM cafe_menu ORDER BY category, name")
        
        current_category = None
        for item in items:
            if item['category'] != current_category:
                current_category = item['category']
                self.menu_text.insert('end', f"\n=== {current_category} ===\n")
            
            self.menu_text.insert('end',
                f"{item['name']} - ${item['price']}\n  {item['description']}\n"
            )
    
    def show_daily_sales(self):
        """Show daily sales report"""
        self.report_text.delete('1.0', 'end')
        today = datetime.now().strftime('%Y-%m-%d')
        
        orders = db.fetchall(
            """SELECT SUM(total_amount) as total, COUNT(*) as count
               FROM cafe_orders
               WHERE DATE(order_date) = ?""",
            (today,)
        )
        
        if orders and orders[0]['total']:
            self.report_text.insert('end', f"Daily Sales Report for {today}\n\n")
            self.report_text.insert('end', f"Total Orders: {orders[0]['count']}\n")
            self.report_text.insert('end', f"Total Revenue: ${orders[0]['total']:.2f}\n")
        else:
            self.report_text.insert('end', "No sales today yet.")
    
    def show_popular_items(self):
        """Show popular items report"""
        self.report_text.delete('1.0', 'end')
        
        items = db.fetchall(
            """SELECT m.name, SUM(oi.quantity) as total_sold, SUM(oi.price * oi.quantity) as revenue
               FROM cafe_order_items oi
               JOIN cafe_menu m ON oi.menu_item_id = m.id
               GROUP BY m.id
               ORDER BY total_sold DESC
               LIMIT 10"""
        )
        
        self.report_text.insert('end', "Top 10 Popular Items\n\n")
        for item in items:
            self.report_text.insert('end',
                f"{item['name']}: {item['total_sold']} sold, ${item['revenue']:.2f} revenue\n"
            )
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
