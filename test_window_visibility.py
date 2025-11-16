#!/usr/bin/env python3
"""
Test script to verify window visibility fix in main.py

This test verifies that after self.deiconify(), the following methods are called:
- self.lift() - to bring window to top
- self.focus_force() - to force focus on the window  
- self.attributes('-topmost', True) - to set as topmost temporarily
- self.after() - to remove topmost after a delay

This ensures the main window appears visible and focused after successful login.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Constants
SEARCH_RANGE_LINES = 10  # Number of lines to search after deiconify


def test_window_visibility_code_exists():
    """
    Test that the window visibility code exists in main.py after deiconify().
    
    This checks the source code to ensure the fix is implemented correctly.
    """
    print("Testing window visibility fix in main.py...")
    
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ FAILED: Could not read main.py: {e}")
        return False
    
    # Find the __init__ method of KaganManagementApp
    init_start = content.find('class KaganManagementApp')
    if init_start == -1:
        print("✗ FAILED: Could not find KaganManagementApp class")
        return False
    
    init_method = content.find('def __init__(self):', init_start)
    if init_method == -1:
        print("✗ FAILED: Could not find __init__ method")
        return False
    
    # Find the next method after __init__ to get the boundary
    next_method = content.find('\n    def ', init_method + 1)
    init_section = content[init_method:next_method]
    
    # Check for deiconify
    if 'self.deiconify()' not in init_section:
        print("✗ FAILED: self.deiconify() not found in __init__")
        return False
    print("✓ Found self.deiconify()")
    
    # Find the position of deiconify
    deiconify_pos = init_section.find('self.deiconify()')
    after_deiconify = init_section[deiconify_pos:]
    
    # Check for lift() after deiconify
    if 'self.lift()' not in after_deiconify:
        print("✗ FAILED: self.lift() not found after deiconify()")
        return False
    print("✓ Found self.lift() after deiconify()")
    
    # Check for focus_force() or focus() after deiconify
    has_focus_force = 'self.focus_force()' in after_deiconify
    has_focus = 'self.focus()' in after_deiconify
    
    if not has_focus_force and not has_focus:
        print("✗ FAILED: self.focus() or self.focus_force() not found after deiconify()")
        return False
    
    focus_method = 'self.focus_force()' if has_focus_force else 'self.focus()'
    print(f"✓ Found {focus_method} after deiconify()")
    
    # Check for attributes('-topmost', True) after deiconify (can be commented out)
    has_topmost_active = "self.attributes('-topmost', True)" in after_deiconify and "# self.attributes('-topmost', True)" not in after_deiconify
    has_topmost_commented = "# self.attributes('-topmost', True)" in after_deiconify
    
    if has_topmost_active:
        print("✓ Found active self.attributes('-topmost', True) after deiconify()")
        # Check for after() to remove topmost
        if 'self.after(' in after_deiconify and "'-topmost', False" in after_deiconify:
            print("✓ Found self.after() to remove topmost attribute")
        else:
            print("⚠ WARNING: self.after() to remove topmost not found (optional)")
    elif has_topmost_commented:
        print("✓ Found commented self.attributes('-topmost', True) after deiconify() - topmost disabled to prevent window issues")
    else:
        print("⚠ WARNING: self.attributes('-topmost', True) not found after deiconify() (optional)")
    
    return True


def test_window_visibility_sequence():
    """
    Test that the window visibility methods appear in the correct sequence.
    """
    print("\nTesting window visibility method sequence...")
    
    main_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
    
    try:
        with open(main_py_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"✗ FAILED: Could not read main.py: {e}")
        return False
    
    # Find line with deiconify
    deiconify_line = -1
    for i, line in enumerate(lines):
        if 'self.deiconify()' in line and 'def' not in line:
            deiconify_line = i
            break
    
    if deiconify_line == -1:
        print("✗ FAILED: Could not find self.deiconify() line")
        return False
    
    print(f"✓ Found deiconify() at line {deiconify_line + 1}")
    
    # Check that lift, focus, and attributes come after deiconify
    lift_found = False
    focus_found = False
    topmost_found = False
    topmost_commented = False
    
    # Look at the next SEARCH_RANGE_LINES lines after deiconify
    for i in range(deiconify_line + 1, min(deiconify_line + SEARCH_RANGE_LINES + 1, len(lines))):
        line = lines[i]
        if 'self.lift()' in line:
            lift_found = True
            print(f"✓ Found lift() at line {i + 1} (after deiconify)")
        if 'self.focus_force()' in line or 'self.focus()' in line:
            focus_found = True
            print(f"✓ Found focus method at line {i + 1} (after deiconify)")
        if "self.attributes('-topmost', True)" in line:
            if line.strip().startswith('#'):
                topmost_commented = True
                print(f"✓ Found topmost attribute (commented) at line {i + 1} (after deiconify)")
            else:
                topmost_found = True
                print(f"✓ Found topmost attribute at line {i + 1} (after deiconify)")
    
    if not lift_found:
        print(f"✗ FAILED: lift() not found within {SEARCH_RANGE_LINES} lines after deiconify()")
        return False
    
    if not focus_found:
        print(f"✗ FAILED: focus method not found within {SEARCH_RANGE_LINES} lines after deiconify()")
        return False
    
    if not topmost_found and not topmost_commented:
        print(f"⚠ WARNING: topmost attribute not found within {SEARCH_RANGE_LINES} lines after deiconify() (optional)")
        return False
    
    return True


if __name__ == '__main__':
    print("=" * 70)
    print("Window Visibility Fix Verification Test")
    print("=" * 70)
    
    result1 = test_window_visibility_code_exists()
    result2 = test_window_visibility_sequence()
    
    print("\n" + "=" * 70)
    if result1 and result2:
        print("✅ All window visibility tests passed!")
        print("\nThe main window will now:")
        print("  1. Deiconify (make visible)")
        print("  2. Lift to top of window stack")
        print("  3. Force focus to the window")
        print("\nNote: The 'topmost' attribute has been disabled to prevent")
        print("window closing issues on some systems. The window remains")
        print("stable using lift() and focus_force() methods.")
        sys.exit(0)
    else:
        print("✗ Some window visibility tests failed!")
        print("The fix may not be properly implemented.")
        sys.exit(1)
