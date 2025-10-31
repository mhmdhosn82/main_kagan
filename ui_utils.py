"""
UI utilities and theme configuration for Kagan Collection Management Software
Implements glassmorphism effects and Vazir font integration
"""
import customtkinter as ctk
from tkinter import font as tkfont
import os

try:
    from PIL import ImageFont
except ImportError:
    ImageFont = None

# Theme colors for glassmorphism
COLORS = {
    'primary': '#6366f1',       # Indigo
    'secondary': '#8b5cf6',     # Purple
    'background': '#0f172a',    # Dark blue
    'surface': '#1e293b',       # Slightly lighter dark
    'glass': '#1e293b',         # Glass surface
    'text': '#f1f5f9',          # Light text
    'text_secondary': '#cbd5e1', # Secondary text
    'success': '#10b981',       # Green
    'warning': '#f59e0b',       # Orange
    'error': '#ef4444',         # Red
    'border': '#334155'         # Border color
}

def _set_default_kwargs(kwargs, defaults):
    """
    Helper function to set default kwargs only if not already provided.
    
    Modifies kwargs dictionary in place by adding default values for any
    keys not already present. The dictionary is returned for convenience
    but is the same object that was passed in (modified in place).
    
    Args:
        kwargs: Dictionary of keyword arguments to modify
        defaults: Dictionary of default values to apply
        
    Returns:
        The same kwargs dictionary (modified in place) for convenience
    """
    for key, value in defaults.items():
        if key not in kwargs:
            kwargs[key] = value
    return kwargs

class GlassFrame(ctk.CTkFrame):
    """Custom frame with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        defaults = {
            'fg_color': COLORS['glass'],
            'corner_radius': 15,
            'border_width': 1,
            'border_color': COLORS['border']
        }
        super().__init__(master, **_set_default_kwargs(kwargs, defaults))

class GlassButton(ctk.CTkButton):
    """Custom button with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        defaults = {
            'corner_radius': 10,
            'fg_color': COLORS['primary'],
            'hover_color': COLORS['secondary'],
            'border_width': 1,
            'border_color': COLORS['border']
        }
        super().__init__(master, **_set_default_kwargs(kwargs, defaults))

class GlassEntry(ctk.CTkEntry):
    """Custom entry with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        defaults = {
            'corner_radius': 10,
            'fg_color': COLORS['surface'],
            'border_color': COLORS['border'],
            'text_color': COLORS['text']
        }
        super().__init__(master, **_set_default_kwargs(kwargs, defaults))

class GlassLabel(ctk.CTkLabel):
    """Custom label for glassmorphism UI"""
    def __init__(self, master, **kwargs):
        if 'text_color' not in kwargs:
            kwargs['text_color'] = COLORS['text']
        super().__init__(
            master,
            **kwargs
        )

class GlassScrollableFrame(ctk.CTkScrollableFrame):
    """Custom scrollable frame with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        defaults = {
            'fg_color': COLORS['glass'],
            'corner_radius': 15,
            'border_width': 1,
            'border_color': COLORS['border']
        }
        super().__init__(master, **_set_default_kwargs(kwargs, defaults))


def setup_vazir_font():
    """Setup Vazir font for Persian text support"""
    # Get the fonts directory path
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    
    # Define font file paths
    font_files = {
        'regular': os.path.join(fonts_dir, 'Vazir-Regular.ttf'),
        'bold': os.path.join(fonts_dir, 'Vazir-Bold.ttf'),
        'medium': os.path.join(fonts_dir, 'Vazir-Medium.ttf'),
        'light': os.path.join(fonts_dir, 'Vazir-Light.ttf'),
    }
    
    # Try to load Vazir font
    font_family = 'Vazir'
    
    # Check if font files exist
    if all(os.path.exists(f) for f in font_files.values()):
        try:
            # Try to pre-register fonts using PIL/Pillow if available
            # The font objects are loaded and discarded - this is intentional as
            # it helps register the fonts with the system on some platforms
            if ImageFont is not None:
                try:
                    for font_file in font_files.values():
                        ImageFont.truetype(font_file, 12)
                except OSError as e:
                    # Font loading failed but we can still try to use the font family name
                    print(f"Note: Could not pre-load font file: {e}")
        except OSError as e:
            print(f"Warning: Could not load Vazir font: {e}")
            font_family = 'Arial'  # Fallback to Arial
    else:
        print("Warning: Vazir font files not found, using Arial as fallback")
        font_family = 'Arial'
    
    # Return font configurations for different text styles
    return {
        'title': (font_family, 24, 'bold'),
        'heading': (font_family, 18, 'bold'),
        'subheading': (font_family, 14, 'bold'),
        'body': (font_family, 12),
        'small': (font_family, 10)
    }

FONTS = setup_vazir_font()

def create_title_label(parent, text):
    """Create a title label"""
    return GlassLabel(parent, text=text, font=FONTS['title'])

def create_heading_label(parent, text):
    """Create a heading label"""
    return GlassLabel(parent, text=text, font=FONTS['heading'])

def create_section_header(parent, title):
    """Create a section header with styling"""
    frame = GlassFrame(parent)
    label = GlassLabel(frame, text=title, font=FONTS['heading'])
    label.pack(pady=10, padx=20)
    return frame