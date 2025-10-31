"""
Settings Section Module
Handles application configuration and preferences
"""
import customtkinter as ctk
from ui_utils import *
from database import db
from translations import tr, translator
from auth import session
import hashlib
import os
import shutil
from datetime import datetime
from tkinter import filedialog, messagebox

class SettingsSection:
    def __init__(self, parent):
        self.parent = parent
        self.frame = GlassScrollableFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the settings section UI"""
        # Header
        header = create_section_header(self.frame, tr('settings_title'))
        header.pack(fill='x', padx=10, pady=10)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self.frame, fg_color=COLORS['surface'])
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add(tr('appearance'))
        self.tabview.add(tr('business'))
        self.tabview.add(tr('sms_config'))
        self.tabview.add(tr('backup'))
        if session.is_admin():
            self.tabview.add(tr('users'))
        
        self.setup_appearance_tab()
        self.setup_business_tab()
        self.setup_sms_tab()
        self.setup_backup_tab()
        if session.is_admin():
            self.setup_users_tab()
    
    def get_setting(self, key, default=''):
        """Get setting value"""
        result = db.fetchone("SELECT value FROM settings WHERE key = ?", (key,))
        return result['value'] if result else default
    
    def save_setting(self, key, value):
        """Save setting value"""
        db.execute("UPDATE settings SET value = ? WHERE key = ?", (value, key))
    
    def setup_appearance_tab(self):
        """Setup appearance settings"""
        tab = self.tabview.tab(tr('appearance'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Theme setting
        GlassLabel(form_frame, text=tr('theme'), font=FONTS['subheading']).pack(pady=10)
        
        theme_var = ctk.StringVar(value=self.get_setting('theme', 'dark'))
        theme_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=theme_var,
            values=["dark", "light"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        theme_menu.pack(pady=5)
        
        def save_theme():
            self.save_setting('theme', theme_var.get())
            ctk.set_appearance_mode(theme_var.get())
            messagebox.showinfo("Success", "Theme updated successfully!")
        
        GlassButton(form_frame, text=tr('save'), command=save_theme).pack(pady=5)
        
        # Language setting
        GlassLabel(form_frame, text=tr('language'), font=FONTS['subheading']).pack(pady=10)
        
        lang_var = ctk.StringVar(value=self.get_setting('language', 'fa'))
        lang_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=lang_var,
            values=["fa", "en"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        lang_menu.pack(pady=5)
        
        def save_language():
            self.save_setting('language', lang_var.get())
            translator.set_language(lang_var.get())
            messagebox.showinfo("Success", "Language updated! Please restart the application.")
        
        GlassButton(form_frame, text=tr('save'), command=save_language).pack(pady=5)
    
    def setup_business_tab(self):
        """Setup business settings"""
        tab = self.tabview.tab(tr('business'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Currency
        GlassLabel(form_frame, text=tr('currency')).pack(pady=5)
        currency_entry = GlassEntry(form_frame, width=300)
        currency_entry.insert(0, self.get_setting('currency', 'Toman'))
        currency_entry.pack(pady=5)
        
        # Tax rate
        GlassLabel(form_frame, text="Tax Rate (%)").pack(pady=5)
        tax_entry = GlassEntry(form_frame, width=300)
        tax_entry.insert(0, self.get_setting('tax_rate', '9'))
        tax_entry.pack(pady=5)
        
        # Business hours
        GlassLabel(form_frame, text="Business Hours").pack(pady=5)
        hours_entry = GlassEntry(form_frame, width=300)
        hours_entry.insert(0, self.get_setting('business_hours', '09:00-22:00'))
        hours_entry.pack(pady=5)
        
        # Contact phone
        GlassLabel(form_frame, text=tr('phone')).pack(pady=5)
        phone_entry = GlassEntry(form_frame, width=300)
        phone_entry.insert(0, self.get_setting('contact_phone', ''))
        phone_entry.pack(pady=5)
        
        # Contact email
        GlassLabel(form_frame, text=tr('email')).pack(pady=5)
        email_entry = GlassEntry(form_frame, width=300)
        email_entry.insert(0, self.get_setting('contact_email', ''))
        email_entry.pack(pady=5)
        
        # Loyalty points rate
        GlassLabel(form_frame, text="Loyalty Points per Dollar").pack(pady=5)
        loyalty_entry = GlassEntry(form_frame, width=300)
        loyalty_entry.insert(0, self.get_setting('loyalty_points_rate', '1'))
        loyalty_entry.pack(pady=5)
        
        def save_business():
            self.save_setting('currency', currency_entry.get())
            self.save_setting('tax_rate', tax_entry.get())
            self.save_setting('business_hours', hours_entry.get())
            self.save_setting('contact_phone', phone_entry.get())
            self.save_setting('contact_email', email_entry.get())
            self.save_setting('loyalty_points_rate', loyalty_entry.get())
            messagebox.showinfo("Success", "Business settings saved successfully!")
        
        GlassButton(form_frame, text=tr('save'), command=save_business).pack(pady=20)
    
    def setup_sms_tab(self):
        """Setup SMS configuration"""
        tab = self.tabview.tab(tr('sms_config'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text=tr('sms_config'), font=FONTS['heading']).pack(pady=10)
        
        # SMS Provider
        GlassLabel(form_frame, text="SMS Provider").pack(pady=5)
        provider_var = ctk.StringVar(value=self.get_setting('sms_provider', 'none'))
        provider_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=provider_var,
            values=["none", "twilio", "kavenegar", "ghasedak"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        provider_menu.pack(pady=5)
        
        # API Key
        GlassLabel(form_frame, text="API Key").pack(pady=5)
        api_key_entry = GlassEntry(form_frame, width=300)
        api_key_entry.insert(0, self.get_setting('sms_api_key', ''))
        api_key_entry.pack(pady=5)
        
        # API Secret
        GlassLabel(form_frame, text="API Secret").pack(pady=5)
        api_secret_entry = GlassEntry(form_frame, width=300, show="*")
        api_secret_entry.insert(0, self.get_setting('sms_api_secret', ''))
        api_secret_entry.pack(pady=5)
        
        def save_sms():
            self.save_setting('sms_provider', provider_var.get())
            self.save_setting('sms_api_key', api_key_entry.get())
            self.save_setting('sms_api_secret', api_secret_entry.get())
            messagebox.showinfo("Success", "SMS settings saved successfully!")
        
        GlassButton(form_frame, text=tr('save'), command=save_sms).pack(pady=20)
    
    def setup_backup_tab(self):
        """Setup backup and restore"""
        tab = self.tabview.tab(tr('backup'))
        
        form_frame = GlassFrame(tab)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(form_frame, text=tr('backup'), font=FONTS['heading']).pack(pady=10)
        
        # Backup path
        GlassLabel(form_frame, text="Backup Directory").pack(pady=5)
        
        path_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        path_frame.pack(pady=5)
        
        self.backup_path_entry = GlassEntry(path_frame, width=250)
        self.backup_path_entry.insert(0, self.get_setting('backup_path', './backups'))
        self.backup_path_entry.pack(side='left', padx=5)
        
        def browse_path():
            path = filedialog.askdirectory()
            if path:
                self.backup_path_entry.delete(0, 'end')
                self.backup_path_entry.insert(0, path)
        
        GlassButton(path_frame, text="Browse", command=browse_path, width=80).pack(side='left')
        
        # Auto backup
        auto_backup_var = ctk.BooleanVar(value=self.get_setting('auto_backup', '1') == '1')
        auto_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Enable Automatic Backups",
            variable=auto_backup_var
        )
        auto_checkbox.pack(pady=10)
        
        # Backup frequency
        GlassLabel(form_frame, text="Backup Frequency").pack(pady=5)
        freq_var = ctk.StringVar(value=self.get_setting('backup_frequency', 'daily'))
        freq_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=freq_var,
            values=["daily", "weekly", "monthly"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        freq_menu.pack(pady=5)
        
        def save_backup_settings():
            self.save_setting('backup_path', self.backup_path_entry.get())
            self.save_setting('auto_backup', '1' if auto_backup_var.get() else '0')
            self.save_setting('backup_frequency', freq_var.get())
            messagebox.showinfo("Success", "Backup settings saved successfully!")
        
        GlassButton(form_frame, text=tr('save'), command=save_backup_settings).pack(pady=10)
        
        # Manual backup button
        GlassButton(
            form_frame,
            text="Backup Now",
            command=self.backup_database,
            fg_color=COLORS['success']
        ).pack(pady=5)
        
        # Restore button
        GlassButton(
            form_frame,
            text="Restore from Backup",
            command=self.restore_database,
            fg_color=COLORS['warning']
        ).pack(pady=5)
    
    def backup_database(self):
        """Create database backup"""
        try:
            backup_dir = self.get_setting('backup_path', './backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'kagan_backup_{timestamp}.db')
            
            # Copy database
            db_path = os.path.join(os.path.dirname(__file__), 'kagan.db')
            shutil.copy2(db_path, backup_file)
            
            # Record backup
            file_size = os.path.getsize(backup_file)
            db.execute(
                """INSERT INTO backup_history (backup_date, backup_path, backup_size, status)
                   VALUES (?, ?, ?, ?)""",
                (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), backup_file, file_size, 'success')
            )
            
            messagebox.showinfo("Success", f"Backup created successfully!\n{backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {str(e)}")
    
    def restore_database(self):
        """Restore database from backup"""
        backup_file = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
        )
        
        if not backup_file:
            return
        
        if messagebox.askyesno("Confirm", "This will replace the current database. Continue?"):
            try:
                db_path = os.path.join(os.path.dirname(__file__), 'kagan.db')
                
                # Close database connection
                db.close()
                
                # Restore backup
                shutil.copy2(backup_file, db_path)
                
                messagebox.showinfo("Success", "Database restored successfully! Please restart the application.")
            except Exception as e:
                messagebox.showerror("Error", f"Restore failed: {str(e)}")
    
    def setup_users_tab(self):
        """Setup user management (admin only)"""
        tab = self.tabview.tab(tr('users'))
        
        # User list
        list_frame = GlassFrame(tab)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        GlassLabel(list_frame, text="User Management", font=FONTS['heading']).pack(pady=10)
        
        # Users display
        users_text = ctk.CTkTextbox(
            list_frame,
            fg_color=COLORS['surface'],
            text_color=COLORS['text'],
            height=200
        )
        users_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        def refresh_users():
            users = db.fetchall("SELECT * FROM users ORDER BY id")
            users_text.delete('1.0', 'end')
            for user in users:
                status = "Active" if user['is_active'] else "Inactive"
                users_text.insert('end', 
                    f"ID: {user['id']} | {user['username']} | {user['full_name']} | "
                    f"Role: {user['role']} | Status: {status}\n"
                )
        
        refresh_users()
        
        # Add user form
        add_frame = GlassFrame(tab)
        add_frame.pack(fill='x', padx=10, pady=10)
        
        GlassLabel(add_frame, text="Add New User", font=FONTS['subheading']).pack(pady=10)
        
        GlassLabel(add_frame, text="Username").pack(pady=2)
        username_entry = GlassEntry(add_frame, width=250)
        username_entry.pack(pady=2)
        
        GlassLabel(add_frame, text="Password").pack(pady=2)
        password_entry = GlassEntry(add_frame, width=250, show="*")
        password_entry.pack(pady=2)
        
        GlassLabel(add_frame, text="Full Name").pack(pady=2)
        fullname_entry = GlassEntry(add_frame, width=250)
        fullname_entry.pack(pady=2)
        
        GlassLabel(add_frame, text="Role").pack(pady=2)
        role_var = ctk.StringVar(value="employee")
        role_menu = ctk.CTkOptionMenu(
            add_frame,
            variable=role_var,
            values=["admin", "manager", "employee"],
            fg_color=COLORS['surface'],
            button_color=COLORS['primary']
        )
        role_menu.pack(pady=2)
        
        def add_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required!")
                return
            
            try:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                db.execute(
                    """INSERT INTO users (username, password_hash, full_name, role, created_date)
                       VALUES (?, ?, ?, ?, ?)""",
                    (username, password_hash, fullname, role_var.get(), 
                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                messagebox.showinfo("Success", "User added successfully!")
                username_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
                fullname_entry.delete(0, 'end')
                refresh_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {str(e)}")
        
        GlassButton(add_frame, text="Add User", command=add_user).pack(pady=10)
    
    def get_frame(self):
        """Return the main frame"""
        return self.frame
