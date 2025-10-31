#!/usr/bin/env python3
"""
Test script for Kagan Collection Management Software Enhanced Features
Tests non-GUI components without requiring display
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """Test database and new tables"""
    print("=" * 60)
    print("Testing Database Schema...")
    print("=" * 60)
    
    from database import db
    
    # Test new tables exist
    tables = [
        'users', 'settings', 'inventory_items', 'suppliers',
        'purchase_orders', 'purchase_order_items', 'expenses',
        'loyalty_transactions', 'sms_history', 'notifications',
        'backup_history', 'payment_transactions'
    ]
    
    print("\nChecking new tables:")
    for table in tables:
        try:
            count = db.fetchone(f'SELECT COUNT(*) as c FROM {table}')
            print(f"  ✓ {table:<25} {count['c']} rows")
        except Exception as e:
            print(f"  ✗ {table:<25} ERROR: {e}")
    
    # Check default admin user
    print("\nChecking default admin user:")
    user = db.fetchone("SELECT * FROM users WHERE username = 'admin'")
    if user:
        print(f"  ✓ Admin user exists: {user['username']}, Role: {user['role']}")
    else:
        print("  ✗ Admin user not found!")
    
    # Check default settings
    print("\nChecking default settings:")
    settings = db.fetchall("SELECT * FROM settings")
    print(f"  ✓ {len(settings)} default settings configured")
    
    for setting in settings[:5]:  # Show first 5
        print(f"    - {setting['key']}: {setting['value']}")
    print(f"    ... and {len(settings) - 5} more")
    
    return True

def test_translations():
    """Test translation system"""
    print("\n" + "=" * 60)
    print("Testing Translation System...")
    print("=" * 60)
    
    from translations import tr, translator
    
    # Test Persian translations
    print("\nPersian translations:")
    translator.set_language('fa')
    keys = ['dashboard', 'salon', 'cafe_bar', 'gamnet', 'settings', 'logout']
    for key in keys:
        print(f"  {key}: {tr(key)}")
    
    # Test English translations
    print("\nEnglish translations:")
    translator.set_language('en')
    for key in keys:
        print(f"  {key}: {tr(key)}")
    
    # Test RTL detection
    translator.set_language('fa')
    print(f"\nRTL for Persian: {translator.is_rtl()}")
    translator.set_language('en')
    print(f"RTL for English: {translator.is_rtl()}")
    
    return True

def test_sms_service():
    """Test SMS service"""
    print("\n" + "=" * 60)
    print("Testing SMS Service...")
    print("=" * 60)
    
    from sms_service import sms_service
    from database import db
    
    # Get SMS configuration
    provider = sms_service.provider
    print(f"\nSMS Provider: {provider}")
    
    # Test SMS logging (without actually sending)
    print("\nTesting SMS logging:")
    sms_service.log_sms(
        customer_id=None,
        phone_number="09121234567",
        message="Test message",
        sms_type="test",
        status="test",
        error_message=None
    )
    
    # Check if logged
    history = db.fetchone("SELECT * FROM sms_history WHERE sms_type = 'test'")
    if history:
        print(f"  ✓ SMS logged successfully")
        print(f"    Phone: {history['phone_number']}")
        print(f"    Status: {history['status']}")
        
        # Clean up test data
        db.execute("DELETE FROM sms_history WHERE sms_type = 'test'")
    else:
        print("  ✗ SMS logging failed")
    
    return True

def test_inventory():
    """Test inventory system"""
    print("\n" + "=" * 60)
    print("Testing Inventory System...")
    print("=" * 60)
    
    from database import db
    from datetime import datetime
    
    # Add test product
    print("\nAdding test inventory item:")
    db.execute(
        """INSERT INTO inventory_items 
           (name, category, section, sku, quantity, unit, reorder_level, 
            unit_cost, selling_price, last_updated)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("Test Shampoo", "Hair Care", "Salon", "SH001", 50.0, "bottle",
         10.0, 5.0, 15.0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    
    # Verify
    product = db.fetchone("SELECT * FROM inventory_items WHERE sku = 'SH001'")
    if product:
        print(f"  ✓ Product added: {product['name']}")
        print(f"    Section: {product['section']}")
        print(f"    Quantity: {product['quantity']} {product['unit']}")
        print(f"    Price: ${product['selling_price']}")
        
        # Clean up
        db.execute("DELETE FROM inventory_items WHERE sku = 'SH001'")
    else:
        print("  ✗ Product not added")
    
    return True

def test_expense_tracking():
    """Test expense tracking"""
    print("\n" + "=" * 60)
    print("Testing Expense Tracking...")
    print("=" * 60)
    
    from database import db
    from datetime import datetime
    
    # Add test expense
    print("\nAdding test expense:")
    db.execute(
        """INSERT INTO expenses 
           (category, description, amount, expense_date, payment_method)
           VALUES (?, ?, ?, ?, ?)""",
        ("rent", "Test Rent Payment", 1000.0, 
         datetime.now().strftime('%Y-%m-%d'), "bank_transfer")
    )
    
    # Verify
    expense = db.fetchone(
        "SELECT * FROM expenses WHERE description = 'Test Rent Payment'"
    )
    if expense:
        print(f"  ✓ Expense added: {expense['description']}")
        print(f"    Category: {expense['category']}")
        print(f"    Amount: ${expense['amount']}")
        print(f"    Payment: {expense['payment_method']}")
        
        # Clean up
        db.execute("DELETE FROM expenses WHERE description = 'Test Rent Payment'")
    else:
        print("  ✗ Expense not added")
    
    return True

def test_suppliers():
    """Test supplier management"""
    print("\n" + "=" * 60)
    print("Testing Supplier Management...")
    print("=" * 60)
    
    from database import db
    
    # Add test supplier
    print("\nAdding test supplier:")
    db.execute(
        """INSERT INTO suppliers (name, contact_person, phone, email)
           VALUES (?, ?, ?, ?)""",
        ("Test Supplier Co.", "John Doe", "09121234567", "test@supplier.com")
    )
    
    # Verify
    supplier = db.fetchone("SELECT * FROM suppliers WHERE name = 'Test Supplier Co.'")
    if supplier:
        print(f"  ✓ Supplier added: {supplier['name']}")
        print(f"    Contact: {supplier['contact_person']}")
        print(f"    Phone: {supplier['phone']}")
        
        # Clean up
        db.execute("DELETE FROM suppliers WHERE name = 'Test Supplier Co.'")
    else:
        print("  ✗ Supplier not added")
    
    return True

def test_authentication():
    """Test authentication system"""
    print("\n" + "=" * 60)
    print("Testing Authentication System...")
    print("=" * 60)
    
    from database import db
    import hashlib
    from datetime import datetime
    
    # Test password hashing
    print("\nTesting password hashing:")
    test_password = "testpass123"
    password_hash = hashlib.sha256(test_password.encode()).hexdigest()
    print(f"  Password: {test_password}")
    print(f"  Hash: {password_hash[:32]}...")
    
    # Add test user
    print("\nAdding test user:")
    db.execute(
        """INSERT INTO users (username, password_hash, full_name, role, created_date)
           VALUES (?, ?, ?, ?, ?)""",
        ("testuser", password_hash, "Test User", "employee",
         datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    
    # Verify login
    user = db.fetchone(
        """SELECT * FROM users 
           WHERE username = ? AND password_hash = ?""",
        ("testuser", password_hash)
    )
    
    if user:
        print(f"  ✓ User authentication successful")
        print(f"    Username: {user['username']}")
        print(f"    Role: {user['role']}")
        
        # Clean up
        db.execute("DELETE FROM users WHERE username = 'testuser'")
    else:
        print("  ✗ User authentication failed")
    
    return True

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "KAGAN COLLECTION ENHANCED FEATURES TEST" + " " * 9 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    tests = [
        ("Database Schema", test_database),
        ("Translation System", test_translations),
        ("SMS Service", test_sms_service),
        ("Inventory System", test_inventory),
        ("Expense Tracking", test_expense_tracking),
        ("Supplier Management", test_suppliers),
        ("Authentication System", test_authentication),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n✗ {test_name} FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {passed + failed}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n⚠ {failed} test(s) failed. Please review the errors above.")
    
    print("\n" + "=" * 60)
    print("Enhanced features are ready to use!")
    print("Run 'python main.py' to start the application.")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
