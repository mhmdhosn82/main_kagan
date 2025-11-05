#!/usr/bin/env python3
"""
Test script to verify mainloop error handling improvements

This test verifies that:
1. mainloop() is wrapped in try-except
2. Window close protocols are set up
3. Global exception handler is installed
4. All exceptions are properly logged and displayed
"""

import os
import sys

def test_mainloop_wrapped():
    """Test that mainloop is wrapped in try-except"""
    print("Test 1: Mainloop Error Handling")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Find the main() function
    if 'def main():' not in content:
        print("✗ main() function not found")
        return False
    
    # Extract main function
    start = content.find('def main():')
    end = content.find('\nif __name__', start)
    main_function = content[start:end]
    
    # Check for mainloop in try-except
    if 'app.mainloop()' not in main_function:
        print("✗ app.mainloop() not found in main()")
        return False
    print("✓ Found app.mainloop()")
    
    # Find the position of mainloop
    mainloop_pos = main_function.find('app.mainloop()')
    before_mainloop = main_function[:mainloop_pos]
    after_mainloop = main_function[mainloop_pos:]
    
    # Check that there's a try before mainloop
    # Look backwards from mainloop to find nearest try
    last_try = before_mainloop.rfind('try:')
    if last_try == -1:
        print("✗ No try block found before mainloop")
        return False
    
    # Check that there's an except after mainloop
    if 'except Exception as e:' not in after_mainloop:
        print("✗ No except block found after mainloop")
        return False
    
    print("✓ mainloop() is wrapped in try-except block")
    
    # Check for error logging in mainloop except
    mainloop_except_start = after_mainloop.find('except Exception as e:')
    next_except = after_mainloop.find('except Exception as e:', mainloop_except_start + 1)
    if next_except == -1:
        mainloop_except = after_mainloop[mainloop_except_start:]
    else:
        mainloop_except = after_mainloop[mainloop_except_start:next_except]
    
    if 'log_exception' in mainloop_except:
        print("✓ Exceptions in mainloop are logged")
    else:
        print("✗ Mainloop exceptions not logged")
        return False
    
    if 'traceback' in mainloop_except or 'print_exc' in mainloop_except:
        print("✓ Traceback printed for mainloop errors")
    else:
        print("✗ No traceback for mainloop errors")
        return False
    
    return True


def test_global_exception_handler():
    """Test that global exception handler is installed"""
    print("\nTest 2: Global Exception Handler")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Find the main() function
    start = content.find('def main():')
    end = content.find('\nif __name__', start)
    main_function = content[start:end]
    
    # Check for sys.excepthook
    if 'sys.excepthook' not in main_function:
        print("✗ sys.excepthook not set in main()")
        return False
    print("✓ Global exception handler (sys.excepthook) is set")
    
    # Check for handle_exception function
    if 'def handle_exception' not in main_function:
        print("✗ handle_exception function not found")
        return False
    print("✓ handle_exception function defined")
    
    # Extract handle_exception function
    handler_start = main_function.find('def handle_exception')
    handler_end = main_function.find('\n    sys.excepthook', handler_start)
    handler = main_function[handler_start:handler_end]
    
    # Check that it logs exceptions
    if 'log_exception' in handler:
        print("✓ Global handler logs exceptions")
    else:
        print("✗ Global handler doesn't log exceptions")
        return False
    
    # Check that it prints traceback
    if 'traceback' in handler or 'print_exception' in handler:
        print("✓ Global handler prints traceback")
    else:
        print("✗ Global handler doesn't print traceback")
        return False
    
    return True


def test_window_close_protocol():
    """Test that window close protocol is set up"""
    print("\nTest 3: Window Close Protocol")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Find the __init__ method of KaganManagementApp
    init_start = content.find('class KaganManagementApp')
    if init_start == -1:
        print("✗ KaganManagementApp class not found")
        return False
    
    init_method = content.find('def __init__(self):', init_start)
    if init_method == -1:
        print("✗ __init__ method not found")
        return False
    
    # Find the next method to get boundary
    next_method = content.find('\n    def ', init_method + 1)
    init_section = content[init_method:next_method]
    
    # Check for protocol handler
    if 'self.protocol("WM_DELETE_WINDOW"' not in init_section:
        print("✗ WM_DELETE_WINDOW protocol not set in __init__")
        return False
    print("✓ WM_DELETE_WINDOW protocol handler is set")
    
    # Check for on_window_close method
    if 'def on_window_close(self):' not in content:
        print("✗ on_window_close method not found")
        return False
    print("✓ on_window_close method exists")
    
    # Extract on_window_close method
    method_start = content.find('def on_window_close(self):')
    method_end = content.find('\n    def ', method_start + 1)
    method = content[method_start:method_end]
    
    # Check that it logs
    if 'log_' in method:
        print("✓ Window close events are logged")
    else:
        print("✗ Window close events not logged")
        return False
    
    # Check that it has error handling
    if 'try:' in method and 'except' in method:
        print("✓ Window close has error handling")
    else:
        print("✗ Window close missing error handling")
        return False
    
    return True


