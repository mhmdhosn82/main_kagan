#!/usr/bin/env python3
"""
Test SMS Manual Functionality
Tests that SMS requires proper configuration before sending
"""
import os
import sys
from database import Database
from sms_service import SMSService

def test_sms_not_configured():
    """Test that SMS fails when not configured"""
    print("\n=== Testing SMS Not Configured ===\n")
    
    # Create a fresh database connection
    db = Database()
    
    # Ensure SMS is not configured
    db.execute("UPDATE settings SET value = 'none' WHERE key = 'sms_provider'")
    db.execute("UPDATE settings SET value = '' WHERE key = 'sms_api_key'")
    db.execute("UPDATE settings SET value = '' WHERE key = 'sms_sender_number'")
    
    # Create SMS service
    sms = SMSService()
    
    # Check configuration status
    is_configured = sms.is_configured()
    print(f"1. SMS is_configured() when provider='none': {is_configured}")
    assert not is_configured, "SMS should not be configured when provider is 'none'"
    print("   ✓ Correctly returns False")
    
    # Try to send SMS
    result = sms.send_sms('1234567890', 'Test message', 'manual', None)
    print(f"\n2. Attempt to send SMS when not configured:")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    assert not result['success'], "SMS should fail when not configured"
    assert 'not configured' in result['message'].lower(), "Error message should mention configuration"
    print("   ✓ Correctly fails with proper error message")

def test_sms_configured_with_provider_but_no_api_key():
    """Test that SMS fails when provider is set but API key is missing"""
    print("\n=== Testing SMS with Provider but No API Key ===\n")
    
    db = Database()
    
    # Set provider but no API key
    db.execute("UPDATE settings SET value = 'twilio' WHERE key = 'sms_provider'")
    db.execute("UPDATE settings SET value = '' WHERE key = 'sms_api_key'")
    db.execute("UPDATE settings SET value = '' WHERE key = 'sms_sender_number'")
    
    # Create SMS service
    sms = SMSService()
    
    # Check configuration status
    is_configured = sms.is_configured()
    print(f"1. SMS is_configured() when provider='twilio' but no API key: {is_configured}")
    assert not is_configured, "SMS should not be configured without API key"
    print("   ✓ Correctly returns False")
    
    # Try to send SMS
    result = sms.send_sms('1234567890', 'Test message', 'manual', None)
    print(f"\n2. Attempt to send SMS without API key:")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    assert not result['success'], "SMS should fail without API key"
    print("   ✓ Correctly fails")

def test_sms_configured_properly():
    """Test that SMS validates properly when configured"""
    print("\n=== Testing SMS Properly Configured ===\n")
    
    db = Database()
    
    # Set proper configuration
    db.execute("UPDATE settings SET value = 'twilio' WHERE key = 'sms_provider'")
    db.execute("UPDATE settings SET value = 'test_api_key_12345' WHERE key = 'sms_api_key'")
    db.execute("UPDATE settings SET value = 'test_secret' WHERE key = 'sms_api_secret'")
    db.execute("UPDATE settings SET value = '+1234567890' WHERE key = 'sms_sender_number'")
    
    # Create SMS service
    sms = SMSService()
    
    # Check configuration status
    is_configured = sms.is_configured()
    print(f"1. SMS is_configured() with valid settings: {is_configured}")
    assert is_configured, "SMS should be configured with valid settings"
    print("   ✓ Correctly returns True")
    
    # Verify settings are loaded
    print(f"\n2. Loaded settings:")
    print(f"   Provider: {sms.provider}")
    print(f"   API Key: [REDACTED]")
    print(f"   Sender: {sms.sender_number}")
    assert sms.provider == 'twilio', "Provider should be 'twilio'"
    assert sms.api_key == 'test_api_key_12345', "API key should match"
    assert sms.sender_number == '+1234567890', "Sender number should match"
    print("   ✓ All settings loaded correctly")
    
    # Note: Actual SMS sending will fail because it's a test API key
    # but the validation should pass
    print("\n3. SMS service is ready to send (actual provider integration needed)")
    print("   ✓ Configuration validation successful")

def test_sms_history_logged():
    """Test that failed SMS attempts are logged"""
    print("\n=== Testing SMS History Logging ===\n")
    
    db = Database()
    
    # Ensure SMS is not configured
    db.execute("UPDATE settings SET value = 'none' WHERE key = 'sms_provider'")
    db.execute("UPDATE settings SET value = '' WHERE key = 'sms_api_key'")
    
    # Create a test customer
    db.execute(
        "INSERT OR REPLACE INTO customers (id, name, phone, registration_date) VALUES (?, ?, ?, datetime('now'))",
        (9999, 'Test Customer', '9999999999')
    )
    
    # Create SMS service and try to send
    sms = SMSService()
    result = sms.send_sms('9999999999', 'Test message', 'manual', 9999)
    
    print(f"1. SMS send result: {result['success']}")
    assert not result['success'], "SMS should fail when not configured"
    
    # Check if it was logged
    history = db.fetchall(
        "SELECT * FROM sms_history WHERE customer_id = ? ORDER BY id DESC LIMIT 1",
        (9999,)
    )
    
    print(f"\n2. Checking SMS history:")
    if history:
        sms_record = history[0]
        print(f"   Customer ID: {sms_record['customer_id']}")
        print(f"   Phone: {sms_record['phone_number']}")
        print(f"   Status: {sms_record['status']}")
        print(f"   Error: {sms_record['error_message']}")
        assert sms_record['status'] == 'not_configured', "Status should be 'not_configured'"
        print("   ✓ Failed SMS attempt logged correctly")
    else:
        print("   ✗ No history found!")
        raise AssertionError("SMS should be logged even when it fails")
    
    # Cleanup
    db.execute("DELETE FROM customers WHERE id = ?", (9999,))
    db.execute("DELETE FROM sms_history WHERE customer_id = ?", (9999,))

def test_no_automatic_scheduling():
    """Test that automatic scheduling method is removed"""
    print("\n=== Testing No Automatic SMS Scheduling ===\n")
    
    sms = SMSService()
    
    # Check that the automatic scheduling method doesn't exist
    has_schedule_method = hasattr(sms, 'schedule_automatic_sms')
    print(f"1. Has 'schedule_automatic_sms' method: {has_schedule_method}")
    assert not has_schedule_method, "Automatic scheduling method should be removed"
    print("   ✓ Automatic scheduling method successfully removed")
    
    # Verify manual methods still exist
    manual_methods = ['send_sms', 'send_survey_sms', 'send_birthday_sms', 
                      'send_promotional_sms', 'send_inactive_customer_sms']
    
    print(f"\n2. Checking manual SMS methods:")
    for method in manual_methods:
        has_method = hasattr(sms, method)
        print(f"   {method}: {'✓' if has_method else '✗'}")
        assert has_method, f"Manual method {method} should exist"
    print("   ✓ All manual methods available")

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Manual SMS Functionality")
    print("=" * 60)
    
    try:
        test_sms_not_configured()
        test_sms_configured_with_provider_but_no_api_key()
        test_sms_configured_properly()
        test_sms_history_logged()
        test_no_automatic_scheduling()
        
        print("\n" + "=" * 60)
        print("✅ All SMS Manual Functionality Tests Passed!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"❌ Test Failed: {str(e)}")
        print("=" * 60)
        return 1
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
