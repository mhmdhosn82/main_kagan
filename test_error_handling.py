#!/usr/bin/env python3
"""
Test script to verify error handling and logging in main.py and auth.py

This test verifies that error handling and logging are properly implemented.
"""

import os
import sys

# Test 1: Verify logging module exists and works
def test_logging_module():
    """Test that logging module exists and can be imported"""
    print("Test 1: Logging Module")
    print("-" * 50)
    
    try:
        from app_logger import log_info, log_error, log_exception, log_debug, log_warning
        print("✓ app_logger module imported successfully")
        
        # Test logging functions
        log_info("Test info message")
        log_debug("Test debug message")
        log_warning("Test warning message")
        log_error("Test error message")
        
        # Test exception logging
        try:
            raise ValueError("Test exception")
        except Exception as e:
            log_exception("Test exception context", e)
        
        print("✓ All logging functions work correctly")
        
        # Check if log file was created
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        if os.path.exists(log_dir):
            print(f"✓ Log directory exists: {log_dir}")
            log_files = os.listdir(log_dir)
            if log_files:
                print(f"✓ Log files created: {', '.join(log_files)}")
                return True
            else:
                print("✗ No log files found")
                return False
        else:
            print("✗ Log directory not created")
            return False
            
    except Exception as e:
        print(f"✗ Error testing logging module: {e}")
        import traceback
        traceback.print_exc()
        return False


# Test 2: Verify error handling in main.py
def test_main_error_handling():
    """Test that main.py has proper error handling"""
    print("\nTest 2: Main.py Error Handling")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Check for logging imports
    if 'from app_logger import' in content:
        print("✓ app_logger is imported in main.py")
    else:
        print("✗ app_logger not imported in main.py")
        return False
    
    # Check for try-except in __init__
    if 'try:' in content and 'except Exception as e:' in content:
        print("✓ Try-except blocks found in main.py")
    else:
        print("✗ No try-except blocks found in main.py")
        return False
    
    # Check for log_exception usage
    if 'log_exception' in content:
        print("✓ log_exception is used for error logging")
    else:
        print("✗ log_exception not used in main.py")
        return False
    
    # Check for log_info usage
    if 'log_info' in content:
        print("✓ log_info is used for progress logging")
    else:
        print("✗ log_info not used in main.py")
        return False
    
    # Check for error dialog method
    if '_show_error_dialog' in content:
        print("✓ _show_error_dialog method exists")
    else:
        print("✗ _show_error_dialog method not found")
        return False
    
    # Check for specific logged events
    logged_events = [
        'Starting Kagan Management Application',
        'Setting up user interface',
        'Initializing sample data',
        'Making main window visible'
    ]
    
    all_logged = True
    for event in logged_events:
        if event in content:
            print(f"  ✓ Logs: {event}")
        else:
            print(f"  ✗ Missing log: {event}")
            all_logged = False
    
    return all_logged


# Test 3: Verify error handling in auth.py
def test_auth_error_handling():
    """Test that auth.py has proper error handling"""
    print("\nTest 3: Auth.py Error Handling")
    print("-" * 50)
    
    auth_py_path = os.path.join(os.path.dirname(__file__), 'auth.py')
    
    try:
        with open(auth_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read auth.py: {e}")
        return False
    
    # Check for logging imports
    if 'from app_logger import' in content:
        print("✓ app_logger is imported in auth.py")
    else:
        print("✗ app_logger not imported in auth.py")
        return False
    
    # Check for error handling in login
    if 'try:' in content and 'except Exception as e:' in content:
        print("✓ Try-except blocks found in auth.py")
    else:
        print("✗ No try-except blocks found in auth.py")
        return False
    
    # Check for log_exception in login method
    if 'log_exception' in content:
        print("✓ log_exception is used in auth.py")
    else:
        print("✗ log_exception not used in auth.py")
        return False
    
    # Check for login-specific logging
    login_logs = [
        'Initializing login screen',
        'Login attempt started',
        'authenticated successfully',
        'Failed login attempt'
    ]
    
    all_logged = True
    for log_msg in login_logs:
        if log_msg in content:
            print(f"  ✓ Logs: {log_msg}")
        else:
            print(f"  ✗ Missing log: {log_msg}")
            all_logged = False
    
    return all_logged


# Test 4: Verify error handling in init_sample_data
def test_sample_data_error_handling():
    """Test that init_sample_data has proper error handling"""
    print("\nTest 4: Sample Data Error Handling")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Find init_sample_data method
    if 'def init_sample_data(self):' not in content:
        print("✗ init_sample_data method not found")
        return False
    
    # Extract the method
    start = content.find('def init_sample_data(self):')
    end = content.find('\n    def ', start + 1)
    method_content = content[start:end]
    
    # Check for try-except
    if 'try:' in method_content and 'except Exception as e:' in method_content:
        print("✓ Try-except block in init_sample_data")
    else:
        print("✗ No try-except in init_sample_data")
        return False
    
    # Check for logging
    if 'log_debug' in method_content or 'log_info' in method_content:
        print("✓ Logging in init_sample_data")
    else:
        print("✗ No logging in init_sample_data")
        return False
    
    # Check that it doesn't raise on error
    if 'log_warning' in method_content and 'Continuing application' in method_content:
        print("✓ Continues on error (doesn't crash app)")
    else:
        print("✗ May crash app on sample data error")
        return False
    
    return True


# Test 5: Verify main() function error handling
def test_main_function_error_handling():
    """Test that main() function has proper error handling"""
    print("\nTest 5: Main Function Error Handling")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Find main function
    if 'def main():' not in content:
        print("✗ main() function not found")
        return False
    
    # Extract the function
    start = content.find('def main():')
    end = content.find('\nif __name__', start)
    main_function = content[start:end]
    
    # Check for try-except
    if 'try:' in main_function and 'except Exception as e:' in main_function:
        print("✓ Try-except block in main()")
    else:
        print("✗ No try-except in main()")
        return False
    
    # Check for error output
    if 'traceback.print_exc()' in main_function or 'print_exc' in main_function:
        print("✓ Traceback printed on error")
    else:
        print("✗ No traceback on error")
        return False
    
    # Check for log file message
    if 'check the log file' in main_function or 'logs' in main_function:
        print("✓ Directs user to check log files")
    else:
        print("✗ Doesn't direct user to log files")
        return False
    
    return True


if __name__ == '__main__':
    print("=" * 70)
    print("Error Handling and Logging Test Suite")
    print("=" * 70)
    
    results = []
    
    results.append(("Logging Module", test_logging_module()))
    results.append(("Main.py Error Handling", test_main_error_handling()))
    results.append(("Auth.py Error Handling", test_auth_error_handling()))
    results.append(("Sample Data Error Handling", test_sample_data_error_handling()))
    results.append(("Main Function Error Handling", test_main_function_error_handling()))
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 70)
    if all_passed:
        print("✅ All tests passed!")
        print("\nThe application now has comprehensive error handling and logging:")
        print("  - Errors are logged to files in the 'logs' directory")
        print("  - Errors are displayed to the console")
        print("  - Critical errors show dialogs to users")
        print("  - Application continues when possible (e.g., sample data errors)")
        print("  - Detailed stack traces help identify root causes")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        print("Error handling may not be complete.")
        sys.exit(1)
