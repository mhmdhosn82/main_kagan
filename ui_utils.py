# Updated ui_utils.py

# Assuming COLORS is defined somewhere in your code

class GlassLabel:
    def __init__(self, **kwargs):
        if 'text_color' not in kwargs:
            kwargs['text_color'] = COLORS['text']
        # Other initialization code goes here
        
        # Set attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)