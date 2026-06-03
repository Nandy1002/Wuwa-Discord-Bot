import os
import io
import html
from PIL import Image, ImageDraw, ImageFont

def generate_echoset_table_image(echosets, page_num, total_pages, asset_resolver):
    """
    Generates an image of a table containing the icon, name, and id for a list of EchoSets.
    """
    scale = 2
    row_height = 70 * scale
    icon_size = 56 * scale
    padding = 15 * scale
    header_height = 50 * scale
    footer_height = 40 * scale
    
    col1_x = padding
    col2_x = col1_x + icon_size + 15 * scale  # Name
    col3_x = col2_x + 260 * scale             # ID (Name column gets 260px)
    
    width = col3_x + 60 * scale               # ID column gets 60px
    height = header_height + (len(echosets) * row_height) + footer_height
    
    # Discord dark theme background color
    bg_color = (49, 51, 56)
    text_color = (255, 255, 255)
    line_color = (66, 69, 73)
    
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 26 * scale)
        header_font = ImageFont.truetype("arial.ttf", 28 * scale)
    except IOError:
        try:
            font = ImageFont.load_default(size=26 * scale)
            header_font = ImageFont.load_default(size=28 * scale)
        except TypeError:
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()
        
    # Draw Header
    draw.text((col1_x, padding), "Icon", font=header_font, fill=text_color)
    draw.text((col2_x, padding), "Name", font=header_font, fill=text_color)
    draw.text((col3_x, padding), "ID", font=header_font, fill=text_color)
    
    # Draw line under header
    draw.line([(0, header_height), (width, header_height)], fill=line_color, width=2 * scale)
    
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
        text_y = y + (row_height - (26 * scale)) // 2
        name_text = html.unescape(es.name or es.key.title())
        draw.text((col2_x, text_y), name_text, font=font, fill=text_color)
        
        # Draw ID
        draw.text((col3_x, text_y), es.key, font=font, fill=text_color)
        
        # Draw line under row
        y += row_height
        draw.line([(0, y), (width, y)], fill=line_color, width=1 * scale)
        
    # Draw Footer
    footer_text = f"Page {page_num} of {total_pages}"
    draw.text((padding, y + 5 * scale), footer_text, font=font, fill=(150, 150, 150))
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def generate_weapon_table_image(weapons, page_num, total_pages, asset_resolver):
    """
    Generates an image of a table containing the icon, name, id, rarity, and type for a list of Weapons.
    """
    scale = 2
    row_height = 70 * scale
    icon_size = 56 * scale
    padding = 15 * scale
    header_height = 50 * scale
    footer_height = 40 * scale
    
    col1_x = padding
    col2_x = col1_x + icon_size + 15 * scale  # Name
    col3_x = col2_x + 260 * scale             # ID (Name gets 260px)
    col4_x = col3_x + 60 * scale              # Type (ID gets 60px)
    col5_x = col4_x + 140 * scale             # Rarity (Type gets 140px)
    
    width = col5_x + 100 * scale              # Rarity gets 100px
    height = header_height + (len(weapons) * row_height) + footer_height
    
    # Discord dark theme background color
    bg_color = (49, 51, 56)
    text_color = (255, 255, 255)
    line_color = (66, 69, 73)
    
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 26 * scale)
        header_font = ImageFont.truetype("arial.ttf", 28 * scale)
    except IOError:
        try:
            font = ImageFont.load_default(size=26 * scale)
            header_font = ImageFont.load_default(size=28 * scale)
        except TypeError:
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()
        
    # Draw Header
    draw.text((col1_x, padding), "Icon", font=header_font, fill=text_color)
    draw.text((col2_x, padding), "Name", font=header_font, fill=text_color)
    draw.text((col3_x, padding), "ID", font=header_font, fill=text_color)
    draw.text((col4_x, padding), "Type", font=header_font, fill=text_color)
    draw.text((col5_x, padding), "Rarity", font=header_font, fill=text_color)
    
    # Draw line under header
    draw.line([(0, header_height), (width, header_height)], fill=line_color, width=2 * scale)
    
    y = header_height
    for w in weapons:
        # Draw Icon
        if w.icon:
            icon_path = asset_resolver(w.icon)
            if icon_path and os.path.exists(icon_path):
                try:
                    with Image.open(icon_path) as img:
                        img = img.convert("RGBA")
                        img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
                        temp.paste(img, (col1_x, y + (row_height - icon_size) // 2))
                        image.paste(temp, (0, 0), temp)
                except Exception as e:
                    print(f"Error loading image {icon_path}: {e}")
                    
        # Draw Name
        text_y = y + (row_height - (26 * scale)) // 2
        name_text = html.unescape(w.name or w.key.title())
        draw.text((col2_x, text_y), name_text, font=font, fill=text_color)
        
        # Draw ID
        draw.text((col3_x, text_y), w.key, font=font, fill=text_color)

        # Draw Type
        draw.text((col4_x, text_y), w.type or '', font=font, fill=text_color)

        # Draw Rarity
        rarity_color = text_color
        if w.rarity:
            if "5" in w.rarity:
                rarity_color = (255, 215, 0)  # Yellow
            elif "4" in w.rarity:
                rarity_color = (180, 100, 255) # Purple
            elif "3" in w.rarity:
                rarity_color = (64, 164, 255) # Blue
                
        draw.text((col5_x, text_y), w.rarity or '', font=font, fill=rarity_color)
        
        # Draw line under row
        y += row_height
        draw.line([(0, y), (width, y)], fill=line_color, width=1 * scale)
        
    # Draw Footer
    footer_text = f"Page {page_num} of {total_pages}"
    draw.text((padding, y + 5 * scale), footer_text, font=font, fill=(150, 150, 150))
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

def generate_character_table_image(characters, page_num, total_pages, asset_resolver):
    """
    Generates an image of a table containing the attribute icon, name, weapon type icon, rarity, and id.
    """
    scale = 2
    row_height = 70 * scale
    icon_size = 56 * scale
    padding = 15 * scale
    header_height = 50 * scale
    footer_height = 40 * scale
    
    col1_x = padding                          # Attribute
    col2_x = col1_x + icon_size + 15 * scale  # Name
    col3_x = col2_x + 220 * scale             # Weapon Type (Name gets 220px)
    col4_x = col3_x + icon_size + 20 * scale  # Rarity (Weapon gets icon_size+20)
    col5_x = col4_x + 120 * scale             # ID (Rarity gets 120px)
    
    width = col5_x + 80 * scale               # ID gets 80px
    height = header_height + (len(characters) * row_height) + footer_height
    
    bg_color = (49, 51, 56)
    text_color = (255, 255, 255)
    line_color = (66, 69, 73)
    
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 26 * scale)
        header_font = ImageFont.truetype("arial.ttf", 28 * scale)
    except IOError:
        try:
            font = ImageFont.load_default(size=26 * scale)
            header_font = ImageFont.load_default(size=28 * scale)
        except TypeError:
            font = ImageFont.load_default()
            header_font = ImageFont.load_default()
        
    draw.text((col1_x, padding), "Attr", font=header_font, fill=text_color)
    draw.text((col2_x, padding), "Name", font=header_font, fill=text_color)
    draw.text((col3_x, padding), "Wpn", font=header_font, fill=text_color)
    draw.text((col4_x, padding), "Rarity", font=header_font, fill=text_color)
    draw.text((col5_x, padding), "ID", font=header_font, fill=text_color)
    
    draw.line([(0, header_height), (width, header_height)], fill=line_color, width=2 * scale)
    
    y = header_height
    for char in characters:
        if char.element:
            attr_path = f"n:/wuwabot/img/attribute/{char.element.lower()}.png"
            if os.path.exists(attr_path):
                try:
                    with Image.open(attr_path) as img:
                        img = img.convert("RGBA")
                        img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
                        temp.paste(img, (col1_x, y + (row_height - icon_size) // 2))
                        image.paste(temp, (0, 0), temp)
                except Exception as e:
                    pass

        text_y = y + (row_height - (26 * scale)) // 2
        name_text = html.unescape(char.name or char.key.title())
        draw.text((col2_x, text_y), name_text, font=font, fill=text_color)
        
        if char.weapon_type:
            wpn_path = f"n:/wuwabot/img/attribute/{char.weapon_type.lower()}.png"
            if os.path.exists(wpn_path):
                try:
                    with Image.open(wpn_path) as img:
                        img = img.convert("RGBA")
                        img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
                        temp = Image.new('RGBA', image.size, (0, 0, 0, 0))
                        temp.paste(img, (col3_x, y + (row_height - icon_size) // 2))
                        image.paste(temp, (0, 0), temp)
                except Exception as e:
                    pass

        rarity_color = text_color
        if char.rarity:
            rarity_str = str(char.rarity)
            if "5" in rarity_str:
                rarity_color = (255, 215, 0)
            elif "4" in rarity_str:
                rarity_color = (180, 100, 255)
            draw.text((col4_x, text_y), f"{rarity_str}-Star", font=font, fill=rarity_color)
            
        draw.text((col5_x, text_y), str(char.numeric_id), font=font, fill=text_color)
        
        y += row_height
        draw.line([(0, y), (width, y)], fill=line_color, width=1 * scale)
        
    footer_text = f"Page {page_num} of {total_pages}"
    draw.text((padding, y + 5 * scale), footer_text, font=font, fill=(150, 150, 150))
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer
