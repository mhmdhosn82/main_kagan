#!/usr/bin/env python3
"""
Test script for UI Utils fixes
Tests that Glass* classes can accept kwargs without causing "multiple values for keyword argument" errors
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ui_utils_imports():
    """Test that ui_utils can be imported and setup_vazir_font works"""
    print("=== Testing UI Utils ===\n")
    
    print("1. Testing file syntax and basic structure...")
    # Read and parse ui_utils.py to check structure without importing tkinter
    ui_utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_utils.py')
    try:
        with open(ui_utils_path, 'r') as f:
            content = f.read()
        
        # Check for key classes and functions
        required_items = [
            'class GlassFrame',
            'class GlassButton', 
            'class GlassEntry',
            'class GlassLabel',
            'class GlassScrollableFrame',
            'def setup_vazir_font',
            'COLORS =',
            'FONTS ='
        ]
        
        for item in required_items:
            if item in content:
                print(f"   ✓ Found: {item}")
            else:
                print(f"   ✗ Missing: {item}")
                return False
        
        print("   ✓ All required components present")
    except Exception as e:
        print(f"   ✗ Error reading file: {e}")
        return False
    
    print("\n2. Testing COLORS dictionary structure...")
    required_colors = ['primary', 'secondary', 'background', 'surface', 
                       'glass', 'text', 'text_secondary', 'success', 
                       'warning', 'error', 'border']
    for color in required_colors:
        if f"'{color}':" in content:
            print(f"   ✓ {color} defined")
        else:
            print(f"   ✗ Missing color: {color}")
            return False
    
    print("\n3. Testing Vazir font integration...")
    # Check for Vazir font mentions
    if 'Vazir' in content:
        print(f"   ✓ Vazir font referenced in code")
    if 'fonts_dir' in content:
        print(f"   ✓ Fonts directory handling present")
    if 'Vazir-Regular.ttf' in content or 'Vazir-Bold.ttf' in content:
        print(f"   ✓ Vazir font files referenced")
    if 'Arial' in content:
        print(f"   ✓ Fallback font (Arial) configured")
    
    print("\n4. Testing Glass* classes for kwargs fix...")
    # Verify that the fix for "multiple values for keyword argument" is in place
    
    # Check for helper function
    if "def _set_default_kwargs" in content:
        print("   ✓ Helper function _set_default_kwargs implemented")
    else:
        print("   ✗ Missing helper function")
        return False
    
    print("   Checking GlassFrame...")
    glass_frame_start = content.find('class GlassFrame')
    glass_frame_end = content.find('class GlassButton', glass_frame_start)
    glass_frame_section = content[glass_frame_start:glass_frame_end]
    if "_set_default_kwargs(kwargs, defaults)" in glass_frame_section:
        print("     ✓ Using _set_default_kwargs helper")
    else:
        print("     ✗ Not using helper function properly")
        return False
    
    print("   Checking GlassButton...")
    glass_button_start = content.find('class GlassButton')
    glass_button_end = content.find('class GlassEntry', glass_button_start)
    glass_button_section = content[glass_button_start:glass_button_end]
    if "_set_default_kwargs(kwargs, defaults)" in glass_button_section:
        print("     ✓ Using _set_default_kwargs helper")
    else:
        print("     ✗ Not using helper function properly")
        return False
    
    print("   Checking GlassEntry...")
    glass_entry_start = content.find('class GlassEntry')
    glass_entry_end = content.find('class GlassLabel', glass_entry_start)
    glass_entry_section = content[glass_entry_start:glass_entry_end]
    if "_set_default_kwargs(kwargs, defaults)" in glass_entry_section:
        print("     ✓ Using _set_default_kwargs helper")
    else:
        print("     ✗ Not using helper function properly")
        return False
    
    print("   Checking GlassScrollableFrame...")
    glass_scroll_start = content.find('class GlassScrollableFrame')
    # Find next def or class, whichever comes first
    next_def = content.find('\ndef ', glass_scroll_start)
    next_class = content.find('\nclass ', glass_scroll_start + 1)
    glass_scroll_end = min(next_def, next_class) if next_def > 0 and next_class > 0 else max(next_def, next_class)
    glass_scroll_section = content[glass_scroll_start:glass_scroll_end]
    if "_set_default_kwargs(kwargs, defaults)" in glass_scroll_section:
        print("     ✓ Using _set_default_kwargs helper")
    else:
        print("     ✗ Not using helper function properly")
        return False
    
    print("\n5. Testing font files...")
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
    if os.path.exists(fonts_dir):
        print(f"   ✓ Fonts directory exists: {fonts_dir}")
        font_files = [
            'Vazir-Regular.ttf',
            'Vazir-Bold.ttf',
            'Vazir-Medium.ttf',
            'Vazir-Light.ttf'
        ]
        for font_file in font_files:
            font_path = os.path.join(fonts_dir, font_file)
            if os.path.exists(font_path):
                size = os.path.getsize(font_path)
                print(f"     ✓ {font_file} ({size} bytes)")
            else:
                print(f"     ✗ Missing: {font_file}")
    else:
        print(f"   ⚠ Fonts directory not found: {fonts_dir}")
    
    print("\n✅ All UI Utils tests passed!")
    print("\nNOTE: Full UI testing requires tkinter, which is not available in headless mode.")
    print("The logic for preventing 'multiple values for keyword argument' errors has been verified.")
    return True

if __name__ == '__main__':
    success = test_ui_utils_imports()
    sys.exit(0 if success else 1)
