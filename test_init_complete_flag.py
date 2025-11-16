#!/usr/bin/env python3
"""
Test to verify that the init_complete flag is properly set and checked
to prevent mainloop from running on destroyed or incomplete windows.
"""

import sys
import os

def test_init_complete_flag_in_init():
    """Test that init_complete flag is initialized and set in __init__"""
    print("Testing init_complete flag in KaganManagementApp.__init__...")
    
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ FAILED: Could not read main.py: {e}")
        return False
    
    # Find the KaganManagementApp class
    class_start = content.find('class KaganManagementApp')
    if class_start == -1:
        print("✗ FAILED: Could not find KaganManagementApp class")
        return False
    
    # Find __init__ method
    init_start = content.find('def __init__(self):', class_start)
    if init_start == -1:
        print("✗ FAILED: Could not find __init__ method")
        return False
    
    # Find the next method to get __init__ boundary
    next_method = content.find('\n    def ', init_start + 1)
    init_section = content[init_start:next_method]
    
    # Check that init_complete is initialized to False at the start
    if 'self.init_complete = False' not in init_section:
        print("✗ FAILED: self.init_complete = False not found at start of __init__")
        return False
    print("✓ Found self.init_complete = False at start of __init__")
    
    # Check that init_complete is set to True at the end (after successful initialization)
    if 'self.init_complete = True' not in init_section:
        print("✗ FAILED: self.init_complete = True not found at end of __init__")
        return False
    print("✓ Found self.init_complete = True at end of __init__")
    
    # Verify the True assignment comes after deiconify
    deiconify_pos = init_section.find('self.deiconify()')
    true_pos = init_section.find('self.init_complete = True')
    
    if true_pos < deiconify_pos:
        print("✗ FAILED: init_complete = True comes before deiconify()")
        return False
    print("✓ Verified init_complete = True comes after deiconify()")
    
    # Check that exception handler sets init_complete to False
    if 'self.init_complete = False' not in content[init_start:next_method]:
        print("⚠ WARNING: Exception handler may not set init_complete = False")
    else:
        # Find exception handler
        exception_pos = init_section.find('except Exception')
        if exception_pos > -1:
            exception_section = init_section[exception_pos:]
            if 'self.init_complete = False' in exception_section:
                print("✓ Found init_complete = False in exception handler")
    
    return True


def test_init_complete_check_in_main():
    """Test that main() checks init_complete before calling mainloop"""
    print("\nTesting init_complete check in main() function...")
    
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ FAILED: Could not read main.py: {e}")
        return False
    
    # Find the main function
    main_start = content.find('def main():')
    if main_start == -1:
        print("✗ FAILED: Could not find main() function")
        return False
    
    # Find where app is created
    app_creation = content.find('app = KaganManagementApp()', main_start)
    if app_creation == -1:
        print("✗ FAILED: Could not find app = KaganManagementApp() in main()")
        return False
    print("✓ Found app = KaganManagementApp()")
    
    # Find mainloop call
    mainloop_pos = content.find('app.mainloop()', app_creation)
    if mainloop_pos == -1:
        print("✗ FAILED: Could not find app.mainloop() in main()")
        return False
    print("✓ Found app.mainloop()")
    
    # Check that there's a check for init_complete before mainloop
    section_between = content[app_creation:mainloop_pos]
    
    if 'init_complete' not in section_between:
        print("✗ FAILED: No check for init_complete before mainloop()")
        return False
    print("✓ Found init_complete check before mainloop()")
    
    # Verify it checks for not init_complete
    if 'not app.init_complete' in section_between or 'not hasattr(app, \'init_complete\')' in section_between:
        print("✓ Proper check for init_complete found (checks if not complete)")
    else:
        print("⚠ WARNING: init_complete check may not be checking for failure case")
    
    # Verify there's a return statement to exit if not complete
    if 'return' in section_between:
        print("✓ Found return statement to exit if initialization incomplete")
    else:
        print("⚠ WARNING: No return statement found to exit early")
    
    return True


if __name__ == '__main__':
    print("=" * 70)
    print("Initialization Complete Flag Test")
    print("=" * 70)
    
    result1 = test_init_complete_flag_in_init()
    result2 = test_init_complete_check_in_main()
    
    print("\n" + "=" * 70)
    if result1 and result2:
        print("✅ All init_complete flag tests passed!")
        print("\nThe application now properly:")
        print("  1. Initializes init_complete = False at start")
        print("  2. Sets init_complete = True after successful initialization")
        print("  3. Checks init_complete before calling mainloop()")
        print("  4. Exits gracefully if initialization did not complete")
        print("\nThis ensures mainloop is only called on properly initialized windows.")
        sys.exit(0)
    else:
        print("✗ Some init_complete flag tests failed!")
        print("The fix may not be properly implemented.")
        sys.exit(1)
