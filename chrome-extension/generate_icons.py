"""
Generate extension icons using PIL/Pillow
Run: pip install pillow
Then: python generate_icons.py
"""

try:
    from PIL import Image, ImageDraw
    import os
    
    def create_icon(size):
        """Create an icon with gradient background and interceptor symbol"""
        # Create image with gradient
        img = Image.new('RGB', (size, size))
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background
        for y in range(size):
            # Interpolate between two colors
            r = int(102 + (118 - 102) * y / size)
            g = int(126 + (75 - 126) * y / size)
            b = int(234 + (162 - 234) * y / size)
            draw.line([(0, y), (size, y)], fill=(r, g, b))
        
        # Draw circular arrow (interceptor symbol)
        line_width = max(2, size // 16)
        center = size // 2
        radius = size // 3
        
        # Draw arc
        bbox = [center - radius, center - radius, center + radius, center + radius]
        draw.arc(bbox, start=130, end=410, fill='white', width=line_width)
        
        # Draw arrow head
        arrow_x = center + int(radius * 0.7)
        arrow_y = center - int(radius * 0.7)
        arrow_size = size // 8
        
        draw.line([
            (arrow_x, arrow_y),
            (arrow_x + arrow_size, arrow_y - arrow_size // 2)
        ], fill='white', width=line_width)
        
        draw.line([
            (arrow_x, arrow_y),
            (arrow_x + arrow_size // 2, arrow_y + arrow_size)
        ], fill='white', width=line_width)
        
        return img
    
    # Create icons directory if it doesn't exist
    icons_dir = 'icons'
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    # Generate icons
    sizes = [16, 48, 128]
    for size in sizes:
        icon = create_icon(size)
        filename = os.path.join(icons_dir, f'icon{size}.png')
        icon.save(filename, 'PNG')
        print(f'✓ Generated {filename}')
    
    print('\n✓ All icons generated successfully!')
    print('You can now load the extension in Chrome.')

except ImportError:
    print('Error: Pillow library not found.')
    print('Please install it using: pip install pillow')
    print('\nAlternatively, open icons/create_icons.html in your browser to generate icons.')
