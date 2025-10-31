"""
Supplier Management and Expense Tracking Section Module
Handles suppliers, purchase orders, and expenses
"""
import customtkinter as ctk
from ui_utils import *
from database import db
from translations import tr
from tkinter import messagebox
from datetime import datetime

class SupplierSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the supplier section UI"""
        header = create_section_header(self.frame, tr('supplier_management'))
        header.pack(fill='x', padx=10, pady=10)
        
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tabview.add("Suppliers List")
        self.tabview.add(tr('add_supplier'))
        self.tabview.add(tr('purchase_orders'))
        
        self.setup_list_tab()
        self.setup_add_tab()
        self.setup_po_tab()
    
    def setup_list_tab(self):
        """Setup suppliers list"""
        tab = self.tabview.tab("Suppliers List")
        
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.suppliers_text = ctk.CTkTextbox(list_frame, fg_color=COLORS['surface'])
        self.suppliers_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassButton(tab, text=tr('refresh'), command=self.refresh_suppliers).pack(pady=5)
        
        self.refresh_suppliers()
    
    def refresh_suppliers(self):
        """Refresh suppliers list"""
        self.suppliers_text.delete('1.0', 'end')
        suppliers = db.fetchall("SELECT * FROM suppliers ORDER BY name")
        
        for sup in suppliers:
            status = "Active" if sup['is_active'] else "Inactive"
            self.suppliers_text.insert('end',
                f"ID: {sup['id']} | {sup['name']} | Contact: {sup['contact_person'] or 'N/A'}\n"
                f"Phone: {sup['phone'] or 'N/A'} | Email: {sup['email'] or 'N/A'}\n"
                f"Status: {status} | Notes: {sup['notes'] or 'N/A'}\n"
                f"{'-'*80}\n\n"
            )
    
    def setup_add_tab(self):
        """Setup add supplier form"""
        tab = self.tabview.tab(tr('add_supplier'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text=tr('add_supplier'), font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text=tr('name')).pack(pady=2)
        name_entry = GlassEntry(form_frame, width=300)
        name_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('contact_person')).pack(pady=2)
        contact_entry = GlassEntry(form_frame, width=300)
        contact_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('phone')).pack(pady=2)
        phone_entry = GlassEntry(form_frame, width=300)
        phone_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('email')).pack(pady=2)
        email_entry = GlassEntry(form_frame, width=300)
        email_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('address')).pack(pady=2)
        address_entry = GlassEntry(form_frame, width=300)
        address_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('notes')).pack(pady=2)
        notes_entry = GlassEntry(form_frame, width=300)
        notes_entry.pack(pady=2)
        
        def add_supplier():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Supplier name is required")
                return
            
            db.execute(
                """INSERT INTO suppliers (name, contact_person, phone, email, address, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (name, contact_entry.get(), phone_entry.get(), email_entry.get(),
                 address_entry.get(), notes_entry.get())
            )
            
            messagebox.showinfo("Success", "Supplier added successfully!")
            for entry in [name_entry, contact_entry, phone_entry, email_entry, address_entry, notes_entry]:
                entry.delete(0, 'end')
            self.refresh_suppliers()
        
        GlassButton(form_frame, text=tr('add'), command=add_supplier, 
                   fg_color=COLORS['success']).pack(pady=20)
    
    def setup_po_tab(self):
        """Setup purchase orders"""
        tab = self.tabview.tab(tr('purchase_orders'))
        
        GlassLabel(tab, text="Purchase Orders", font=FONTS['heading']).pack(pady=10)
        
        po_text = ctk.CTkTextbox(tab, fg_color=COLORS['surface'], height=300)
        po_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        pos = db.fetchall(
            """SELECT po.*, s.name as supplier_name
               FROM purchase_orders po
               JOIN suppliers s ON po.supplier_id = s.id
               ORDER BY po.order_date DESC
               LIMIT 50"""
        )
        
        for po in pos:
            po_text.insert('end',
                f"PO #{po['id']} | Supplier: {po['supplier_name']} | "
                f"Date: {po['order_date']} | Amount: ${po['total_amount']:.2f} | "
                f"Status: {po['status']}\n"
            )
    
    def get_frame(self):
        return self.frame


class ExpenseSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the expense section UI"""
        header = create_section_header(self.frame, tr('expense_tracking'))
        header.pack(fill='x', padx=10, pady=10)
        
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tabview.add("Expenses List")
        self.tabview.add(tr('add_expense'))
        
        self.setup_list_tab()
        self.setup_add_tab()
    
    def setup_list_tab(self):
        """Setup expenses list"""
        tab = self.tabview.tab("Expenses List")
        
        filter_frame = GlassFrame(tab)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(filter_frame, text="Category:").pack(side='left', padx=5)
        
        category_var = ctk.StringVar(value="all")
        category_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=category_var,
            values=["all", "rent", "utilities", "salaries", "supplies", "other"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary'],
            command=lambda _: self.refresh_expenses(category_var.get())
        )
        category_menu.pack(side='left', padx=5)
        
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.expenses_text = ctk.CTkTextbox(list_frame, fg_color=COLORS['surface'])
        self.expenses_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_expenses()
    
    def refresh_expenses(self, category="all"):
        """Refresh expenses list"""
        self.expenses_text.delete('1.0', 'end')
        
        if category == "all":
            expenses = db.fetchall(
                "SELECT * FROM expenses ORDER BY expense_date DESC LIMIT 100"
            )
        else:
            expenses = db.fetchall(
                "SELECT * FROM expenses WHERE category = ? ORDER BY expense_date DESC LIMIT 100",
                (category,)
            )
        
        total = sum(exp['amount'] for exp in expenses)
        
        self.expenses_text.insert('end', 
            f"Total Expenses: ${total:.2f}\n"
            f"{'-'*80}\n\n"
        )
        
        for exp in expenses:
            self.expenses_text.insert('end',
                f"Date: {exp['expense_date']} | Category: {exp['category']} | "
                f"Amount: ${exp['amount']:.2f}\n"
                f"Description: {exp['description']}\n"
                f"Payment: {exp['payment_method'] or 'N/A'}\n"
                f"{'-'*80}\n\n"
            )
    
    def setup_add_tab(self):
        """Setup add expense form"""
        tab = self.tabview.tab(tr('add_expense'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text=tr('add_expense'), font=FONTS['heading']).pack(pady=10)
        
        GlassLabel(form_frame, text=tr('expense_category')).pack(pady=2)
        category_var = ctk.StringVar(value="other")
        category_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=category_var,
            values=["rent", "utilities", "salaries", "supplies", "maintenance", "marketing", "other"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        category_menu.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('description')).pack(pady=2)
        desc_entry = GlassEntry(form_frame, width=300)
        desc_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('amount')).pack(pady=2)
        amount_entry = GlassEntry(form_frame, width=300)
        amount_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('date')).pack(pady=2)
        date_entry = GlassEntry(form_frame, width=300)
        date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        date_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('payment_method')).pack(pady=2)
        payment_var = ctk.StringVar(value="cash")
        payment_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=payment_var,
            values=["cash", "card", "bank_transfer", "check"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        payment_menu.pack(pady=2)
        
        GlassLabel(form_frame, text="Receipt Number").pack(pady=2)
        receipt_entry = GlassEntry(form_frame, width=300)
        receipt_entry.pack(pady=2)
        
        GlassLabel(form_frame, text=tr('notes')).pack(pady=2)
        notes_entry = GlassEntry(form_frame, width=300)
        notes_entry.pack(pady=2)
        
        def add_expense():
            try:
                amount = float(amount_entry.get())
                
                db.execute(
                    """INSERT INTO expenses 
                       (category, description, amount, expense_date, payment_method, receipt_number, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (category_var.get(), desc_entry.get(), amount, date_entry.get(),
                     payment_var.get(), receipt_entry.get(), notes_entry.get())
                )
                
                messagebox.showinfo("Success", "Expense added successfully!")
                
                for entry in [desc_entry, amount_entry, receipt_entry, notes_entry]:
                    entry.delete(0, 'end')
                date_entry.delete(0, 'end')
                date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                
                self.refresh_expenses()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
        
        GlassButton(form_frame, text=tr('add'), command=add_expense,
                   fg_color=COLORS['success']).pack(pady=20)
    
    def get_frame(self):
        return self.frame
