#!/usr/bin/env python3
"""
Demo script for Kagan Collection Management Software
Demonstrates the application capabilities without GUI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database
from datetime import datetime, timedelta

def clear_database():
    """Clear all data from database"""
    db = database.db
    tables = [
        'messages', 'employee_commissions', 'attendance', 'campaigns',
        'invoices', 'gamnet_reservations', 'gamnet_sessions', 'gamnet_devices',
        'cafe_order_items', 'cafe_orders', 'cafe_menu',
        'salon_service_records', 'salon_appointments', 'salon_services',
        'customers', 'employees'
    ]
    for table in tables:
        db.execute(f'DELETE FROM {table}')
    print('Database cleared\n')

def setup_demo_data():
    """Setup comprehensive demo data"""
    db = database.db
    
    print('=== Setting Up Kagan Collection Demo Data ===\n')
    
    # 1. Add Employees
    print('1. Adding Employees...')
    employees = [
        ('Ali Karimi', '09121234567', 'Senior Stylist', 'Salon', 3000, 15),
        ('Reza Hosseini', '09121234568', 'Junior Stylist', 'Salon', 2000, 10),
        ('Sara Ahmadi', '09121234569', 'Head Barista', 'Cafe', 2500, 12),
        ('Mina Rezaei', '09121234570', 'Barista', 'Cafe', 1800, 8),
        ('Hassan Moradi', '09121234571', 'Gaming Manager', 'Gamnet', 2200, 5),
    ]
    
    for emp in employees:
        db.execute(
            '''INSERT INTO employees (name, phone, role, section, base_salary, commission_rate, hire_date)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (*emp, datetime.now().strftime('%Y-%m-%d'))
        )
        print(f'   ✓ {emp[0]} - {emp[2]} ({emp[3]})')
    
    # 2. Add Salon Services
    print('\n2. Adding Salon Services...')
    services = [
        ('Haircut', 25.0, 45, 15),
        ('Hair Coloring', 60.0, 90, 20),
        ('Beard Trim', 15.0, 20, 10),
        ('Hair Mask', 35.0, 60, 15),
        ('Full Service', 80.0, 120, 18),
    ]
    
    for svc in services:
        db.execute(
            '''INSERT INTO salon_services (name, price, duration_minutes, commission_rate)
               VALUES (?, ?, ?, ?)''',
            svc
        )
        print(f'   ✓ {svc[0]} - ${svc[1]} ({svc[2]} min)')
    
    # 3. Add Cafe Menu
    print('\n3. Adding Cafe Menu Items...')
    menu_items = [
        ('Espresso', 'Drinks', 3.5, 'Classic espresso shot'),
        ('Cappuccino', 'Drinks', 4.5, 'Espresso with steamed milk'),
        ('Latte', 'Drinks', 5.0, 'Smooth latte with milk foam'),
        ('Turkish Coffee', 'Drinks', 4.0, 'Traditional Turkish coffee'),
        ('Club Sandwich', 'Food', 8.0, 'Triple-decker club sandwich'),
        ('Burger', 'Food', 10.0, 'Classic burger with fries'),
        ('Cheesecake', 'Desserts', 6.0, 'New York style cheesecake'),
        ('Brownie', 'Desserts', 5.0, 'Chocolate brownie with ice cream'),
    ]
    
    for item in menu_items:
        db.execute(
            '''INSERT INTO cafe_menu (name, category, price, description)
               VALUES (?, ?, ?, ?)''',
            item
        )
        print(f'   ✓ {item[0]} ({item[1]}) - ${item[2]}')
    
    # 4. Add Gaming Devices
    print('\n4. Adding Gaming Devices...')
    devices = [
        ('PC-01', 'PC', 5.0),
        ('PC-02', 'PC', 5.0),
        ('PC-03', 'PC', 6.0),
        ('PS5-01', 'PlayStation', 8.0),
        ('XBOX-01', 'Xbox', 8.0),
        ('VR-01', 'VR', 12.0),
    ]
    
    for device in devices:
        db.execute(
            '''INSERT INTO gamnet_devices (device_number, device_type, hourly_rate)
               VALUES (?, ?, ?)''',
            device
        )
        print(f'   ✓ {device[0]} ({device[1]}) - ${device[2]}/hr')
    
    # 5. Add Customers
    print('\n5. Adding Customers...')
    customers = [
        ('Mohammad Rezaei', '09123456789', '1990-05-15'),
        ('Fateme Hosseini', '09123456788', '1992-08-22'),
        ('Amir Mohammadi', '09123456787', '1988-03-10'),
        ('Zahra Ahmadi', '09123456786', '1995-12-05'),
        ('Mehdi Karimi', '09123456785', '1991-07-18'),
    ]
    
    for cust in customers:
        db.execute(
            '''INSERT INTO customers (name, phone, birthdate, registration_date, loyalty_points, wallet_balance)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (*cust, datetime.now().strftime('%Y-%m-%d'), 100, 50.0)
        )
        print(f'   ✓ {cust[0]} - {cust[1]}')
    
    # 6. Create Sample Appointments
    print('\n6. Creating Sample Appointments...')
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    appointments = [
        (1, 1, today.strftime('%Y-%m-%d'), '10:00', 'Haircut'),
        (2, 1, today.strftime('%Y-%m-%d'), '11:30', 'Hair Coloring'),
        (3, 2, tomorrow.strftime('%Y-%m-%d'), '14:00', 'Full Service'),
    ]
    
    for apt in appointments:
        db.execute(
            '''INSERT INTO salon_appointments (customer_id, stylist_id, appointment_date, appointment_time, service_type, status)
               VALUES (?, ?, ?, ?, ?, 'pending')''',
            apt
        )
        print(f'   ✓ Customer {apt[0]} with Stylist {apt[1]} on {apt[2]} at {apt[3]}')
    
    # 7. Create Sample Campaign
    print('\n7. Creating Sample Campaign...')
    end_date = today + timedelta(days=30)
    db.execute(
        '''INSERT INTO campaigns (name, description, discount_percentage, code, start_date, end_date, is_active)
           VALUES (?, ?, ?, ?, ?, ?, 1)''',
        ('Welcome Offer', '20% off for new customers', 20.0, 'WELCOME20',
         today.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    )
    print('   ✓ Welcome Offer (20% off) - Code: WELCOME20')
    
    # 8. Create Sample Invoices
    print('\n8. Creating Sample Invoices...')
    invoices = [
        (1, 75.0, 0.0, 75.0, 'Cash', None),
        (2, 120.0, 24.0, 96.0, 'Card', 'WELCOME20'),
        (3, 45.0, 0.0, 45.0, 'Wallet', None),
    ]
    
    for inv in invoices:
        db.execute(
            '''INSERT INTO invoices (customer_id, invoice_date, total_amount, discount_amount, 
                                    final_amount, payment_method, campaign_code, is_paid)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1)''',
            (inv[0], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), *inv[1:])
        )
        print(f'   ✓ Invoice for Customer {inv[0]} - ${inv[3]} ({inv[4]})')
        
        # Update customer stats
        db.execute(
            '''UPDATE customers 
               SET total_spent = total_spent + ?, 
                   last_visit_date = ?,
                   loyalty_points = loyalty_points + ?
               WHERE id = ?''',
            (inv[3], datetime.now().strftime('%Y-%m-%d'), int(inv[3]), inv[0])
        )
    
    print('\n=== Demo Data Setup Complete! ===\n')

def show_statistics():
    """Display system statistics"""
    db = database.db
    
    print('=== System Statistics ===\n')
    
    # Employee stats
    emp_count = db.fetchone('SELECT COUNT(*) as c FROM employees WHERE is_active = 1')
    print(f'Active Employees: {emp_count["c"]}')
    
    for section in ['Salon', 'Cafe', 'Gamnet']:
        count = db.fetchone('SELECT COUNT(*) as c FROM employees WHERE section = ? AND is_active = 1', (section,))
        print(f'  - {section}: {count["c"]}')
    
    # Customer stats
    cust_count = db.fetchone('SELECT COUNT(*) as c FROM customers')
    print(f'\nTotal Customers: {cust_count["c"]}')
    
    active = db.fetchone(
        '''SELECT COUNT(*) as c FROM customers
           WHERE last_visit_date IS NOT NULL'''
    )
    print(f'Active Customers: {active["c"]}')
    
    # Revenue stats
    revenue = db.fetchone('SELECT SUM(final_amount) as total FROM invoices WHERE is_paid = 1')
    print(f'\nTotal Revenue: ${revenue["total"]:.2f}' if revenue["total"] else '\nTotal Revenue: $0.00')
    
    # Service stats
    services = db.fetchone('SELECT COUNT(*) as c FROM salon_services')
    menu = db.fetchone('SELECT COUNT(*) as c FROM cafe_menu')
    devices = db.fetchone('SELECT COUNT(*) as c FROM gamnet_devices')
    
    print(f'\nSalon Services: {services["c"]}')
    print(f'Cafe Menu Items: {menu["c"]}')
    print(f'Gaming Devices: {devices["c"]}')
    
    # Appointments
    appointments = db.fetchone('SELECT COUNT(*) as c FROM salon_appointments WHERE status = "pending"')
    print(f'\nPending Appointments: {appointments["c"]}')
    
    # Campaigns
    campaigns = db.fetchone('SELECT COUNT(*) as c FROM campaigns WHERE is_active = 1')
    print(f'Active Campaigns: {campaigns["c"]}')
    
    print('\n' + '='*50 + '\n')

def main():
    """Main demo function"""
    print('\n' + '='*50)
    print('  KAGAN COLLECTION MANAGEMENT SYSTEM - DEMO')
    print('='*50 + '\n')
    
    # Clear and setup
    clear_database()
    setup_demo_data()
    show_statistics()
    
    print('Demo completed successfully!')
    print('\nTo run the full GUI application, execute:')
    print('  python main.py')
    print('\nNote: GUI requires a display environment with tkinter support.')
    print('')

if __name__ == '__main__':
    main()
