import os
import io
from PIL import Image, ImageDraw, ImageFont

def generate_echoset_table_image(echosets, page_num, total_pages, asset_resolver):
    """
    Generates an image of a table containing the icon, name, and id for a list of EchoSets.
    """
    row_height = 60
    icon_size = 48
    padding = 10
    header_height = 40
    footer_height = 30
    
    col1_x = padding
    col2_x = col1_x + icon_size + 20
    col3_x = col2_x + 250
    
    width = col3_x + 250
    height = header_height + (len(echosets) * row_height) + footer_height
    
    # Discord dark theme background color
    bg_color = (49, 51, 56)
    text_color = (255, 255, 255)
    line_color = (66, 69, 73)
    
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        # For Pillow >= 9.2.0, size parameter is supported on load_default
        font = ImageFont.load_default(size=18)
        header_font = ImageFont.load_default(size=20)
    except TypeError:
        # Fallback for older Pillow
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        
    # Draw Header
    draw.text((col1_x, padding), "Icon", font=header_font, fill=text_color)
    draw.text((col2_x, padding), "Name", font=header_font, fill=text_color)
    draw.text((col3_x, padding), "ID", font=header_font, fill=text_color)
    
    # Draw line under header
    draw.line([(0, header_height), (width, header_height)], fill=line_color, width=2)
    
    y = header_height
    for es in echosets:
        # Draw Icon
        if es.icon:
            icon_path = asset_resolver(es.icon)
            if icon_path and os.path.exists(icon_path):
                try:
                    with Image.open(icon_path) as img:
                        # Convert to RGBA for transparency if needed
                        img = img.convert("RGBA")
                        img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                        # Create an RGBA background block to safely paste transparent images over RGB
                        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
                        temp.paste(img, (col1_x, y + (row_height - icon_size) // 2))
                        image.paste(temp, (0, 0), temp)
                except Exception as e:
                    print(f"Error loading image {icon_path}: {e}")
                    
        # Draw Name
        text_y = y + (row_height - 18) // 2
        draw.text((col2_x, text_y), es.name or es.key.title(), font=font, fill=text_color)
        
        # Draw ID
        draw.text((col3_x, text_y), es.key, font=font, fill=text_color)
        
        # Draw line under row
        y += row_height
        draw.line([(0, y), (width, y)], fill=line_color, width=1)
        
    # Draw Footer
    footer_text = f"Page {page_num} of {total_pages}"
    draw.text((padding, y + 5), footer_text, font=font, fill=(150, 150, 150))
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer
