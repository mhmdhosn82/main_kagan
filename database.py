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

# Global database instance
db = Database()
