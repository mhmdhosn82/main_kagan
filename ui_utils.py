"""
UI utilities and theme configuration for Kagan Collection Management Software
Implements glassmorphism effects and Vazir font integration
"""
import customtkinter as ctk
from tkinter import font as tkfont
import os

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

class GlassFrame(ctk.CTkFrame):
    """Custom frame with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS['glass'],
            corner_radius=15,
            border_width=1,
            border_color=COLORS['border'],
            **kwargs
        )

class GlassButton(ctk.CTkButton):
    """Custom button with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=10,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            border_width=1,
            border_color=COLORS['border'],
            **kwargs
        )

class GlassEntry(ctk.CTkEntry):
    """Custom entry with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=10,
            fg_color=COLORS['surface'],
            border_color=COLORS['border'],
            text_color=COLORS['text'],
            **kwargs
        )

class GlassLabel(ctk.CTkLabel):
    """Custom label for glassmorphism UI"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            text_color=COLORS['text'],
            **kwargs
        )

class GlassScrollableFrame(ctk.CTkScrollableFrame):
    """Custom scrollable frame with glassmorphism effect"""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS['glass'],
            corner_radius=15,
            border_width=1,
            border_color=COLORS['border'],
            **kwargs
        )

def setup_vazir_font():
    """Setup Vazir font for Persian text support"""
    # For now, we'll use system fonts
    # In production, you would download and install Vazir font
    return {
        'title': ('Arial', 24, 'bold'),
        'heading': ('Arial', 18, 'bold'),
        'subheading': ('Arial', 14, 'bold'),
        'body': ('Arial', 12),
        'small': ('Arial', 10)
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
