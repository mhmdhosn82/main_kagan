#!/usr/bin/env python3
"""
Test script for Kagan Collection Management Software
Tests database operations without GUI
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database
from datetime import datetime

def test_database():
    """Test database operations"""
    db = database.db
    
    print('=== Testing Database Operations ===\n')
    
    # Test 1: Add an employee
    print('1. Adding sample employee...')
    db.execute(
        '''INSERT INTO employees (name, phone, role, section, base_salary, commission_rate, hire_date)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        ('John Doe', '1234567890', 'Stylist', 'Salon', 3000, 15, datetime.now().strftime('%Y-%m-%d'))
    )
    emp = db.fetchone('SELECT * FROM employees ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Employee added: {emp["name"]} (ID: {emp["id"]})')
    
    # Test 2: Add a customer
    print('\n2. Adding sample customer...')
    db.execute(
        '''INSERT INTO customers (name, phone, registration_date)
           VALUES (?, ?, ?)''',
        ('Jane Smith', '0987654321', datetime.now().strftime('%Y-%m-%d'))
    )
    cust = db.fetchone('SELECT * FROM customers ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Customer added: {cust["name"]} (ID: {cust["id"]})')
    
    # Test 3: Add a salon service
    print('\n3. Adding salon service...')
    db.execute(
        '''INSERT INTO salon_services (name, price, duration_minutes, commission_rate)
           VALUES (?, ?, ?, ?)''',
        ('Haircut', 25.0, 45, 15)
    )
    svc = db.fetchone('SELECT * FROM salon_services ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Service added: {svc["name"]} - ${svc["price"]}')
    
    # Test 4: Add a cafe menu item
    print('\n4. Adding cafe menu item...')
    db.execute(
        '''INSERT INTO cafe_menu (name, category, price, description)
           VALUES (?, ?, ?, ?)''',
        ('Coffee', 'Drinks', 4.5, 'Fresh brewed coffee')
    )
    menu = db.fetchone('SELECT * FROM cafe_menu ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Menu item added: {menu["name"]} - ${menu["price"]}')
    
    # Test 5: Add a gaming device
    print('\n5. Adding gaming device...')
    db.execute(
        '''INSERT INTO gamnet_devices (device_number, device_type, hourly_rate)
           VALUES (?, ?, ?)''',
        ('PC-01', 'PC', 5.0)
    )
    device = db.fetchone('SELECT * FROM gamnet_devices ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Device added: {device["device_number"]} - ${device["hourly_rate"]}/hr')
    
    # Test 6: Create an invoice
    print('\n6. Creating invoice...')
    db.execute(
        '''INSERT INTO invoices (customer_id, invoice_date, total_amount, discount_amount, final_amount)
           VALUES (?, ?, ?, ?, ?)''',
        (cust['id'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 100.0, 10.0, 90.0)
    )
    invoice = db.fetchone('SELECT * FROM invoices ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Invoice created: #{invoice["id"]} - ${invoice["final_amount"]}')
    
    # Test 7: Create a campaign
    print('\n7. Creating campaign...')
    db.execute(
        '''INSERT INTO campaigns (name, description, discount_percentage, code, start_date, end_date)
           VALUES (?, ?, ?, ?, ?, ?)''',
        ('Test Campaign', 'Test discount', 20.0, 'TEST20', 
         datetime.now().strftime('%Y-%m-%d'), 
         datetime.now().strftime('%Y-%m-%d'))
    )
    campaign = db.fetchone('SELECT * FROM campaigns ORDER BY id DESC LIMIT 1')
    print(f'   ✓ Campaign created: {campaign["name"]} - {campaign["discount_percentage"]}%')
    
    # Summary
    print('\n=== Summary ===')
    print(f'Employees: {db.fetchone("SELECT COUNT(*) as c FROM employees")["c"]}')
    print(f'Customers: {db.fetchone("SELECT COUNT(*) as c FROM customers")["c"]}')
    print(f'Services: {db.fetchone("SELECT COUNT(*) as c FROM salon_services")["c"]}')
    print(f'Menu Items: {db.fetchone("SELECT COUNT(*) as c FROM cafe_menu")["c"]}')
    print(f'Devices: {db.fetchone("SELECT COUNT(*) as c FROM gamnet_devices")["c"]}')
    print(f'Invoices: {db.fetchone("SELECT COUNT(*) as c FROM invoices")["c"]}')
    print(f'Campaigns: {db.fetchone("SELECT COUNT(*) as c FROM campaigns")["c"]}')
    
    print('\n✅ All database operations successful!')

if __name__ == '__main__':
    test_database()