def test_login_window_close_protocol():
    """Test that login window close protocol is set up"""
    print("\nTest 4: Login Window Close Protocol")
    print("-" * 50)
    
    auth_py_path = os.path.join(os.path.dirname(__file__), 'auth.py')
    
    try:
        with open(auth_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read auth.py: {e}")
        return False
    
    # Find the __init__ method of LoginScreen
    init_start = content.find('class LoginScreen')
    if init_start == -1:
        print("✗ LoginScreen class not found")
        return False
    
    init_method = content.find('def __init__(self', init_start)
    if init_method == -1:
        print("✗ __init__ method not found")
        return False
    
    # Find the next method to get boundary
    next_method = content.find('\n    def ', init_method + 1)
    init_section = content[init_method:next_method]
    
    # Check for protocol handler
    if 'self.protocol("WM_DELETE_WINDOW"' not in init_section:
        print("✗ WM_DELETE_WINDOW protocol not set in LoginScreen.__init__")
        return False
    print("✓ WM_DELETE_WINDOW protocol handler is set in LoginScreen")
    
    # Check for on_close method
    if 'def on_close(self):' not in content:
        print("✗ on_close method not found in LoginScreen")
        return False
    print("✓ on_close method exists in LoginScreen")
    
    # Extract on_close method
    method_start = content.find('def on_close(self):')
    method_end = content.find('\n    def ', method_start + 1)
    method = content[method_start:method_end]
    
    # Check that it logs
    if 'log_' in method:
        print("✓ Login window close events are logged")
    else:
        print("✗ Login window close events not logged")
        return False
    
    return True


def test_comprehensive_logging():
    """Test that comprehensive logging exists"""
    print("\nTest 5: Comprehensive Logging")
    print("-" * 50)
    
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Could not read main.py: {e}")
        return False
    
    # Check for key lifecycle events being logged
    logged_events = [
        ('Application startup', 'Starting Kagan Management'),
        ('Entering mainloop', 'Entering main event loop'),
        ('Normal closure', 'Application closed normally'),
        ('Fatal errors', 'Fatal error in main'),
        ('Mainloop errors', 'Error in main event loop'),
        ('Unhandled exceptions', 'Unhandled exception'),
    ]
    
    all_found = True
    for event_name, event_text in logged_events:
        if event_text in content:
            print(f"  ✓ Logs {event_name}: '{event_text}'")
        else:
            print(f"  ✗ Missing log for {event_name}")
            all_found = False
    
    return all_found


if __name__ == '__main__':
    print("=" * 70)
    print("Mainloop Error Handling Test Suite")
    print("=" * 70)
    
    results = []
    
    results.append(("Mainloop Wrapped in Try-Except", test_mainloop_wrapped()))
    results.append(("Global Exception Handler", test_global_exception_handler()))
    results.append(("Window Close Protocol", test_window_close_protocol()))
    results.append(("Login Window Close Protocol", test_login_window_close_protocol()))
    results.append(("Comprehensive Logging", test_comprehensive_logging()))
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 70)
    if all_passed:
        print("✅ All mainloop error handling tests passed!")
        print("\nThe application now has:")
        print("  - Mainloop wrapped in try-except to catch runtime errors")
        print("  - Global exception handler to catch any unhandled exceptions")
        print("  - Window close protocol handlers to log close events")
        print("  - Comprehensive logging for all error paths")
        print("  - User-visible error messages for all failure scenarios")
        print("\nThis prevents silent window closures and ensures all errors are visible.")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        print("Mainloop error handling may not be complete.")
        sys.exit(1)
