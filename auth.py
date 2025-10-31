"""
Login Screen for Kagan Collection Management Software
Handles user authentication and session management
"""
import customtkinter as ctk
import hashlib
from ui_utils import *
from database import db
from translations import tr, translator

class LoginScreen(ctk.CTkToplevel):
    """Login screen for authentication"""
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        
        self.on_login_success = on_login_success
        self.authenticated_user = None
        
        # Configure window
        self.title(tr('login'))
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Center on screen
        self.center_window()
        
        # Setup UI
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup login UI"""
        # Main container
        container = GlassFrame(self)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Logo/Title
        title_label = GlassLabel(
            container,
            text=tr('app_title'),
            font=FONTS['heading']
        )
        title_label.pack(pady=(30, 10))
        
        subtitle_label = GlassLabel(
            container,
            text=tr('login'),
            font=FONTS['subheading']
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username field
        username_label = GlassLabel(container, text=tr('username'))
        username_label.pack(pady=(10, 5))
        
        self.username_entry = GlassEntry(container, width=300)
        self.username_entry.pack(pady=(0, 10))
        
        # Password field
        password_label = GlassLabel(container, text=tr('password'))
        password_label.pack(pady=(10, 5))
        
        self.password_entry = GlassEntry(container, width=300, show="*")
        self.password_entry.pack(pady=(0, 20))
        
        # Bind Enter key to login
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_button = GlassButton(
            container,
            text=tr('login_button'),
            command=self.login,
            width=300,
            height=40
        )
        login_button.pack(pady=10)
        
        # Error message label
        self.error_label = GlassLabel(
            container,
            text="",
            text_color=COLORS['error'],
            font=FONTS['small']
        )
        self.error_label.pack(pady=10)
        
        # Language toggle
        lang_frame = ctk.CTkFrame(container, fg_color="transparent")
        lang_frame.pack(pady=20)
        
        GlassLabel(lang_frame, text="Language / زبان:").pack(side='left', padx=5)
        
        lang_button = ctk.CTkButton(
            lang_frame,
            text="فارسی / English",
            command=self.toggle_language,
            width=100,
            height=25,
            font=FONTS['small']
        )
        lang_button.pack(side='left', padx=5)
        
        # Default credentials hint
        hint_label = GlassLabel(
            container,
            text="Default: admin / admin123",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        hint_label.pack(pady=(10, 0))
    
    def toggle_language(self):
        """Toggle between Persian and English"""
        current = translator.current_language
        new_lang = 'en' if current == 'fa' else 'fa'
        translator.set_language(new_lang)
        
        # Recreate UI with new language
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()
    
    def login(self):
        """Authenticate user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.error_label.configure(text=tr('login_failed'))
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Check credentials
        user = db.fetchone(
            """SELECT * FROM users 
               WHERE username = ? AND password_hash = ? AND is_active = 1""",
            (username, password_hash)
        )
        
        if user:
            # Update last login
            from datetime import datetime
            db.execute(
                "UPDATE users SET last_login = ? WHERE id = ?",
                (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user['id'])
            )
            
            self.authenticated_user = user
            self.destroy()
            self.on_login_success(user)
        else:
            self.error_label.configure(text=tr('login_failed'))
            self.password_entry.delete(0, 'end')

class SessionManager:
    """Manage user session"""
    def __init__(self):
        self.current_user = None
    
    def set_user(self, user):
        """Set current user"""
        self.current_user = user
    
    def get_user(self):
        """Get current user"""
        return self.current_user
    
    def has_permission(self, permission):
        """Check if user has permission"""
        if not self.current_user:
            return False
        
        role = self.current_user['role']
        
        # Admin has all permissions
        if role == 'admin':
            return True
        
        # Define role permissions
        role_permissions = {
            'manager': ['view', 'create', 'edit', 'reports'],
            'employee': ['view', 'create']
        }
        
        return permission in role_permissions.get(role, [])
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.current_user and self.current_user['role'] == 'admin'
    
    def logout(self):
        """Clear session"""
        self.current_user = None

# Global session manager
session = SessionManager()
