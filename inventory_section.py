"""
Inventory Management Section Module
Handles product inventory, stock levels, and alerts
"""
import customtkinter as ctk
from ui_utils import *
from database import db
from translations import tr
from tkinter import messagebox
from datetime import datetime

class InventorySection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the inventory section UI"""
        # Header
        header = create_section_header(self.frame, tr('inventory_management'))
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add(tr('products'))
        self.tabview.add(tr('low_stock_alerts'))
        self.tabview.add(tr('add_product'))
        
        self.setup_products_tab()
        self.setup_alerts_tab()
        self.setup_add_tab()
    
    def setup_products_tab(self):
        """Setup products listing"""
        tab = self.tabview.tab(tr('products'))
        
        # Filters
        filter_frame = GlassFrame(tab)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(filter_frame, text="Section:").pack(side='left', padx=5)
        
        section_var = ctk.StringVar(value="all")
        section_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=section_var,
            values=["all", "Salon", "Cafe", "Gamnet"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary'],
            command=lambda _: self.refresh_products(section_var.get())
        )
        section_menu.pack(side='left', padx=5)
        
        GlassButton(
            filter_frame,
            text=tr('refresh'),
            command=lambda: self.refresh_products(section_var.get()),
            width=100
        ).pack(side='left', padx=5)
        
        # Products display
        products_frame = GlassFrame(tab)
        products_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.products_text = ctk.CTkTextbox(
            products_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        self.products_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_products()
    
    def refresh_products(self, section="all"):
        """Refresh products display"""
        self.products_text.delete('1.0', 'end')
        
        if section == "all":
            products = db.fetchall(
                """SELECT i.*, s.name as supplier_name 
                   FROM inventory_items i
                   LEFT JOIN suppliers s ON i.supplier_id = s.id
                   ORDER BY i.section, i.name"""
            )
        else:
            products = db.fetchall(
                """SELECT i.*, s.name as supplier_name 
                   FROM inventory_items i
                   LEFT JOIN suppliers s ON i.supplier_id = s.id
                   WHERE i.section = ?
                   ORDER BY i.name""",
                (section,)
            )
        
        self.products_text.insert('end', 
            f"{'ID':<5} {'Name':<30} {'Section':<10} {'Qty':<10} {'Unit':<8} "
            f"{'Cost':<10} {'Price':<10} {'Reorder':<10}\n"
            f"{'-'*100}\n"
        )
        
        for product in products:
            qty = f"{product['quantity']:.1f}" if product['quantity'] else "0.0"
            cost = f"${product['unit_cost']:.2f}" if product['unit_cost'] else "$0.00"
            price = f"${product['selling_price']:.2f}" if product['selling_price'] else "$0.00"
            reorder = f"{product['reorder_level']:.1f}" if product['reorder_level'] else "N/A"
            
            # Warning if low stock
            warning = " ⚠ LOW STOCK" if (product['quantity'] or 0) <= (product['reorder_level'] or 0) else ""
            
            self.products_text.insert('end',
                f"{product['id']:<5} {product['name']:<30} {product['section']:<10} "
                f"{qty:<10} {product['unit'] or 'unit':<8} {cost:<10} {price:<10} {reorder:<10}{warning}\n"
            )
    
    def setup_alerts_tab(self):
        """Setup low stock alerts"""
        tab = self.tabview.tab(tr('low_stock_alerts'))
        
        alerts_frame = GlassFrame(tab)
        alerts_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(alerts_frame, text="Low Stock Items", font=FONTS['heading']).pack(pady=10)
        
        alerts_text = ctk.CTkTextbox(
            alerts_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text']
        )
        alerts_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Get low stock items
        low_stock = db.fetchall(
            """SELECT i.*, s.name as supplier_name 
               FROM inventory_items i
               LEFT JOIN suppliers s ON i.supplier_id = s.id
               WHERE i.quantity <= i.reorder_level
               ORDER BY (i.reorder_level - i.quantity) DESC"""
        )
        
        if not low_stock:
            alerts_text.insert('end', "No low stock alerts at this time.\n\n")
        else:
            alerts_text.insert('end', f"⚠ {len(low_stock)} items need reordering:\n\n")
            
            for item in low_stock:
                shortage = (item['reorder_level'] or 0) - (item['quantity'] or 0)
                alerts_text.insert('end',
                    f"Product: {item['name']}\n"
                    f"Section: {item['section']}\n"
                    f"Current Stock: {item['quantity']:.1f} {item['unit'] or 'units'}\n"
                    f"Reorder Level: {item['reorder_level']:.1f}\n"
                    f"Shortage: {shortage:.1f}\n"
                    f"Supplier: {item['supplier_name'] or 'Not specified'}\n"
                    f"{'-'*60}\n\n"
                )
    
    def setup_add_tab(self):
        """Setup add/edit product interface"""
        tab = self.tabview.tab(tr('add_product'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text=tr('add_product'), font=FONTS['heading']).pack(pady=10)
        
        # Product name
        GlassLabel(form_frame, text=tr('name')).pack(pady=2)
        name_entry = GlassEntry(form_frame, width=300)
        name_entry.pack(pady=2)
        
        # Category
        GlassLabel(form_frame, text="Category").pack(pady=2)
        category_entry = GlassEntry(form_frame, width=300)
        category_entry.pack(pady=2)
        
        # Section
        GlassLabel(form_frame, text="Section").pack(pady=2)
        section_var = ctk.StringVar(value="Salon")
        section_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=section_var,
            values=["Salon", "Cafe", "Gamnet"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        section_menu.pack(pady=2)
        
        # SKU
        GlassLabel(form_frame, text="SKU (Stock Keeping Unit)").pack(pady=2)
        sku_entry = GlassEntry(form_frame, width=300)
        sku_entry.pack(pady=2)
        
        # Quantity
        GlassLabel(form_frame, text=tr('quantity')).pack(pady=2)
        qty_entry = GlassEntry(form_frame, width=300)
        qty_entry.pack(pady=2)
        
        # Unit
        GlassLabel(form_frame, text="Unit (e.g., piece, liter, kg)").pack(pady=2)
        unit_entry = GlassEntry(form_frame, width=300)
        unit_entry.insert(0, "piece")
        unit_entry.pack(pady=2)
        
        # Unit cost
        GlassLabel(form_frame, text=tr('unit_cost')).pack(pady=2)
        cost_entry = GlassEntry(form_frame, width=300)
        cost_entry.pack(pady=2)
        
        # Selling price
        GlassLabel(form_frame, text=tr('selling_price')).pack(pady=2)
        price_entry = GlassEntry(form_frame, width=300)
        price_entry.pack(pady=2)
        
        # Reorder level
        GlassLabel(form_frame, text=tr('reorder_level')).pack(pady=2)
        reorder_entry = GlassEntry(form_frame, width=300)
        reorder_entry.pack(pady=2)
        
        # Supplier
        GlassLabel(form_frame, text="Supplier (ID)").pack(pady=2)
        supplier_entry = GlassEntry(form_frame, width=300)
        supplier_entry.pack(pady=2)
        
        def add_product():
            try:
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Product name is required")
                    return
                
                db.execute(
                    """INSERT INTO inventory_items 
                       (name, category, section, sku, quantity, unit, reorder_level, 
                        unit_cost, selling_price, supplier_id, last_updated)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (name, category_entry.get(), section_var.get(), sku_entry.get(),
                     float(qty_entry.get() or 0), unit_entry.get(),
                     float(reorder_entry.get() or 0),
                     float(cost_entry.get() or 0), float(price_entry.get() or 0),
                     int(supplier_entry.get()) if supplier_entry.get() else None,
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                
                messagebox.showinfo("Success", "Product added successfully!")
                
                # Clear form
                for entry in [name_entry, category_entry, sku_entry, qty_entry,
                             cost_entry, price_entry, reorder_entry, supplier_entry]:
                    entry.delete(0, 'end')
                unit_entry.delete(0, 'end')
                unit_entry.insert(0, "piece")
                
                self.refresh_products()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        
        GlassButton(
            form_frame,
            text=tr('add'),
            command=add_product,
            fg_color=COLORS['success']
        ).pack(pady=20)
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
