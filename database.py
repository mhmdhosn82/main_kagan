"""
Database module for Kagan Collection Management Software
Handles all database operations and schema creation
"""
import sqlite3
from datetime import datetime
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'kagan.db')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create all necessary database tables"""
        
        # Employees table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                role TEXT NOT NULL,
                section TEXT NOT NULL,
                base_salary REAL DEFAULT 0,
                commission_rate REAL DEFAULT 0,
                hire_date TEXT,
                is_active INTEGER DEFAULT 1,
                last_work_date TEXT
            )
        ''')
        
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                birthdate TEXT,
                loyalty_points INTEGER DEFAULT 0,
                wallet_balance REAL DEFAULT 0,
                registration_date TEXT,
                last_visit_date TEXT,
                total_spent REAL DEFAULT 0
            )
        ''')
        
        # Salon appointments
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salon_appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                stylist_id INTEGER,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                service_type TEXT,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (stylist_id) REFERENCES employees(id)
            )
        ''')
        
        # Salon services
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salon_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                duration_minutes INTEGER,
                commission_rate REAL DEFAULT 0
            )
        ''')
        
        # Salon service records
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS salon_service_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                stylist_id INTEGER,
                service_id INTEGER,
                service_date TEXT,
                price REAL,
                commission REAL,
                rating INTEGER,
                review TEXT,
                invoice_id INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (stylist_id) REFERENCES employees(id),
                FOREIGN KEY (service_id) REFERENCES salon_services(id)
            )
        ''')
        
        # Cafe menu items
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cafe_menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                description TEXT,
                is_available INTEGER DEFAULT 1
            )
        ''')
        
        # Cafe orders
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cafe_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                barista_id INTEGER,
                order_date TEXT,
                total_amount REAL,
                split_count INTEGER DEFAULT 1,
                invoice_id INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (barista_id) REFERENCES employees(id)
            )
        ''')
        
        # Cafe order items
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cafe_order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                menu_item_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (order_id) REFERENCES cafe_orders(id),
                FOREIGN KEY (menu_item_id) REFERENCES cafe_menu(id)
            )
        ''')
        
        # Gamnet devices
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gamnet_devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_number TEXT UNIQUE NOT NULL,
                device_type TEXT,
                hourly_rate REAL NOT NULL,
                is_available INTEGER DEFAULT 1,
                status TEXT DEFAULT 'available'
            )
        ''')
        
        # Gamnet sessions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gamnet_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                customer_id INTEGER,
                start_time TEXT,
                end_time TEXT,
                duration_minutes INTEGER,
                charge REAL,
                invoice_id INTEGER,
                FOREIGN KEY (device_id) REFERENCES gamnet_devices(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Gamnet reservations
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS gamnet_reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                customer_id INTEGER,
                reservation_date TEXT,
                reservation_time TEXT,
                duration_minutes INTEGER,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (device_id) REFERENCES gamnet_devices(id),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Invoices
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                invoice_date TEXT,
                total_amount REAL,
                discount_amount REAL DEFAULT 0,
                final_amount REAL,
                payment_method TEXT,
                campaign_code TEXT,
                is_paid INTEGER DEFAULT 0,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Campaigns
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                discount_percentage REAL,
                code TEXT UNIQUE,
                start_date TEXT,
                end_date TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Employee attendance
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                date TEXT,
                check_in_time TEXT,
                check_out_time TEXT,
                is_late INTEGER DEFAULT 0,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        ''')
        
        # Employee commissions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_commissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                service_date TEXT,
                service_type TEXT,
                amount REAL,
                is_paid INTEGER DEFAULT 0,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        ''')
        
        # Messages and notifications
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_type TEXT,
                recipient_id INTEGER,
                message_type TEXT,
                content TEXT,
                sent_date TEXT,
                is_sent INTEGER DEFAULT 0
            )
        ''')
        
        # Users and authentication
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                role TEXT DEFAULT 'employee',
                is_active INTEGER DEFAULT 1,
                created_date TEXT,
                last_login TEXT
            )
        ''')
        
        # Settings
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                category TEXT,
                description TEXT
            )
        ''')
        
        # Inventory management
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                section TEXT,
                sku TEXT UNIQUE,
                quantity REAL DEFAULT 0,
                unit TEXT,
                reorder_level REAL,
                unit_cost REAL,
                selling_price REAL,
                supplier_id INTEGER,
                last_updated TEXT,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )
        ''')
        
        # Suppliers
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_person TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                notes TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # Purchase orders
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id INTEGER,
                order_date TEXT,
                delivery_date TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )
        ''')
        
        # Purchase order items
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_order_id INTEGER,
                inventory_item_id INTEGER,
                quantity REAL,
                unit_cost REAL,
                total_cost REAL,
                FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id),
                FOREIGN KEY (inventory_item_id) REFERENCES inventory_items(id)
            )
        ''')
        
        # Expenses
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                description TEXT,
                amount REAL,
                expense_date TEXT,
                payment_method TEXT,
                receipt_number TEXT,
                notes TEXT
            )
        ''')
        
        # Loyalty rewards
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS loyalty_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                transaction_type TEXT,
                points INTEGER,
                description TEXT,
                transaction_date TEXT,
                invoice_id INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # SMS history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sms_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                phone_number TEXT,
                message TEXT,
                sms_type TEXT,
                status TEXT DEFAULT 'pending',
                sent_date TEXT,
                delivery_status TEXT,
                error_message TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Notifications
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                message TEXT,
                notification_type TEXT,
                is_read INTEGER DEFAULT 0,
                created_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Backup history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_date TEXT,
                backup_path TEXT,
                backup_size INTEGER,
                status TEXT,
                notes TEXT
            )
        ''')
        
        # Payment gateway transactions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                transaction_id TEXT,
                gateway TEXT,
                amount REAL,
                status TEXT,
                transaction_date TEXT,
                notes TEXT,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id)
            )
        ''')
        
        self.conn.commit()
    
    def execute(self, query, params=()):
        """Execute a query"""
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor
    
    def fetchone(self, query, params=()):
        """Fetch one result"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetchall(self, query, params=()):
        """Fetch all results"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def initialize_defaults(self):
        """Initialize default users and settings"""
        import hashlib
        
        # Check if admin user exists
        admin = self.fetchone("SELECT * FROM users WHERE username = 'admin'")
        if not admin:
            # Create default admin user
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            self.execute(
                """INSERT INTO users (username, password_hash, full_name, role, created_date)
                   VALUES (?, ?, ?, ?, ?)""",
                ('admin', password_hash, 'Administrator', 'admin', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
        
        # Initialize default settings
        default_settings = [
            ('theme', 'dark', 'appearance', 'Application theme'),
            ('language', 'fa', 'appearance', 'Interface language (fa/en)'),
            ('font_family', 'Vazir', 'appearance', 'Font family'),
            ('currency', 'Toman', 'business', 'Default currency'),
            ('tax_rate', '9', 'business', 'Tax rate percentage'),
            ('business_hours', '09:00-22:00', 'business', 'Business hours'),
            ('contact_phone', '', 'business', 'Contact phone number'),
            ('contact_email', '', 'business', 'Contact email'),
            ('sms_api_key', '', 'sms', 'SMS gateway API key'),
            ('sms_api_secret', '', 'sms', 'SMS gateway API secret'),
            ('sms_provider', 'none', 'sms', 'SMS provider (twilio/kavenegar/none)'),
            ('backup_path', './backups', 'system', 'Database backup directory'),
            ('auto_backup', '1', 'system', 'Enable automatic backups'),
            ('backup_frequency', 'daily', 'system', 'Backup frequency'),
            ('loyalty_points_rate', '1', 'loyalty', 'Points per dollar spent'),
            ('loyalty_redemption_rate', '100', 'loyalty', 'Points needed for $1 discount'),
        ]
        
        for key, value, category, description in default_settings:
            existing = self.fetchone("SELECT * FROM settings WHERE key = ?", (key,))
            if not existing:
                self.execute(
                    """INSERT INTO settings (key, value, category, description)
                       VALUES (?, ?, ?, ?)""",
                    (key, value, category, description)
                )

# Global database instance
db = Database()
db.initialize_defaults()
